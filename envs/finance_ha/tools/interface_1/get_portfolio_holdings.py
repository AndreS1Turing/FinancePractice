import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPortfolioHoldings(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], investor_id: str) -> str:
        
        portfolios = data.get("portfolios", {})
        portfolio_holdings = data.get("portfolio_holdings", {})
        investors = data.get("investors", {})
        
        if str(investor_id) not in investors:
            return json.dumps({"error": f"Investor {investor_id} not found"})
        
        # Find the investor's portfolio
        investor_portfolio = None
        for portfolio in portfolios.values():
            if portfolio.get("investor_id") == investor_id:
                investor_portfolio = portfolio
                break
        
        if not investor_portfolio:
            return json.dumps([])  # No portfolio found, return empty array
        
        portfolio_id = investor_portfolio.get("portfolio_id")
        
        # Get all holdings for this portfolio
        results = []
        for holding in portfolio_holdings.values():
            if holding.get("portfolio_id") == portfolio_id:
                results.append(holding)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_portfolio_holdings",
                "description": "Retrieves all portfolio holdings for a given investor",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "investor_id": {"type": "string", "description": "The ID of the investor whose portfolio is being queried"}
                    },
                    "required": ["investor_id"]
                }
            }
        }
