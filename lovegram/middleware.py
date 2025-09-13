# chat/middleware.py
from django.utils.timezone import now
from django.utils.deprecation import MiddlewareMixin
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


    

