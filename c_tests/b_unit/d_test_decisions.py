import os
os.environ['OPENAI_API_KEY'] = 'sk-dummy'
os.environ['ANTHROPIC_API_KEY'] = 'sk-dummy'
os.environ['GEMINI_API_KEY'] = 'sk-dummy'

from a_platform.a_core.d_session.b_context import Decision, ExecutionContext

def test_add_decision():
    ctx = ExecutionContext()
    dec = Decision(id="D-01", status="adopted", decision="Use SQLite", reason="Simple")
    ctx.add_decision(dec)
    assert len(ctx.decisions) == 1
    assert ctx.decisions[0].id == "D-01"
