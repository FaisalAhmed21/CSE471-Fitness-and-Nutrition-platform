from django.db import models
from django.contrib.auth import get_user_model
import uuid
from django.utils import timezone
from django.utils.timezone import now

User = get_user_model()

class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    client_usrname = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, default="")
    age = models.CharField(max_length=200, blank=True, default="")
    weight = models.CharField(max_length=200, blank=True, default="")
    height = models.CharField(max_length=200, blank=True, default="")
    bio = models.CharField(max_length=400, blank=True, default="")
    gender = models.CharField(max_length=200, blank=True, default="")
    achievement = models.CharField(max_length=200, blank=True, default="")
    personalTrainer = models.CharField(max_length=200, blank=True, default="")

    def __str__(self):
        return self.client_usrname


class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    trainer_tag = models.CharField(max_length=10, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    joined_date = models.DateField(default=timezone.now, blank=True)
    bio = models.CharField(max_length=400, blank=True, null=True)
    gender = models.CharField(max_length=200, blank=True, null=True, default="Choose option")
    achievement = models.CharField(max_length=200, blank=True, null=True, default="none")
    time1 = models.CharField(max_length=200, blank=True, null=True)
    time2 = models.CharField(max_length=200, blank=True, null=True)
    time3 = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.trainer_tag


class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    owner_usrname = models.CharField(max_length=10, unique=True, default="head")
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Discussion(models.Model):
    dnumber = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=200, default="Untitled")
    statement = models.TextField()
    datetime = models.DateTimeField(default=timezone.now, blank=True, null=True)
    posted_by = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="discussions_posted", blank=True, null=True)
    answer_by = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="discussions_answered", blank=True, null=True)
    resolved_by = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name="discussions_resolved", blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True, default="pending")
    views_count = models.IntegerField(default=0)
    upvotes = models.IntegerField(default=0)
    upvoted_by = models.ManyToManyField(User, related_name="upvoted_discussions", blank=True)
    viewed_by = models.ManyToManyField(User, related_name="viewed_discussions", blank=True)

    def __str__(self):
        return f"{self.posted_by} -> Discussion {self.dnumber}"
    
    def has_upvoted(self, user):
        """Check if user has already upvoted this discussion"""
        return self.upvoted_by.filter(id=user.id).exists()
    
    def has_viewed(self, user):
        """Check if user has already viewed this discussion"""
        return self.viewed_by.filter(id=user.id).exists()
    
    class Meta:
        ordering = ['-datetime']


class DiscussionReply(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name="replies")
    reply_text = models.TextField()
    replied_by_client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="client_replies", blank=True, null=True)
    replied_by_trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name="trainer_replies", blank=True, null=True)
    datetime = models.DateTimeField(default=timezone.now)
    is_solution = models.BooleanField(default=False)

    def __str__(self):
        replier = self.replied_by_client or self.replied_by_trainer
        return f"Reply to {self.discussion.dnumber} by {replier}"
    
    class Meta:
        ordering = ['datetime']


class Plan(models.Model):
    plan_id = models.CharField(max_length=100, default=uuid.uuid4, unique=True)
    plan_name = models.CharField(max_length=100, unique=True)
    plan_description = models.TextField(max_length=1000, blank=True, null=True)
    plan_point = models.IntegerField()
    plan_trainer = models.CharField(max_length=100, blank=True, null=True)
    plan_topic = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.plan_name)


class Plan_Content(models.Model):
    plan_content_id = models.CharField(max_length=100, default=uuid.uuid4, unique=True)
    plan_id = models.ForeignKey(Plan, on_delete=models.CASCADE)
    plan_content_tag = models.TextField(max_length=5000, blank=True, null=True)
    plan_content_description = models.TextField(max_length=5000, blank=True, null=True)
    content_img = models.ImageField(upload_to='images/', blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    upload_by = models.ForeignKey(Trainer, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.plan_content_tag)


class Rating(models.Model):
    rnumber = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=100, blank=True, null=True)
    statement = models.TextField()
    datetime = models.DateTimeField(default=timezone.now, blank=True, null=True)
    posted_by = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="ratings_posted", blank=True, null=True)
    about = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True, default="none")

    def __str__(self):
        return f"{self.posted_by} -> Rating {self.rnumber}"


class Appointment(models.Model):
    anumber = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=100, blank=True, null=True)
    statement = models.TextField()
    datetime = models.DateTimeField(default=timezone.now, blank=True, null=True)
    posted_by = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name="appointments_posted", blank=True, null=True)
    booked_by = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="appointments_booked", blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True, default="Available")

    def __str__(self):
        return f"{self.posted_by} -> Appointment {self.anumber}"


class Payment(models.Model):
    staff_username = models.OneToOneField(Trainer, on_delete=models.CASCADE)
    payment_date = models.DateField()
    payment_amount = models.IntegerField()

    def __str__(self):
        return str(self.staff_username)
    
    
class BMIRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    height_in_meters = models.FloatField()
    weight_in_kg = models.FloatField()
    bmi_value = models.FloatField()
    comment = models.CharField(max_length=50)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.bmi_value}"
    

class wPlan(models.Model):
    wplan_id = models.CharField(max_length=100, default=uuid.uuid4, unique=True)
    wplan_name = models.CharField(max_length=100, unique=True)
    wplan_description = models.TextField(max_length=2000, blank=True, null=True)
    wplan_point = models.IntegerField()
    wplan_trainer = models.CharField(max_length=100, blank=True, null=True)
    wplan_topic = models.CharField(max_length=100, blank=True, null=True)
    wplan_image = models.ImageField(upload_to='wplans/', blank=True, null=True)  # Add this field

    def __str__(self):
        return str(self.wplan_name)


class wPlan_Content(models.Model):
    wplan_content_id = models.CharField(max_length=100, default=uuid.uuid4, unique=True)
    wplan_id = models.ForeignKey(wPlan, on_delete=models.CASCADE)
    wplan_content_tag = models.TextField(max_length=5000, blank=True, null=True)
    wplan_content_description = models.TextField(max_length=5000, blank=True, null=True)
    wcontent_img = models.ImageField(upload_to='images/', blank=True, null=True)
    wcontent_count = models.ImageField(upload_to='countdown/', blank=True, null=True)
    wdatetime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    wupload_by = models.ForeignKey(Trainer, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.wplan_content_tag)
    

class Enroll(models.Model):      
    client_usrname = models.CharField(max_length=10, unique=True)
    Email=models.EmailField(max_length=200, blank=True, null=True)
    Gender=models.CharField(max_length=15, blank=True, null=True)
    phone=models.CharField(max_length=15, blank=True, null=True)
    member=models.CharField(max_length=200, blank=True, null=True)
    paymentStatus=models.CharField(max_length=55,blank=True,null=True)
    payment_method=models.CharField(max_length=20, blank=True, null=True)  # 'stripe' or 'bkash'
    Price=models.IntegerField(blank=True,null=True)
    DueDate=models.DateTimeField(blank=True,null=True)
    subscription_start_date=models.DateTimeField(blank=True,null=True)
    subscription_end_date=models.DateTimeField(blank=True,null=True)
    is_active=models.BooleanField(default=False)
    timeStamp=models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return self.client_usrname
    
    def is_subscription_valid(self):
        """Check if subscription is still valid"""
        if self.is_active and self.subscription_end_date:
            if timezone.is_naive(self.subscription_end_date):
                self.subscription_end_date = timezone.make_aware(self.subscription_end_date, timezone.get_default_timezone())
            return self.subscription_end_date > timezone.now()
        return False
    

class MembershipPlan(models.Model):
    plan=models.CharField(max_length=185)
    price=models.IntegerField(max_length=55)

    def __int__(self):
        return self.id

from django.db import models
from django.contrib.auth.models import User

class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=100)
    stripe_subscription_id = models.CharField(max_length=100)
