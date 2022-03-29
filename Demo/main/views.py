from urllib.error import HTTPError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.views.generic import UpdateView

from .models import Waitlist, Message
from .forms import WaitlistModelForm

from twilio.rest import Client

import datetime
import pytz

# Create your views here.
def send_message(num, text, request):
    # Your Account SID from twilio.com/console
    account_sid = str(settings.TWILIO_ACCOUNT_SID)
    # Your Auth Token from twilio.com/console
    auth_token = str(settings.TWILIO_AUTH_TOKEN)
    acc_num = settings.TWILIO_NUMBER
    client = Client(account_sid, auth_token)
    try:
        message = client.messages.create(
            to=num,
            from_=acc_num,
            body=text
        )
        messages.success(request, 'Message sent')
        print(message.sid)
        return True
    except Exception:
        try:
            validation_request = client.validation_requests.create(
                friendly_name='A new Customer',
                phone_number=num
            )
            num = validation_request.phone_number
            message = client.messages.create(
                to=num,
                from_=acc_num,
                body=text
            )
            messages.success(request, 'Message sent')
            print(message.sid)
            return True
        except Exception as ex:
            if HTTPError:
                messages.error(request, "Cannot send text at this moment.")
                print("Chhange twilio sid and auth or the numb")
            else:
                messages.error(request, 'An error occured')
                print(ex)
            return redirect('../')

timezones = []
for tz in pytz.all_timezones:
    timezones.append(tz)

def time_to_utc(naive, timezone):
    local = pytz.timezone(timezone)
    local_dt = local.localize(naive, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    return utc_dt

def utc_to_time(naive, timezone):
    return naive.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(timezone))

def waitlist_create(request):
    form = WaitlistModelForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        UTC = pytz.utc
        dt = datetime.datetime.now(UTC)
        now = dt + datetime.timedelta(hours=-4)
        obj.checkin = now
        obj.save()
        waitlist = form.cleaned_data.get('party_name')
        form = WaitlistModelForm()
        messages.success(request, f"New reservation created for {waitlist}")
        return redirect('../waitlist')
    else:
        for msg in form.errors:
            messages.error(request, f'{msg}: {form.errors[msg]}')
    context={
        'form' : form,
    }
    return render(request, 'main/waitlist_create.html', context)

def waitlist_view(request):
    waitlist = Waitlist.objects.filter(user=request.user)
    if request.method=='POST':
        id_num = request.POST.get('message-id', None)
        id_num2 = request.POST.get('message-id2', None)
        id_upd = request.POST.get('update-id', None)
        id_seated = request.POST.get('seated-id', None)
        id_canncelled = request.POST.get('cancel-id', None)
        if id_num:
            obj = Waitlist.objects.get(id=id_num)
            if obj.state == False:
                num = str(obj.phone)
                txt = Message.objects.filter(user=request.user).get(message_number=1)
                print(txt.message_number)
                body = txt.message_text
                state = send_message(num, body,request)
                if state == True:
                    obj.state = True
                    obj.save()
                    obj.time_message_sent = datetime.now()
            else:
                messages.error(request,'First message has already been sent')
        elif id_num2:
            obj = Waitlist.objects.get(id=id_num2)
            if obj.state==True:
                num = str(obj.phone)
                txt = Message.objects.filter(user=request.user).get(message_number=2)
                print(txt.message_number)
                body = txt.message_text
                send_message(num, body, request)
                obj.time_message_sent = datetime.now()
                messages.success(request, "Message successfully")
            else:
                messages.error(request, "Send first message first")
        elif id_upd:
            obj = Waitlist.objects.get(id=id_upd)
            return redirect(f'../waitlist_update/{obj.id}')
        elif id_seated:
            obj = Waitlist.objects.get(id=id_seated)
            obj.checked_in = True
            obj.save()
            obj.delete()
            messages.success(request, 'Customer has been attended to.')
            return redirect('../waitlist')
        elif id_canncelled:
            obj = Waitlist.objects.get(id=id_canncelled)
            obj.cancelled = True
            obj.save()
            obj.delete()
            messages.success(request, "Customer has cancelled reservation successfully.")
            return redirect('../waitlist')
    context = {
        'object':waitlist,
    }
    return render(request, 'main/waitlist.html', context)

class WaitlistUpdateView(UpdateView):
    form_class = WaitlistModelForm
    template_name = 'main/waitlist_update.html'

    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(Waitlist, id=id)

    def form_valid(self,form):
        print(form.cleaned_data)
        form.save()
        messages.success(self.request, 'Waitlist updated')
        return redirect('../waitlist')

def message_view(request):
    texts = Message.objects.filter(user=request.user)
    one = texts[0]
    two = texts[1]
    if request.user.tz != "":
        timez = request.user.tz
    else:
        timez = "US/Central"


    if request.method =='POST':
        one_text = request.POST.get('one_text')
        two_text = request.POST.get('two_text')
        tz = request.POST.get('timezone')
        one_text = " ".join(one_text.split())
        two_text = " ".join(two_text.split())
        one.message_text = one_text
        two.message_text = two_text
        one.save()
        two.save()
        request.user.tz = tz
        request.user.save()
        return redirect("/settings")

    context = {
        'one': one,
        'two': two,
        'timezones': timezones,
        'timez':timez,
    }
    return render(request, 'main/settings.html', context)

def home(request):
    return render(request, 'main/home.html', {})