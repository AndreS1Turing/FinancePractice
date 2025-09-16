import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetFundInfo(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: Optional[str] = None, 
               fund_type: Optional[str] = None, status: Optional[str] = None) -> str:
        
        funds = data.get("funds", {})
        results = []
        
        for fund in funds.values():
            if fund_id and fund.get("fund_id") != fund_id:
                continue
            if fund_type and fund.get("fund_type") != fund_type:
                continue
            if status and fund.get("status") != status:
                continue
            results.append(fund)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_fund_info",
                "description": "Retrieves information about one or more funds",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "Filter by specific fund ID"},
                        "fund_type": {"type": "string", "description": "Filter by fund type (hedge_fund, private_equity, venture_capital, real_estate, mutual_fund)"},
                        "status": {"type": "string", "description": "Filter by fund status (pending_approval, open, closed)"}
                    },
                    "required": []
                }
            }
        }
