import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetInvestorProfile(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: Optional[str] = None, 
               account_status: Optional[str] = None) -> str:
        
        investors = data.get("investors", {})
        results = []
        
        for investor in investors.values():
            if investor_id and investor.get("investor_id") != investor_id:
                continue
            if account_status and investor.get("status") != account_status:
                continue
            results.append(investor)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_investor_profile",
                "description": "Retrieves profile information for one or more investors",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "Filter by specific investor ID"},
                        "account_status": {"type": "string", "description": "Filter by account status (pending, active, inactive, archived)"}
                    },
                    "required": []
                }
            }
        }
