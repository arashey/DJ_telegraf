from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now, timedelta


# مدل کاربر سفارشی
class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, verbose_name="شماره تلفن")
    is_verified = models.BooleanField(default=False, verbose_name="تأیید شده")
    is_online = models.BooleanField(default=False) 
    last_activity = models.DateTimeField(null=True, blank=True)     

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def is_user_online(self):
        if self.last_activity:
            return self.last_activity >= now() - timedelta(minutes=5)
        return False


# مدل چت
class Chat(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    participants = models.ManyToManyField(User, related_name='chats')
    is_group = models.BooleanField(default=False)

    def __str__(self):
        return self.name if self.name else "چت خصوصی"

# مدل پیام
class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(null=True, blank=True)  # تاریخ آخرین ویرایش
    file = models.FileField(upload_to='message_files/', null=True, blank=True) 
    status = models.CharField(max_length=20, choices=[('sent', 'ارسال‌شده'), ('read', 'خوانده‌شده')], default='sent')


    def __str__(self):
        return f"{self.sender.username}: {self.text[:30]}"
    

class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to="profile_pics/", blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


