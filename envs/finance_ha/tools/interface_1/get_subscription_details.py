import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetSubscriptionDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], subscription_id: Optional[str] = None,
               investor_id: Optional[str] = None, fund_id: Optional[str] = None,
               status: Optional[str] = None) -> str:
        
        subscriptions = data.get("subscriptions", {})
        results = []
        
        for subscription in subscriptions.values():
            if subscription_id and subscription.get("subscription_id") != subscription_id:
                continue
            if investor_id and subscription.get("investor_id") != investor_id:
                continue
            if fund_id and subscription.get("fund_id") != fund_id:
                continue
            if status and subscription.get("status") != status:
                continue
            results.append(subscription)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_subscription_details",
                "description": "Retrieves details of subscription records",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subscription_id": {"type": "string", "description": "Filter by subscription ID"},
                        "investor_id": {"type": "string", "description": "Filter by investor ID"},
                        "fund_id": {"type": "string", "description": "Filter by fund ID"},
                        "status": {"type": "string", "description": "Filter by status (pending, approved, active, cancelled)"}
                    },
                    "required": []
                }
            }
        }
