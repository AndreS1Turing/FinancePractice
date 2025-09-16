import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class GetDocumentInfo(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], doc_id: Optional[str] = None,
               user_id: Optional[str] = None, document_type: Optional[str] = None) -> str:
        
        documents = data.get("documents", {})
        results = []
        
        for document in documents.values():
            if doc_id and document.get("document_id") != doc_id:
                continue
            if user_id and document.get("uploaded_by_id") != user_id:
                continue
            if document_type and document.get("document_type") != document_type:
                continue
            results.append(document)
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_document_info",
                "description": "Retrieves metadata for uploaded documents",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "doc_id": {"type": "string", "description": "Filter by document ID"},
                        "user_id": {"type": "string", "description": "Filter by the ID of the user who uploaded the document"},
                        "document_type": {"type": "string", "description": "Filter by the type of document (prospectus, investor_agreement, kyc, report)"}
                    },
                    "required": []
                }
            }
        }
