from django.contrib.auth.mixins import AccessMixin

from django.http import HttpResponseForbidden


class AdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:  # Ensure only admin users can access
            return HttpResponseForbidden("You are not authorized to perform this action.")
        return super().dispatch(request, *args, **kwargs)
        