from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer, ProductQuantitySerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# @api_view(['PUT'])
# def update_product_stock(request, pk):
#     # return Response('success', status=status.HTTP_200_OK)
#     try:
#         product = Product.objects.get(pk=pk)
#     except Product.DoesNotExist:
#         return Response(status=404)

#     serializer = ProductSerializer(product, data=request.data)

#     if serializer.is_valid():
#         serializer.save()

#         return Response(serializer.data)

#     return Response(serializer.errors, status=400)
class UpdateProductStockView(APIView):
    def put(self, request, pk, format=None):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        quantitySerializer = ProductQuantitySerializer(data=request.data)
        productSerializer = ProductSerializer(product)
        if quantitySerializer.is_valid(raise_exception=True):
            quantity = quantitySerializer.validated_data['quantity']

            if quantity < 0 and abs(quantity) > product.stock:
                return Response({"error": "Insufficient stock"}, status=status.HTTP_400_BAD_REQUEST)
            
            product.stock += quantity
            product.save()
        
            return Response(productSerializer.data, status=status.HTTP_200_OK)

        return Response(quantitySerializer.errors, status=status.HTTP_400_BAD_REQUEST)