import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateUploadDocument(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str, document_type: str, 
               confidentiality_level: str, file_name: str, file_format: str) -> str:
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        documents = data.get("documents", {})
        users = data.get("users", {})
        
        if str(user_id) not in users:
            return json.dumps({"error": f"User {user_id} not found"})
        
        valid_doc_types = ['prospectus', 'investor_agreement', 'kyc', 'report']
        if document_type not in valid_doc_types:
            return json.dumps({"error": f"Invalid document type. Must be one of {valid_doc_types}"})
        
        valid_formats = ['pdf', 'docx', 'xlsx', 'csv']
        if file_format.lower() not in valid_formats:
            return json.dumps({"error": f"Invalid file format. Must be one of {valid_formats}"})
        
        valid_confidentiality = ['public', 'internal', 'confidential']
        if confidentiality_level not in valid_confidentiality:
            return json.dumps({"error": f"Invalid confidentiality level. Must be one of {valid_confidentiality}"})
        
        doc_id = generate_id(documents)
        timestamp = "2025-10-01T00:00:00"
        
        new_document = {
            "document_id": doc_id,
            "name": file_name,
            "document_type": document_type,
            "format": file_format.lower(),
            "confidentiality_level": confidentiality_level,
            "uploaded_by_id": user_id,
            "status": "available",
            "created_at": timestamp
        }
        
        documents[doc_id] = new_document
        return json.dumps({"doc_id": doc_id, "success": True, "status": "available"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_upload_document",
                "description": "Creates a record for a new document uploaded to the system",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The ID of the user uploading the document"},
                        "document_type": {"type": "string", "description": "The type of document (prospectus, investor_agreement, kyc, report)"},
                        "confidentiality_level": {"type": "string", "description": "The confidentiality level (public, internal, confidential)"},
                        "file_name": {"type": "string", "description": "The name of the file"},
                        "file_format": {"type": "string", "description": "The file format (pdf, docx, xlsx, csv)"}
                    },
                    "required": ["user_id", "document_type", "confidentiality_level", "file_name", "file_format"]
                }
            }
        }
