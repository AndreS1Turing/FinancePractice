import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateUserAccount(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str, role: Optional[str] = None, 
               email: Optional[str] = None) -> str:
        
        users = data.get("users", {})
        
        if str(user_id) not in users:
            return json.dumps({"error": f"User {user_id} not found"})
        
        # Check if email already exists (if provided)
        if email:
            for uid, user in users.items():
                if uid != str(user_id) and user.get("email") == email:
                    return json.dumps({"error": "Email already exists"})
        
        # Validate role if provided
        if role:
            valid_roles = ['system_administrator', 'fund_manager', 'compliance_officer', 'finance_officer', 'trader', 'investor']
            if role not in valid_roles:
                return json.dumps({"error": f"Invalid role. Must be one of {valid_roles}"})
        
        timestamp = "2025-10-01T00:00:00"
        
        # Update fields if provided
        if role:
            users[str(user_id)]["role"] = role
        if email:
            users[str(user_id)]["email"] = email
        
        users[str(user_id)]["updated_at"] = timestamp
        
        return json.dumps(users[str(user_id)])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_user_account",
                "description": "Updates information for an existing user account",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The ID of the user to update"},
                        "role": {"type": "string", "description": "The new role for the user (system_administrator, fund_manager, compliance_officer, finance_officer, trader, investor)"},
                        "email": {"type": "string", "description": "The new email address for the user"}
                    },
                    "required": ["user_id"]
                }
            }
        }
