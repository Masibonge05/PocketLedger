require('dotenv').config();
const express = require('express');
const twilio = require('twilio');
const axios = require('axios');
const axiosRetry = require('axios-retry').default;
const { createClient } = require('redis');

const app = express();
const port = process.env.PORT || 3000;

app.use(express.urlencoded({ extended: false }));
app.use(express.json());

const twilioAuthToken = process.env.TWILIO_AUTH_TOKEN || 'test_token';
const ledgerUrl = process.env.LEDGER_ENGINE_URL || 'http://localhost:8000';
const internalApiKey = process.env.INTERNAL_API_KEY || 'super_secret_internal_key';
const redisUrl = process.env.REDIS_URL || 'redis://localhost:6379';

const redisClient = createClient({ url: redisUrl });
redisClient.on('error', (err) => console.log('Redis Client Error', err));
redisClient.connect().catch(console.error);

axiosRetry(axios, { 
    retries: 3, 
    retryDelay: axiosRetry.exponentialDelay 
});

const rateLimiter = async (req, res, next) => {
    try {
        const fromNumber = req.body.From || 'unknown';
        const key = `rate_limit:${fromNumber}`;
        const limit = 30;
        
        const currentCount = await redisClient.incr(key);
        if (currentCount === 1) {
            await redisClient.expire(key, 3600);
        }
        
        if (currentCount > limit) {
            const twiml = new twilio.twiml.MessagingResponse();
            twiml.message("Rate limit exceeded. Please try again later.");
            return res.type('text/xml').send(twiml.toString());
        }
        next();
    } catch (err) {
        console.error("Rate limiter error:", err);
        next();
    }
};

const validateTwilioRequest = (req, res, next) => {
    const twilioSignature = req.headers['x-twilio-signature'];
    
    if (!twilioSignature) {
        return res.status(403).send('No signature provided');
    }

    const url = `https://${req.get('host')}${req.originalUrl}`;
    const params = req.body;

    const isValid = twilio.validateRequest(twilioAuthToken, twilioSignature, url, params);

    if (isValid || process.env.NODE_ENV === 'development') {
        next();
    } else {
        res.status(403).send('Invalid signature');
    }
};

app.post('/webhook/whatsapp', rateLimiter, validateTwilioRequest, async (req, res) => {
    try {
        const incomingMsg = req.body.Body || '';
        const fromNumber = req.body.From;
        const mediaUrl = req.body.MediaUrl0;
        const mediaContentType = req.body.MediaContentType0;

        let payload = {
            merchant_id: fromNumber,
            source_channel: mediaUrl ? "voice" : "text",

            item_name: "Pending AI parsing",
            quantity: 1,
            unit_price_if_stated: null,
            transaction_type: "Manual cash sale"
        };
        
        if (mediaUrl) {
            payload.audio_url = mediaUrl;
        } else {
            payload.raw_text = incomingMsg;
        }

        const messageSid = req.body.MessageSid;
        const ledgerResponse = await axios.post(`${ledgerUrl}/internal/transactions`, payload, {
            headers: {
                'x-internal-token': internalApiKey,
                'x-idempotency-key': messageSid
            }
        });

        const twiml = new twilio.twiml.MessagingResponse();
        twiml.message(`Recorded sale. Health Score: ${ledgerResponse.data.health_score}, Evidence %: ${ledgerResponse.data.evidence_confidence_pct}`);
        
        res.type('text/xml').send(twiml.toString());
    } catch (error) {
        console.error("Error routing to Ledger:", error.message);
        
        const twiml = new twilio.twiml.MessagingResponse();
        twiml.message("Sorry, I couldn't process that right now. Please use the fallback buttons to log your sale.");
        res.type('text/xml').send(twiml.toString());
    }
});

app.listen(port, () => {
    console.log(`Ingestion Gateway listening on port ${port}`);
});
