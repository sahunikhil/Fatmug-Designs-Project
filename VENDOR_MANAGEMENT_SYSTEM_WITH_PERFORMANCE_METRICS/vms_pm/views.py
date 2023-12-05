from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
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


class HistoricalPerformanceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows historical performance to be viewed or edited.
    """

    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
