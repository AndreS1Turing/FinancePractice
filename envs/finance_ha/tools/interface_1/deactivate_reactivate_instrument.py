import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DeactivateReactivateInstrument(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], instrument_id: str, action: str,
               fund_manager_approval: bool, compliance_officer_approval: bool) -> str:
        
        instruments = data.get("instruments", {})
        
        if str(instrument_id) not in instruments:
            return json.dumps({"error": f"Instrument {instrument_id} not found"})
        
        if action not in ['deactivate', 'reactivate']:
            return json.dumps({"error": "Action must be either 'deactivate' or 'reactivate'"})
        
        if not fund_manager_approval or not compliance_officer_approval:
            return json.dumps({"error": "Both fund manager and compliance officer approval are required"})
        
        timestamp = "2025-10-01T00:00:00"
        new_status = "inactive" if action == "deactivate" else "active"
        
        instruments[str(instrument_id)]["status"] = new_status
        instruments[str(instrument_id)]["updated_at"] = timestamp
        
        return json.dumps(instruments[str(instrument_id)])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "deactivate_reactivate_instrument",
                "description": "Changes the status of an instrument to active or inactive",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "instrument_id": {"type": "string", "description": "The ID of the instrument"},
                        "action": {"type": "string", "description": "The action to perform (deactivate, reactivate)"},
                        "fund_manager_approval": {"type": "boolean", "description": "Approval from a Fund Manager (True/False)"},
                        "compliance_officer_approval": {"type": "boolean", "description": "Approval from a Compliance Officer (True/False)"}
                    },
                    "required": ["instrument_id", "action", "fund_manager_approval", "compliance_officer_approval"]
                }
            }
        }
