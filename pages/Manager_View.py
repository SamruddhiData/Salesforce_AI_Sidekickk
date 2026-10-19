import pandas as pd
import streamlit as st

st.set_page_config(page_title="Manager view", page_icon="👥", layout="wide")
st.title("👥 Manager view")
st.caption("Team figures below are SYNTHETIC demo data. The 'You' row is counted from this session. "
           "Design principle: managers see adoption and wins, not rep drafts or edits.")

ev = st.session_state.get("events", [])
n = lambda name: sum(e["event"] == name for e in ev)
team = pd.DataFrame([
    {"Rep": "Dana (synthetic)", "Suggestions": 11, "Drafts used": 7, "Wins shared": 2},
    {"Rep": "Ravi (synthetic)", "Suggestions": 6, "Drafts used": 1, "Wins shared": 0},
    {"Rep": "Meera (synthetic)", "Suggestions": 0, "Drafts used": 0, "Wins shared": 0},
    {"Rep": "You (this session)", "Suggestions": n("suggestion_shown"), "Drafts used": n("draft_used"), "Wins shared": n("win_shared")},
])
team["Acceptance"] = team.apply(lambda r: f"{r['Drafts used'] / r['Suggestions']:.0%}" if r["Suggestions"] else "–", axis=1)
a, b = st.columns(2)
a.metric("Reps who tried it (activation)", f"{(team['Suggestions'] > 0).sum()} / {len(team)}")
b.metric("Wins shared this week", int(team["Wins shared"].sum()))
st.dataframe(team, hide_index=True, width="stretch")

st.subheader("Coaching prompts (rule-based)")
for _, r in team.iterrows():
    if r["Suggestions"] == 0:
        st.info(f"{r['Rep']}: hasn't tried the Sidekick. Offer a 10-minute pairing on one live deal.")
    elif r["Drafts used"] == 0:
        st.info(f"{r['Rep']}: sees suggestions but doesn't use drafts. Ask what feels off (trust or tone?).")
st.subheader("Visible wins")
wins = [e for e in ev if e["event"] == "win_shared"]
if wins:
    for w in wins:
        st.success(f"You used a Sidekick follow-up on {w['opportunity']} at {w['time']}.")
else:
    st.write("No wins shared in this session yet. Use a draft on the main page and tick 'Share this win'.")

