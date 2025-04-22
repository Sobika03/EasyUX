from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden
from django.urls import resolve

EXEMPT_URL_NAMES = [
    'login',
    'logout',
    'admin:index',
    'subscription_plans',  # add your exempt view names here
]

class SubscriptionRequiredMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.user.is_authenticated:
            return None  # Let login-required logic handle unauthenticated users

        # Skip exempt URLs
        if resolve(request.path_info).url_name in EXEMPT_URL_NAMES:
            return None

        org = getattr(request.user, 'organization', None)
        sub = getattr(org, 'subscription', None)

        if not org or not sub or not sub.is_active():
            return HttpResponseForbidden("Your organization's subscription is inactive or expired.")

        return None  # Allow the request