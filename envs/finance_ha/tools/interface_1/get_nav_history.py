import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetNavHistory(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, start_date: Optional[str] = None,
               end_date: Optional[str] = None) -> str:
        
        nav_records = data.get("nav_records", {})
        funds = data.get("funds", {})
        
        if str(fund_id) not in funds:
            return json.dumps({"error": f"Fund {fund_id} not found"})
        
        results = []
        
        for nav_record in nav_records.values():
            if nav_record.get("fund_id") != fund_id:
                continue
            
            # Date filtering on nav_date field
            if start_date or end_date:
                nav_date = nav_record.get("nav_date", "")
                if start_date and nav_date < start_date:
                    continue
                if end_date and nav_date > end_date:
                    continue
            
            results.append(nav_record)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_nav_history",
                "description": "Retrieves the historical NAV values for a fund",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "The ID of the fund to query"},
                        "start_date": {"type": "string", "description": "The start date for the historical period (ISO format)"},
                        "end_date": {"type": "string", "description": "The end date for the historical period (ISO format)"}
                    },
                    "required": ["fund_id"]
                }
            }
        }
