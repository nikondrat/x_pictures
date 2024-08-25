from rest_framework.throttling import ScopedRateThrottle


class BackedScopedRateThrottle(ScopedRateThrottle):
    def allow_request(self, request, view):
        return super().allow_request(request, view)
