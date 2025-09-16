import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CalculateNav(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, calculation_date: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        funds = data.get("funds", {})
        nav_records = data.get("nav_records", {})
        
        if str(fund_id) not in funds:
            return json.dumps({"error": f"Fund {fund_id} not found"})
        
        # Check if NAV already exists for this date
        for nav in nav_records.values():
            if nav.get("fund_id") == fund_id and nav.get("nav_date") == calculation_date:
                return json.dumps({"error": f"NAV already exists for fund {fund_id} on {calculation_date}"})
        
        nav_id = generate_id(nav_records)
        timestamp = "2025-10-01T00:00:00"
        
        # In a real system, this would perform actual NAV calculation
        # For now, we'll use placeholder values
        calculated_nav = 1000000.0  # Placeholder NAV value
        
        new_nav_record = {
            "nav_id": nav_id,
            "fund_id": fund_id,
            "nav_date": calculation_date,
            "total_assets": 1200000.0,
            "liabilities": 200000.0,
            "nav_value": calculated_nav,
            "calculated_by_id": "system",  # In real system, would be actual user ID
            "created_at": timestamp
        }
        
        nav_records[nav_id] = new_nav_record
        return json.dumps({"nav_value": calculated_nav, "success": True, "nav_record": new_nav_record})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "calculate_nav",
                "description": "Calculates and updates the Net Asset Value (NAV) for a fund on a specific date",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "The ID of the fund for which to calculate the NAV"},
                        "calculation_date": {"type": "string", "description": "The date for the NAV calculation (ISO format)"}
                    },
                    "required": ["fund_id", "calculation_date"]
                }
            }
        }
