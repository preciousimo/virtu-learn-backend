from django.http import HttpResponseForbidden

class RestrictHostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.META.get('HTTP_HOST') != 'virtulearn.vercel.app':
            return HttpResponseForbidden("Access Forbidden")
        return self.get_response(request)
