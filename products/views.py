from rest_framework import generics
from utils.mixins import SerializerByMethodMixin

from .models import Product
from .permissions import AuthSellerPermission, SellerOwnerPermission
from .serializers import CreateProductSerializer, ListProductSerializer


# Create your views here.
class ProductView(SerializerByMethodMixin, generics.ListCreateAPIView):
    permission_classes = [AuthSellerPermission]

    queryset = Product.objects.all()
    serializer_map = {"GET": ListProductSerializer, "POST": CreateProductSerializer}

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProductParamsView(SerializerByMethodMixin, generics.RetrieveUpdateAPIView):
    permission_classes = [SellerOwnerPermission]

    queryset = Product.objects.all()
    serializer_map = {"GET": ListProductSerializer, "PATCH": CreateProductSerializer}
