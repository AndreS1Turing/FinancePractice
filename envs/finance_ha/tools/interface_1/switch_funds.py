import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class SwitchFunds(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str, source_fund_id: str, 
               target_fund_id: str, amount_to_switch: float) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        fund_switches = data.get("fund_switches", {})
        investors = data.get("investors", {})
        funds = data.get("funds", {})
        
        if str(investor_id) not in investors:
            return json.dumps({"error": f"Investor {investor_id} not found"})
        
        if str(source_fund_id) not in funds:
            return json.dumps({"error": f"Source fund {source_fund_id} not found"})
        
        if str(target_fund_id) not in funds:
            return json.dumps({"error": f"Target fund {target_fund_id} not found"})
        
        switch_id = generate_id(fund_switches)
        timestamp = "2025-10-01T00:00:00"
        
        new_switch = {
            "switch_id": switch_id,
            "investor_id": investor_id,
            "source_fund_id": source_fund_id,
            "target_fund_id": target_fund_id,
            "switch_amount": amount_to_switch,
            "status": "processed",
            "requested_at": timestamp,
            "processed_at": timestamp
        }
        
        fund_switches[switch_id] = new_switch
        return json.dumps(new_switch)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "switch_funds",
                "description": "Moves an investor's investment from a source fund to a target fund",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "The ID of the investor switching funds"},
                        "source_fund_id": {"type": "string", "description": "The ID of the fund to move assets from"},
                        "target_fund_id": {"type": "string", "description": "The ID of the fund to move assets to"},
                        "amount_to_switch": {"type": "number", "description": "The monetary amount to switch between funds"}
                    },
                    "required": ["investor_id", "source_fund_id", "target_fund_id", "amount_to_switch"]
                }
            }
        }
