from django.contrib import admin

# Register your models here.
from myapp.models import Subscriber, Newsletter


def send_newsletter(modeladmin, request, queryset):
    for newsletter in queryset:
        newsletter.send(request)
send_newsletter.short_description = "Send selected Newsletters to all subscribers"

class NewsletterAdmin(admin.ModelAdmin):
    actions = [send_newsletter]

# Register your models here.
admin.site.register(Subscriber)
admin.site.register(Newsletter, NewsletterAdmin)