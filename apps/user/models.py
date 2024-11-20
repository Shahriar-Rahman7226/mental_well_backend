from django.contrib.auth.models import PermissionsMixin, BaseUserManager, AbstractBaseUser
from django.core.mail import send_mail
from django.db import models
# from address_app.models import HubModel
from abstract.base_model import CustomModel
from external.choice_tuple import UserRole, Gender


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, email=None):
        if not phone_number:
            raise ValueError('Phone number is required')
        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, email):
        user = self.create_user(phone_number, password, email)
        user.is_superuser = True
        user.is_staff = True
        user.user_role = UserRole[0][0]
        user.first_name = 'Shahriar'
        user.last_name = 'Rahman'
        user.save(using=self._db)
        return user


class UserModel(AbstractBaseUser, CustomModel, PermissionsMixin):
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    profile_pic = models.ImageField(upload_to="profile_pic/", blank=True, null=True)
    language = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True, choices=Gender)
    user_role = models.CharField(max_length=50, blank=True, null=True, choices=UserRole)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    two_factor = models.BooleanField(default=False)
    login_attempt = models.PositiveIntegerField(default=0, blank=True, null=True)

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        db_table = 'user_models'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name if self.full_name else ''} -- {self.phone_number if self.phone_number else ''} -- {self.user_role if self.user_role else ''}" 
