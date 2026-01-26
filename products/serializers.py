from rest_framework import serializers
from decimal import Decimal
from products.models import Category, Product, Review, ProductImage
from django.conf import settings
from django.contrib.auth import get_user_model


class CategorySerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Category
        fields = ['id', 'name', 'description', 'product_count']
    product_count = serializers.IntegerField(read_only = True, help_text="Returns the number of product in this category")
    


# class ProductSerializer(serializers.Serializer): 
#     id = serializers.IntegerField()
#     name = serializers.CharField()
#     unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, source = 'price')
#     price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
#     # category = serializers.PrimaryKeyRelatedField(
#     #     queryset = Category.objects.all()   
#     # )
#     # category = serializers.StringRelatedField()
#     # category = CategorySerializer()
#     category = serializers.HyperlinkedRelatedField(
#         queryset = Category.objects.all(), 
#         view_name = 'view_specific_category',
#     )   
    
#     def calculate_tax(self, product): 
#         return round(product.price * Decimal(1.1), 2)
    
class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductSerializer(serializers.ModelSerializer):
    images =  ProductImageSerializer(many = True, read_only = True)
    class Meta: 
        model = Product
        fields = ['id', 'name', 'description', 'stock', 'price', 'category', 'price_with_tax', 'images']
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    def calculate_tax(self, product):
        return round(product.price * Decimal(1.1), 2)



class SimpleUserSerializer(serializers.ModelSerializer): 
    name = serializers.SerializerMethodField(method_name='get_name')
    class Meta: 
        model = get_user_model()
        fields = ['id', 'name', 'email']

    def get_name(self, obj): 
        return obj.get_full_name()



class ReviewSerializer(serializers.ModelSerializer): 
    user = serializers.SerializerMethodField(method_name='get_user')
    class Meta: 
        model = Review 
        fields = ['id', 'user', 'product', 'ratings', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['user', 'product']
        
    def get_user(self, obj): 
        return SimpleUserSerializer(obj.user).data
    
    def create(self, validated_data):
        product_id = self.context['product_pk']
        review = Review.objects.create(product_id = product_id, **validated_data)
        return review
    
    
    
