from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import CustomUserViewSet
from .views import custom_login, NhaXeViewSet, TuyenXeViewSet, ChuyenXeViewSet, BookingViewSet, DeliveryViewSet
from django.conf import settings
from django.conf.urls.static import static
from . import views

router = DefaultRouter()
router.register(r"userprofiles", CustomUserViewSet)
router.register(r"nha-xe", NhaXeViewSet)
router.register(r"tuyen-xe", TuyenXeViewSet)
router.register(r"chuyen-xe", ChuyenXeViewSet)
router.register(r"booking" , BookingViewSet)
router.register(r"delivery" , DeliveryViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path(
        "userprofiles/",
        CustomUserViewSet.as_view({"get": "list"}),
        name="userprofiles-list",
    ),
    path("user/login", custom_login, name="custom_login"),
    path("nha-xe/<int:pk>/doanh-thu-theo-thang/", NhaXeViewSet.as_view({'get': 'doanh_thu_theo_thang'}), name='nha-xe-doanh-thu-theo-thang'),
    path('nha-xe/', views.get_all_nha_xe, name='get_all_nha_xe'),
    path('tuyen-xe/', views.get_all_tuyen_xe, name='get_all_tuyen_xe'),  
    path('chuyen-xe/', views.get_all_chuyen_xe, name='get_all_chuyen_xe'),  
    path('booking/', views.get_all_booking, name='get_all_booking'),
    path('delivery/', views.get_all_delivery, name='get_all_delivery'),
    path('get-nha-xe-by-user/<int:user_id>/', views.get_nha_xe_by_user, name='get_nha_xe_by_user'),
    path('get-tuyen-xe-by-nhaxe/<int:nha_xe_id>/', views.get_tuyen_xe_by_nha_xe, name='get_tuyen_xe_by_nha_xe'),
    path('booking/user/<int:user_id>/', views.get_booking_by_user, name='get_booking_by_user'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
