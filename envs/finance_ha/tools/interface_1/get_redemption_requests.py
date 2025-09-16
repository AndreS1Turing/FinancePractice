import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetRedemptionRequests(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: Optional[str] = None,
               fund_id: Optional[str] = None, status: Optional[str] = None) -> str:
        
        redemptions = data.get("redemptions", {})
        results = []
        
        for redemption in redemptions.values():
            if investor_id and redemption.get("investor_id") != investor_id:
                continue
            if fund_id and redemption.get("fund_id") != fund_id:
                continue
            if status and redemption.get("status") != status:
                continue
            results.append(redemption)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_redemption_requests",
                "description": "Retrieves records of redemption requests",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "Filter by investor ID"},
                        "fund_id": {"type": "string", "description": "Filter by fund ID"},
                        "status": {"type": "string", "description": "Filter by status (pending, approved, processed, rejected)"}
                    },
                    "required": []
                }
            }
        }
