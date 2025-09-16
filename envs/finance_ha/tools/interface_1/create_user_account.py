import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateUserAccount(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_name: str, email: str, role: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        users = data.get("users", {})
        
        # Check if email already exists
        for user in users.values():
            if user.get("email") == email:
                return json.dumps({"error": "Email already exists"})
        
        valid_roles = ['system_administrator', 'fund_manager', 'compliance_officer', 'finance_officer', 'trader', 'investor']
        if role not in valid_roles:
            return json.dumps({"error": f"Invalid role. Must be one of {valid_roles}"})
        
        user_id = generate_id(users)
        timestamp = "2025-10-01T00:00:00"
        
        # Split name into first and last
        name_parts = user_name.split(" ", 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""
        
        new_user = {
            "user_id": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "role": role,
            "status": "active",
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        users[user_id] = new_user
        return json.dumps({"user_id": user_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_user_account",
                "description": "Creates a new user account in the system",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_name": {"type": "string", "description": "The full name of the user"},
                        "email": {"type": "string", "description": "The user's email address"},
                        "role": {"type": "string", "description": "The role to assign (system_administrator, fund_manager, compliance_officer, finance_officer, trader, investor)"}
                    },
                    "required": ["user_name", "email", "role"]
                }
            }
        }
