from django.urls import path
from products import views



urlpatterns = [
    path('', views.CategoryView.as_view(), name='category_list'), 
    path('<int:pk>/', views.CategoryDetails.as_view(), name ='view_specific_category'), 
]
