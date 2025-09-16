import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetInstrumentDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], instrument_id: Optional[str] = None,
               ticker: Optional[str] = None, asset_class: Optional[str] = None) -> str:
        
        instruments = data.get("instruments", {})
        results = []
        
        for instrument in instruments.values():
            if instrument_id and instrument.get("instrument_id") != instrument_id:
                continue
            if ticker and instrument.get("ticker") != ticker:
                continue
            if asset_class and instrument.get("asset_class") != asset_class:
                continue
            results.append(instrument)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_instrument_details",
                "description": "Retrieves details for one or more financial instruments",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "instrument_id": {"type": "string", "description": "Filter by instrument ID"},
                        "ticker": {"type": "string", "description": "Filter by instrument ticker symbol"},
                        "asset_class": {"type": "string", "description": "Filter by asset class (equity, debt, derivative, real_estate, commodity)"}
                    },
                    "required": []
                }
            }
        }
