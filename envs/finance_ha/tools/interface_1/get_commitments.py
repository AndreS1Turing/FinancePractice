import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetCommitments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], commitment_id: Optional[str] = None,
               investor_id: Optional[str] = None, fund_id: Optional[str] = None,
               status: Optional[str] = None) -> str:
        
        commitments = data.get("commitments", {})
        results = []
        
        for commitment in commitments.values():
            if commitment_id and commitment.get("commitment_id") != commitment_id:
                continue
            if investor_id and commitment.get("investor_id") != investor_id:
                continue
            if fund_id and commitment.get("fund_id") != fund_id:
                continue
            if status and commitment.get("status") != status:
                continue
            results.append(commitment)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_commitments",
                "description": "Retrieves commitment records",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "commitment_id": {"type": "string", "description": "Filter by commitment ID"},
                        "investor_id": {"type": "string", "description": "Filter by investor ID"},
                        "fund_id": {"type": "string", "description": "Filter by fund ID"},
                        "status": {"type": "string", "description": "Filter by status (pending, fulfilled)"}
                    },
                    "required": []
                }
            }
        }
