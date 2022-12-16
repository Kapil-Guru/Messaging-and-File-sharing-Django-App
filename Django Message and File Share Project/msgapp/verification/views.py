from django.shortcuts import render, redirect
from django.views import View
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
import pyotp
from .models import App_Users
import base64
from django.http import HttpResponse
from sendsms.message import SmsMessage
# Create your views here.

class GenerateKey:
    def returnValue(self, phone):
        return str(phone) + str(datetime.date(datetime.now())) + "Some Random Secret Key"

class Startup(View):
    def get(self, request):
        return render(request, 'verification/index.html', {})
    def post(self, request):
        request.session['entered_phone_number'] = request.POST['phone_number']
        url = reverse('verification:verify')
        if (request.session.get('viewed', False)):
            del request.session['viewed']
        return redirect(url)

class Verify(View):
    def get(self, request):
        viewed_bool = request.session.get('viewed', False)
        if viewed_bool:
            resend_message = "OTP has been resent"
        else:
            request.session['viewed'] = True
            resend_message = None
        phone_number = request.session['entered_phone_number']
        try:
            user = App_Users.objects.get(mobile = phone_number)
            user.counter += 1
            counter = user.counter
            user.save()
            keygen = GenerateKey()
            key = base64.b32encode(keygen.returnValue(phone_number).encode())
            OTP = pyotp.HOTP(key)  # HOTP Model for OTP is created
            generated_otp = OTP.at(counter)
            print(generated_otp)
            message = SmsMessage(body=generated_otp, from_phone='+91984023788', to=[user.mobile])
            message.send()
        except ObjectDoesNotExist:
            counter = 1
        return render(request,'verification/verify.html',{'error_message': None, 'resend_message': resend_message})

    def post(self, request):
        user_entered_otp = request.POST['otp']
        phone_number = request.session['entered_phone_number']
        try:
            user = App_Users.objects.get(mobile = phone_number)
            counter = user.counter

        except ObjectDoesNotExist:
            user = None
            counter = 1
        keygen = GenerateKey()
        key = base64.b32encode(keygen.returnValue(phone_number).encode())  # Key is generated
        OTP = pyotp.HOTP(key)  # HOTP Model for OTP is created
        print(OTP.at(counter))
        if OTP.verify(user_entered_otp, counter):
            if user:
                request.session['is_authenticated'] = True
                request.session['phone_number'] = user.mobile
                request.session['name'] = user.name
                request.session['has_name'] = True
                return redirect(reverse('home:search'))
            else:
                request.session['has_name'] = False
                url = reverse('verification:name')
                return redirect(url)
        
        return render(request,'verification/verify.html',{'error_message': 'Invalid OTP'})

class NameView(View):
    def get(self, request):
        print(request.session['entered_phone_number'])
        return render(request,'verification/name.html',{})
    def post(self, request):
        if request.session['has_name']:
            db_obj = App_Users.get(mobile = request.user.phone_number, name = request.user.name)
            db_obj.name = request.POST['name']
            db_obj.save()
            request.user.name = request.POST['name'];
        else:
            name = request.POST['name']
            db_obj = App_Users(mobile = request.session['entered_phone_number'], name = name, counter = 1)
            db_obj.save()
            request.session['phone_number'] = request.session['entered_phone_number']
            request.session['name'] = name
            request.session['is_authenticated'] = True
            request.session['has_name'] = True
        return redirect(reverse('home:search'))
