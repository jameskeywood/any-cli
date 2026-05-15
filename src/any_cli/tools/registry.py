from any_cli.tools.base import BaseTool
from any_cli.tools.list_dir import ListDirTool
from any_cli.tools.read_file import ReadFileTool


TOOLS: dict[str, BaseTool] = {
    "read_file": ReadFileTool(),
    "list_dir": ListDirTool(),
}


def get_tools() -> list[BaseTool]:
    return list(TOOLS.values())

