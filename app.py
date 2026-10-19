import time
import pandas as pd
import streamlit as st
from data import (load_opportunities, recommend, build_email, edit_rate,
                  is_stalled, MINUTES_PER_DRAFT, STALLED_DAYS)

st.set_page_config(page_title="Salesforce AI Sidekick", page_icon="🤖", layout="wide")
df = load_opportunities()
S = st.session_state
S.setdefault("events", [])
S.setdefault("recs", {})
S.setdefault("drafts", {})
S.setdefault("used", {})
S.setdefault("selected", df["Opportunity"][0])

def log(event, opp, detail=""):
    S["events"].append({"time": time.strftime("%H:%M:%S"), "event": event, "opportunity": opp, "detail": detail})

def count(name):
    return sum(e["event"] == name for e in S["events"])

st.title("🤖 Salesforce AI Sidekick")
st.caption("Prototype with synthetic data. Rule-based suggestions; no real Salesforce account or AI model is connected.")

# ---- Sidebar: value + telemetry (measured in this session only) ----
with st.sidebar:
    st.header("📈 Your value this session")
    shown, accepted = count("suggestion_shown"), count("draft_used")
    c1, c2 = st.columns(2)
    c1.metric("Suggestions", shown)
    c2.metric("Drafts used", accepted)
    rates = [int(e["detail"].split("=")[1].rstrip("%")) for e in S["events"] if e["event"] == "draft_used"]
    st.metric("Avg. edit rate", f"{sum(rates) / len(rates):.0f}%" if rates else "–")
    st.metric("Est. time saved", f"{accepted * MINUTES_PER_DRAFT} min")
    st.caption(f"Illustrative estimate: {MINUTES_PER_DRAFT} min per draft is an assumption, not a measurement. "
               "All other numbers are counted from this session.")
    with st.expander("Telemetry log (session only)"):
        if S["events"]:
            st.dataframe(pd.DataFrame(S["events"]), hide_index=True)
        else:
            st.write("No events yet.")

# ---- Nudge: surface the deal that needs attention, in context ----
stalled = df[df.apply(is_stalled, axis=1)].sort_values("Deal Value", ascending=False)
if not stalled.empty:
    top = stalled.iloc[0]
    st.warning(f"**{top['Opportunity']}** has had no activity for {top['Days Since Activity']} days "
               f"(rule: {STALLED_DAYS}+ days). Worth a look.")
    def review(name=top["Opportunity"]):
        S["selected"] = name
        log("nudge_accepted", name)
    st.button("Review this deal", on_click=review)

st.header("📊 Sales Opportunities")
st.dataframe(df.drop(columns=["Last Note"]), width="stretch", hide_index=True)

st.header("🔍 Opportunity")
opp = st.selectbox("Select a sales opportunity", df["Opportunity"], key="selected")
row = df[df["Opportunity"] == opp].iloc[0]
m = st.columns(4)
m[0].metric("Deal Value", f"${row['Deal Value']:,}")
m[1].metric("Stage", row["Stage"])
m[2].metric("Priority", row["Priority"])
m[3].metric("Days since activity", row["Days Since Activity"])
st.caption(f"Contact: {row['Contact']} · Close date: {row['Close Date']} · Note: {row['Last Note']}")

# ---- Recommendation ----
st.header("🤖 AI Sidekick")
if st.button("Suggest next step"):
    with st.spinner("Reading the opportunity record…"):
        time.sleep(0.5)
        S["recs"][opp] = recommend(row)
    log("suggestion_shown", opp)
rec = S["recs"].get(opp)
if rec is None:
    st.info("No suggestion yet. Click **Suggest next step** to get one for this deal.")
else:
    st.success(f"Recommended next step: **{rec['action']}**")
    if rec["stalled"]:
        st.warning("This deal looks stalled, so a follow-up is time-sensitive.")
    with st.expander("💡 Why this recommendation? (sources from the record)", expanded=True):
        for text, field in rec["reasons"]:
            st.write(f"• {text}  `{field}`")
        st.caption("Predefined rules over sample data. Not an AI-generated prediction.")

    # ---- Email: review, edit, then use ----
    st.header("✉️ Follow-up email")
    if st.button("Draft follow-up email"):
        subj, body = build_email(row)
        S["drafts"][opp] = (subj, body)
        S[f"subj_{opp}"], S[f"body_{opp}"] = subj, body
        S["used"].pop(opp, None)
        log("draft_generated", opp)
    if opp in S["drafts"]:
        st.text_input("Subject", key=f"subj_{opp}")
        st.text_area("Body (edit freely; nothing is sent)", key=f"body_{opp}", height=260)
        if st.button("✅ Use this draft"):
            o_subj, o_body = S["drafts"][opp]
            rate = edit_rate(o_subj + " " + o_body, S[f"subj_{opp}"] + " " + S[f"body_{opp}"])
            S["used"][opp] = f"Subject: {S[f'subj_{opp}']}\n\n{S[f'body_{opp}']}"
            log("draft_used", opp, f"edit_rate={rate}%")
            st.rerun()
        if opp in S["used"]:
            st.success("Draft recorded as used. Use the copy icon on the block below to copy it.")
            st.code(S["used"][opp], language=None)
            def share(name=opp):
                if S.get(f"share_{name}"):
                    log("win_shared", name)
            st.checkbox("Share this win with my team (shows on the Manager view)", key=f"share_{opp}", on_change=share)

    # ---- Feedback tied to this recommendation ----
    st.header("💬 Was this helpful?")
    helpful = st.radio("Recommendation for this deal", ["Yes", "No"], horizontal=True, key=f"fb_{opp}")
    reason = ""
    if helpful == "No":
        reason = st.selectbox("What was off?", ["Wrong priority", "Missing context", "Not relevant", "Other"], key=f"why_{opp}")
    if st.button("Submit feedback"):
        log("feedback", opp, f"{helpful}{': ' + reason if reason else ''}")
        st.success("Thanks. Recorded in this session's telemetry log.")

