from django.contrib import admin
from .models import CustomUser , NhaXe, TuyenXe, ChuyenXe, Booking, Delivery

# Đăng ký mô hình CustomUser để nó xuất hiện trong trang Admin
admin.site.register(CustomUser)
admin.site.register(NhaXe)
admin.site.register(TuyenXe)
admin.site.register(ChuyenXe)
admin.site.register(Booking)
admin.site.register(Delivery)
