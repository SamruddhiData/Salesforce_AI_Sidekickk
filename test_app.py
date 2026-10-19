from streamlit.testing.v1 import AppTest
from data import edit_rate, load_opportunities, recommend, is_stalled

def test_logic():
    df = load_opportunities()
    assert is_stalled(df.iloc[0]) and not is_stalled(df.iloc[1])
    assert all(f in df.columns for _, f in recommend(df.iloc[0])["reasons"])
    assert edit_rate("a b c d", "a b c d") == 0 and edit_rate("a b c d", "a b x y") > 0

def test_flow():
    at = AppTest.from_file("app.py", default_timeout=15).run()
    assert not at.exception
    next(b for b in at.button if b.label == "Suggest next step").click().run()
    next(b for b in at.button if b.label == "Draft follow-up email").click().run()
    next(b for b in at.button if "Use this draft" in b.label).click().run()
    assert not at.exception
    events = [e["event"] for e in at.session_state["events"]]
    assert events == ["suggestion_shown", "draft_generated", "draft_used"], events
    next(b for b in at.button if b.label == "Submit feedback").click().run()
    assert not at.exception and at.session_state["events"][-1]["event"] == "feedback"

def test_manager_page():
    at = AppTest.from_file("pages/Manager_View.py", default_timeout=15).run()
    assert not at.exception

