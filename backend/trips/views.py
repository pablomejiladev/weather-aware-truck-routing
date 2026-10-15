import requests
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import TripRequestSerializer
from .services.planner import plan_trip


class PlanTripView(APIView):
    def post(self, request):
        form = TripRequestSerializer(data=request.data)
        form.is_valid(raise_exception=True)
        data = form.validated_data
        try:
            result = plan_trip(
                data["origin"],
                data["destination"],
                data["departure"],
                data["load_lb"],
                data["interval_miles"],
            )
        except ValueError as exc:
            return Response({"error": str(exc)}, status=400)
        except requests.RequestException as exc:
            return Response({"error": f"Upstream service failed: {exc}"}, status=502)
        return Response(result)


class HealthView(APIView):
    def get(self, request):
        return Response({"status": "ok"})
