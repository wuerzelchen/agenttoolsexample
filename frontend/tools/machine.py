from langchain_core.tools import tool
import requests
from typing import Dict, Any


def wrap_machine_api(wrapper_config: Dict[str, Any]):
    @tool
    def list_ids(temperature: str) -> str:
        """List all IDs for machines."""
        request = {
            "method": "GET",
            "url": f"{wrapper_config['endpoint']}",
            "headers": {
                "Authorization": f"Bearer {wrapper_config['access_token']}",
                "Content-Type": "application/json"
            }
        }
        response = requests.request(**request)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")
    return list_ids
