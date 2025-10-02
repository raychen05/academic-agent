import asyncio
from app.short_term import add_message, get_messages
from app.orchestrator import handle_user_message

async def test_basic_flow():
    conv_id = 'test-conv'
    add_message(conv_id, 'user', 'Hello, I work on gene expression analysis')
    add_message(conv_id, 'assistant', 'Nice! What organism?')
    res = await handle_user_message(conv_id, 'user', 'Human. Summarize my previous settings and remind me')
    assert isinstance(res, str)

if __name__ == '__main__':
    asyncio.run(test_basic_flow())