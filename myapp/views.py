from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from .models import Subscriber
from .forms import SubscriberForm
import random
from django.core.mail import send_mail, EmailMessage
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
        useremail =request.POST['email']
        if Subscriber.objects.filter(email=useremail).exists():
            messages.error(request, 'The Email is already used')
            return redirect('index')
        else:

            sub = Subscriber(email=useremail, conf_num=random_digits())
            sub.save()
            messages.success(request, 'Mail Send Sucessfully Check and Confirm it ')
            contextpaart = {
                'email': useremail,
                'conf_num': sub.conf_num,
            }
            message = get_template('mailtemplate.html').render(contextpaart)
            msg = EmailMessage(
                'Newsletter Subscription',
                message,
                'ftalamarlapremanath@gmail.com',
                ['talamarlapremanath143@gmail.com'],
            )
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send()
            return render(request, 'index.html', {'email': sub.email, 'action': 'added', 'form': SubscriberForm()})
    else:
        return render(request, 'index.html', {'form': SubscriberForm()})


def confirm(request):
    sub = get_object_or_404(Subscriber,email=request.GET['email'])
    if sub.conf_num == request.GET['conf_num']:
        sub.confirmed = True
        sub.save()
        messages.success(request, 'Mail Confirmed Successfully ')

        return render(request, 'index.html', {'email': sub.email, 'action': 'confirmed'})
    else:
        messages.warning(request, 'Mail Denied Try Again ')

        return render(request, 'index.html', {'email': sub.email, 'action': 'denied'})

def delete(request):
    sub = get_object_or_404(Subscriber,email=request.GET['email'])
    if sub.conf_num == request.GET['conf_num']:
        sub.delete()
        messages.info(request, 'Mail Deleted Successfully ')

        return render(request, 'index.html', {'email': sub.email, 'action': 'unsubscribed'})
    else:
        messages.warning(request, 'Mail Denied Try Again ')

        return render(request, 'index.html', {'email': sub.email, 'action': 'denied'})

def news(request):
    context={}
    subscribers = Subscriber.objects.filter(confirmed=True)
    form = NewsForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
    context['form'] = form
    for sub in subscribers:
        contextpaart = {
            'email': sub.email,
            'conf_num': sub.conf_num,
        }
        message = get_template('mailtemplate2.html').render(contextpaart)
        msg = EmailMessage(
            'News letter - New Post ',
            message,
             settings.FROM_EMAIL,
              [sub.email, ],
        )
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()
        # html_content =  '<br><a href="{}?email={}&conf_num={}">Unsubscribe</a>.'.format(request.build_absolute_uri('/delete/'),
        #                                                                    sub.email,
        #                                                                    sub.conf_num)
        # send_mail(
        #      'new newsletter',
        #      html_content,
        #      settings.FROM_EMAIL,
        #      [sub.email, ],
        #      fail_silently=False,
        #  )


    return render(request,'news.html',context)