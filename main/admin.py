from django.contrib import admin
from .models import Client, Trainer, Owner, Discussion, DiscussionReply, Plan, Plan_Content, Rating, Payment, Appointment, wPlan, wPlan_Content, MembershipPlan, Enroll
# Register your models here.
def show_message(modeladmin, request, queryset):
    queryset.update(status='read')
    
admin.site.register(Client)
admin.site.register(Trainer)
admin.site.register(Owner)
admin.site.register(Discussion)
admin.site.register(DiscussionReply)
admin.site.register(Plan)
admin.site.register(Plan_Content)
admin.site.register(Rating)
admin.site.register(Payment)
admin.site.register(Appointment)
admin.site.register(wPlan)
admin.site.register(wPlan_Content)
admin.site.register(MembershipPlan)
admin.site.register(Enroll)