from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.utils import timezone

from knox.auth import TokenAuthentication

from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer


# Create your views here.


class VendorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows vendors to be viewed or edited.
    """
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows purchase orders to be viewed or edited.
    """
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def acknowledge_purchase_order(self, request, pk=None):
        """
        Acknowledges a purchase order by updating the acknowledgement date and saving the purchase order.

        Args:
            request (Request): The request object.
            pk (int, optional): The primary key of the purchase order. Defaults to None.

        Returns:
            Response: The response object containing the serialized purchase order data if the serializer is valid, 
                      otherwise the response object containing the serializer errors and a status of 400.
        """
        purchase_order = self.get_object()
        print(purchase_order, '***************\n')
        purchase_order.acknowledgement_date = timezone.now()
        purchase_order.save()
        serializer = PurchaseOrderSerializer(
            purchase_order,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            purchase_order.update_average_response_time()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HistoricalPerformanceDetailView(APIView):
    """
    Retrieves the historical performance.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, vendor_id):
        """
        Retrieves the historical performance data for a specified vendor.

        Parameters:
            request (Request): The request object.
            vendor_id (int): The ID of the vendor.

        Returns:
            Response: The serialized historical performance data for the vendor.

        Raises:
            HistoricalPerformance.DoesNotExist: If the historical performance data is not found for the specified vendor.
        """
        historical_performances = HistoricalPerformance.objects.filter(
            vendor__id=vendor_id)
        if not historical_performances:
            return Response({'detail': 'No historical performance data found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = HistoricalPerformanceSerializer(
            historical_performances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
