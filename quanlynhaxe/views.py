from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser, NhaXe, TuyenXe, ChuyenXe, Booking, Delivery, Review
from django.contrib.auth.hashers import check_password
from rest_framework import viewsets
from .serializers import NhaXeSerializer, TuyenXeSerializer, ChuyenXeSerializer, BookingSerializer, DeliverySerializer , ReviewSerializer
from rest_framework.decorators import api_view
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum

@csrf_exempt  # Bỏ qua việc kiểm tra CSRF cho ví dụ này (chỉ dùng cho môi trường phát triển)
def custom_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = CustomUser.objects.get(username=username)
            if check_password(password, user.password):  # Kiểm tra mật khẩu
                # Đăng nhập thành công, trả về thông tin của user
                return JsonResponse(
                    {
                        "id": user.id,
                        "username": user.username,
                        "role": user.role,
                        "is_active": user.is_active,
                        "is_staff": user.is_staff,
                        "is_superuser": user.is_superuser,
                    }
                )
            else:
                # Đăng nhập không thành công
                return JsonResponse({"error": "Invalid credentials"}, status=400)
        except CustomUser.DoesNotExist:
            # Không tìm thấy người dùng
            return JsonResponse({"error": "User not found"}, status=404)
    else:
        # Trả về lỗi nếu request không phải là POST
        return JsonResponse({"error": "Only POST requests are allowed"}, status=400)

@api_view(['GET'])
def get_nha_xe_by_user(request, user_id):
    try:
        user = CustomUser.objects.get(pk=user_id)
        nha_xe_list = NhaXe.objects.filter(user=user)
        serializer = NhaXeSerializer(nha_xe_list, many=True)
        return Response(serializer.data)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def get_tuyen_xe_by_nha_xe(request, nha_xe_id):
    try:
        # Lấy nhà xe dựa trên nha_xe_id
        nha_xe = NhaXe.objects.get(pk=nha_xe_id)
        
        # Lấy danh sách tuyến xe của nhà xe này
        tuyen_xe_list = TuyenXe.objects.filter(nha_xe=nha_xe)
        
        # Serialize và trả về dữ liệu
        serializer = TuyenXeSerializer(tuyen_xe_list, many=True)
        return Response(serializer.data)
    
    except NhaXe.DoesNotExist:
        return Response({"error": "Nhà xe not found"}, status=404)
    
    except Exception as e:
        return Response({'error': str(e)}, status=500)
@api_view(['GET'])
def get_booking_by_user(request, user_id):
    try:
        user = CustomUser.objects.get(pk=user_id)
        booking_list = Booking.objects.filter(nguoi_dung=user)
        serializer = BookingSerializer(booking_list, many=True)
        return Response(serializer.data)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

class NhaXeViewSet(viewsets.ModelViewSet):
    queryset = NhaXe.objects.all()
    serializer_class = NhaXeSerializer

    @action(detail=True, methods=['get'])
    def doanh_thu_theo_thang(self, request, pk=None):
        try:
            nhaxe = self.get_object()
            year = request.query_params.get('year')
            month = request.query_params.get('month')

            tuyenxe_qs = TuyenXe.objects.filter(nha_xe=nhaxe)
            chuyenxe_qs = ChuyenXe.objects.filter(tuyen_xe__in=tuyenxe_qs, thoi_gian_khoi_hanh__year=year, thoi_gian_khoi_hanh__month=month)

            doanh_thu = chuyenxe_qs.aggregate(total_doanh_thu=Sum('gia_ve'))
            so_chuyen_xe = chuyenxe_qs.count()

            return Response({
                'year': year,
                'month': month,
                'doanh_thu': doanh_thu['total_doanh_thu'] or 0,
                'so_chuyen_xe': so_chuyen_xe
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class TuyenXeViewSet(viewsets.ModelViewSet):
    queryset = TuyenXe.objects.all()
    serializer_class = TuyenXeSerializer


class ChuyenXeViewSet(viewsets.ModelViewSet):
    queryset = ChuyenXe.objects.all()
    serializer_class = ChuyenXeSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer




@api_view(['GET'])
def get_all_nha_xe(request):
    nha_xe = NhaXe.objects.all()
    serializer = NhaXeSerializer(nha_xe, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_all_chuyen_xe(request):
    chuyen_xe = ChuyenXe.objects.all()
    serializer = ChuyenXeSerializer(chuyen_xe, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_all_tuyen_xe(request):
    tuyen_xe = TuyenXe.objects.all()
    serializer = TuyenXe(TuyenXe, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_all_booking(request):
    booking = Booking.objects.all()
    serializer = Booking(Booking, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_all_delivery(request):
    delivery = Delivery.objects.all()
    serializer = Delivery(Delivery, many=True)
    return Response(serializer.data)
