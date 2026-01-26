from django.shortcuts import render, redirect
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin
from orders.serializer import CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer, OrderSerializer, CreateOrderSerializer, UpdateOrderSerializer, EmptySerializer
from orders.models import Cart, CartItem, Order, OrderItem
from rest_framework import permissions
from rest_framework.decorators import action, api_view
from orders.services import OrderServices
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from sslcommerz_lib import SSLCOMMERZ
from django.conf import settings
from django.http import HttpResponseRedirect
from rest_framework.views import APIView


class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet, ListModelMixin): 
    serializer_class = CartSerializer 
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Cart.objects.none()
        return Cart.objects.prefetch_related('items__product').filter(user = self.request.user)
    
    def create(self, request, *args, **kwargs):
        existing_cart = Cart.objects.filter(user = request.user).first();  
        if existing_cart: 
            serializer = self.get_serializer(existing_cart); 
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return super().create(request, *args, **kwargs)
    
    

class CartItemViewSet(ModelViewSet): 
    http_method_names = ['get', 'post', 'patch', 'delete']
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH': 
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs.get('cart_pk')}
    
    def get_queryset(self):
        return CartItem.objects.select_related('product').filter(cart_id = self.kwargs.get('cart_pk'))
    

class OrderViewSet(ModelViewSet): 
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk = None): 
        order = self.get_object()
        OrderServices.cancel_order(order = order, user = request.user)
        return Response({'status': 'Order Canceled'})
    
    @action(detail= True, methods=['patch'])
    def update_status(self, request, pk = None): 
        order = self.get_object()
        serializer = UpdateOrderSerializer(order, data = request.data, partial = True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': f'Order status updated to {request.data['status']}'})
        
    def get_serializer_class(self):
        if self.action == 'cancel': 
            return EmptySerializer
        if self.request.method == 'POST': 
            return CreateOrderSerializer
        elif self.request.method == 'PATCH': 
            return UpdateOrderSerializer
        return OrderSerializer
    
    def get_serializer_context(self):
        if getattr(self, 'swagger_fake_view', False):
            return {}
        return {'user_id': self.request.user.id, 'user': self.request.user}
    
    def get_permissions(self):
        if self.action in ['update_status', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return {}
        if self.request.user.is_staff: 
            return Order.objects.prefetch_related('items__product').all()
        return Order.objects.prefetch_related('items__product').filter(user=self.request.user)


@api_view(['POST'])
def initiate_payment(request):

    user = request.user
    amount = request.data.get("amount")
    order_id = request.data.get("orderId")
    num_items = request.data.get("numItems")
    
    ssl_settings = {'store_id': 'phima6975dc6e2e54d',
                'store_pass': 'phima6975dc6e2e54d@ssl', 'issandbox': True}
    sslcz = SSLCOMMERZ(ssl_settings)
    post_body = {}
    post_body['total_amount'] = amount
    post_body['currency'] = "BDT"
    post_body['tran_id'] = f"tr_{order_id}"
    post_body['success_url'] = f"{settings.BACKEND_URL}/api/payment/success"
    post_body['fail_url'] = f"{settings.BACKEND_URL}/api/payment/fail"
    post_body['cancel_url'] = f"{settings.BACKEND_URL}/api/payment/cancel"
    post_body['emi_option'] = 0
    post_body['cus_name'] = f"{user.first_name} {user.last_name}"
    post_body['cus_email'] = user.email 
    post_body['cus_phone'] = user.phone_number
    post_body['cus_add1'] = user.address
    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = num_items
    post_body['product_name'] = "E-commerce Products"
    post_body['product_category'] = "General Category"
    post_body['product_profile'] = "general"


    response = sslcz.createSession(post_body) # API response
    
    if response.get("status") == 'SUCCESS' : 
        return Response({"payment_url": response.get("GatewayPageURL")})
    return Response({"error" : "Payment initiation failed"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(["POST"])
def payment_success(request): 
    order_id = request.data.get("tran_id").split('_')[1]
    order = Order.objects.get(id = order_id)
    order.status = "Ready to ship"
    order.save()
    return HttpResponseRedirect(f"{settings.FRONTEND_URL}/dashboard/orders")

@api_view(["POST"])
def payment_cancel(request): 
    return HttpResponseRedirect(f"{settings.FRONTEND_URL}/dashboard/orders")

@api_view(["POST"])
def payment_fail(request): 
    return HttpResponseRedirect(f"{settings.FRONTEND_URL}/dashboard/orders")




class HasOrderedProduct(APIView): 
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, product_id): 
        user = request.user
        has_ordered = OrderItem.objects.filter(order__user = user, product_id = product_id).exists(); 
        return Response({"has_ordered": has_ordered})