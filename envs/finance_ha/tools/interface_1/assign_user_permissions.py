import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class AssignUserPermissions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str, permissions: List[str]) -> str:
        
        users = data.get("users", {})
        
        if str(user_id) not in users:
            return json.dumps({"error": f"User {user_id} not found"})
        
        # In a real system, we might have a separate permissions table
        # For now, we'll add permissions as a field to the user record
        timestamp = "2025-10-01T00:00:00"
        users[str(user_id)]["permissions"] = permissions
        users[str(user_id)]["updated_at"] = timestamp
        
        return json.dumps(users[str(user_id)])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "assign_user_permissions",
                "description": "Assigns specific permissions to a user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The ID of the user"},
                        "permissions": {"type": "array", "items": {"type": "string"}, "description": "A list of permissions to grant"}
                    },
                    "required": ["user_id", "permissions"]
                }
            }
        }
