from django.utils.cache import add_never_cache_headers

class NoCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # If the user is authenticated, we want to prevent browser caching
        # This solves the "back button after logout" issue.
        if request.user.is_authenticated:
            add_never_cache_headers(response)
        return response
