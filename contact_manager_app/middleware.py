import requests
from django.http import JsonResponse


class RegionRestrictionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = requests.get(f"https://ipinfo.io/json")
        country = response.json().get("country")

        if country not in ["UA", "PL"]:
            return JsonResponse({"detail": "Access restricted by region."}, status=403)

        return self.get_response(request)
