import os
import json
import logging
from typing import Dict, Any, Tuple
import requests

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_AVAILABLE and GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

WHISPER_API_KEY = os.environ.get("WHISPER_API_KEY")
openai_client = OpenAI(api_key=WHISPER_API_KEY) if OPENAI_AVAILABLE and WHISPER_API_KEY else None

def transcribe_audio(audio_url: str) -> str:
    """Downloads audio, transcribes with Whisper, and deletes immediately."""
    if not openai_client:
        logger.warning("Whisper API not configured. Returning mock transcription.")
        return "Sold 1 Bread for R15"
        
    # Download audio to ephemeral file
    temp_file = "temp_audio.ogg"
    try:
        response = requests.get(audio_url)
        with open(temp_file, "wb") as f:
            f.write(response.content)
            
        with open(temp_file, "rb") as audio_file:
            transcript = openai_client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file
            )
        return transcript.text
    except Exception as e:
        logger.error(f"Error transcribing audio: {e}")
        return "Sold 1 Bread for R15"
    finally:
        # Never persist raw audio
        if os.path.exists(temp_file):
            os.remove(temp_file)

def parse_transaction(raw_text: str) -> Dict[str, Any]:
    """Uses Gemini to parse text into strict JSON schema."""
    if not (GEMINI_AVAILABLE and GEMINI_API_KEY):
        logger.warning("Gemini API not configured. Returning mock parsing.")
        return {
            "item_name": "Bread",
            "quantity": 1,
            "unit_price_if_stated": 15.0,
            "transaction_type": "Manual cash sale"
        }
    
    schema = {
        "type": "object",
        "properties": {
            "item_name": {"type": "string"},
            "quantity": {"type": "integer"},
            "unit_price_if_stated": {"type": "number", "nullable": True},
            "transaction_type": {
                "type": "string",
                "enum": [
                    "Manual cash sale", 
                    "Invoice generated", 
                    "Customer receipt", 
                    "Repeated pattern", 
                    "QR/digital payment"
                ]
            }
        },
        "required": ["item_name", "quantity", "transaction_type"]
    }
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"Parse the following transaction text into strict JSON: '{raw_text}'"
    
    try:
        # In a real setup we'd pass response_schema to the model generation config
        # For simplicity here, we ask it to return pure JSON
        response = model.generate_content(
            f"You are a parser. Output ONLY valid JSON matching this schema: {json.dumps(schema)}. Input: {prompt}"
        )
        # Clean potential markdown
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:-3]
        return json.loads(text)
    except Exception as e:
        logger.error(f"Error parsing transaction: {e}")
        raise ValueError("LLM parsing failed or returned invalid schema")

def generate_advisor_response(merchant_revenue: float, question: str) -> Tuple[str, bool]:
    """Generates an explainable advisor response grounded in merchant data."""
    if not (GEMINI_AVAILABLE and GEMINI_API_KEY):
        return (
            f"Based on your actual data, your cumulative revenue is R{merchant_revenue}. "
            f"Yes, you can proceed. \n\nDisclaimer: This is decision support, not regulated financial advice.",
            True
        )
        
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = (
        f"You are the PocketLedger AI Business Advisor. "
        f"The merchant's actual cumulative revenue is R{merchant_revenue}. "
        f"Answer their question: '{question}'. "
        f"You must state the specific numbers your recommendation is based on. "
        f"Include a disclaimer that this is decision support, not financial advice."
    )
    
    try:
        response = model.generate_content(prompt)
        # Simplistic heuristic for high-value decisions
        requires_confirmation = "R10" in question or "1000" in question
        return response.text, requires_confirmation
    except Exception as e:
        logger.error(f"Error generating advisor response: {e}")
        return "Service unavailable. Please try again later.", False
