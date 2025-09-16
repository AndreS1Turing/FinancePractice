import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CloseFund(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, compliance_officer_approval: bool,
               fund_manager_approval: bool) -> str:
        
        funds = data.get("funds", {})
        subscriptions = data.get("subscriptions", {})
        trades = data.get("trades", {})
        
        if str(fund_id) not in funds:
            return json.dumps({"error": f"Fund {fund_id} not found"})
        
        if not compliance_officer_approval or not fund_manager_approval:
            return json.dumps({"error": "Both compliance officer and fund manager approval are required"})
        
        # Check for active investors
        active_subscriptions = [s for s in subscriptions.values() 
                               if s.get("fund_id") == fund_id and s.get("status") == "active"]
        
        # Check for open positions (pending trades)
        open_trades = [t for t in trades.values() 
                      if t.get("fund_id") == fund_id and t.get("status") in ["pending_approval", "approved"]]
        
        if active_subscriptions:
            return json.dumps({"error": "Cannot close fund with active investors"})
        
        if open_trades:
            return json.dumps({"error": "Cannot close fund with open positions"})
        
        timestamp = "2025-10-01T00:00:00"
        funds[str(fund_id)]["status"] = "closed"
        funds[str(fund_id)]["updated_at"] = timestamp
        
        return json.dumps(funds[str(fund_id)])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "close_fund",
                "description": "Closes a fund, preventing further activity. This is not possible if the fund has active investors or open positions",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "The ID of the fund to close"},
                        "compliance_officer_approval": {"type": "boolean", "description": "Approval from a Compliance Officer (True/False)"},
                        "fund_manager_approval": {"type": "boolean", "description": "Approval from a Fund Manager (True/False)"}
                    },
                    "required": ["fund_id", "compliance_officer_approval", "fund_manager_approval"]
                }
            }
        }
