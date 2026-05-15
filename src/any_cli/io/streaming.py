from rich.console import Console


async def stream_to_console(
    console: Console,
    stream,
) -> str:
    content = ""

    async for chunk in stream:
        content += chunk

        console.print(chunk, end="")

    console.print()

    return content

