from typing import Dict, List, Optional, Any
from ..client.logseq_client import LogseqAPIClient
from ..mcp import mcp

# Initialize client with configuration
logseq_client = LogseqAPIClient()

@mcp.tool()
def get_all_pages() -> List[Dict]:
    """
    Gets all pages from the Logseq graph.
    
    Journal pages can be identified by the "journal?" attribute set to true and 
    will include a "journalDay" attribute in the format YYYYMMDD.
    
    Returns:
        list: A list of all pages in the Logseq graph.
    """
    """Fetch all pages from Logseq."""
    return logseq_client.get_all_pages()

@mcp.tool()
def get_page(name: str) -> Optional[Dict]:
    """
    Gets a specific page from the Logseq graph by name.
    
    For journal pages, use the format "mmm dth, yyyy" (e.g., "Apr 4th, 2025").
    Note that journal pages are automatically created in Logseq with this date format.
    
    Journal pages have specific attributes:
    - "journal?": true - Indicates this is a journal page
    - "journalDay": YYYYMMDD - The date in numeric format (e.g., 20250404 for April 4, 2025)
    
    Args:
        name (str): The name of the page to retrieve.
        
    Returns:
        dict: Information about the requested page.
    """
    """Fetch a specific page by name."""
    return logseq_client.get_page(name)

@mcp.tool() 
def create_page(name: str, properties: Optional[Dict] = None) -> Dict:
    """
    Creates a new page in the Logseq graph.
    
    For journal pages, use the format "mmm dth, yyyy" (e.g., "Apr 4th, 2025").
    Journal pages are specially formatted in Logseq with automatic dating.
    
    When you create a journal page, Logseq automatically:
    - Sets "journal?": true
    - Sets "journalDay": YYYYMMDD (e.g., 20250404 for April 4, 2025)
    - Formats the page as a journal entry
    
    Args:
        name (str): The name of the new page.
        properties (dict, optional): Properties to set on the new page.
        
    Returns:
        dict: Information about the created page.
    """
    """Create a new page with the given name and properties."""
    return logseq_client.create_page(name, properties)

@mcp.tool()
def delete_page(name: str) -> Dict:
    """
    Deletes a page from the Logseq graph.
    
    This operation removes the specified page and all its blocks. This action cannot be undone.
    
    For journal pages, use the format "mmm dth, yyyy" (e.g., "Apr 4th, 2025").
    
    Args:
        name (str): The name of the page to delete.
        
    Returns:
        dict: Result of the deletion operation.
    """
    """Delete a page from the Logseq graph."""
    return logseq_client.delete_page(name)

@mcp.tool()
def get_page_linked_references(page_name: str) -> List[Dict]:
    """
    Gets all linked references to a specific page in the Logseq graph.
    
    This returns blocks that contain links to the specified page using
    the Logseq double bracket notation: [[Page Name]].
    
    For journal pages, use the format "mmm dth, yyyy" (e.g., "Apr 4th, 2025").
    
    Args:
        page_name (str): The name of the page to find references to.
        
    Returns:
        list: A list of blocks that reference the specified page.
    """
    """Get all blocks that link to the specified page."""
    return logseq_client.get_page_linked_references(page_name) 