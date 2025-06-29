from django.http import JsonResponse

class SessionTypeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip auth-related paths
        if request.path in ['/login/', '/driver_login/', '/logout/']:
            return self.get_response(request)
        
        # Check customer routes
        if request.path.startswith('/booking/') and not request.session.get('customer_session'):
            return JsonResponse({'error': 'Customer access required'}, status=403)
            
        # Check driver routes
        if request.path.startswith('/driver_booking/') and not request.session.get('driver_session'):
            return JsonResponse({'error': 'Driver access required'}, status=403)
            
        return self.get_response(request)