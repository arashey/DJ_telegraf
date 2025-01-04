# chat/middleware.py
from django.utils.timezone import now
from django.utils.deprecation import MiddlewareMixin

"""class UpdateLastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # اگر کاربر وارد شده باشد، زمان آخرین فعالیت‌اش به روز می‌شود
        if request.user.is_authenticated:
            print(f"Updating last_activity for user: {request.user.username}")
            request.user.last_activity = now()  # زمان کنونی را برای last_activity ذخیره می‌کند
            request.user.save(update_fields=['last_activity'])  # فقط فیلد last_activity را به روز می‌کند
        return self.get_response(request)"""
from datetime import timedelta
from django.utils.timezone import now
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model

class UpdateLastActivityMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user = request.user
        if user.is_authenticated:
            # به روز رسانی زمان آخرین فعالیت
            user.last_activity = now()
            user.save()


    

