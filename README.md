
# Fatmug Designs Project

Develop a Vendor Management System using Django and Django REST Framework. This system will handle vendor profiles, track purchase orders, and calculate vendor performance metrics.

## Authors

- [@sahunikhil](https://www.github.com/sahunikhil)


## Installation

There is no need to install python libraries. We can just activate
virtual environment and start using it.

```bash
  venv\Scripts\activate     # For Windows
  source venv/bin/activate  # For Linux
```
To run the Django development server, come inside project directory where manage.py resides and run:
```bash
    python3 manage.py runserver
```

## Documentation

Read Project-Requirements.pdf for full requirements.

*Specifications*:

1. Vendor
- Vendor code will be generated automatically.
- All CRUD operations are added.

2. Purchase Order
- Purchase Order code will be generated automatically.
- All CRUD operations are added.

3. Miscellaneous
- We have to create Purchase Order having Vendor null. So that when update/assign Vendor to it, the issue_date will be updated to datetime.now().

- When we acknowledge Purchase Order through API call, it should already have Vendor assigned to it. Also acknowledge_date will be updated on this API call.

- When status field is updated, then metrics for that vendor will be updated.

- On each updation of Vendor fields, the Historical Performance model instance will be created.

- All the API endpoints need Token for authentication, expect Generate API endpoint which need basic auth for athentication.

You can see API documentation on:

http://127.0.0.1:8000/api/schema/swagger-ui/

http://127.0.0.1:8000/api/schema/redoc/

You can also see screenshots on the Screenshots Folder.
## Additional libraries

- Used django-fieldsignals for field signals
- Used django-rest-knox for Token Authentication
- Used drf-spectacular for documentation


## API Endpoints

- admin/
- api/ ^vendors/$ [name='vendor-list']
- api/ ^vendors\.(?P<format>[a-z0-9]+)/?$ [name='vendor-list']
- api/ ^vendors/(?P<pk>[^/.]+)/$ [name='vendor-detail']
- api/ ^vendors/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$ [name='vendor-detail']
- api/ ^purchase_orders/$ [name='purchaseorder-list']
- api/ ^purchase_orders\.(?P<format>[a-z0-9]+)/?$ [name='purchaseorder-list']
- api/ ^purchase_orders/(?P<pk>[^/.]+)/$ [name='purchaseorder-detail']
- api/ ^purchase_orders/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$ [name='purchaseorder-detail']
- api/ ^$ [name='api-root']
- api/ ^\.(?P<format>[a-z0-9]+)/?$ [name='api-root']
- api-auth/
- api/purchase_orders/<int:pk>/acknowledge/ [name='acknowledge_purchase_order']
- api/auth/
- api/vendors/<int:vendor_id>/performance [name='historicalperformance-detail']
- api/schema/ [name='schema']
- api/schema/swagger-ui/ [name='swagger-ui']
- api/schema/redoc/ [name='redoc']
