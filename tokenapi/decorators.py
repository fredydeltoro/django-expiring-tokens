from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps # Python 2.4 fallback

class HttpResponseUnauthorized(HttpResponse):
    status_code = 401

def token_required(view_func):
    """Decorator which ensures the user has provided a correct user and token pair."""

    @csrf_exempt
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = None
        token = None
        basic_auth = request.META.get('HTTP_AUTHORIZATION')
        if basic_auth:
            auth_method, auth_string = basic_auth.split(' ', 1)
            if auth_method.lower() == 'basic':
                auth_string = auth_string.strip().decode('base64')
                user, token = auth_string.split(':', 1)

        if not (user and token):
            user = request.REQUEST.get('user')
            token = request.REQUEST.get('token')

        if user and token:
            try:
                user = authenticate(pk=user, token=token)
            except:
                raise HttpResponseForbidden
            if user:
                login(request, user)
                return view_func(request, *args, **kwargs)
        return HttpResponseUnauthorized()
    return _wrapped_view
