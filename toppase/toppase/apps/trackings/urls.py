from django.conf.urls import url

from .views import StoreViewSet, OrderViewSet, TrackingDashboradView, TrackingBusinessView, OrderCSVCreateApiView, OrderDetailView, ProductViewSet, CourierViewSet

# VIEWSETS URLS

store_list = StoreViewSet.as_view({
    'get': 'list',
})
store_detail = StoreViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
})

order_list = OrderViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
order_detail = OrderViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


product_list = ProductViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
product_detail = ProductViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

courier_list = CourierViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
courier_detail = CourierViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


# URL PATTERNS


urlpatterns = [
    # Tracking
    url(r'^store/(?P<pk>[0-9]+)/$',
        TrackingBusinessView.as_view(),
        name='tracking'),
    # Dashboard
    url(r'^dashboard$',
        TrackingDashboradView.as_view(),
        name='dashboard'),
    # Order Detail
    url(r'^store/(?P<store_id>[0-9]+)/order/(?P<pk>[0-9]+)/$',
        OrderDetailView.as_view(),
        name='order-detail'),
    # API STORE
    url(r'^api/stores/$',
        store_list,
        name='store-list-api'),
    url(r'^api/store/(?P<pk>[0-9]+)/$',
        store_detail,
        name='store-detail-api'),
    # API ORDER
    url(r'^api/store/(?P<store_id>[0-9]+)/orders/$',
        order_list,
        name='order-list-api'),
    url(r'^api/store/(?P<store_id>[0-9]+)/order/(?P<pk>[0-9]+)/$',
        order_detail,
        name='order-detail-api'),
    # API ORDER_CSV
    url(r'^api/order-csv/$',
        OrderCSVCreateApiView.as_view(),
        name='order-csv-api'),
    # API COURIER
    url(r'^api/store/(?P<store_id>[0-9]+)/couriers/$',
        courier_list,
        name='courier-list-api'),
    url(r'^api/store/(?P<store_id>[0-9]+)/courier/(?P<pk>[a-zA-Z0-9]+)/$',
        courier_detail,
        name='courier-detail-api'),
    #API PRODUCT
    url(r'^api/store/(?P<store_id>[0-9]+)/products/$',
        product_list,
        name='product-list-api'),
    url(r'^api/store/(?P<store_id>[0-9]+)/product/(?P<pk>[a-zA-Z0-9]+)/$',
        product_detail,
        name='product-detail-api'),

]
