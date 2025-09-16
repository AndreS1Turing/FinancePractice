import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DeactivateUserAccount(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str) -> str:
        
        users = data.get("users", {})
        
        if str(user_id) not in users:
            return json.dumps({"error": f"User {user_id} not found"})
        
        timestamp = "2025-10-01T00:00:00"
        users[str(user_id)]["status"] = "deactivated"
        users[str(user_id)]["updated_at"] = timestamp
        
        return json.dumps(users[str(user_id)])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "deactivate_user_account",
                "description": "Deactivates a user account, revoking access",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The ID of the user to deactivate"}
                    },
                    "required": ["user_id"]
                }
            }
        }
