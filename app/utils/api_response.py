from rest_framework.response import Response
from rest_framework import status
from typing import Any, Dict, Optional

def api_response(
    data: Optional[Any] = None,
    message: str = "",
    success: bool = True,
    status_code: int = status.HTTP_200_OK
) -> Response:
    """
    Standardized API response helper.
    """
    response_data: Dict[str, Any] = {
        "success": success,
        "message": message,
        "status_code": status_code, # Added status_code to the response_data
    }
    if data is not None:
        response_data["data"] = data
    
    return Response(response_data, status=status_code)