from django.dispatch import receiver
from django.utils import timezone
from fieldsignals import post_save_changed

from .models import HistoricalPerformance, PurchaseOrder, Vendor


@receiver(post_save_changed, sender=PurchaseOrder)
def PO_field_changes(sender, instance, changed_fields, **kwargs):

    # When vendor is assigned to a purchase order, update issue_date.
    if 'vendor' in changed_fields and changed_fields['vendor'][1] is not None:
        instance.issue_date = timezone.now()
        instance.save()

    # Update Metrics
    if 'status' in changed_fields:
        # Fulfilment Rate
        completed_orders_for_vendor = PurchaseOrder.objects.filter(
            vendor=instance.vendor, status='completed')
        instance.vendor.fulfillment_rate = (
            completed_orders_for_vendor.count() / instance.vendor.purchaseorder_set.count()) * 100

        if changed_fields['status'][1] == 'completed':
            # On-Time Delivery Rate
            orders_completed_on_time = PurchaseOrder.objects.filter(
                vendor=instance.vendor, status='completed', delivery_date__gte=timezone.now())
            instance.vendor.on_time_delivery_rate = (
                orders_completed_on_time.count() / (completed_orders_for_vendor.count() if completed_orders_for_vendor.count() > 0 else 1)) * 100

            # Quality Rating Average
            completed_orders_with_rating = PurchaseOrder.objects.filter(
                vendor=instance.vendor, status='completed', quality_rating__isnull=False)
            sum_of_ratings = sum(
                obj.quality_rating for obj in completed_orders_with_rating)
            instance.vendor.quality_rating_avg = sum_of_ratings / \
                (completed_orders_with_rating.count()
                 if completed_orders_with_rating.count() > 0 else 1)
    instance.vendor.save()


@receiver(post_save_changed, sender=Vendor)
def Vendor_field_changes(sender, instance, changed_fields, **kwargs):

    # Save historical performance
    HistoricalPerformance.objects.create(
        vendor=instance,
        on_time_delivery_rate=instance.on_time_delivery_rate,
        quality_rating_avg=instance.quality_rating_avg,
        average_response_time=instance.average_response_time,
        fulfillment_rate=instance.fulfillment_rate
    )
