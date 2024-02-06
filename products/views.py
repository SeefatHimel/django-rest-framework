from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer


# Create your views here.
@api_view(["POST", "GET"])
def products(request, fomat=None):
    if request.method == "GET":
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT", "DELETE", "GET"])
def product(request, id, fomat=None):
    try:
        product = Product.objects.get(pk=id)
    except:
        return Response(
            {"message": "Product Not Found"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        product.delete()
        return Response(
            {"message": "Product Deleted"}, status=status.HTTP_204_NO_CONTENT
        )
