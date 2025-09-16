import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class OnboardInvestor(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], legal_entity_name: str, incorporation_registration_number: str,
               date_of_incorporation: str, country_of_incorporation: str, registered_business_address: str,
               tax_identification_number: str, source_of_funds_declaration: str, 
               compliance_officer_approval: bool) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        investors = data.get("investors", {})
        
        if not compliance_officer_approval:
            return json.dumps({"error": "Compliance officer approval is required"})
        
        # Check valid source of funds
        valid_sources = ['retained_earnings', 'shareholder_capital', 'asset_sale', 'external_investment', 'other']
        if source_of_funds_declaration not in valid_sources:
            return json.dumps({"error": f"Invalid source of funds. Must be one of {valid_sources}"})
        
        investor_id = generate_id(investors)
        timestamp = "2025-10-01T00:00:00"
        
        new_investor = {
            "investor_id": investor_id,
            "legal_entity_name": legal_entity_name,
            "incorporation_number": incorporation_registration_number,
            "incorporation_date": date_of_incorporation,
            "incorporation_country": country_of_incorporation,
            "business_address": registered_business_address,
            "tax_id": tax_identification_number,
            "source_of_funds": source_of_funds_declaration,
            "status": "active",
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        investors[investor_id] = new_investor
        return json.dumps({"investor_id": investor_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "onboard_investor",
                "description": "Creates a new investor profile after verifying all required information and obtaining compliance approval",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "legal_entity_name": {"type": "string", "description": "The legal name of the investing entity"},
                        "incorporation_registration_number": {"type": "string", "description": "The official registration number"},
                        "date_of_incorporation": {"type": "string", "description": "The date the entity was incorporated"},
                        "country_of_incorporation": {"type": "string", "description": "The country of incorporation"},
                        "registered_business_address": {"type": "string", "description": "The official registered address"},
                        "tax_identification_number": {"type": "string", "description": "The entity's tax ID number"},
                        "source_of_funds_declaration": {"type": "string", "description": "A declaration outlining the source of funds (retained_earnings, shareholder_capital, asset_sale, external_investment, other)"},
                        "compliance_officer_approval": {"type": "boolean", "description": "Flag indicating approval from a Compliance Officer (True/False)"}
                    },
                    "required": ["legal_entity_name", "incorporation_registration_number", "date_of_incorporation", 
                               "country_of_incorporation", "registered_business_address", "tax_identification_number",
                               "source_of_funds_declaration", "compliance_officer_approval"]
                }
            }
        }
