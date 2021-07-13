from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Subscriber
from .forms import SubscriberForm
import random
from django.core.mail import send_mail
from .forms import NewsForm

# Create your views here.
def random_digits():
    return "%0.12d" % random.randint(0, 999999999999)

# Create your views here.
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def new(request):
    if request.method == 'POST':
        sub = Subscriber(email=request.POST['email'], conf_num=random_digits())
        sub.save()
        html_content = 'Thank you for signing up for my email newsletter! \
                        Please complete the process by \
                         <a href="{}?email={}&conf_num={}"> clicking here to \
                         confirm your registration</a>.'.format(request.build_absolute_uri('/confirm/'),sub.email,sub.conf_num)

        response = send_mail(
            'Newsletter Confirmation',
            html_content,
            settings.FROM_EMAIL,
            [sub.email,],
            fail_silently=False,
        )
        return render(request, 'index.html', {'email': sub.email, 'action': 'added', 'form': SubscriberForm()})
    else:
        return render(request, 'index.html', {'form': SubscriberForm()})

def confirm(request):
    sub = Subscriber.objects.get(email=request.GET['email'])
    if sub.conf_num == request.GET['conf_num']:
        sub.confirmed = True
        sub.save()
        return render(request, 'index.html', {'email': sub.email, 'action': 'confirmed'})
    else:
        return render(request, 'index.html', {'email': sub.email, 'action': 'denied'})

def delete(request):
    sub = Subscriber.objects.get(email=request.GET['email'])
    if sub.conf_num == request.GET['conf_num']:
        sub.delete()
        return render(request, 'index.html', {'email': sub.email, 'action': 'unsubscribed'})
    else:
        return render(request, 'index.html', {'email': sub.email, 'action': 'denied'})

def news(request):
    context={}
    subscribers = Subscriber.objects.filter(confirmed=True)
    form = NewsForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
    context['form'] = form
    for sub in subscribers:
        html_content =  '<br><a href="{}?email={}&conf_num={}">Unsubscribe</a>.'.format(request.build_absolute_uri('/delete/'),
                                                                           sub.email,
                                                                           sub.conf_num)
        send_mail(
             'new newsletter',
             html_content,
             settings.FROM_EMAIL,
             [sub.email, ],
             fail_silently=False,
         )

    return render(request,'news.html',context)