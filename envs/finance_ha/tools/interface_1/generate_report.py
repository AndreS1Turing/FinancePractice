import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GenerateReport(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], report_type: str, requester_role: str, time_period: str,
               fund_id: Optional[str] = None, investor_id: Optional[str] = None) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        reports = data.get("reports", {})
        funds = data.get("funds", {})
        investors = data.get("investors", {})
        
        # Validate report type
        valid_report_types = ['performance', 'financial', 'audit_trail', 'compliance']
        if report_type not in valid_report_types:
            return json.dumps({"error": f"Invalid report type. Must be one of {valid_report_types}"})
        
        # Validate requester role
        valid_roles = ['system_administrator', 'fund_manager', 'compliance_officer', 'finance_officer']
        if requester_role not in valid_roles:
            return json.dumps({"error": f"Invalid requester role. Must be one of {valid_roles}"})
        
        # Validate fund_id if provided
        if fund_id and str(fund_id) not in funds:
            return json.dumps({"error": f"Fund {fund_id} not found"})
        
        # Validate investor_id if provided
        if investor_id and str(investor_id) not in investors:
            return json.dumps({"error": f"Investor {investor_id} not found"})
        
        report_id = generate_id(reports)
        timestamp = "2025-10-01T00:00:00"
        
        # Determine reference type and ID
        reference_type = None
        reference_id = None
        if fund_id:
            reference_type = "fund"
            reference_id = fund_id
        elif investor_id:
            reference_type = "investor"
            reference_id = investor_id
        
        # Parse time period for start/end dates (simplified)
        start_date = "2025-01-01"  # Placeholder
        end_date = "2025-12-31"    # Placeholder
        
        new_report = {
            "report_id": report_id,
            "report_type": report_type,
            "reference_id": reference_id,
            "reference_type": reference_type,
            "generated_by_id": "system",  # In real system, would be actual user ID
            "start_date": start_date,
            "end_date": end_date,
            "status": "completed",
            "created_at": timestamp
        }
        
        reports[report_id] = new_report
        return json.dumps({"report_id": report_id, "success": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "generate_report",
                "description": "Generates a report based on specified criteria",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "report_type": {"type": "string", "description": "Type of report (performance, financial, audit_trail, compliance)"},
                        "requester_role": {"type": "string", "description": "The role of the user requesting the report, for permission checks (system_administrator, fund_manager, compliance_officer, finance_officer)"},
                        "time_period": {"type": "string", "description": "The reporting period (e.g., 'Q3-2025')"},
                        "fund_id": {"type": "string", "description": "The fund ID for fund-specific reports"},
                        "investor_id": {"type": "string", "description": "The investor ID for investor-specific reports"}
                    },
                    "required": ["report_type", "requester_role", "time_period"]
                }
            }
        }
