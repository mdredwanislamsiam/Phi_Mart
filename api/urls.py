from django.urls import path, include
from products.views import ProductViewSet, CategoryViewSet, ReviewViewSet, ProductImageViewSet
from rest_framework_nested import routers
from orders.views import CartViewSet, CartItemViewSet, OrderViewSet, initiate_payment, payment_success

router = routers.DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('categories', CategoryViewSet)
router.register('carts', CartViewSet, basename='carts')
router.register('orders', OrderViewSet, basename='orders')


product_router = routers.NestedDefaultRouter(router, 'products', lookup ='product')
product_router.register('reviews', ReviewViewSet, basename='product-review')
product_router.register('images', ProductImageViewSet, basename='product-images' )

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', CartItemViewSet, basename='cart-items')



urlpatterns =[
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('payment/initiate', initiate_payment, name = "initiate-payment"), 
    path('payment/success', payment_success, name = "payment-success"), 
    
]+ router.urls + product_router.urls + carts_router.urls
