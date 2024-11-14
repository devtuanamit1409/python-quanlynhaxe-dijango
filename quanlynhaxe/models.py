from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator

ROLE_CHOICES = (
    ("user", "User"),
    ("admin", "Admin"),
    ("garage", "Garage"),
)


class CustomUserManager(BaseUserManager):
    def create_user(self, username, role, password=None):
        if not username:
            raise ValueError("Người dùng phải có tên đăng nhập")

        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)

        # Tạo NhaXe nếu vai trò là "garage"
        if role == "garage":
            NhaXe.objects.create(user=user)

        return user

    def create_superuser(self, username, role, password=None):
        user = self.create_user(
            username=username, role=role, password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES , default="user")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = CustomUserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["role"]

    def __str__(self):
        return self.username


class NhaXe(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE,null=True)
    ten = models.CharField(max_length=100)
    dia_chi = models.CharField(max_length=255)
    so_dien_thoai = models.CharField(max_length=20)
    email = models.EmailField()
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    da_xac_nhan = models.BooleanField(default=False)
    khoa = models.BooleanField(default=False)


class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    nhaxe = models.ForeignKey(NhaXe, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)


class TuyenXe(models.Model):
    nha_xe = models.ForeignKey(NhaXe, on_delete=models.CASCADE)
    diem_xuat_phat = models.CharField(max_length=255)
    diem_den = models.CharField(max_length=255)
    gia_ve = models.DecimalField(max_digits=10, decimal_places=2)
    thoi_gian_khoi_hanh = models.CharField(max_length=255)


class ChuyenXe(models.Model):
    tuyen_xe = models.ForeignKey(TuyenXe, on_delete=models.CASCADE)
    thoi_gian_khoi_hanh = models.DateTimeField()
    so_ve_con_lai = models.IntegerField(default=0)


class Booking(models.Model):
    chuyen_xe = models.ForeignKey(TuyenXe, on_delete=models.CASCADE)
    nguoi_dung = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ten_khach_hang = models.CharField(max_length=255 , null=True)
    ngay_dat = models.DateTimeField(auto_now_add=True)
    phuong_thuc_thanh_toan = models.CharField(max_length=100)
    da_thanh_toan = models.BooleanField(default=False)


class Delivery(models.Model):
    nhaxe = models.ForeignKey(NhaXe, on_delete=models.CASCADE)
    ho_ten_nguoi_gui = models.CharField(max_length=100)
    so_dien_thoai_nguoi_gui = models.CharField(max_length=20)
    email_nguoi_gui = models.EmailField()
    ho_ten_nguoi_nhan = models.CharField(max_length=100)
    so_dien_thoai_nguoi_nhan = models.CharField(max_length=20)
    email_nguoi_nhan = models.EmailField()
    thoi_gian_gui = models.DateTimeField()
    thoi_gian_nhan = models.DateTimeField(null=True, blank=True)
    da_gui_email = models.BooleanField(default=False)