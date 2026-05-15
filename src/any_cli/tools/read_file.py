from pathlib import Path

from any_cli.tools.base import BaseTool


class ReadFileTool(BaseTool):
    name = "read_file"

    description = "Read a file from disk"

    schema = {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
            }
        },
        "required": ["path"],
    }

    async def execute(self, arguments: dict) -> str:
        path = Path(arguments["path"])

        if not path.exists():
            return "File does not exist"

        if not path.is_file():
            return "Path is not a file"

        return path.read_text()

