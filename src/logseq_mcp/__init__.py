from .mcp import mcp
from .utils.logging import log
from .tools import (
    get_all_pages, 
    get_page, 
    create_page,
    get_page_blocks,
    get_block,
    create_block, 
    update_block,
    search_blocks,
    get_page_linked_references,
)
import os
import inspect

__all__ = ["get_all_pages", "get_page", "create_page", "get_page_blocks", "get_block", "create_block", "update_block", "search_blocks", "get_page_linked_references"]


def main():
  """Main function to run the Logseq MCP server"""
  log("Starting Logseq MCP server...")
  mcp.run(transport="stdio")