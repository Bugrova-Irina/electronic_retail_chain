from django.urls import path

from retail.apps import RetailConfig
from retail.views import SellerListAPIView, SellerRetrieveAPIView, SellerUpdateAPIView, SellerDestroyAPIView

app_name = RetailConfig.name

urlpatterns = [
    path("", SellerListAPIView.as_view(), name="sellers-list"),
    path("<int:pk>/", SellerRetrieveAPIView.as_view(), name="seller-retrieve"),
    path("<int:pk>/update/", SellerUpdateAPIView.as_view(), name="seller-update"),
    path("create/", SellerUpdateAPIView.as_view(), name="seller-create"),
    path("<int:pk>/delete/", SellerDestroyAPIView.as_view(), name="seller-delete"),
]
