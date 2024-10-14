from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    ROLE_CHOICES = [
        ('P', 'Patient'),
        ('H', 'Healthcare Worker'),
    ]
    
    user_id = models.AutoField(primary_key=True)  # 自動增長的用戶ID
    username = models.CharField(max_length=150, unique=True)  # 帳號
    password = models.CharField(max_length=128)  # 密碼
    date_of_birth = models.DateField(null=True, blank=True)  # 生日
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)  # 性別
    role = models.CharField(max_length=1, choices=ROLE_CHOICES)  # 身分 (患者/醫護人員)
    notes = models.TextField(null=True, blank=True)  # 備註
    is_active = models.BooleanField(default=True)  # 註銷狀態
    deactivated_at = models.DateField(null=True, blank=True)  # 註銷日期

    USERNAME_FIELD = 'username'  # 使用者登入時的帳號欄位
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username


class GaitParameter(models.Model):
    gait_parameter_id = models.AutoField(primary_key=True)
    measurement_time = models.DateTimeField(auto_now_add=True)
    video_name = models.CharField(max_length=255)  # 影片名稱，應為字符串
    json_name = models.CharField(max_length=255)  # JSON 文件名，應為字符串
    user_name = models.CharField(max_length=255)  # 使用者名稱，應為字符串
    average_step_time = models.FloatField()  # 平均步伐用時長度
    average_stride_length = models.FloatField()  # 平均步伐長度
    movement_speed = models.FloatField()  # 移動速度
    stance = models.FloatField()  # 每一步的步幅長度
    health_value = models.FloatField()  # 健康指數
    each_of_step_length = models.FloatField()  # 每一步的步幅長度
    y_values = models.JSONField()  # 步態數據中右腳Y軸的數值
    left_y_value = models.JSONField()  # 步態數據中左腳Y軸的數值

    def __str__(self):
        return f"GaitParameter {self.gait_parameter_id}"


class HistoryRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # 這裡與使用者資料表的user_id關聯
    gait_parameter = models.ForeignKey(GaitParameter, on_delete=models.CASCADE)  # 與步態參數關聯
    issue_id = models.IntegerField()  # 假設為整數ID
    record_time = models.DateTimeField(auto_now_add=True)  # 紀錄時間

    def __str__(self):
        return f"HistoryRecord {self.record_id}"


class IssueAndSuggestion(models.Model):
    issue_id = models.AutoField(primary_key=True)
    issue_name = models.CharField(max_length=255)  # 問題名稱
    record = models.ForeignKey(HistoryRecord, on_delete=models.CASCADE)  # 與紀錄關聯
    suggestion = models.TextField()  # 建議

    def __str__(self):
        return f"IssueAndSuggestion {self.issue_id}"
