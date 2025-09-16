import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetUserAccount(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: Optional[str] = None,
               email: Optional[str] = None, role: Optional[str] = None) -> str:
        
        users = data.get("users", {})
        results = []
        
        for user in users.values():
            if user_id and user.get("user_id") != user_id:
                continue
            if email and user.get("email") != email:
                continue
            if role and user.get("role") != role:
                continue
            results.append(user)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_user_account",
                "description": "Retrieves user account details",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "Filter by user ID"},
                        "email": {"type": "string", "description": "Filter by user email"},
                        "role": {"type": "string", "description": "Filter by user role (system_administrator, fund_manager, compliance_officer, finance_officer, trader, investor)"}
                    },
                    "required": []
                }
            }
        }
