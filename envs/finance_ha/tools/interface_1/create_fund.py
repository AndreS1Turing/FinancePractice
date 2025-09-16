import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateFund(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_name: str, fund_type: str, base_currency: str,
               initial_size: float, manager_id: str, compliance_officer_review: bool,
               fund_manager_approval: bool) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        funds = data.get("funds", {})
        users = data.get("users", {})
        
        if not compliance_officer_review or not fund_manager_approval:
            return json.dumps({"error": "Both compliance officer review and fund manager approval are required"})
        
        if str(manager_id) not in users:
            return json.dumps({"error": f"Manager {manager_id} not found"})
        
        # Check if fund name already exists
        for fund in funds.values():
            if fund.get("name") == fund_name:
                return json.dumps({"error": "Fund name already exists"})
        
        valid_fund_types = ['hedge_fund', 'private_equity', 'venture_capital', 'real_estate', 'mutual_fund']
        if fund_type not in valid_fund_types:
            return json.dumps({"error": f"Invalid fund type. Must be one of {valid_fund_types}"})
        
        fund_id = generate_id(funds)
        timestamp = "2025-10-01T00:00:00"
        
        new_fund = {
            "fund_id": fund_id,
            "name": fund_name,
            "fund_type": fund_type,
            "base_currency": base_currency,
            "initial_size": initial_size,
            "manager_id": manager_id,
            "status": "open",
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        funds[fund_id] = new_fund
        return json.dumps({"fund_id": fund_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_fund",
                "description": "Creates a new fund after compliance review and fund manager approval",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_name": {"type": "string", "description": "The name of the new fund"},
                        "fund_type": {"type": "string", "description": "The type of fund (hedge_fund, private_equity, venture_capital, real_estate, mutual_fund)"},
                        "base_currency": {"type": "string", "description": "The base currency for the fund, e.g., 'USD'"},
                        "initial_size": {"type": "number", "description": "The initial size or capital of the fund"},
                        "manager_id": {"type": "string", "description": "The ID of the assigned Fund Manager"},
                        "compliance_officer_review": {"type": "boolean", "description": "Flag indicating the fund structure has been reviewed by a Compliance Officer (True/False)"},
                        "fund_manager_approval": {"type": "boolean", "description": "Flag indicating final approval from a Fund Manager (True/False)"}
                    },
                    "required": ["fund_name", "fund_type", "base_currency", "initial_size", "manager_id", 
                               "compliance_officer_review", "fund_manager_approval"]
                }
            }
        }
