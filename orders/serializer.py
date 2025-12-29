from rest_framework import serializers
from orders.models import Cart, CartItem, Order, OrderItem
from products.serializers import ProductSerializer
from products.models import Product 
from orders.services import OrderServices



class SimpleProductSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Product 
        fields = ['id', 'name', 'price']


class AddCartItemSerializer(serializers.ModelSerializer): 
    product_id = serializers.IntegerField()
    class Meta: 
        model = CartItem
        fields = ['id', 'product_id', 'quantity']
        
    def save(self, **kwargs): 
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try: 
            cart_item = CartItem.objects.get(cart_id = cart_id, product_id = product_id)
            cart_item.quantity += quantity
            self.instance = cart_item.save()
        except CartItem.DoesNotExist: 
            self.instance = CartItem.objects.create(cart_id = cart_id, **self.validated_data)
        return self.instance

    def validate_product_id(self, value): 
        if not Product.objects.filter(pk = value): 
            raise serializers.ValidationError(f"Product {value} does not exist")
        return value


class UpdateCartItemSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = CartItem
        fields = ['quantity']


class CartItemSerializer(serializers.ModelSerializer): 
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField(method_name='get_total_price')
    class Meta: 
        model = CartItem
        fields = ['id', 'quantity', 'product', 'total_price']
    
    def get_total_price(self, item:CartItem): 
        return item.product.price*item.quantity
     

class CartSerializer(serializers.ModelSerializer): 
    items = CartItemSerializer(many = True, read_only = True)
    total = serializers.SerializerMethodField(method_name='get_total_price')
    class Meta: 
        model = Cart 
        fields = ['id', 'user', 'items', 'total']
        read_only_fields = ['user']
    def get_total_price(self, cart:Cart): 
        # total = 0
        # items = CartItem.objects.filter(cart = cart)
        # for cart_item in items: 
        #     total += (cart_item.product.price*cart_item.quantity)
        # return total
        
        return sum([item.product.price * item.quantity for item in cart.items.all()])
    
    
    
class CreateOrderSerializer(serializers.Serializer): 
    cart_id = serializers.UUIDField()
    
    def validate_cart_id(self, cart_id): 
        if not Cart.objects.filter(pk = cart_id).exists(): 
            raise serializers.ValidationError("No Such Cart Found")
        if not CartItem.objects.filter(cart_id = cart_id).exists(): 
            raise serializers.ValidationError("Empty Cart")
        return cart_id
    
    def create(self, validated_data):
        user_id = self.context['user_id']
        cart_id = validated_data['cart_id']
        
        try: 
            order = OrderServices.create_order(user_id, cart_id)
            return order 
        except ValueError as e: 
            raise serializers.ValidationError(str(e))
        
        
    def to_representation(self, instance):
        return OrderSerializer(instance).data

class OrderItemSerializer(serializers.ModelSerializer): 
    product = SimpleProductSerializer()
    class Meta: 
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price', 'total_price']
    
    
class UpdateOrderSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Order 
        fields = ['status']
    
    # def update(self, instance, validate_data): 
    #     user = self.context['user']
    #     new_status = validate_data['status']
        
    #     if new_status == Order.CANCELED: 
    #         return OrderServices.cancel_order(order=instance, user= user)
          
    #     if not user.is_staff: 
    #         raise serializers.ValidationError({'detail': 'You are not the admin'})
          
    #     return super().update(instance=instance, validated_data= validate_data)
    
    
class EmptySerializer(serializers.Serializer): 
    pass
    
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many = True)
    class Meta: 
        model = Order
        fields = ['id', 'user', 'status', 'total_price', 'created_at', 'items']