from prompt_toolkit import PromptSession


session = PromptSession()


async def get_user_input() -> str:
    return await session.prompt_async("> ")

