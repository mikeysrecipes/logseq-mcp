import requests
import os
from typing import Dict, List, Optional, Any, Union


class LogseqAPIClient:
    """Client for interacting with the Logseq API"""
    
    def __init__(self, api_url: str = None, token: str = None):
        """
        Initialize the Logseq API client
        
        Args:
            api_url: URL of the Logseq API (default from mcp config)
            token: API token for authentication (default from mcp config)
        """
        
        self.api_url = api_url or os.getenv("LOGSEQ_API_URL", "http://localhost:12315")
        self.token = token or os.getenv("LOGSEQ_TOKEN")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests"""
        headers = {
            "Content-Type": "application/json"
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    def call_api(self, method: str, args: List = None) -> Any:
        """
        Call the Logseq API using the proper format
        
        Args:
            method: API method to call (e.g., "logseq.Editor.getCurrentBlock")
            args: Arguments for the method
            
        Returns:
            API response (could be a dict, list, or other JSON-serializable data)
        """
        url = f"{self.api_url}/api"
        headers = self._get_headers()
        
        data = {
            "method": method,
            "args": args or []
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 401:
                return {
                    "success": False,
                    "error": f"401 Unauthorized: Please provide a valid token in LOGSEQ_API_TOKEN environment variable"
                }
            
            response.raise_for_status()
            
            # Parse JSON response
            json_response = response.json()
            
            # Some Logseq API endpoints return the result directly, others wrap it in a result field
            # We need to handle both cases
            if isinstance(json_response, dict) and "result" in json_response:
                return json_response
            return json_response
            
        except requests.exceptions.RequestException as e:
            print(f"API request error: {e}")
            return {"success": False, "error": str(e)}
    
    # Legacy API methods - now using the proper format
    
    def get_current_graph(self) -> Dict:
        """Get information about the current graph"""
        return self.call_api("logseq.App.getCurrentGraph")
    
    def get_all_pages(self) -> List[Dict]:
        """Get all pages in the graph"""
        response = self.call_api("logseq.Editor.getAllPages")
        if isinstance(response, list):
            return response
        return response.get("result", []) if isinstance(response, dict) else []
    
    def get_page(self, page_name: str) -> Optional[Dict]:
        """Get a page by name"""
        response = self.call_api("logseq.Editor.getPage", [page_name])
        if response is None:
            return None
        return response.get("result") if isinstance(response, dict) else response
    
    def get_page_blocks(self, page_name: str) -> List[Dict]:
        """Get all blocks for a page"""
        response = self.call_api("logseq.Editor.getPageBlocksTree", [page_name])
        if isinstance(response, list):
            return response
        return response.get("result", []) if isinstance(response, dict) else []
    
    def search_blocks(self, query: str) -> List[Dict]:
        """Search for blocks matching a query"""
        response = self.call_api("logseq.Editor.search", [query])
        if isinstance(response, list):
            return response
        return response.get("result", []) if isinstance(response, dict) else []
    
    def create_page(self, page_name: str, properties: Dict = None) -> Dict:
        """Create a new page"""
        params = [page_name]
        if properties:
            params.append(properties)
        response = self.call_api("logseq.Editor.createPage", params)
        if isinstance(response, dict) and "result" in response:
            return response.get("result")
        return response
    
    def create_block(self, page_name: str, content: str, properties: Dict = None) -> Dict:
        """Create a new block on a page"""
        params = [page_name, content]
        if properties:
            params.append(properties)
        response = self.call_api("logseq.Editor.appendBlockInPage", params)
        if isinstance(response, dict) and "result" in response:
            return response.get("result")
        return response
    
    def update_block(self, block_id: str, content: str, properties: Dict = None) -> Dict:
        """Update an existing block"""
        params = [block_id, content]
        if properties:
            params.append(properties)
        response = self.call_api("logseq.Editor.updateBlock", params)
        if isinstance(response, dict) and "result" in response:
            return response.get("result")
        return response
    
    def get_block(self, block_id: str) -> Optional[Dict]:
        """Get a block by ID"""
        response = self.call_api("logseq.Editor.getBlock", [block_id])
        if response is None:
            return None
        return response.get("result") if isinstance(response, dict) else response
    
    def get_block_properties(self, block_id: str) -> Dict:
        """Get properties of a block"""
        response = self.call_api("logseq.Editor.getBlockProperties", [block_id])
        if isinstance(response, dict) and "result" in response:
            return response.get("result", {})
        return response if isinstance(response, dict) else {}
    
    def get_page_linked_references(self, page_name: str) -> List[Dict]:
        """Get linked references to a page"""
        response = self.call_api("logseq.Editor.getPageLinkedReferences", [page_name])
        if isinstance(response, list):
            return response
        return response.get("result", []) if isinstance(response, dict) else []
    
    def delete_page(self, page_name: str) -> Dict:
        """Delete a page from the graph"""
        response = self.call_api("logseq.Editor.deletePage", [page_name])
        if isinstance(response, dict) and "result" in response:
            return response.get("result")
        return response
    
    def remove_block(self, block_id: str) -> Dict:
        """Remove a block and its children from the graph"""
        response = self.call_api("logseq.Editor.removeBlock", [block_id])
        if isinstance(response, dict) and "result" in response:
            return response.get("result")
        return response
    
    def insert_block(self, parent_block_id: str, content: str, properties: Dict = None, before: bool = False) -> Dict:
        """Insert a new block as a child of the specified parent block"""
        params = [parent_block_id, content]
        if properties:
            params.append(properties)
        
        # Choose the appropriate API method based on the 'before' parameter
        method = "logseq.Editor.insertBlock"
        if before:
            method = "logseq.Editor.prependBlock"
            
        response = self.call_api(method, params)
        if isinstance(response, dict) and "result" in response:
            return response.get("result")
        return response
        
    def move_block(self, block_id: str, target_block_id: str, as_child: bool = False) -> Dict:
        """Move a block to a new location in the graph"""
        # Determine the appropriate API method based on the as_child parameter
        method = "logseq.Editor.moveBlock"
        
        # The API expects a structured argument for the move operation
        move_params = {
            "srcUUID": block_id,
            "targetUUID": target_block_id,
            "isChild": as_child
        }
        
        response = self.call_api(method, [move_params])
        if isinstance(response, dict) and "result" in response:
            return response.get("result")
        return response
