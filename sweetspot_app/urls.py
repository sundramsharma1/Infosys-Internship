from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, CakeViewSet, CakeCustomizationViewSet, CartViewSet, OrderViewSet , AddCakeToCartViewSet,AdminCustomerViewSet, AdminCakeViewSet, AdminCakeCustomizationViewSet, AdminOrderViewSet, AdminStoreViewSet

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'cakes', CakeViewSet)
router.register(r'cake-customizations', CakeCustomizationViewSet)
router.register(r'carts', CartViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'add-cake-to-cart', AddCakeToCartViewSet, basename='add-cake-to-cart')


# Admin routers
router.register(r'admin/customers', AdminCustomerViewSet, basename='admin-customer')
router.register(r'admin/cakes', AdminCakeViewSet, basename='admin-cake')
router.register(r'admin/cake_customizations', AdminCakeCustomizationViewSet, basename='admin-cake_customization')
router.register(r'admin/orders', AdminOrderViewSet, basename='admin-order')
router.register(r'admin/stores', AdminStoreViewSet, basename='admin-store')


urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]





















# from django.urls import path 
# from .views import CakeAPIView,UserLoginAPIView,CustomerRegistrationAPIView,CakeRetrieveUpdateDestroyAPIView,CakeCustomizationAPIView,CustomizeOptionRetrieveUpdateDestroyAPIView,CartAPIView,CartRetrieveUpdateDestroyAPIView,OrderListCreateAPIView,OrderRetrieveUpdateDestroyAPIView
# urlpatterns = [
#     path('users/register/', CustomerRegistrationAPIView.as_view() ,name='userRegistration'),
#     path('users/login/',UserLoginAPIView.as_view(),name='userLogin'),
#     path('cakes/',CakeAPIView.as_view(),name='cake'),
#     path('cakes/<int:pk>/',CakeRetrieveUpdateDestroyAPIView().as_view(),name='cakeRetrieveUpdate'),
#     path('cart/',CartAPIView.as_view(),name='cart'),
#     path('cart/<int:pk>/',CartRetrieveUpdateDestroyAPIView.as_view(),name='cartRetrieveUpdate'),
#     path('order/',OrderListCreateAPIView.as_view(),name='order'),
#     path('order/<int:pk>/',OrderRetrieveUpdateDestroyAPIView.as_view(),name='orderRetrieveUpdate'),
#     path('customize/',CakeCustomizationAPIView.as_view(),name='customize')
#     ,path('customize/<int:pk>/',CustomizeOptionRetrieveUpdateDestroyAPIView.as_view(),name='customizeRetrieveUpdate') 
# ]
