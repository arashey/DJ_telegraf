from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from .models import User, Chat, Message, Notification,Profile
from django.contrib.auth.decorators import login_required
from .forms import ChatForm, MessageForm, ProfileForm
from django.utils import timezone
from django.utils.timezone import now, timedelta
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def register(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # بررسی فیلدهای خالی
        if not phone_number or not username or not password:
            return render(request, 'register.html', {'error': "تمام فیلدها باید پر شوند."})

        # بررسی تکراری بودن شماره تلفن
        if User.objects.filter(phone_number=phone_number).exists():
            return render(request, 'register.html', {'error': "این شماره تلفن قبلاً ثبت شده است."})

        # بررسی تکراری بودن نام کاربری
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': "این نام کاربری قبلاً ثبت شده است."})

        # ایجاد کاربر جدید
        user = User.objects.create(
            username=username,
            phone_number=phone_number,
            password=make_password(password),
        )

        # ارسال کد تایید یا هر فرآیند دیگر (مثل ارسال ایمیل یا پیامک)
        # ارسال کد تایید به کاربر

        # ارجاع به صفحه تایید
        return redirect('verify')

    return render(request, 'register.html')



# ویوی تأیید کد
def verify(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        verification_code = request.POST.get('verification_code')

        user = User.objects.filter(phone_number=phone_number).first()
        if user and verification_code == "1234":  # این مقدار باید با مقدار واقعی جایگزین شود
            user.is_verified = True
            user.save()
            login(request, user)
            return redirect('chat_list')

        return render(request, 'verify.html', {'error': "کد تأیید اشتباه است."})

    return render(request, 'verify.html')


# ویوی ورود
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            user.is_online = True  # تنظیم وضعیت آنلاین
            user.save()
            login(request, user)
            return redirect('chat_list')

        return render(request, 'login.html', {'error': "نام کاربری یا رمز عبور اشتباه است."})

    return render(request, 'login.html')

def logout_view(request):
    user = request.user
    user.is_online = False  # تنظیم وضعیت آفلاین
    user.save()
    logout(request)
    return redirect('login')


def chat_list(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # به‌روزرسانی فعالیت آخر کاربر
    request.user.last_activity = now()
    request.user.save()

    # دریافت چت‌هایی که کاربر در آن عضو است
    chats = Chat.objects.filter(participants=request.user).prefetch_related('messages')

    # پیدا کردن آخرین پیام هر چت و افزودن آن به context
    chats = chats.annotate(last_message_time=Max('messages__timestamp'))

    # تعریف زمان برای تشخیص آنلاین بودن کاربران (برای مثال: 5 دقیقه اخیر)
    online_threshold = now() - timedelta(minutes=5)

    # افزودن کاربر مقابل و وضعیت آنلاین بودن آن‌ها به چت‌های خصوصی
    for chat in chats:
        if not chat.is_group:
            chat.other_participant = chat.participants.exclude(id=request.user.id).first()
            if chat.other_participant:
                chat.other_participant.is_online = chat.other_participant.last_activity and chat.other_participant.last_activity > online_threshold

    # اگر درخواست POST باشد، چت جدید ایجاد شود
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.is_group = False
            chat.save()
            chat.participants.add(request.user)
            return redirect('chat_list')

    else:
        form = ChatForm()

    context = {
        'chats': chats,
        'form': form,
    }

    return render(request, 'chat_list.html', context)



from django.db.models import Max

@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    # پیدا کردن کاربری که در حال چت کردن با او هستیم (به جز کاربر فعلی)
    chat_partner = chat.participants.exclude(id=request.user.id).first()

    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)  # اضافه کردن `request.FILES` برای دریافت فایل‌ها
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.sender = request.user
            message.status = 'sent'  # وضعیت پیام به "ارسال‌شده" تغییر می‌کند
            message.save()

            # ایجاد اعلان برای اعضای چت (غیر از ارسال‌کننده)
            for participant in chat.participants.all():
                if participant != request.user:
                    Notification.objects.create(
                        user=participant,
                        message=f"پیام جدید در چت '{chat.name}'",
                        timestamp=message.timestamp  # اضافه کردن زمان ارسال پیام به اعلان
                    )

            return redirect('chat_detail', chat_id=chat.id)  # پس از ارسال پیام دوباره به همین صفحه برگردیم
    else:
        form = MessageForm()

    messages = chat.messages.all()  # دریافت پیام‌های چت

    # تغییر وضعیت پیام‌ها به "خوانده‌شده" برای کاربر فعلی
    for message in messages:
        if message.status == 'sent' and message.sender != request.user:
            message.status = 'read'
            message.save()

    notifications = request.user.notifications.filter(is_read=False)

    context = {
        'chat': chat,
        'messages': messages,
        'form': form,
        'notifications': notifications,
        'chat_partner': chat_partner  # اضافه کردن اطلاعات کاربر چت‌شونده
    }

    return render(request, 'chat_detail.html', context)




@login_required
def find_user_and_create_chat(request):
    if request.method == "POST":
        username = request.POST.get("username")
        recipient = User.objects.filter(username=username).first()

        if not recipient:
            return render(request, "find_user.html", {"error": "کاربر موردنظر یافت نشد."})

        # بررسی وجود چت خصوصی بین دو کاربر
        chat = Chat.objects.filter(is_group=False, participants=request.user).filter(participants=recipient).first()

        if not chat:
            # اگر چت وجود ندارد، ایجاد شود
            chat = Chat.objects.create(is_group=False)
            chat.participants.add(request.user, recipient)

        return redirect("chat_detail", chat_id=chat.id)

    return render(request, "find_user.html")



@login_required
def mark_notifications_as_read(request):
    # تمام اعلان‌های کاربر را به عنوان خوانده شده علامت‌گذاری می‌کنیم
    request.user.notifications.update(is_read=True)
    return redirect('chat_list')  # یا هر صفحه دیگری که می‌خواهید




@login_required
def create_chat(request):
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.save()
            
            # اضافه کردن کاربر فعلی به چت
            chat.participants.add(request.user)
            
            # اگر در فرم انتخاب شده بودند، کاربران دیگر را هم به چت اضافه کن
            participants = form.cleaned_data['participants']
            for participant in participants:
                chat.participants.add(participant)
            
            return redirect('chat_list')  # به لیست چت‌ها برگردیم
    else:
        form = ChatForm()

    return render(request, 'create_chat.html', {'form': form})



@login_required
def edit_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    # فقط کاربر فرستنده پیام می‌تواند آن را ویرایش کند
    if message.sender != request.user:
        return HttpResponse("شما اجازه ویرایش این پیام را ندارید.", status=403)

    if request.method == 'POST':
        new_text = request.POST.get('text')  # نام درست فیلد
        if new_text:
            message.text = new_text
            message.last_edited = timezone.now()  # تاریخ ویرایش را بروزرسانی می‌کنیم
            message.save()
            return redirect('chat_detail', chat_id=message.chat.id)  # بازگشت به صفحه چت

    return render(request, 'edit_message.html', {'message': message})


@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    # فقط کاربر فرستنده پیام می‌تواند آن را حذف کند
    if message.sender != request.user:
        return HttpResponse("شما اجازه حذف این پیام را ندارید.", status=403)

    chat_id = message.chat.id
    message.delete()  # حذف پیام
    return redirect('chat_detail', chat_id=chat_id)  # بازگشت به صفحه چت


@login_required
def add_participant(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    
    if not chat.is_group:
        return HttpResponse("این چت یک چت گروهی نیست.", status=400)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        user_to_add = get_object_or_404(User, username=username)
        
        if user_to_add not in chat.participants.all():
            chat.participants.add(user_to_add)
            chat.save()
            return redirect('chat_detail', chat_id=chat.id)
        else:
            return HttpResponse("این کاربر قبلاً عضو چت است.", status=400)
    
    return render(request, 'add_participant.html', {'chat': chat})


@login_required
def create_group(request):
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            # ایجاد گروه جدید
            group = form.save(commit=False)
            group.is_group = True  # تعیین اینکه این چت یک گروه است
            group.save()

            # اضافه کردن اعضای گروه
            member_ids = request.POST.getlist('members')  # لیست ID اعضای گروه
            members = User.objects.filter(id__in=member_ids)  # گرفتن کاربران انتخاب‌شده
            group.participants.add(*members)  # اضافه کردن اعضای گروه به صورت دسته‌ای

            # اضافه کردن کاربر فعلی به گروه
            group.participants.add(request.user)

            return redirect('chat_list')  # بازگشت به لیست چت‌ها
    else:
        form = ChatForm()

    # نمایش کاربران برای انتخاب اعضای گروه
    users = User.objects.exclude(id=request.user.id)  # لیست کاربران غیر از خود کاربر

    return render(request, 'create_group.html', {'form': form, 'users': users})



@login_required
def create_or_edit_profile(request):
    # پیدا کردن یا ایجاد پروفایل
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile_detail", user_id=request.user.id)
    else:
        form = ProfileForm(instance=profile)

    return render(request, "create_edit_profile.html", {"form": form})



def profile_detail(request, user_id):
    try:
        profile = Profile.objects.get(user__id=user_id)
    except Profile.DoesNotExist:
        profile = None  # اگر پروفایلی پیدا نشد، پروفایل را None قرار می‌دهیم

    return render(request, 'profile_detail.html', {'profile': profile})



from django.shortcuts import render, get_object_or_404, redirect
from .models import Chat

def delete_chat(request, chat_id):
    # دریافت چت از دیتابیس
    chat = get_object_or_404(Chat, id=chat_id)
    
    # بررسی اینکه کاربر جاری عضوی از چت باشد یا خیر
    if chat.user != request.user:
        return redirect('chats')  # در صورتی که کاربر حق حذف نداشته باشد

    if request.method == 'POST':
        # حذف چت
        chat.delete()
        return redirect('chats')  # هدایت به صفحه چت‌ها بعد از حذف
    else:
        # در صورت درخواست غیر POST
        return redirect('chats')
    


"""@csrf_exempt
def update_last_activity(request):
    if request.user.is_authenticated:
        request.user.last_activity = now()
        request.user.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=403)"""
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils.timezone import now
from datetime import timedelta
from .models import User

@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    user.last_activity = now()  # به روز رسانی زمان آخرین فعالیت
    user.is_online = True  # وضعیت آنلاین
    user.save()

@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    user.last_activity = now()  # به روز رسانی زمان آخرین فعالیت
    user.is_online = False  # وضعیت آفلاین
    user.save()


@login_required
def delete_avatar(request):
    user = request.user
    if user.profile and user.profile.avatar:
        user.profile.avatar.delete()  # حذف عکس پروفایل
    return redirect('profile_edit')













