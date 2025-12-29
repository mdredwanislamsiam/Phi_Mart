from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin
from orders.serializer import CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer, OrderSerializer, CreateOrderSerializer, UpdateOrderSerializer, EmptySerializer
from orders.models import Cart, CartItem, Order, OrderItem
from rest_framework import permissions
from rest_framework.decorators import action
from orders.services import OrderServices
from rest_framework.response import Response


class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet, ListModelMixin): 
    serializer_class = CartSerializer 
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Cart.objects.none()
        return Cart.objects.prefetch_related('items__product').filter(user = self.request.user)
    

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
            return Cart.objects.none()
        return {'user_id': self.request.user.id, 'user': self.request.user}
    
    def get_permissions(self):
        if self.action in ['update_status', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Cart.objects.none()
        if self.request.user.is_staff: 
            return Order.objects.prefetch_related('items__product').all()
        return Order.objects.prefetch_related('items__product').filter(user=self.request.user)
