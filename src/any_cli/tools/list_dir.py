from pathlib import Path

from any_cli.tools.base import BaseTool


class ListDirTool(BaseTool):
    name = "list_dir"

    description = "List files in a directory"

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
            return "Directory does not exist"

        if not path.is_dir():
            return "Path is not a directory"

        files = sorted(
            item.name
            for item in path.iterdir()
        )

        return "\n".join(files)

