from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


# 유저를 생성하는 매니저 클래스
class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(
        self,
        email,
        name,
        password,
        sogang_mail,
        student_number,
        first_major,
        **extra_fields,
    ):
        if not email:
            raise ValueError("must have user email(ID)")
        if not name:
            raise ValueError("must have user name")
        if not password:
            raise ValueError("must have user password")
        if not sogang_mail:
            raise ValueError("must have sogang_mail")
        if not student_number:
            raise ValueError("must have student_number")
        if not first_major:
            raise ValueError("must have first_major")

        email = self.normalize_email(email)
        sogang_mail = self.normalize_email(sogang_mail)

        user = self.model(
            email=email,
            name=name,
            sogang_mail=sogang_mail,
            student_number=student_number,
            first_major=first_major,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password, **extra_fields):
        extra_fields.setdefault("sogang_mail", "default@sogang.ac.kr")
        extra_fields.setdefault("student_number", "00000000")
        extra_fields.setdefault("first_major", "None")

        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            password=password,
            **extra_fields,
        )

        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

# 재정의한 User
class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    email = models.EmailField(max_length=100, unique=True)
    name = models.CharField(max_length=30, unique=True)  # 사용자의 이름 validators=[validate_unique_nickname]
    sogang_mail = models.CharField(max_length=100, unique=True)  # 서강 이메일
    student_number = models.CharField(max_length=100, unique=True)  # 학번 ex) 20201111
    first_major = models.CharField(max_length=50)  # 본전공
    second_major = models.CharField(max_length=50, null=True, blank=True)  # 2전공
    third_major = models.CharField(max_length=50, null=True, blank=True)  # 3전공
    is_operator = models.BooleanField(default=False)  # 기본값은 '학생 유저'
    # photo = models.ImageField()   # 학생의 사진

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"  # 기본적으로 username으로 사용할 필드를 email 필드로 수정
    REQUIRED_FIELDS = ["name"]  # User 객체 생성할 때 필수적으로 제공해야 하는 필드 리스트.

    def __str__(self):
        return f"{self.name} | {self.student_number} | {self.first_major}"
    

    
