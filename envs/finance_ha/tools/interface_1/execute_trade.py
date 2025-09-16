import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ExecuteTrade(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], fund_id: str, instrument_id: str, quantity: float,
               price_limit: float, trader_id: str, fund_manager_approval: bool) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        trades = data.get("trades", {})
        funds = data.get("funds", {})
        instruments = data.get("instruments", {})
        users = data.get("users", {})
        
        if str(fund_id) not in funds:
            return json.dumps({"error": f"Fund {fund_id} not found"})
        
        if str(instrument_id) not in instruments:
            return json.dumps({"error": f"Instrument {instrument_id} not found"})
        
        if str(trader_id) not in users:
            return json.dumps({"error": f"Trader {trader_id} not found"})
        
        if not fund_manager_approval:
            return json.dumps({"error": "Fund manager approval is required"})
        
        trade_id = generate_id(trades)
        timestamp = "2025-10-01T00:00:00"
        
        new_trade = {
            "trade_id": trade_id,
            "fund_id": fund_id,
            "instrument_id": instrument_id,
            "trader_id": trader_id,
            "approved_by_id": None,  # Would be set in real system
            "side": "buy" if quantity > 0 else "sell",
            "quantity": abs(quantity),
            "price": price_limit,
            "counterparty": None,
            "status": "executed",
            "execution_timestamp": timestamp,
            "created_at": timestamp
        }
        
        trades[trade_id] = new_trade
        return json.dumps({"trade_id": trade_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "execute_trade",
                "description": "Executes a trade after receiving approval from a Fund Manager",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fund_id": {"type": "string", "description": "The ID of the fund conducting the trade"},
                        "instrument_id": {"type": "string", "description": "The ID of the instrument to be traded"},
                        "quantity": {"type": "number", "description": "The quantity of the instrument to trade"},
                        "price_limit": {"type": "number", "description": "The price limit for the trade"},
                        "trader_id": {"type": "string", "description": "The ID of the Trader executing the trade"},
                        "fund_manager_approval": {"type": "boolean", "description": "Approval from a Fund Manager (True/False)"}
                    },
                    "required": ["fund_id", "instrument_id", "quantity", "price_limit", "trader_id", "fund_manager_approval"]
                }
            }
        }
