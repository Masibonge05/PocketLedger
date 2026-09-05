import os
import requests
import streamlit as st
import pandas as pd
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="PocketLedger | Financial Identity Passport",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CONFIGURATION
# ============================================================

LEDGER_ENGINE_URL = os.environ.get(
    "LEDGER_ENGINE_URL",
    "http://localhost:8000"
)

DEFAULT_MERCHANT_ID = "+27821234567"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #f8fafc;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .dashboard-title {
        font-size: 2.3rem;
        font-weight: 750;
        margin-bottom: 0;
    }

    .dashboard-subtitle {
        color: #64748b;
        margin-bottom: 2rem;
    }

    .section-title {
        font-size: 1.35rem;
        font-weight: 700;
        margin-top: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def fetch_json(endpoint, timeout=10):

    try:

        response = requests.get(
            f"{LEDGER_ENGINE_URL}{endpoint}",
            timeout=timeout
        )

        if response.status_code == 200:
            return response.json(), None

        return None, (
            f"Backend returned {response.status_code}: "
            f"{response.text}"
        )

    except requests.exceptions.ConnectionError:

        return None, (
            "Could not connect to the Ledger Engine. "
            "Make sure FastAPI is running."
        )

    except requests.exceptions.Timeout:

        return None, "The request timed out."

    except Exception as e:

        return None, f"Error communicating with backend: {e}"


def money(value):

    return f"R {value:,.2f}"


def stock_status(quantity):

    if quantity <= 0:
        return "OUT OF STOCK"

    elif quantity <= 10:
        return "LOW STOCK"

    else:
        return "IN STOCK"


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="dashboard-title">PocketLedger</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Financial Identity Passport & Business Dashboard'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# TABS
# ============================================================

tab1, tab2 = st.tabs(
    [
        "🏦 Lender View",
        "🧑🏾‍🌾 Merchant View"
    ]
)


# ################################################################
# ################################################################
# LENDER VIEW
# ################################################################
# ################################################################

with tab1:

    st.header("Financial Identity Passport")

    st.write(
        "A lender-focused view of the merchant's financial "
        "activity, business health and evidence strength."
    )

    # ------------------------------------------------------------
    # LENDER AUTHENTICATION
    # ------------------------------------------------------------

    st.sidebar.header("🔐 Lender Authentication")

    oauth_token = st.sidebar.text_input(
        "OAuth 2.0 Token",
        type="password",
        key="lender_oauth"
    )

    if not oauth_token:

        st.info(
            "🔐 Please authenticate to view merchant "
            "financial information."
        )

    elif oauth_token != "mock_valid_token":

        st.error(
            "❌ Invalid or expired OAuth token."
        )

    else:

        st.success(
            "✅ Authentication successful."
        )

        merchant_id = st.text_input(
            "Merchant ID",
            value=DEFAULT_MERCHANT_ID,
            key="lender_merchant_id"
        )

        if st.button(
            "Load Financial Passport",
            type="primary",
            key="load_passport"
        ):

            with st.spinner(
                "Loading merchant financial passport..."
            ):

                passport_data, passport_error = fetch_json(
                    f"/api/passport/{merchant_id}"
                )

                revenue_data, revenue_error = fetch_json(
                    f"/api/dashboard/revenue/{merchant_id}"
                )

                if passport_data:

                    st.session_state.lender_passport = (
                        passport_data
                    )

                if revenue_data:

                    st.session_state.lender_revenue = (
                        revenue_data
                    )

                if passport_error:
                    st.error(passport_error)

                if revenue_error:
                    st.error(revenue_error)

        # --------------------------------------------------------
        # DISPLAY LENDER DATA
        # --------------------------------------------------------

        if "lender_passport" in st.session_state:

            data = st.session_state.lender_passport

            st.divider()

            st.subheader("💰 Financial Overview")

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Cumulative Revenue",
                money(data["cumulative_revenue"])
            )

            col2.metric(
                "Total Transactions",
                f"{data['total_transactions']:,}"
            )

            average_transaction = (
                data["cumulative_revenue"]
                / data["total_transactions"]
                if data["total_transactions"] > 0
                else 0
            )

            col3.metric(
                "Average Transaction",
                money(average_transaction)
            )

            col4.metric(
                "Operating History",
                f"{data['operating_history_months']} months"
            )

            # ----------------------------------------------------
            # TRUST METRICS
            # ----------------------------------------------------

            st.divider()

            st.subheader(
                "🛡️ Business Trust & Health"
            )

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Business Health",
                f"{data['health_score']}/100"
            )

            col2.metric(
                "Evidence Confidence",
                f"{data['evidence_confidence_pct']}%"
            )

            col3.metric(
                "Revenue Consistency",
                f"{data['revenue_consistency_pct']}%"
            )

            # ----------------------------------------------------
            # GAUGES
            # ----------------------------------------------------

            col1, col2 = st.columns(2)

            health_score = data["health_score"]

            fig_health = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=health_score,
                    title={
                        "text": "Business Health Score"
                    },
                    gauge={
                        "axis": {
                            "range": [0, 100]
                        },
                        "bar": {
                            "color": "darkblue"
                        }
                    }
                )
            )

            col1.plotly_chart(
                fig_health,
                use_container_width=True
            )

            evidence_score = data[
                "evidence_confidence_pct"
            ]

            fig_evidence = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=evidence_score,
                    title={
                        "text": "Evidence Confidence"
                    },
                    gauge={
                        "axis": {
                            "range": [0, 100]
                        },
                        "bar": {
                            "color": "green"
                        }
                    }
                )
            )

            col2.plotly_chart(
                fig_evidence,
                use_container_width=True
            )

            # ----------------------------------------------------
            # REVENUE PERFORMANCE
            # ----------------------------------------------------

            st.divider()

            st.subheader(
                "📈 Revenue Performance"
            )

            if "lender_revenue" in st.session_state:

                revenue = st.session_state.lender_revenue

                chart1, chart2, chart3 = st.tabs(
                    [
                        "Daily",
                        "Weekly",
                        "Monthly"
                    ]
                )

                # =================================================
                # DAILY GRAPH
                # =================================================

                with chart1:

                    daily = revenue.get(
                        "daily",
                        []
                    )

                    if daily:

                        dates = [
                            item["date"]
                            for item in daily
                        ]

                        values = [
                            item["revenue"]
                            for item in daily
                        ]

                        fig = go.Figure()

                        fig.add_trace(
                            go.Scatter(
                                x=dates,
                                y=values,
                                mode="lines+markers",
                                name="Daily Revenue"
                            )
                        )

                        fig.update_layout(
                            title="Daily Revenue — Last 7 Days",
                            xaxis_title="Date",
                            yaxis_title="Revenue (R)",
                            hovermode="x unified"
                        )

                        st.plotly_chart(
                            fig,
                            use_container_width=True
                        )

                # =================================================
                # WEEKLY GRAPH
                # =================================================

                with chart2:

                    weekly = revenue.get(
                        "weekly",
                        []
                    )

                    if weekly:

                        labels = [
                            f"{item['week_start']} → "
                            f"{item['week_end']}"
                            for item in weekly
                        ]

                        values = [
                            item["revenue"]
                            for item in weekly
                        ]

                        fig = go.Figure()

                        fig.add_trace(
                            go.Bar(
                                x=labels,
                                y=values,
                                name="Weekly Revenue"
                            )
                        )

                        fig.update_layout(
                            title="Weekly Revenue — Last 4 Weeks",
                            xaxis_title="Week",
                            yaxis_title="Revenue (R)"
                        )

                        st.plotly_chart(
                            fig,
                            use_container_width=True
                        )

                # =================================================
                # MONTHLY GRAPH
                # =================================================

                with chart3:

                    monthly = revenue.get(
                        "monthly",
                        []
                    )

                    if monthly:

                        labels = [
                            f"{item['year']}-"
                            f"{item['month']:02d}"
                            for item in monthly
                        ]

                        values = [
                            item["revenue"]
                            for item in monthly
                        ]

                        fig = go.Figure()

                        fig.add_trace(
                            go.Bar(
                                x=labels,
                                y=values,
                                name="Monthly Revenue"
                            )
                        )

                        fig.update_layout(
                            title="Monthly Revenue — Last 6 Months",
                            xaxis_title="Month",
                            yaxis_title="Revenue (R)"
                        )

                        st.plotly_chart(
                            fig,
                            use_container_width=True
                        )

            # ----------------------------------------------------
            # BLOCKCHAIN
            # ----------------------------------------------------

            st.divider()

            st.subheader(
                "⛓️ Financial Data Integrity"
            )

            if st.button(
                "🔎 Verify Blockchain Integrity",
                key="verify_lender"
            ):

                with st.spinner(
                    "Verifying financial state..."
                ):

                    verify_data, verify_error = fetch_json(
                        f"/api/verify/{merchant_id}"
                    )

                    if verify_data:

                        if verify_data.get(
                            "is_valid"
                        ):

                            st.success(
                                "✅ Integrity Verified — "
                                "current financial data matches "
                                "the blockchain state."
                            )

                            st.code(
                                verify_data["live_hash"],
                                language="text"
                            )

                        else:

                            st.error(
                                "❌ Integrity Verification Failed."
                            )

                    elif verify_error:

                        st.error(verify_error)


# ################################################################
# ################################################################
# MERCHANT VIEW
# ################################################################
# ################################################################

with tab2:

    st.header("Merchant Business Dashboard")

    st.write(
        "Track your daily money, sales performance and "
        "inventory."
    )

    # ------------------------------------------------------------
    # MERCHANT ID
    # ------------------------------------------------------------

    merchant_id = st.text_input(
        "Merchant ID",
        value=DEFAULT_MERCHANT_ID,
        key="merchant_dashboard_id"
    )

    # ------------------------------------------------------------
    # REFRESH BUTTON
    # ------------------------------------------------------------

    if st.button(
        "🔄 Refresh Business Dashboard",
        type="primary",
        key="refresh_merchant"
    ):

        with st.spinner(
            "Updating business information..."
        ):

            passport, passport_error = fetch_json(
                f"/api/passport/{merchant_id}"
            )

            revenue, revenue_error = fetch_json(
                f"/api/dashboard/revenue/{merchant_id}"
            )

            inventory, inventory_error = fetch_json(
                f"/api/dashboard/inventory/{merchant_id}"
            )

            daily_sales, daily_sales_error = fetch_json(
                f"/api/dashboard/daily-sales/{merchant_id}"
            )

            if passport:
                st.session_state.merchant_passport = passport

            if revenue:
                st.session_state.merchant_revenue = revenue

            if inventory:
                st.session_state.merchant_inventory = inventory

            if daily_sales:
                st.session_state.merchant_daily_sales = daily_sales

            if passport_error:
                st.error(passport_error)

            if revenue_error:
                st.error(revenue_error)

            if inventory_error:
                st.error(inventory_error)

            if daily_sales_error:
                st.error(daily_sales_error)

    # ============================================================
    # MONEY OVERVIEW
    # ============================================================

    if "merchant_passport" in st.session_state:

        data = st.session_state.merchant_passport

        st.divider()

        st.subheader("💰 Money Overview")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Revenue",
            money(data["cumulative_revenue"])
        )

        col2.metric(
            "Total Sales",
            f"{data['total_transactions']:,}"
        )

        average_sale = (
            data["cumulative_revenue"]
            / data["total_transactions"]
            if data["total_transactions"] > 0
            else 0
        )

        col3.metric(
            "Average Sale",
            money(average_sale)
        )

        col4.metric(
            "Business Health",
            f"{data['health_score']}/100"
        )

    # ============================================================
    # TODAY'S SALES
    # ============================================================

    st.divider()

    st.subheader("🛒 Today's Sales")

    if "merchant_daily_sales" in st.session_state:

        daily_sales = st.session_state.merchant_daily_sales

        sales = daily_sales.get(
            "sales",
            []
        )

        if sales:

            rows = []

            for sale in sales:

                rows.append(
                    {
                        "Time": sale.get(
                            "time",
                            ""
                        ),
                        "Product": sale.get(
                            "product",
                            "Unknown"
                        ),
                        "Quantity": sale.get(
                            "quantity",
                            1
                        ),
                        "Revenue": money(
                            sale.get(
                                "revenue",
                                0
                            )
                        )
                    }
                )

            sales_df = pd.DataFrame(rows)

            st.dataframe(
                sales_df,
                use_container_width=True,
                hide_index=True
            )

            # -----------------------------------------------
            # TODAY'S TOTALS
            # -----------------------------------------------

            today_revenue = daily_sales.get(
                "total_revenue",
                0
            )

            today_transactions = daily_sales.get(
                "total_transactions",
                0
            )

            # Expense data is not yet stored by backend.
            today_expenses = 0.0

            today_profit = (
                today_revenue - today_expenses
            )

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Today's Revenue",
                money(today_revenue)
            )

            col2.metric(
                "Today's Expenses",
                money(today_expenses)
            )

            col3.metric(
                "Today's Profit",
                money(today_profit)
            )

        else:

            st.info(
                "No sales have been recorded today."
            )

    else:

        st.info(
            "Click **Refresh Business Dashboard** "
            "to load today's sales."
        )

    # ============================================================
    # WEEKLY PERFORMANCE
    # ============================================================

    st.divider()

    st.subheader("📅 Weekly Performance")

    if "merchant_revenue" in st.session_state:

        revenue = st.session_state.merchant_revenue

        weekly = revenue.get(
            "weekly",
            []
        )

        if weekly:

            latest_week = weekly[-1]

            weekly_revenue = latest_week.get(
                "revenue",
                0
            )

            weekly_expenses = 0.0

            weekly_profit = (
                weekly_revenue
                - weekly_expenses
            )

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Weekly Revenue",
                money(weekly_revenue)
            )

            col2.metric(
                "Weekly Expenses",
                money(weekly_expenses)
            )

            col3.metric(
                "Weekly Profit",
                money(weekly_profit)
            )

            # -----------------------------------------------
            # WEEKLY GRAPH
            # -----------------------------------------------

            labels = [
                f"{item['week_start']} → "
                f"{item['week_end']}"
                for item in weekly
            ]

            values = [
                item["revenue"]
                for item in weekly
            ]

            fig = go.Figure()

            fig.add_trace(
                go.Bar(
                    x=labels,
                    y=values,
                    name="Revenue"
                )
            )

            fig.update_layout(
                title="Weekly Revenue",
                xaxis_title="Week",
                yaxis_title="Revenue (R)"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    # ============================================================
    # MONTHLY PERFORMANCE
    # ============================================================

    st.divider()

    st.subheader("📆 Monthly Performance")

    if "merchant_revenue" in st.session_state:

        revenue = st.session_state.merchant_revenue

        monthly = revenue.get(
            "monthly",
            []
        )

        if monthly:

            latest_month = monthly[-1]

            monthly_revenue = latest_month.get(
                "revenue",
                0
            )

            monthly_expenses = 0.0

            monthly_profit = (
                monthly_revenue
                - monthly_expenses
            )

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Monthly Revenue",
                money(monthly_revenue)
            )

            col2.metric(
                "Monthly Expenses",
                money(monthly_expenses)
            )

            col3.metric(
                "Monthly Profit",
                money(monthly_profit)
            )

            # -----------------------------------------------
            # MONTHLY GRAPH
            # -----------------------------------------------

            labels = [
                f"{item['year']}-"
                f"{item['month']:02d}"
                for item in monthly
            ]

            values = [
                item["revenue"]
                for item in monthly
            ]

            fig = go.Figure()

            fig.add_trace(
                go.Bar(
                    x=labels,
                    y=values,
                    name="Revenue"
                )
            )

            fig.update_layout(
                title="Monthly Revenue",
                xaxis_title="Month",
                yaxis_title="Revenue (R)"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    # ============================================================
    # INVENTORY
    # ============================================================

    st.divider()

    st.subheader("📦 Current Inventory")

    if "merchant_inventory" in st.session_state:

        inventory_data = st.session_state.merchant_inventory

        inventory = inventory_data.get(
            "inventory",
            []
        )

        if inventory:

            rows = []

            for item in inventory:

                quantity = item.get(
                    "quantity_on_hand",
                    0
                )

                rows.append(
                    {
                        "Product": item.get(
                            "name",
                            "Unknown"
                        ),
                        "Quantity Available": quantity,
                        "Unit Price": money(
                            item.get(
                                "unit_price",
                                0
                            )
                        ),
                        "Stock Status": stock_status(
                            quantity
                        )
                    }
                )

            inventory_df = pd.DataFrame(rows)

            st.dataframe(
                inventory_df,
                use_container_width=True,
                hide_index=True
            )

            # -----------------------------------------------
            # INVENTORY SUMMARY
            # -----------------------------------------------

            total_products = len(inventory)

            low_stock = sum(
                1
                for item in inventory
                if 0 < item.get(
                    "quantity_on_hand",
                    0
                ) <= 10
            )

            out_of_stock = sum(
                1
                for item in inventory
                if item.get(
                    "quantity_on_hand",
                    0
                ) <= 0
            )

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Products Tracked",
                total_products
            )

            col2.metric(
                "Low Stock",
                low_stock
            )

            col3.metric(
                "Out of Stock",
                out_of_stock
            )

        else:

            st.info(
                "No inventory items have been recorded."
            )

    # ============================================================
    # WHATSAPP / AI TRANSACTION SIMULATOR
    # ============================================================

    st.divider()

    st.subheader(
        "💬 Log New Sale"
    )

    st.write(
        "This simulates the WhatsApp → AI → Ledger Engine "
        "pipeline."
    )

    sim_text = st.text_area(
        "WhatsApp Message",
        value="I just sold 3 loaves of bread for R45",
        key="merchant_transaction_text"
    )

    if st.button(
        "🚀 Log Transaction via AI",
        key="log_transaction"
    ):

        with st.spinner(
            "Processing transaction..."
        ):

            try:

                payload = {
                    "merchant_id": merchant_id,
                    "source_channel": "text",
                    "raw_text": sim_text
                }

                headers = {
                    "x-internal-token":
                        "super_secret_internal_key"
                }

                response = requests.post(
                    f"{LEDGER_ENGINE_URL}"
                    "/internal/transactions",
                    json=payload,
                    headers=headers,
                    timeout=30
                )

                if response.status_code == 200:

                    result = response.json()

                    st.success(
                        "✅ Transaction logged successfully!"
                    )

                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        "Evidence Weight",
                        result.get(
                            "recorded_weight",
                            0
                        )
                    )

                    col2.metric(
                        "Health Score",
                        f"{result.get('health_score', 0)}/100"
                    )

                    col3.metric(
                        "Evidence Confidence",
                        f"{result.get('evidence_confidence_pct', 0)}%"
                    )

                    transaction_id = result.get(
                        "transaction_id"
                    )

                    if transaction_id:

                        st.success(
                            f"Transaction ID: "
                            f"{transaction_id}"
                        )

                        st.markdown(
                            f"[📄 Download Receipt PDF]"
                            f"({LEDGER_ENGINE_URL}"
                            f"/api/invoice/"
                            f"{transaction_id})"
                        )

                        st.info(
                            "🔄 Refresh the dashboard above "
                            "to update sales and inventory."
                        )

                else:

                    st.error(
                        "Transaction failed: "
                        f"{response.text}"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Could not connect to the Ledger Engine."
                )

            except Exception as e:

                st.error(
                    f"Error connecting to backend: {e}"
                )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "PocketLedger • Financial Identity Passport • "
    "AI-powered financial record keeping"
)
