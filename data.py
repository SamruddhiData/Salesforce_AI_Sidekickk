"""Synthetic CRM data and rule logic. No real Salesforce or LLM is connected."""
import difflib
import pandas as pd

OPPORTUNITIES = [
    {"Opportunity": "Acme Corp - CRM Upgrade", "Stage": "Negotiation", "Priority": "High",
     "Deal Value": 50000, "Next Action": "Send revised proposal", "Contact": "Priya Shah",
     "Days Since Activity": 9, "Close Date": "2026-11-30",
     "Last Note": "Asked for a 2-year price option; budget freeze until Q1."},
    {"Opportunity": "BrightTech - Software Deal", "Stage": "Proposal", "Priority": "Medium",
     "Deal Value": 35000, "Next Action": "Schedule product demo", "Contact": "Marcus Lee",
     "Days Since Activity": 3, "Close Date": "2026-12-15",
     "Last Note": "Liked the pilot results; wants to see reporting features."},
    {"Opportunity": "Nova Ltd - Annual Renewal", "Stage": "Qualification", "Priority": "Low",
     "Deal Value": 20000, "Next Action": "Confirm customer requirements", "Contact": "Elena Rossi",
     "Days Since Activity": 14, "Close Date": "2027-01-31",
     "Last Note": "Requirements call was postponed twice."},
]
STALLED_DAYS = 7          # rule threshold, shown to the user
MINUTES_PER_DRAFT = 8     # ILLUSTRATIVE assumption, labelled as such in the UI

def load_opportunities():
    return pd.DataFrame(OPPORTUNITIES)

def is_stalled(row):
    return row["Days Since Activity"] >= STALLED_DAYS

def recommend(row):
    """Rule-based recommendation. Each reason names the CRM field it uses."""
    reasons = [
        (f"Stage is {row['Stage']}.", "Stage"),
        (f"Priority is {row['Priority']}.", "Priority"),
        (f"Last activity was {row['Days Since Activity']} days ago"
         + (f" (rule: stalled at {STALLED_DAYS}+ days)." if is_stalled(row) else "."), "Days Since Activity"),
        (f"Latest note: {row['Last Note']}", "Last Note"),
    ]
    return {"action": row["Next Action"], "stalled": bool(is_stalled(row)), "reasons": reasons}

def build_email(row):
    first = row["Contact"].split()[0]
    subject = f"Follow-up: {row['Opportunity']}"
    body = (f"Hi {first},\n\nThanks for your time recently. Following up on {row['Opportunity']}: "
            f"our next step is to {row['Next Action'].lower()}.\n\n"
            f"On your earlier point: {row['Last Note']}\n\n"
            "Could we find 20 minutes this week to talk it through?\n\nBest regards,\nSales Team")
    return subject, body

def edit_rate(original, edited):
    """Percent of words changed, from a word-level diff."""
    return round((1 - difflib.SequenceMatcher(None, original.split(), edited.split()).ratio()) * 100)

