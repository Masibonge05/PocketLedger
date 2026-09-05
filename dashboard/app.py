import streamlit as st
import requests
import pandas as pd
import os
import plotly.graph_objects as go

st.set_page_config(page_title="PocketLedger Dashboard", layout="wide")

LEDGER_ENGINE_URL = os.environ.get("LEDGER_ENGINE_URL", "http://localhost:8000")

st.title("PocketLedger: Financial Identity Passport")

tab1, tab2 = st.tabs(["Lender View (Passport)", "Merchant View (Live Demo Simulator)"])

with tab1:
    st.sidebar.header("Lender Authentication")
    oauth_token = st.sidebar.text_input("OAuth 2.0 Token", type="password")
    
    if not oauth_token:
        st.info("Please authenticate to view merchant passports.")
        st.stop()
        
    if oauth_token != "mock_valid_token":
        st.error("Invalid or expired OAuth token.")
        st.stop()
        
    merchant_id = st.text_input("Enter Merchant ID (e.g. +27821234567)")
    
    if "passport_loaded" not in st.session_state:
        st.session_state.passport_loaded = False
        
    if st.button("Load Passport"):
        with st.spinner("Fetching data..."):
            try:
                response = requests.get(f"{LEDGER_ENGINE_URL}/api/passport/{merchant_id}")
                if response.status_code == 200:
                    st.session_state.passport_data = response.json()
                    st.session_state.passport_loaded = True
                else:
                    st.error("Passport not found or consent not granted.")
                    st.session_state.passport_loaded = False
            except Exception as e:
                st.error(f"Error connecting to Ledger Engine: {e}")
                st.session_state.passport_loaded = False
                
    if st.session_state.passport_loaded:
        data = st.session_state.passport_data
        
        st.subheader("Business Profile")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Operating History", f"{data['operating_history_months']} months")
        col2.metric("Total Transactions", data['total_transactions'])
        col3.metric("Cumulative Revenue", f"R {data['cumulative_revenue']:,.2f}")
        col4.metric("Revenue Consistency", f"{data['revenue_consistency_pct']}%")
        
        st.subheader("Trust & Health Metrics")
        col4, col5 = st.columns(2)
        
        fig_health = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = data['health_score'],
            title = {'text': "Business Health Score"},
            gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "darkblue"}}
        ))
        col4.plotly_chart(fig_health)
        
        fig_evidence = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = data['evidence_confidence_pct'],
            title = {'text': "Evidence Confidence Level"},
            gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "green"}}
        ))
        col5.plotly_chart(fig_evidence)
        
        st.subheader("Data Integrity")
        if st.button("Verify Integrity (Blockchain)"):
            with st.spinner("Verifying state anchor on Sepolia..."):
                try:
                    verify_resp = requests.get(f"{LEDGER_ENGINE_URL}/api/verify/{merchant_id}")
                    if verify_resp.status_code == 200:
                        v_data = verify_resp.json()
                        if v_data.get("is_valid"):
                            st.success(f"Integrity Verified. Hash: {v_data['live_hash'][:16]}...")
                        else:
                            st.error("Integrity Verification Failed. Data mismatch.")
                    else:
                        st.error("Verification endpoint failed.")
                except Exception as e:
                    st.error(f"Error connecting to Ledger Engine: {e}")

with tab2:
    st.header("Simulate WhatsApp Transaction")
    st.markdown("Use this to demo logging a transaction live. It will be parsed by Gemini, saved to Supabase, and anchored to Sepolia.")
    
    sim_merchant_id = st.text_input("Merchant ID", value="+27821234567")
    sim_text = st.text_area("WhatsApp Message", value="I just sold 3 loaves of bread for R45")
    
    if st.button("Log Transaction via AI"):
        with st.spinner("Processing through Gemini and Ledger Engine..."):
            try:
                payload = {
                    "merchant_id": sim_merchant_id,
                    "source_channel": "text",
                    "raw_text": sim_text
                }
                headers = {"x-internal-token": "super_secret_internal_key"}
                
                resp = requests.post(f"{LEDGER_ENGINE_URL}/internal/transactions", json=payload, headers=headers)
                
                if resp.status_code == 200:
                    result = resp.json()
                    st.success(f"Transaction logged successfully! Evidence weight: {result.get('recorded_weight')}")
                    st.info(f"New Health Score: {result.get('health_score')}/100")
                    st.info(f"New Evidence Confidence: {result.get('evidence_confidence_pct')}%")
                    
                    tx_id = result.get("transaction_id")
                    
                    st.markdown(f"**Download Receipt:** [Receipt PDF]({LEDGER_ENGINE_URL}/api/invoice/{tx_id})")
                else:
                    st.error(f"Failed to log transaction: {resp.text}")
            except Exception as e:
                st.error(f"Error connecting to backend: {e}")
