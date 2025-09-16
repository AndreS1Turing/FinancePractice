import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateInstrument(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], instrument_id: str, proposed_changes: Dict[str, Any],
               fund_manager_approval: bool, compliance_review_required: bool = False) -> str:
        
        instruments = data.get("instruments", {})
        
        if str(instrument_id) not in instruments:
            return json.dumps({"error": f"Instrument {instrument_id} not found"})
        
        if not fund_manager_approval:
            return json.dumps({"error": "Fund manager approval is required"})
        
        if compliance_review_required:
            # In a real system, this would trigger compliance review workflow
            pass
        
        timestamp = "2025-10-01T00:00:00"
        
        # Update the instrument with changes
        for key, value in proposed_changes.items():
            if key in ["instrument_id", "created_at"]:  # Don't allow changing these fields
                continue
            instruments[str(instrument_id)][key] = value
        
        instruments[str(instrument_id)]["updated_at"] = timestamp
        
        return json.dumps(instruments[str(instrument_id)])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_instrument",
                "description": "Modifies the details of an existing financial instrument",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "instrument_id": {"type": "string", "description": "The ID of the instrument to update"},
                        "proposed_changes": {"type": "object", "description": "A dictionary of proposed changes"},
                        "fund_manager_approval": {"type": "boolean", "description": "Approval from a Fund Manager for the changes (True/False)"},
                        "compliance_review_required": {"type": "boolean", "description": "Optional flag if changes require compliance review (True/False)"}
                    },
                    "required": ["instrument_id", "proposed_changes", "fund_manager_approval"]
                }
            }
        }
