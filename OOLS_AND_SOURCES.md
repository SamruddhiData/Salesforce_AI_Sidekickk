# Tools used and sources (Salesforce AI Sidekick)

## Tools and how they were used
- **Streamlit + pandas (Python):** the prototype. Run with `streamlit run app.py`.
- **pytest + Streamlit AppTest:** headless tests for the rules and the main flow.
- **Claude (Anthropic) as an AI coding and thinking assistant:** reviewed my original Streamlit code, proposed the UX/PM changes, wrote the revised code and tests, and helped draft this document. I reviewed the changes, ran the app, and I can explain every part. *(Edit this paragraph so it matches exactly what you did.)*
- **Data:** synthetic only. No real Salesforce account, no live LLM. Suggestions and emails are rule-based.

## Sources (all opened and checked)
| Source | URL | How it shaped the design |
|---|---|---|
| Salesforce Trailhead: Maximize Sales Performance with Agentforce Actions | https://trailhead.salesforce.com/content/learn/modules/einstein-copilot-sales-actions-for-sellers-quick-look/maximize-sales-performance-with-einstein-copilot-actions | Shows the native Summarize Record and Meeting Follow-Up Email actions. I scoped the Sidekick to the same scenario and added timing, reasons, and value shown back to the rep. |
| Salesforce Agentforce workshop: Get Started | https://developer.salesforce.com/agentforce-workshop/agents/1-get-started | Lists the standard actions (Draft or Revise Email, Summarize Record, etc.). Used to say what is native vs. what I add. |
| Google PAIR, Explainability + Trust | https://pair.withgoogle.com/chapter/People%20+%20AI%20Guidebook%20-%20Explainability%20+%20Trust.pdf | Users should calibrate trust, not trust blindly. Led to "Why this recommendation?" with the source field named per reason. |
| Google PAIR, Feedback + Control | https://pair.withgoogle.com/chapter/People%20+%20AI%20Guidebook%20-%20Feedback%20+%20Control.pdf | Control builds trust; feedback should be easy and explicit plus implicit logs. Led to edit-before-use, "Use this draft", feedback with a reason, and the telemetry log. |
| Einstein Trust Layer explainers (secondary, not official Salesforce docs): https://salesforcegeek.in/einstein-trust-layer-in-salesforce/ and https://salesforcebreak.com/2026/07/31/ai-data-masking-mapping/ | as listed | Describe grounding that respects user permissions and an audit trail. Used in the "how it would work in production" slide. **Replace or back up with the official Salesforce Help page before presenting.** |

## What is research and what is assumption
- **Supported by sources above:** native Salesforce actions exist for summary and email drafting; trust and control are established AI-UX principles.
- **Assumptions I still need to validate (do not present as findings):** reps ignore AI because it appears away from their workflow; a stalled-deal nudge gets accepted; managers will use a coaching view; 8 minutes saved per draft.

## Short user conversations (you must run these yourself)
Talk to 3 to 5 people (sales reps, or students who have done sales or internships). Ask: What do you do the first hour after opening the CRM? When did you last use an AI feature at work, and why or why not? What would make you send an AI-written email without rewriting it? What would your manager need to say or do to change your habits? Record: role, date, one quote, one surprise. **Report only what people actually said, with counts (e.g. "3 of 4").**

## Hypotheses and how the prototype tests them
| # | Hypothesis | Prototype evidence | Production metric |
|---|---|---|---|
| H1 | Nudging at the moment a deal stalls raises activation | `nudge_accepted` events | % of reps who act on a nudge in week 1 |
| H2 | Named sources per reason raise acceptance | `draft_used` after reasons viewed | Acceptance rate, 👎 reasons |
| H3 | Showing the rep their own time saved drives repeat use | Value panel (illustrative minutes) | Reps with 3+ uses per week; week-4 retention |
| H4 | Visible team wins and manager coaching spread adoption | `win_shared`, Manager view | Adoption spread across the team |
Prototype telemetry is session-only demo data; production metrics are proposals.
