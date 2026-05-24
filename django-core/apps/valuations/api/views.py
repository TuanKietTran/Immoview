from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from apps.valuations.domain.services import estimate_price
from apps.valuations.infrastructure.models import ValuationModel
from .serializers import ValuationRequestSerializer, ValuationResponseSerializer


class ValuationEstimateView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ValuationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        result = estimate_price(
            canton=data["canton"],
            property_type=data["property_type"],
            offer_type=data["offer_type"],
            area_m2=data["area_m2"],
            rooms=data.get("rooms"),
        )

        valuation = ValuationModel.objects.create(
            listing_id=data.get("listing_id"),
            canton=result["canton"],
            property_type=result["property_type"],
            offer_type=result["offer_type"],
            area_m2=result["area_m2"],
            estimate_chf=result["estimate_chf"],
            range_low_chf=result["range_low_chf"],
            range_high_chf=result["range_high_chf"],
        )

        return Response(ValuationResponseSerializer(valuation).data, status=201)
