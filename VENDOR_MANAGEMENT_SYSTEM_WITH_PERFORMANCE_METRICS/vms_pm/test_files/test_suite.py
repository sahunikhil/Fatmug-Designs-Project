from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from vms_pm.models import Vendor, PurchaseOrder
from knox.models import AuthToken
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class VendorTests(APITestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        # Create a Vendor object for testing
        self.vendor_data = {'name': 'Test Vendor',
                            'contact_details': 'Contact', 'address': 'Address'}
        self.vendor = Vendor.objects.create(**self.vendor_data)
        # Obtain an authentication token for the user
        self.token = AuthToken.objects.create(self.user)[1]

    def test_generate_token(self):
        """
        Ensure we can generate a token for a user.
        """
        # Simulate basic authentication by using force_login
        self.client.force_login(self.user)
        url = 'http://127.0.0.1:8000/api/auth/login/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_create_vendor(self):
        """
        Ensure we can create a new vendor.
        """
        url = reverse('vendor-list')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, self.vendor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Assuming one vendor is created in setUp
        self.assertEqual(Vendor.objects.count(), 2)
        self.assertEqual(Vendor.objects.last().name, 'Test Vendor')

    def test_retrieve_vendor(self):
        """
        Ensure we can retrieve a vendor.
        """
        url = reverse('vendor-detail', kwargs={'pk': self.vendor.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Vendor')

    def test_update_vendor(self):
        """
        Ensure we can update details of a existing vendor.
        """
        url = reverse('vendor-detail', kwargs={'pk': self.vendor.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        updated_data = {'name': 'Updated Vendor',
                        'contact_details': 'New Contact'}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Vendor.objects.get(
            pk=self.vendor.pk).name, 'Updated Vendor')

    def test_delete_vendor(self):
        """
        Ensure we can delete an existing vendor object.
        """
        url = reverse('vendor-detail', kwargs={'pk': self.vendor.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vendor.objects.count(), 0)


class PurchseOrderTests(APITestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        # Create a Vendor object for testing
        self.vendor_data = {'name': 'Test Vendor',
                            'contact_details': 'Contact', 'address': 'Address'}
        self.vendor = Vendor.objects.create(**self.vendor_data)
        # Create a PurchaseOrder object for testing
        self.purchase_order_data = {
            'vendor': self.vendor,
            'items': {'item1': 10, 'item2': 20},
            'quantity': 30,
            'quality_rating': 4.5,
            'status': 'pending'
        }
        self.purchase_order = PurchaseOrder.objects.create(
            **self.purchase_order_data)
        # Obtain an authentication token for the user
        self.token = AuthToken.objects.create(self.user)[1]

    def test_create_purchase_order(self):
        """
        Ensure we can create a new purchase order.
        """
        url = reverse('purchaseorder-list')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        purchase_order_data = {
            'vendor': self.vendor.pk,
            'items': {'item1': 10, 'item2': 20},
            'quantity': 30,
            'quality_rating': 4.5,
            'status': 'pending'
        }
        response = self.client.post(
            url, purchase_order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Assuming one purchase order is created in setUp
        self.assertEqual(PurchaseOrder.objects.count(), 2)
        self.assertEqual(PurchaseOrder.objects.last().quantity, 30)

    def test_retrieve_purchase_order(self):
        """
        Ensure we can retrieve a purchase order.
        """
        url = reverse('purchaseorder-detail',
                      kwargs={'pk': self.purchase_order.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], 30)

    def test_update_purchase_order(self):
        """
        Ensure we can update details of a existing purchase order.
        """
        url = reverse('purchaseorder-detail',
                      kwargs={'pk': self.purchase_order.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        updated_data = {'status': 'completed'}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(PurchaseOrder.objects.get(
            pk=self.purchase_order.pk).status, 'completed')

    def test_delete_purchase_order(self):
        """
        Ensure we can delete an existing purchase order object.
        """
        url = reverse('purchaseorder-detail',
                      kwargs={'pk': self.purchase_order.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PurchaseOrder.objects.count(), 0)


class HistoricalPerformanceTests(APITestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        # Create a Vendor object for testing
        self.vendor_data = {'name': 'Test Vendor',
                            'contact_details': 'Contact', 'address': 'Address'}
        self.vendor = Vendor.objects.create(**self.vendor_data)
        # Obtain an authentication token for the user
        self.token = AuthToken.objects.create(self.user)[1]

    def test_retrieve_historical_performance(self):
        """
        Ensure we can retrieve historical performance details for a specific vendor.
        """
        url = f'http://127.0.0.1:8000/api/vendors/{self.vendor.pk}/performance'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_nonexistent_historical_performance(self):
        """
        Ensure a 404 response when attempting to retrieve historical performance
        for a vendor that has no historical data.
        """
        nonexistent_vendor_id = 999  # Assuming this vendor ID does not exist
        url = f'http://127.0.0.1:8000/api/vendors/{nonexistent_vendor_id}/performance'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AcknowledgePurchaseOrderTests(APITestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        # Create a Vendor object for testing
        self.vendor_data = {'name': 'Test Vendor', 'contact_details': 'Contact',
                            'address': 'Address', 'vendor_code': 'V1'}
        self.vendor = Vendor.objects.create(**self.vendor_data)
        # Create a PurchaseOrder object for testing
        self.purchase_order_data = {
            'vendor': self.vendor,
            'items': {'item1': 10, 'item2': 20},
            'quantity': 30,
            'quality_rating': 4.5,
            'status': 'pending'
        }
        self.purchase_order = PurchaseOrder.objects.create(
            **self.purchase_order_data)
        # Obtain an authentication token for the user
        self.token = AuthToken.objects.create(self.user)[1]

    def test_acknowledge_purchase_order(self):
        """
        Ensure we can acknowledge a purchase order and trigger the recalculation of average_response_time.
        """
        url = reverse('acknowledge_purchase_order', kwargs={
                      'pk': self.purchase_order.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(PurchaseOrder.objects.get(
            pk=self.purchase_order.pk).acknowledgement_date.minute, timezone.now().minute)
