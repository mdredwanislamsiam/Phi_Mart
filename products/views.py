from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from products.models import Product, Category, Review, ProductImage
from rest_framework import status
from products.serializers import ProductSerializer, CategorySerializer, ReviewSerializer, ProductImageSerializer
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from products.filters import ProductFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from products.pagination import DefaultPagination
from api.permissions import IsAdminOrReadOnly
from products.permissions import IsReviewAuthorOrReadOnly
from drf_yasg.utils import swagger_auto_schema

""" Main views"""


class ProductViewSet(ModelViewSet): 
    """
    API endpoint for managing products in the e-commerce store
    - Allow authenticated admin to create, update, and delete products
    - Allows Users to browse and filter product 
    - Support searching by name, description and category
    - Support ordering by price and updated_at
    """
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related('category').all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['price']
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]    
    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     category_id = self.request.query_params.get('category_id')
    #     if category_id is not None: 
    #         queryset = Product.objects.filter(category_id = category_id)
    #     return queryset
    @swagger_auto_schema(
        operation_summary= "Retrive a list of products"
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    
    @swagger_auto_schema(
        operation_summary="Create a product by admin", 
        operation_description="This allow only an admin to create a product", 
        request_body=ProductSerializer, 
        responses={
            201: ProductSerializer, 
            400: "Bad Request"
        }, 
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
     
        
class ProductImageViewSet(ModelViewSet): 
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrReadOnly]
    def get_queryset(self):
        return ProductImage.objects.prefetch_related('product').filter(product_id=self.kwargs.get('product_pk'))
    
    def perform_create(self, serializer): 
        serializer.save(product_id=self.kwargs.get('product_pk'))
       
class CategoryViewSet(ModelViewSet): 
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.annotate(product_count = Count('products')).all()
    serializer_class = CategorySerializer
    

class ReviewViewSet(ModelViewSet): 
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewAuthorOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs.get('product_pk'))
    
    def get_serializer_context(self):
        return {'product_pk': self.kwargs.get('product_pk')}
    
    
    
    
    
    
    
    
    
    """ Previous Practices """

@api_view(['GET', 'POST'])
def view_products(request): 
    if request.method =='GET': 
        products = Product.objects.select_related('category').all()
        serializer = ProductSerializer(products, many = True, context = {'request': request})
        return Response(serializer.data)
    if request.method == 'POST': 
        serializer = ProductSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else: 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductsView(ListCreateAPIView): 
    def get_queryset(self):
        return Product.objects.select_related('category').all()

    def get_serializer_class(self):
        return ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class ViewProducts(APIView): 
    def get(self, request): 
        products = Product.objects.select_related('category').all()
        serializer = ProductSerializer(
            products, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request): 
        serializer = ProductSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def view_specifi_product(request, id): 
    if request.method == 'GET': 
        product = get_object_or_404(Product, pk = id)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)
    if request.method == 'PUT': 
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(
            product, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE': 
        product = get_object_or_404(Product, pk = id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ViewSpecificProduct(APIView): 
    def get(self, request, id): 
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request, id): 
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(
            product, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id): 
        product = get_object_or_404(Product, pk=id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
   

class ProductDetails(RetrieveUpdateDestroyAPIView): 
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'
        
        
        
@api_view(['GET', 'POST'])
def view_categories(request): 
    if request.method == 'GET': 
        categories = Category.objects.annotate(product_count=Count('products')).all()
        serializer = CategorySerializer(categories, many = True)
        return Response(serializer.data)
    if request.method == 'POST': 
        serializer = CategorySerializer(data = request.data)
        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        else: 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewCategories(APIView): 
    def get(self, request): 
        categories = Category.objects.annotate(product_count=Count('products')).all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    def post(self, request): 
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryView(ListCreateAPIView): 
    queryset = Category.objects.annotate(product_count=Count('products')).all()
    serializer_class = CategorySerializer
    
    
    

@api_view()
def view_specific_category(request, pk):
    category = get_object_or_404(Category, pk = pk)
    serializer = CategorySerializer(category)
    return Response(serializer.data)

class ViewSpecificCategory(APIView): 
    def get(self, request, pk): 
        category = get_object_or_404(Category.objects.annotate(product_count=Count('products')).all(), pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    def put(self, request, pk): 
        category = get_object_or_404(Category.objects.annotate(
            product_count=Count('products')).all(), pk=pk)
        serializer = CategorySerializer(category, data = request.data)
        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data)
        else: 
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk): 
        category = get_object_or_404(Category.objects.annotate(
            product_count=Count('products')).all(), pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryDetails(RetrieveUpdateDestroyAPIView): 
    queryset = Category.objects.annotate(product_count=Count('products')).all()
    serializer_class = CategorySerializer
    
    