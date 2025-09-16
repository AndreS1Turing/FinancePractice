import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ProcessRedemption(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, fund_id: str, amount_or_units: float,
               compliance_officer_approval: bool, finance_officer_approval: bool) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        redemptions = data.get("redemptions", {})
        investors = data.get("investors", {})
        funds = data.get("funds", {})
        
        if str(investor_id) not in investors:
            return json.dumps({"error": f"Investor {investor_id} not found"})
        
        if str(fund_id) not in funds:
            return json.dumps({"error": f"Fund {fund_id} not found"})
        
        if not compliance_officer_approval or not finance_officer_approval:
            return json.dumps({"error": "Both compliance officer and finance officer approval are required"})
        
        redemption_id = generate_id(redemptions)
        timestamp = "2025-10-01T00:00:00"
        
        new_redemption = {
            "redemption_id": redemption_id,
            "investor_id": investor_id,
            "fund_id": fund_id,
            "redemption_amount": amount_or_units,
            "redemption_units": None,
            "redemption_fee": 1.00,
            "status": "processed",
            "request_date": timestamp,
            "processed_date": timestamp,
            "updated_at": timestamp
        }
        
        redemptions[redemption_id] = new_redemption
        return json.dumps(new_redemption)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "process_redemption",
                "description": "Processes an investor's request to withdraw funds, including fee calculation",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "The ID of the investor making the redemption"},
                        "fund_id": {"type": "string", "description": "The ID of the fund from which to redeem"},
                        "amount_or_units": {"type": "number", "description": "The amount or number of units to redeem"},
                        "compliance_officer_approval": {"type": "boolean", "description": "Approval from a Compliance Officer (True/False)"},
                        "finance_officer_approval": {"type": "boolean", "description": "Approval from a Finance Officer (True/False)"}
                    },
                    "required": ["investor_id", "fund_id", "amount_or_units", "compliance_officer_approval", "finance_officer_approval"]
                }
            }
        }
