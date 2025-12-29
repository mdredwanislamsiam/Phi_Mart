from django.urls import path
from products import views


urlpatterns = [
    path('', views.ProductsView.as_view(), name = 'product_list'),
    path('<int:id>/', views.ProductDetails.as_view(), name = 'view_specific_product'), 
]
