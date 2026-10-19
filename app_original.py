import streamlit as st
import pandas as pd

# -------------------------------
# 1. Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Salesforce AI Sidekick",
    page_icon="🤖",
    layout="wide"
)

# -------------------------------
# 2. Application Heading
# -------------------------------
st.title("🤖 Salesforce AI Sidekick")
st.subheader("Your AI Assistant for Smarter Sales Workflows")

st.write(
    "Get insights about sales opportunities, prioritize deals, "
    "and prepare customer follow-up emails."
)

# -------------------------------
# 3. Sample Sales Opportunity Data
# -------------------------------
data = {
    "Opportunity": [
        "Acme Corp - CRM Upgrade",
        "BrightTech - Software Deal",
        "Nova Ltd - Annual Renewal"
    ],
    "Stage": [
        "Negotiation",
        "Proposal",
        "Qualification"
    ],
    "Priority": [
        "High",
        "Medium",
        "Low"
    ],
    "Deal Value": [
        50000,
        35000,
        20000
    ],
    "Next Action": [
        "Send revised proposal",
        "Schedule product demo",
        "Confirm customer requirements"
    ]
}

df = pd.DataFrame(data)

# -------------------------------
# 4. Sales Opportunities Dashboard
# -------------------------------
st.header("📊 Sales Opportunities")
st.dataframe(df, width="stretch")

st.divider()

# -------------------------------
# 5. Opportunity Details
# -------------------------------
st.header("🔍 Opportunity Details")

selected_opportunity = st.selectbox(
    "Select a sales opportunity",
    df["Opportunity"]
)

selected_row = df[
    df["Opportunity"] == selected_opportunity
].iloc[0]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Deal Value",
        f"${selected_row['Deal Value']:,}"
    )

with col2:
    st.metric(
        "Current Stage",
        selected_row["Stage"]
    )

with col3:
    st.metric(
        "Next Action",
        selected_row["Next Action"]
    )

with col4:
    st.metric(
        "Priority",
        selected_row["Priority"]
    )

st.divider()

# -------------------------------
# 6. Sales Insight
# -------------------------------
st.header("🤖 AI Sidekick")
st.write(
    "Get a recommendation for your selected sales opportunity."
)

if st.button("Generate Sales Insight"):

    priority = selected_row["Priority"]
    stage = selected_row["Stage"]

    st.success("Sales Insight Generated")

    st.markdown("### Recommended Next Action")
    st.write(selected_row["Next Action"])

    st.markdown("### Priority Guidance")

    if priority == "High":
        st.warning(
            "High Priority: Follow up promptly and resolve "
            "pending customer concerns."
        )
        priority_reason = (
            "This opportunity is marked High Priority in the "
            "sample data, so it should receive earlier attention."
        )

    elif priority == "Medium":
        st.info(
            "Medium Priority: Follow up soon and confirm "
            "the customer's next steps."
        )
        priority_reason = (
            "This opportunity is marked Medium Priority, so "
            "a timely follow-up may help maintain progress."
        )

    else:
        st.success(
            "Low Priority: Continue regular follow-ups "
            "and monitor the opportunity."
        )
        priority_reason = (
            "This opportunity is marked Low Priority in the "
            "sample data, so regular monitoring is suggested."
        )

    st.markdown("### Suggested Approach")

    if stage == "Negotiation":
        st.write(
            "Address pending concerns and share the revised proposal."
        )
        stage_reason = (
            "The opportunity is in Negotiation, where addressing "
            "concerns and clarifying the proposal may help."
        )

    elif stage == "Proposal":
        st.write(
            "Schedule a product demo, explain key benefits, "
            "and ask for feedback."
        )
        stage_reason = (
            "At the Proposal stage, clarifying benefits and "
            "understanding customer feedback can help."
        )

    else:
        st.write(
            "Understand the customer's requirements, identify "
            "their challenges, and qualify the opportunity."
        )
        stage_reason = (
            "The opportunity is in Qualification, so understanding "
            "customer needs is an important next step."
        )

    with st.expander("💡 Why this recommendation?"):
        st.write(priority_reason)
        st.write(stage_reason)
        st.caption(
            "These explanations use predefined rules and sample data. "
            "They are not AI-generated predictions."
        )

st.divider()

# -------------------------------
# 7. Customer Follow-up Email
# -------------------------------
st.header("✉️ Customer Follow-up Email")

customer_name = st.text_input(
    "Customer name",
    placeholder="Enter customer name"
)

if st.button("Generate Follow-up Email"):

    if not customer_name.strip():
        st.warning("Please enter the customer name.")

    else:
        opportunity_name = selected_row["Opportunity"]
        next_action = selected_row["Next Action"]

        email_subject = (
            f"Follow-up regarding {opportunity_name}"
        )

        email_body = f"""Dear {customer_name.strip()},

I hope you are doing well.

I am following up regarding {opportunity_name}.
As a next step, we would like to {next_action.lower()}.

Please let us know a convenient time to discuss
any questions or requirements you may have.

Looking forward to hearing from you.

Best regards,
Sales Team
"""

        st.success("Follow-up email draft is ready!")

        st.text_input(
            "Email Subject",
            value=email_subject,
            key="email_subject_output"
        )

        st.text_area(
            "Email Draft",
            value=email_body,
            height=250,
            key="email_body_output"
        )

        st.caption(
            "Select the email text and press Ctrl+C to copy it. "
            "The email is not sent automatically."
        )

st.divider()

# -------------------------------
# 8. User Feedback
# -------------------------------
st.header("💬 Feedback on Sales Insight")

feedback = st.radio(
    "Was this recommendation helpful?",
    ["Yes", "No"],
    horizontal=True
)

feedback_comment = st.text_area(
    "Any suggestions? (Optional)",
    placeholder="Tell us how we can improve..."
)

if st.button("Submit Feedback"):

    st.session_state["latest_feedback"] = {
        "response": feedback,
        "comment": feedback_comment
    }

    st.success("Thank you! Your feedback has been recorded for this demo.")

# Show the latest feedback during this session
if "latest_feedback" in st.session_state:
    st.caption(
        "Latest feedback response: "
        + st.session_state["latest_feedback"]["response"]
    )

# -------------------------------
# 9. Footer and Disclaimer
# -------------------------------
st.divider()

st.caption(
    "Prototype using synthetic sample data. "
    "Recommendations use predefined rules; no real Salesforce "
    "account or AI model is connected. Feedback is retained "
    "in the current Streamlit session only."
)
