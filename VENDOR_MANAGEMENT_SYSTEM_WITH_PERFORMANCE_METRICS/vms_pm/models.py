from django.db import models
from django.db.models import F, Sum
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import F, ExpressionWrapper, fields

import random
import string
from datetime import datetime

# py manage.py createsuperuser --email admin@example.com --username admin
# pass: 1234

# Create your models here.


def generate_vendor_code():
    return 'V' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))


def generate_po_number():
    return 'PO' + datetime.now().strftime('%Y%m%d%H%M%S') + '-' + ''.join(random.choice(string.digits) for _ in range(5))


class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    vendor_code = models.CharField(
        max_length=50, unique=True, default=generate_vendor_code, editable=False, blank=True)
    on_time_delivery_rate = models.FloatField(null=True, editable=False)
    quality_rating_avg = models.FloatField(null=True, editable=False)
    average_response_time = models.FloatField(null=True, editable=False)
    fulfillment_rate = models.FloatField(null=True, editable=False)

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, null=True, blank=True)
    po_number = models.CharField(
        max_length=50, unique=True, default=generate_po_number, editable=False, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    items = models.JSONField(null=True, blank=True)
    quantity = models.IntegerField(default=0)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    quality_rating = models.FloatField(blank=True,
                                       null=True, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    issue_date = models.DateTimeField(null=True, blank=True)
    acknowledgement_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number

    def update_average_response_time(self):
        if self.issue_date:
            acknowledged_vendor_orders = PurchaseOrder.objects.filter(
                vendor=self.vendor, acknowledgement_date__isnull=False, issue_date__isnull=False)
            self.vendor.average_response_time = acknowledged_vendor_orders.annotate(duration=ExpressionWrapper(
                F('acknowledgement_date') - F('issue_date'),
                output_field=fields.DurationField()
            )).values('duration').aggregate(Sum('duration'))['duration__sum'].total_seconds() / acknowledged_vendor_orders.count()
            self.vendor.save()


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField(editable=False, null=True)
    quality_rating_avg = models.FloatField(editable=False, null=True)
    average_response_time = models.FloatField(editable=False, null=True)
    fulfillment_rate = models.FloatField(editable=False, null=True)
