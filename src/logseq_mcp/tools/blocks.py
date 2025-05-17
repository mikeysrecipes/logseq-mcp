from typing import Dict, List, Optional, Any
from ..client.logseq_client import LogseqAPIClient
from ..mcp import mcp

# Initialize client with configuration
logseq_client = LogseqAPIClient()

@mcp.tool()
def get_page_blocks(page_name: str) -> List[Dict]:
    """
    Gets all blocks from a specific page in the Logseq graph.
    
    For journal pages, use the format "mmm dth, yyyy" (e.g., "Apr 4th, 2025").
    Returned blocks contain information about their hierarchical structure:
      - parent: The parent block's ID
      - level: The indentation level (1 for top-level, 2+ for indented blocks)
      - left: The block to the left (typically the parent for indented blocks)
    
    Blocks from journal pages will have:
      - "journal?": true
      - "journalDay": YYYYMMDD - The date in numeric format (e.g., 20250404)
    
    Args:
        page_name (str): The name of the page to retrieve blocks from.
        
    Returns:
        list: A list of blocks from the specified page.
    """
    """Fetch all blocks from a specific page."""
    return logseq_client.get_page_blocks(page_name)

@mcp.tool()
def get_block(block_id: str) -> Optional[Dict]:
    """
    Gets a specific block from the Logseq graph by its ID.
    
    The returned block contains information about its hierarchical structure:
      - parent: The parent block's ID
      - level: The indentation level (1 for top-level, 2+ for indented blocks)
      - left: The block to the left (typically the parent for indented blocks)
    
    If the block is from a journal page, it will include:
      - "journal?": true
      - "journalDay": YYYYMMDD - Date in numeric format
    
    Args:
        block_id (str): The ID of the block to retrieve.
        
    Returns:
        dict: Information about the requested block.
    """
    """Fetch a specific block by ID."""
    return logseq_client.get_block(block_id)

@mcp.tool()
def create_block(page_name: str, content: str, properties: Optional[Dict] = None) -> Dict:
    """
    Creates a new block on a page in the Logseq graph.
    
    IMPORTANT NOTES:
    1. All blocks are automatically formatted as bullet points in Logseq UI
    2. To create links to other pages, use double brackets: [[Page Name]]
    
    When creating blocks on journal pages:
      - The block will inherit the "journal?" and "journalDay" attributes from the page
      - "journalDay" will be in YYYYMMDD format (e.g., 20250404 for April 4, 2025)
    
    Args:
        page_name (str): The name of the page to create the block on.
        content (str): The content of the new block.
        properties (dict, optional): Properties to set on the new block.
        
    Returns:
        dict: Information about the created block.
    """
    """Create a new block on the specified page."""
    return logseq_client.create_block(page_name, content, properties)

@mcp.tool()
def insert_block(parent_block_id: str, content: str, properties: Optional[Dict] = None, before: bool = False) -> Dict:
    """
    Inserts a new block as a child of the specified parent block.
    
    This allows for creating hierarchical content by adding children to existing blocks.
    
    IMPORTANT NOTES:
    1. All blocks are automatically formatted as bullet points in Logseq UI
    2. To create links to other pages, use double brackets: [[Page Name]]
    3. The new block will be inserted at the beginning or end of the parent's children
       depending on the 'before' parameter
    
    When inserting blocks into journal pages:
      - The block will inherit the "journal?" and "journalDay" attributes
      - "journalDay" will be in YYYYMMDD format (e.g., 20250404 for April 4, 2025)
    
    Args:
        parent_block_id (str): The ID of the parent block to insert under.
        content (str): The content of the new block.
        properties (dict, optional): Properties to set on the new block.
        before (bool, optional): Whether to insert at the beginning of children. 
                                Default is False (append at the end).
        
    Returns:
        dict: Information about the created block.
    """
    """Insert a new block under the specified parent block."""
    return logseq_client.insert_block(parent_block_id, content, properties, before)

@mcp.tool()
def update_block(block_id: str, content: str, properties: Optional[Dict] = None) -> Dict:
    """
    Updates an existing block in the Logseq graph.
    
    IMPORTANT NOTES:
    1. All blocks are automatically formatted as bullet points in Logseq UI
    2. To create links to other pages, use double brackets: [[Page Name]]
    
    When updating blocks on journal pages:
      - The "journal?" and "journalDay" attributes will be preserved
      - "journalDay" will remain in YYYYMMDD format (e.g., 20250404)
    
    Args:
        block_id (str): The ID of the block to update.
        content (str): The new content for the block.
        properties (dict, optional): Properties to update on the block.
        
    Returns:
        dict: Information about the updated block.
    """
    """Update an existing block with new content and properties."""
    return logseq_client.update_block(block_id, content, properties)

@mcp.tool()
def move_block(block_id: str, target_block_id: str, as_child: bool = False) -> Dict:
    """
    Moves a block to a new location in the graph.
    
    This allows for reorganizing the structure of blocks in the graph by moving
    a block (and all its children) to a different location.
    
    IMPORTANT NOTES:
    1. The block will maintain its children when moved
    2. The hierarchical position depends on the 'as_child' parameter:
       - If as_child=True: The block becomes a child of the target block
       - If as_child=False: The block becomes a sibling after the target block
    
    Args:
        block_id (str): The ID of the block to move.
        target_block_id (str): The ID of the target block to move to.
        as_child (bool, optional): Whether to make the block a child of the target.
                                  Default is False (insert as sibling).
        
    Returns:
        dict: Result of the move operation.
    """
    """Move a block to a new location in the graph."""
    return logseq_client.move_block(block_id, target_block_id, as_child)

@mcp.tool()
def remove_block(block_id: str) -> Dict:
    """
    Removes a block from the Logseq graph.
    
    This operation permanently removes the specified block and all its children.
    This action cannot be undone.
    
    To remove a block, you need its block ID, which can be obtained from:
    - get_page_blocks() function
    - get_block() function
    - search_blocks() function
    
    Args:
        block_id (str): The ID of the block to remove.
        
    Returns:
        dict: Result of the removal operation.
    """
    """Remove a block and its children from the graph."""
    return logseq_client.remove_block(block_id)

@mcp.tool()
def search_blocks(query: str) -> List[Dict]:
    """
    Searches for blocks matching a query in the Logseq graph.
    
    Examples of useful queries:
    - page:"Page Name" - find all blocks on a specific page
    - "search term" - find blocks containing the term
    - page:"Apr 4th, 2025" - find all blocks in a journal
    - [[Page Name]] - find references to a specific page
    
    Returned blocks from journal pages will include:
    - "journal?": true
    - "journalDay": YYYYMMDD - The date in numeric format
    
    Args:
        query (str): The search query.
        
    Returns:
        list: A list of blocks matching the search query.
    """
    """Search for blocks matching the query."""
    return logseq_client.search_blocks(query)