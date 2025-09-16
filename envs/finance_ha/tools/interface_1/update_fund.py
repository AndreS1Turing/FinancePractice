import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class UpdateFund(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, changes: Dict[str, Any],
               fund_manager_approval: bool, compliance_review_required: bool = False) -> str:
        
        funds = data.get("funds", {})
        
        if str(fund_id) not in funds:
            return json.dumps({"error": f"Fund {fund_id} not found"})
        
        if not fund_manager_approval:
            return json.dumps({"error": "Fund manager approval is required"})
        
        if compliance_review_required:
            # In a real system, this would trigger compliance review workflow
            pass
        
        timestamp = "2025-10-01T00:00:00"
        
        # Update the fund with changes
        for key, value in changes.items():
            if key in ["fund_id", "created_at"]:  # Don't allow changing these fields
                continue
            funds[str(fund_id)][key] = value
        
        funds[str(fund_id)]["updated_at"] = timestamp
        
        return json.dumps(funds[str(fund_id)])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_fund",
                "description": "Modifies the details of an existing fund",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "The ID of the fund to update"},
                        "changes": {"type": "object", "description": "A dictionary containing the fields and new values to update"},
                        "fund_manager_approval": {"type": "boolean", "description": "Flag indicating approval from a Fund Manager for the changes (True/False)"},
                        "compliance_review_required": {"type": "boolean", "description": "Optional flag if changes require a new compliance review (True/False)"}
                    },
                    "required": ["fund_id", "changes", "fund_manager_approval"]
                }
            }
        }
