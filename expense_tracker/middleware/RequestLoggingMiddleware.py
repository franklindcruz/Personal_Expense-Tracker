import json
from tracker.models import RequestLogs

class RequestLogging:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Prepare request data to be logged
        request_data = {
            "method": request.method,
            "path": request.path,
            "GET": request.GET.dict(),
            "POST": request.POST.dict() if request.method == "POST" else {},
            "user": str(request.user) if request.user.is_authenticated else "Anonymous"
        }
        
        try:
            RequestLogs.objects.create(
                request_info=json.dumps(request_data),
                request_type=request.method,
                request_method=request.path
            )
        except Exception as e:
            # Print to console if logging fails; consider proper error logging in production.
            print("Error logging request:", e)
        
        # Process the request and obtain the response (only one call)
        response = self.get_response(request)
        
        # Optionally log some response data
        response_data = {
            "status_code": response.status_code,
            "content_type": response.get("Content-Type", "")
        }
        print("Response:", response_data)
        
        return response
