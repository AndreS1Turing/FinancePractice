import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool
from datetime import datetime

class GetTradeHistory(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: Optional[str] = None,
               trader_id: Optional[str] = None, instrument_id: Optional[str] = None,
               start_date: Optional[str] = None, end_date: Optional[str] = None) -> str:
        
        trades = data.get("trades", {})
        results = []
        
        for trade in trades.values():
            if fund_id and trade.get("fund_id") != fund_id:
                continue
            if trader_id and trade.get("trader_id") != trader_id:
                continue
            if instrument_id and trade.get("instrument_id") != instrument_id:
                continue
            
            # Date filtering on created_at field
            if start_date or end_date:
                trade_date = trade.get("created_at", "")
                if start_date and trade_date < start_date:
                    continue
                if end_date and trade_date > end_date:
                    continue
            
            results.append(trade)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_trade_history",
                "description": "Retrieves historical trade data",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "Filter by fund ID"},
                        "trader_id": {"type": "string", "description": "Filter by trader ID"},
                        "instrument_id": {"type": "string", "description": "Filter by instrument ID"},
                        "start_date": {"type": "string", "description": "The start date for the query period (ISO format)"},
                        "end_date": {"type": "string", "description": "The end date for the query period (ISO format)"}
                    },
                    "required": []
                }
            }
        }
