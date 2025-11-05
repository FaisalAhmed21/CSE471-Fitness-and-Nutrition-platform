from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .models import Client, Trainer, Owner, Discussion, DiscussionReply, Plan, Plan_Content, Rating, Appointment, Payment, wPlan_Content, wPlan, Enroll, MembershipPlan
from django.contrib.auth.models import User, auth
from django.contrib import messages
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required 
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from datetime import datetime, timedelta
from .forms import CustomForm
from .forms import BMIForm
from .models import BMIRecord
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string, get_template 
import logging
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Q
import stripe
from functools import wraps


def subscription_required(view_func):
    """
    Decorator to check if user has an active subscription before accessing content
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please login to access this content.')
            return redirect('clientLogin')
        
        # Ensure Client record exists for the user
        if not Client.objects.filter(user=request.user).exists():
            Client.objects.create(
                user=request.user,
                client_usrname=request.user.username,
                email=request.user.email,
                first_name=request.user.first_name or "",
                last_name=request.user.last_name or ""
            )
        
        try:
            enrollment = Enroll.objects.get(client_usrname=request.user.username)
            
            # Check if subscription is valid
            if enrollment.is_subscription_valid():
                return view_func(request, *args, **kwargs)
            else:
                # Subscription expired, deactivate it
                enrollment.is_active = False
                enrollment.save()
                messages.warning(request, 'Your subscription has expired. Please renew to access this content.')
                return redirect('enrollment')
        except Enroll.DoesNotExist:
            messages.info(request, 'Please subscribe to access workout and diet plans.')
            return redirect('enrollment')
    
    return wrapper

def homepage(request):
    return render(request, 'home.html')

def clientLogin(request):
    if request.method == 'POST':
        client_usrname = request.POST['clientusrname']
        password = request.POST['password']
        user = auth.authenticate(username=client_usrname, password=password)
        if user is not None and Client.objects.filter(client_usrname=client_usrname).exists():
            auth.login(request, user)
            return redirect('clientProfile')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('clientLogin')
    return render(request, 'client_login.html')

def trainerLogin(request):
    if request.method == 'POST':
        print(request.POST)  # Add this line to debug
        try:
            user_name = request.POST['username']
            password = request.POST['password']
        except KeyError as e:
            print(f"KeyError: {e}")  # This will help you identify if the key is missing
            messages.error(request, 'Invalid form submission')
            return redirect('trainerLogin')

        user = auth.authenticate(username=user_name, password=password)
        if user is not None and Trainer.objects.filter(user=user).exists():
            auth.login(request, user)
            return redirect('trainerProfile')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('trainerLogin')
    return render(request, 'trainer_login.html')


def ownerLogin(request):
    if request.method == 'POST':
        user_name = request.POST['clientusrname']
        #user_name = request.POST.get('owner_usrname', "error")
        password = request.POST['password']
        print(user_name)
        print(password)
        user = auth.authenticate(username=user_name, password=password)
        print('done')
        print(user)
        if user is not None and Owner.objects.filter(user=user).exists():
            print('hello')
            auth.login(request, user)
            return redirect('ownerProfile')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('ownerLogin')

    return render(request, 'owner_login.html')

def clientRegister(request):
    if request.method == 'POST':
        client_usrname = request.POST['clientusrname']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=client_usrname).exists():
                messages.info(request, 'Username Taken')
                return redirect('clientRegister')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('clientRegister')
            else:
                user = User.objects.create_user(
                    username=client_usrname,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                user.save()

                # Create the Client instance
                client = Client.objects.create(
                    user=user,
                    client_usrname=client_usrname,
                    email=email,
                    # Optionally add first_name and last_name if needed
                    first_name=first_name,
                    last_name=last_name
                )
                client.save()
                return redirect('clientLogin')
        else:
            messages.info(request, 'Password not matching')
            return redirect('clientRegister')  
    return render(request, 'client_reg.html')

@login_required(login_url='clientLogin')
def clientProfile(request):
    user = request.user
    
    # Get or create Client object for the user
    try:
        obj = Client.objects.get(user=user)
    except Client.DoesNotExist:
        # Create Client record if it doesn't exist (for Google sign-in users)
        obj = Client.objects.create(
            user=user,
            client_usrname=user.username,
            email=user.email,
            first_name=user.first_name or "",
            last_name=user.last_name or ""
        )
    
    return render(request, 'client_profile.html', {'user': obj, "client": "client"})
    

@login_required(login_url='trainerLogin')
def trainerProfile(request):
    if Trainer.objects.filter(user=request.user).exists():
        user = request.user
        obj = User.objects.get(username=user)
        if Trainer.objects.filter(user=obj).exists():
            obj = Trainer.objects.get(user=obj)
            return render(request, 'trainer_profile.html', {'user': obj, "trainer": "trainer"})
        return render(request, 'trainer_profile.html', {'user': obj})
    else:
        return redirect('trainerLogin')

    
# @login_required
# def trainerProfile(request):
#     return render(request, 'trainer_profile.html')
@login_required
def ownerProfile(request):
        # return redirect('clientLogin')
        return render(request, 'owner_profile.html', {"owner": "owner"})
    
    #return render(request, 'owner_profile.html')
    
@login_required(login_url='clientLogin')
def logoutUser(request):
    if Client.objects.filter(user=request.user).exists():
        logout(request)
        return redirect('clientLogin')
    elif Trainer.objects.filter(user=request.user).exists():
        logout(request)
        return redirect('trainerLogin')
    elif Owner.objects.filter(user=request.user).exists():
        logout(request)
        return redirect('ownerLogin')
    else:
        logout(request)
        return redirect('clientLogin')






@login_required(login_url='clientLogin')
def discussionClientView(request):
    if Client.objects.filter(user=request.user).exists():
        user = request.user
        client = Client.objects.get(user=user)
        
        # Get filter parameters
        filter_status = request.GET.get('status', 'all')
        search_query = request.GET.get('search', '')
        sort_by = request.GET.get('sort', '-datetime')
        
        # Base queryset
        discussions = Discussion.objects.all()
        
        # Apply filters
        if filter_status != 'all':
            discussions = discussions.filter(status=filter_status)
        
        if search_query:
            discussions = discussions.filter(
                Q(title__icontains=search_query) |
                Q(statement__icontains=search_query) |
                Q(tag__icontains=search_query)
            )
        
        # Apply sorting
        if sort_by == 'popular':
            discussions = discussions.order_by('-views_count', '-upvotes')
        elif sort_by == 'upvotes':
            discussions = discussions.order_by('-upvotes')
        else:
            discussions = discussions.order_by(sort_by)
        
        # Get reply counts for each discussion
        discussions_with_counts = []
        for disc in discussions:
            reply_count = disc.replies.count()
            discussions_with_counts.append({
                'discussion': disc,
                'reply_count': reply_count
            })
        
        context = {
            'discussions': discussions_with_counts,
            'current_user': client,
            'filter_status': filter_status,
            'search_query': search_query,
            'sort_by': sort_by,
        }
        return render(request, 'discussion_client_view.html', context)
    else:
        return redirect('clientLogin')


@login_required(login_url='clientLogin')
def discussionDetail(request, discussion_id):
    """View for detailed discussion with replies"""
    discussion = get_object_or_404(Discussion, dnumber=discussion_id)
    
    # Increment view count only if user hasn't viewed before
    if not discussion.has_viewed(request.user):
        discussion.views_count += 1
        discussion.viewed_by.add(request.user)
        discussion.save()
    
    # Get current user
    current_user = None
    is_trainer = False
    if Client.objects.filter(user=request.user).exists():
        current_user = Client.objects.get(user=request.user)
    elif Trainer.objects.filter(user=request.user).exists():
        current_user = Trainer.objects.get(user=request.user)
        is_trainer = True
    
    # Handle reply submission
    if request.method == 'POST':
        reply_text = request.POST.get('reply_text', '').strip()
        mark_as_solution = request.POST.get('mark_as_solution')
        
        if reply_text:
            if is_trainer:
                reply = DiscussionReply.objects.create(
                    discussion=discussion,
                    reply_text=reply_text,
                    replied_by_trainer=current_user
                )
            else:
                reply = DiscussionReply.objects.create(
                    discussion=discussion,
                    reply_text=reply_text,
                    replied_by_client=current_user
                )
            reply.save()
            messages.success(request, 'Reply posted successfully!')
            return redirect('discussionDetail', discussion_id=discussion_id)
        
        # Mark reply as solution
        if mark_as_solution and (is_trainer or current_user == discussion.posted_by):
            reply_id = request.POST.get('reply_id')
            if reply_id:
                reply_obj = DiscussionReply.objects.get(id=reply_id)
                # Unmark any previous solutions
                DiscussionReply.objects.filter(discussion=discussion).update(is_solution=False)
                reply_obj.is_solution = True
                reply_obj.save()
                
                discussion.status = 'resolved'
                if is_trainer:
                    discussion.resolved_by = current_user
                discussion.save()
                messages.success(request, 'Reply marked as solution!')
                return redirect('discussionDetail', discussion_id=discussion_id)
    
    replies = discussion.replies.all()
    
    # Check if current user has upvoted this discussion
    has_upvoted = discussion.has_upvoted(request.user)
    
    context = {
        'discussion': discussion,
        'replies': replies,
        'current_user': current_user,
        'is_trainer': is_trainer,
        'has_upvoted': has_upvoted,
    }
    
    if is_trainer:
        return render(request, 'discussion_detail_trainer.html', context)
    else:
        return render(request, 'discussion_detail.html', context)


@login_required(login_url='trainerLogin')
def discussionTrainerView(request):
    if Trainer.objects.filter(user=request.user).exists():
        cuser = Trainer.objects.get(user=request.user)
        
        # Get filter parameters
        filter_status = request.GET.get('status', 'all')
        search_query = request.GET.get('search', '')
        sort_by = request.GET.get('sort', '-datetime')
        
        # Base queryset
        discussions = Discussion.objects.all()
        
        # Apply filters
        if filter_status != 'all':
            discussions = discussions.filter(status=filter_status)
        
        if search_query:
            discussions = discussions.filter(
                Q(title__icontains=search_query) |
                Q(statement__icontains=search_query) |
                Q(tag__icontains=search_query)
            )
        
        # Apply sorting
        if sort_by == 'popular':
            discussions = discussions.order_by('-views_count', '-upvotes')
        elif sort_by == 'upvotes':
            discussions = discussions.order_by('-upvotes')
        else:
            discussions = discussions.order_by(sort_by)
        
        # Get reply counts for each discussion
        discussions_with_counts = []
        for disc in discussions:
            reply_count = disc.replies.count()
            discussions_with_counts.append({
                'discussion': disc,
                'reply_count': reply_count
            })
        
        context = {
            'discussions': discussions_with_counts,
            'current_user': cuser,
            'filter_status': filter_status,
            'search_query': search_query,
            'sort_by': sort_by,
        }
        
        if request.method == 'POST' and request.POST['status'] == 'resolved':
            dnum = request.POST['dnum']
            status = "resolved"
            resolved_by = cuser
            discussion = Discussion.objects.get(dnumber=dnum)
            discussion.status = status
            discussion.resolved_by = resolved_by
            discussion.save()
            return redirect('discussiontrainerView')
        elif request.method == 'POST' and request.POST['status'] == 'rejected':
            dnum = request.POST['dnum']
            status = "rejected"
            resolved_by = cuser
            discussion = Discussion.objects.get(dnumber=dnum)
            discussion.status = status
            discussion.resolved_by = resolved_by
            discussion.save()
            return redirect('discussiontrainerView')
        return render(request, 'discussion_trainer_view.html', context)
    else:
        return redirect('trainerLogin')


@login_required(login_url='clientLogin')
def postDiscussion(request):
    if Client.objects.filter(user=request.user).exists():
        cuser = Client.objects.get(user=request.user)
        if request.method == 'POST':
            title = request.POST.get('title', 'Untitled')
            tag = request.POST.get('tag', 'General')
            statement = request.POST['statement']
            discussion = Discussion.objects.create(
                title=title,
                tag=tag, 
                statement=statement, 
                datetime=datetime.now(), 
                posted_by=cuser
            )
            discussion.save()
            messages.success(request, 'Discussion posted successfully!')
            return redirect('discussionClientView')
        return render(request, 'post_discussion.html')
    else:
        return redirect('clientLogin')


@login_required
def upvoteDiscussion(request, discussion_id):
    """Handle discussion upvotes - only once per user"""
    discussion = get_object_or_404(Discussion, dnumber=discussion_id)
    
    if discussion.has_upvoted(request.user):
        # User already upvoted, remove upvote
        discussion.upvotes -= 1
        discussion.upvoted_by.remove(request.user)
        messages.info(request, 'Upvote removed.')
    else:
        # Add upvote
        discussion.upvotes += 1
        discussion.upvoted_by.add(request.user)
        messages.success(request, 'Discussion upvoted!')
    
    discussion.save()
    return redirect('discussionDetail', discussion_id=discussion_id)


@login_required
def deleteDiscussion(request, discussion_id):
    """Delete a discussion (only by author or trainer)"""
    discussion = get_object_or_404(Discussion, dnumber=discussion_id)
    
    # Check permissions
    is_author = False
    is_trainer = False
    
    if Client.objects.filter(user=request.user).exists():
        client = Client.objects.get(user=request.user)
        is_author = (discussion.posted_by == client)
    elif Trainer.objects.filter(user=request.user).exists():
        is_trainer = True
    
    if is_author or is_trainer:
        discussion.delete()
        messages.success(request, 'Discussion deleted successfully!')
        if is_trainer:
            return redirect('discussiontrainerView')
        else:
            return redirect('discussionClientView')
    else:
        messages.error(request, 'You do not have permission to delete this discussion.')
        return redirect('discussionClientView')




@login_required(login_url='trainerLogin')
def TrainerPlanView(request):
    if Trainer.objects.filter(user=request.user).exists():
        plans = Plan.objects.all().order_by('plan_id')
        if request.method == 'POST':
            plan_id = request.POST['plan_id']
            plan = Plan.objects.get(plan_id=plan_id)
            plan.delete()
        return render(request, 'trainer_plan_view.html', {'plans': plans})
    else:
        return redirect('trainerLogin')

@login_required(login_url='trainerLogin')
def addPlan(request):
    if Trainer.objects.filter(user=request.user).exists():
        if request.method == 'POST':
            plan_id = request.POST['plan_id']
            plan_name = request.POST['pname']
            plan_description = request.POST['description']
            plan_point = request.POST['point']
            plan_trainer = request.POST['trainer']
            plan_topic = request.POST['topic']

            if plan_point.isdigit() == False:
                messages.info(request, 'Points must be a number')
                return redirect('addPlan')
            else:
                plan = Plan.objects.create(plan_id=plan_id, plan_name=plan_name, plan_description=plan_description, plan_point=plan_point, plan_trainer=plan_trainer, plan_topic=plan_topic)
                plan.save()
                return redirect('TrainerPlanView')
        return render(request, 'add_plan.html')
    else:
        return redirect('trainerLogin')




@login_required(login_url='trainerLogin')
def planView(request):
    if Trainer.objects.filter(user=request.user).exists():
        plan = Plan.objects.all().order_by('plan_id')
        return render(request, 'plan_view.html', {'plan': plan})
    else:
        return redirect('trainerLogin')




@login_required(login_url='trainerLogin')
def planContent(request, plan_id):
    if Trainer.objects.filter(user=request.user).exists():
        plan_content = Plan_Content.objects.all()[::-1]
        return render(request, 'plan_content.html', {'content':plan_content , 'plan_id': plan_id})
    else:
        return redirect('trainerLogin')


@login_required(login_url='trainerLogin')
def addPlanContent(request, plan_id):
    if Trainer.objects.filter(user=request.user).exists():
        plan_id = Plan.objects.get(plan_id=plan_id)
        user = request.user
        if Trainer.objects.filter(user=user).exists():
            user = Trainer.objects.get(user=user)
        if request.method == 'POST':
            plan_content_tag = request.POST['tag']
            plan_content_description = request.POST['description']
            img = request.FILES.get('image')

            plan_content = Plan_Content.objects.create(plan_id=plan_id, plan_content_tag=plan_content_tag, plan_content_description=plan_content_description, content_img=img, datetime = datetime.now(), upload_by=user)
            plan_content.save()
            return redirect(f'/plan-content/{plan_id}/')
        return render(request, 'add_plan_content.html', {'plan_id': plan_id})
    else:
        return redirect('trainerLogin')



@login_required(login_url='clientLogin')
@subscription_required
def planviewClient(request):
    if Client.objects.filter(user=request.user).exists():
        planviewClient = Plan.objects.all().order_by('plan_id')
        return render(request, 'planviewClient.html', {'planviewClient': planviewClient})
    else:
        return redirect('clientLogin')


@login_required(login_url='clientLogin')
@subscription_required
def planContentviewClient(request, plan_id):
    if Client.objects.filter(user=request.user).exists():
        planContentviewClient = Plan_Content.objects.all()[::-1]
        return render(request, 'planContentviewClient.html', {'planContentviewClient':planContentviewClient , 'plan_id': plan_id})
    else:
        return redirect('clientLogin')


#! WORKOUT PLAN

# @login_required(login_url='trainerLogin')
# def wplanView(request):
#     if Trainer.objects.filter(user=request.user).exists():
#         wplan = wPlan.objects.all().order_by('wplan_id')
#         return render(request, 'trainer_wplan_view.html', {'wplan': wplan})
#     else:
#         return redirect('trainerLogin')
@login_required(login_url='trainerLogin')
def wplanView(request):
    if Trainer.objects.filter(user=request.user).exists():
        wplan = wPlan.objects.all().order_by('wplan_id')
        if request.method == 'POST':
            print(request.POST)
            wplan_id = request.POST['wplan_id']
            wplans = wPlan.objects.get(wplan_id=wplan_id)
            wplans.delete()
        return render(request, 'trainer_wplan_view.html', {'wplan': wplan})
    else:
        return redirect('trainerLogin')



@login_required(login_url='clientLogin')
@subscription_required
def wplanviewClient(request):
    if Client.objects.filter(user=request.user).exists():
        wplanviewClient = wPlan.objects.all().order_by('wplan_id')
        return render(request, 'wplanviewClient.html', {'wplanviewClient': wplanviewClient})
    else:
        return redirect('clientLogin')


@login_required(login_url='clientLogin')
@subscription_required
def wplanContentviewClient(request, wplan_id):
    if Client.objects.filter(user=request.user).exists():
        wplanContentviewClient = wPlan_Content.objects.all()[::-1]
        return render(request, 'wplanContentviewClient.html', {'wplanContentviewClient':wplanContentviewClient , 'wplan_id': wplan_id})
    else:
        return redirect('clientLogin')
    












@login_required(login_url='trainerLogin')
def addwPlan(request):
    if Trainer.objects.filter(user=request.user).exists():
        if request.method == 'POST':
            wplan_id = request.POST['wplan_id']
            wplan_name = request.POST['wname']
            wplan_description = request.POST['wdescription']
            wplan_point = request.POST['wpoint']
            wplan_trainer = request.POST['wtrainer']
            wplan_topic = request.POST['wtopic']
            wplan_image = request.FILES.get('wplan_image')

            if wplan_point.isdigit() == False:
                messages.info(request, 'Points must be a number')
                return redirect('addwPlan')
            else:
                wplan = wPlan.objects.create(wplan_id=wplan_id, wplan_name=wplan_name, wplan_description=wplan_description, wplan_point=wplan_point, wplan_trainer=wplan_trainer, wplan_topic=wplan_topic, wplan_image=wplan_image)
                wplan.save()
                return redirect('wplanView')
        return render(request, 'add_work_plan.html')
    else:
        return redirect('trainerLogin')

@login_required(login_url='trainerLogin')
def addwPlanContent(request, wplan_id):
    if Trainer.objects.filter(user=request.user).exists():
        # Retrieve the wPlan instance by its ID
        wplan = wPlan.objects.get(wplan_id=wplan_id)
        user = request.user
        trainer = Trainer.objects.get(user=user)

        if request.method == 'POST':
            wplan_content_tag = request.POST.get('tag')
            wplan_content_description = request.POST.get('description')
            img = request.FILES.get('image')
            countdown_img = request.FILES.get('countdown')  # Assuming countdown is a file field in the form

            # Create and save a new wPlan_Content instance
            wplan_content = wPlan_Content.objects.create(
                wplan_id=wplan,  # Associate with the retrieved wPlan
                wplan_content_tag=wplan_content_tag,
                wplan_content_description=wplan_content_description,
                wcontent_img=img,
                wcontent_count=countdown_img,  # Assign the countdown image
                # wdatetime=timezone.now(), 
                wdatetime = datetime.now(),
                 
                  # Use timezone.now() for current time
                wupload_by=trainer  # Associate with the retrieved Trainer
            )
            wplan_content.save()

            return redirect(f'/wplan-content/{wplan_id}/')  # Redirect to a page that lists content or shows details for the wPlan

        return render(request, 'add_wplan_content.html', {'wplan_id': wplan_id})
    else:
        return redirect('trainerLogin')






@login_required(login_url='trainerLogin')
def wplanContent(request, wplan_id):
    if Trainer.objects.filter(user=request.user).exists():
        wplan_content = wPlan_Content.objects.all()[::-1]
        return render(request, 'trainer_wplan_content.html', {'wcontent':wplan_content , 'wplan_id': wplan_id})
    else:
        return redirect('trainerLogin')






@login_required
def delete_account(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = authenticate(username=request.user.username, password=password)
        if user is not None:
            user.delete()
            logout(request)
            messages.success(request, "Account deleted successfully")
            return redirect('clientLogin')
        else:
            messages.error(request, "Account deletion failed, password incorrect.")
            return redirect('clientProfile')
    else:
        return redirect('clientProfile')

@login_required
def editProfile(request):
    user = request.user
    
    # Get or create Client object
    try:
        client = Client.objects.get(user=user)
    except Client.DoesNotExist:
        client = Client.objects.create(
            user=user,
            client_usrname=user.username,
            email=user.email,
            first_name=user.first_name or "",
            last_name=user.last_name or ""
        )

    if request.method == 'POST':
        client.client_usrname = request.POST.get('clientusrname', client.client_usrname)
        client.first_name = request.POST.get('first_name', client.first_name)
        client.last_name = request.POST.get('last_name', client.last_name)
        client.email = request.POST.get('email', client.email)
        client.phone = request.POST.get('phone', client.phone)
        client.age = request.POST.get('age', client.age)
        client.weight = request.POST.get('weight', client.weight)
        client.height = request.POST.get('height', client.height)
        client.bio = request.POST.get('bio', client.bio)
        client.gender = request.POST.get('gender', client.gender)
        client.achievement = request.POST.get('achievement', client.achievement)
        client.personalTrainer = request.POST.get('personalTrainer', client.personalTrainer)

        client.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('clientProfile') 
        
    return render(request, 'edit_profile.html', {'client': client})

def index(request):
    return render(request,'emailapp/index.html')
    




def custom_message(request):
    #getting information from the form
    if request.method == "POST":
        form = CustomForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            subject = form.cleaned_data['subject']
            print(message)
            
            #sending  email 
            clients = Client.objects.all()
            print(clients)    
            for clients in clients:
                print(clients.client_usrname)
                email = clients.email
                context = {'name': clients.client_usrname,'message': message}
                email_template = get_template('emailapp/email.html').render(context)
                email_address = EmailMessage(subject, email_template,"Fitlife Platform", [email])
                email_address.content_subtype = "html" 
                email_address.send()
            return redirect('custom_message')
        else:
            print(form.errors)
    return render(request,'emailapp/message.html')

def support_view(request):
    return render(request, 'support&faq.html')


def calculate_bmi(height_in_meters, weight_in_kg):

    return weight_in_kg / (height_in_meters ** 2)

def get_bmi_comment(bmi_value):
    if bmi_value < 18.5:
        return "Underweight"
    elif 18.5 <= bmi_value < 24.9:
        return "Good"
    elif 25 <= bmi_value < 30:
        return "Overweight"
    else:
        return "Obese"

@login_required
def bmi_page(request):
    user = request.user
    bmi_records = BMIRecord.objects.filter(user=user).order_by('recorded_at')


    if request.method == "POST":
        form = BMIForm(request.POST)
        if form.is_valid():
            height_in_inches = form.cleaned_data['height_in_inches']
            weight_in_kg = form.cleaned_data['weight_in_kg']
            height_in_meters = height_in_inches * 0.0254
            bmi_value = round(calculate_bmi(height_in_meters, weight_in_kg), 2)
            comment = get_bmi_comment(bmi_value)
            # Save the new BMI record
            bmi_record = BMIRecord.objects.create(
                user=user,
                height_in_meters=height_in_meters,
                weight_in_kg=weight_in_kg,
                bmi_value=bmi_value,
                comment=comment
            )
            return redirect('bmi_page')
    else:
        form = BMIForm()

    latest_bmi = bmi_records.last()

    context = {
        'form': form,
        'latest_bmi': latest_bmi,
        'bmi_records': bmi_records,
    }
    return render(request, 'bmi_page.html', context)

def workout_options(request):
    return render(request, 'workout_options.html')

def arms_beginner(request):
    # Replace with appropriate view logic and template
    return render(request, 'arms_beginner.html')

def arms_intermediate(request):
    # Replace with appropriate view logic and template
    return render(request, 'arms_intermediate.html')

def arms_advanced(request):
    # Replace with appropriate view logic and template
    return render(request, 'arms_advanced.html')

def chest_beginner(request):
    # Replace with appropriate view logic and template
    return render(request, 'chest_beginner.html')

def chest_intermediate(request):
    # Replace with appropriate view logic and template
    return render(request, 'chest_intermediate.html')

def chest_advanced(request):
    # Replace with appropriate view logic and template
    return render(request, 'chest_advanced.html')

def abs_beginner(request):
    # Replace with appropriate view logic and template
    return render(request, 'abs_beginner.html')

def abs_intermediate(request):
    # Replace with appropriate view logic and template
    return render(request, 'abs_intermediate.html')

def abs_advanced(request):
    # Replace with appropriate view logic and template
    return render(request, 'abs_advanced.html')

def legs_beginner(request):
    # Replace with appropriate view logic and template
    return render(request, 'legs_beginner.html')

def legs_intermediate(request):
    # Replace with appropriate view logic and template
    return render(request, 'legs_intermediate.html')

def legs_advanced(request):
    # Replace with appropriate view logic and template
    return render(request, 'legs_advanced.html')


def tracker(request):
    import json
    import requests
    if request.method == 'POST':
        query = request.POST['query']
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query='
        api_request = requests.get(api_url + query, headers={'X-Api-Key': 'IF7UO25/zTEhl8LgzwncKw==EXlc6j1YbuGyqgJm'})
        try:
            api = json.loads(api_request.content)
            print(api_request.content)
        except Exception as e:
            api = "oops! There was an error"
            print(e)
        return render(request, 'tracker.html', {'api': api})
    else:
        return render(request, 'tracker.html', {'query': 'Enter a valid query'})
def premium_content(request):
    return render(request, 'premium_content.html')


@login_required(login_url='clientLogin')
def enrollment_view(request):
    """
    Show enrollment form with payment method selection
    """
    # Check if user already has active subscription
    try:
        enrollment = Enroll.objects.get(client_usrname=request.user.username)
        if enrollment.is_subscription_valid():
            # Redirect to subscription info without showing message
            return redirect('subscription_info')
    except Enroll.DoesNotExist:
        pass
    
    return render(request, 'enroll.html')


@login_required(login_url='clientLogin')
def process_enrollment(request):
    """
    Process enrollment form and redirect to appropriate payment gateway
    """
    if request.method == 'POST':
        username = request.POST.get('Name')
        email = request.POST.get('Email')
        gender = request.POST.get('Gender')
        membership_plan = request.POST.get('member')
        payment_method = request.POST.get('payment_method')

        # Get phone from user's Client profile if available
        phone = ""
        try:
            client = Client.objects.get(user=request.user)
            phone = client.phone
        except Client.DoesNotExist:
            pass

        # Define membership prices and durations
        membership_prices = {
            "1 month - 1000 Taka": (1000, 30),
            "3 month - 2500 Taka": (2500, 90),
            "6 month - 4000 Taka": (4000, 180),
            "1 year - 6000 Taka": (6000, 365),
        }

        if membership_plan not in membership_prices:
            messages.error(request, 'Invalid membership plan selected.')
            return redirect('enrollment')

        price, duration = membership_prices[membership_plan]

        # Create or update enrollment record
        enrollment, created = Enroll.objects.update_or_create(
            client_usrname=username,
            defaults={
                'Email': email,
                'Gender': gender,
                'phone': phone,
                'member': membership_plan,
                'Price': price,
                'payment_method': payment_method,
                'paymentStatus': 'Pending',
                'is_active': False,
            }
        )

        # Store enrollment ID in session for payment processing
        request.session['pending_enrollment_id'] = enrollment.id

        # Redirect based on payment method
        if payment_method == 'stripe':
            return redirect('stripe_checkout')
        elif payment_method == 'bkash':
            return redirect('bkash_payment')
        else:
            messages.error(request, 'Invalid payment method selected.')
            return redirect('enrollment')

    return redirect('enrollment')


@login_required(login_url='clientLogin')
def bkash_payment(request):
    """
    Handle bKash payment with realistic multi-step flow (sandbox/test mode)
    Steps: 1) Enter phone, 2) Enter PIN, 3) Enter OTP, 4) Payment confirmation
    """
    import re
    import random
    
    enrollment_id = request.session.get('pending_enrollment_id')
    if not enrollment_id:
        messages.error(request, 'No pending enrollment found.')
        return redirect('enrollment')

    try:
        enrollment = Enroll.objects.get(id=enrollment_id)
    except Enroll.DoesNotExist:
        messages.error(request, 'Enrollment not found.')
        return redirect('enrollment')

    # Get current payment step (default is 'phone')
    payment_step = request.session.get('bkash_payment_step', 'phone')

    if request.method == 'POST':
        action = request.POST.get('action', '')
        
        # Step 1: Phone number verification
        if action == 'verify_phone':
            phone = request.POST.get('phone', '').strip()
            
            # Validate phone number format
            if not re.match(r'^01[3-9]\d{8}$', phone):
                messages.error(request, 'Invalid bKash account number. Please enter a valid 11-digit number starting with 01.')
                return render(request, 'bkash_payment.html', {
                    'enrollment': enrollment,
                    'payment_step': 'phone'
                })
            
            # Store phone in session
            request.session['bkash_phone'] = phone
            request.session['bkash_payment_step'] = 'pin'
            
            return render(request, 'bkash_payment.html', {
                'enrollment': enrollment,
                'payment_step': 'pin',
                'phone': phone
            })
        
        # Step 2: PIN verification
        elif action == 'verify_pin':
            pin = request.POST.get('pin', '').strip()
            phone = request.session.get('bkash_phone', '')
            
            # Validate PIN format
            if not re.match(r'^\d{5}$', pin):
                messages.error(request, 'Invalid PIN. Please enter a 5-digit PIN.')
                return render(request, 'bkash_payment.html', {
                    'enrollment': enrollment,
                    'payment_step': 'pin',
                    'phone': phone
                })
            
            # Simulate PIN verification delay and generate OTP
            generated_otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            request.session['bkash_otp'] = generated_otp
            request.session['bkash_payment_step'] = 'otp'
            
            # In real bKash, OTP is sent to phone. In sandbox, we show it on screen
            return render(request, 'bkash_payment.html', {
                'enrollment': enrollment,
                'payment_step': 'otp',
                'phone': phone,
                'generated_otp': generated_otp  # Only for sandbox testing
            })
        
        # Step 3: OTP verification
        elif action == 'verify_otp':
            otp = request.POST.get('otp', '').strip()
            phone = request.session.get('bkash_phone', '')
            stored_otp = request.session.get('bkash_otp', '')
            
            # Validate OTP format
            if not re.match(r'^\d{6}$', otp):
                messages.error(request, 'Invalid OTP format. Please enter a 6-digit OTP.')
                return render(request, 'bkash_payment.html', {
                    'enrollment': enrollment,
                    'payment_step': 'otp',
                    'phone': phone,
                    'generated_otp': stored_otp
                })
            
            # In sandbox mode, accept any 6-digit OTP or the generated one
            if len(otp) != 6:
                messages.error(request, 'Invalid OTP. Please try again.')
                return render(request, 'bkash_payment.html', {
                    'enrollment': enrollment,
                    'payment_step': 'otp',
                    'phone': phone,
                    'generated_otp': stored_otp
                })
            
            # Move to confirmation step
            request.session['bkash_payment_step'] = 'confirm'
            
            return render(request, 'bkash_payment.html', {
                'enrollment': enrollment,
                'payment_step': 'confirm',
                'phone': phone
            })
        
        # Step 4: Final payment confirmation
        elif action == 'confirm_payment':
            phone = request.session.get('bkash_phone', '')
            
            # Generate transaction ID
            transaction_id = f"BK{random.randint(10000000, 99999999)}{random.randint(100, 999)}"
            
            # Calculate subscription dates
            membership_prices = {
                "1 month - 1000 Taka": 30,
                "3 month - 2500 Taka": 90,
                "6 month - 4000 Taka": 180,
                "1 year - 6000 Taka": 365,
            }

            duration = membership_prices.get(enrollment.member, 30)
            start_date = timezone.now()
            end_date = start_date + timedelta(days=duration)

            # Update enrollment with payment success
            enrollment.paymentStatus = 'Completed'
            enrollment.subscription_start_date = start_date
            enrollment.subscription_end_date = end_date
            enrollment.DueDate = end_date
            enrollment.is_active = True
            enrollment.phone = phone
            enrollment.save()

            # Clear bKash session data
            for key in ['bkash_phone', 'bkash_otp', 'bkash_payment_step', 'pending_enrollment_id']:
                if key in request.session:
                    del request.session[key]

            # Store transaction info for success page
            request.session['show_payment_alert'] = True
            request.session['transaction_id'] = transaction_id
            request.session['payment_method'] = 'bKash'

            messages.success(request, f'Payment successful! Transaction ID: {transaction_id}')
            return redirect('subscription_success')
        
        # Back button handling
        elif action == 'back':
            current_step = request.session.get('bkash_payment_step', 'phone')
            step_flow = ['phone', 'pin', 'otp', 'confirm']
            
            if current_step in step_flow:
                current_index = step_flow.index(current_step)
                if current_index > 0:
                    new_step = step_flow[current_index - 1]
                    request.session['bkash_payment_step'] = new_step
                    payment_step = new_step
            
            phone = request.session.get('bkash_phone', '')
            generated_otp = request.session.get('bkash_otp', '')
            
            return render(request, 'bkash_payment.html', {
                'enrollment': enrollment,
                'payment_step': payment_step,
                'phone': phone,
                'generated_otp': generated_otp if payment_step == 'otp' else None
            })

    # GET request - show appropriate step
    phone = request.session.get('bkash_phone', '')
    generated_otp = request.session.get('bkash_otp', '')
    
    return render(request, 'bkash_payment.html', {
        'enrollment': enrollment,
        'payment_step': payment_step,
        'phone': phone,
        'generated_otp': generated_otp if payment_step == 'otp' else None
    })


stripe.api_key = settings.STRIPE_SECRET_KEY

# Define pricing plans
SUBSCRIPTION_PLANS = {
    "1 month - 1000 Taka": {
        "price_id": "price_1RAeG3FY2LB9G7C1KwS9VpC4",
    },
    "3 month - 2500 Taka": {
        "price_id": "price_1RAeGcFY2LB9G7C1g6VbUWwE",
    },
    "6 month - 4000 Taka": {
        "price_id": "price_1RAeH7FY2LB9G7C1Km4HvXMh",
    },
    "1 year - 6000 Taka": {
        "price_id": "price_1RAeHtFY2LB9G7C15m5YSfC5",
    }
}


@login_required(login_url='clientLogin')
@csrf_exempt
def stripe_checkout(request):
    """
    Create Stripe checkout session
    """
    enrollment_id = request.session.get('pending_enrollment_id')
    if not enrollment_id:
        messages.error(request, 'No pending enrollment found.')
        return redirect('enrollment')

    try:
        enrollment = Enroll.objects.get(id=enrollment_id)
    except Enroll.DoesNotExist:
        messages.error(request, 'Enrollment not found.')
        return redirect('enrollment')

    if enrollment.member not in SUBSCRIPTION_PLANS:
        messages.error(request, 'Invalid plan selected')
        return redirect('enrollment')

    try:
        # Store the enrollment ID in the metadata so we can retrieve it later
        checkout_session = stripe.checkout.Session.create(
            success_url=settings.DOMAIN_URL + '/stripe-success/?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=settings.DOMAIN_URL + '/payment-cancelled/',
            payment_method_types=['card'],
            mode='subscription',
            customer_email=enrollment.Email,
            client_reference_id=str(enrollment.id),  # Store enrollment ID
            line_items=[
                {
                    'price': SUBSCRIPTION_PLANS[enrollment.member]['price_id'],
                    'quantity': 1,
                }
            ],
            metadata={
                'enrollment_id': enrollment.id,
                'username': enrollment.client_usrname,
            }
        )
        return redirect(checkout_session.url)

    except Exception as e:
        messages.error(request, f'Payment error: {str(e)}')
        return redirect('enrollment')


def stripe_success(request):
    """
    Handle successful Stripe payment - No login required as user is coming from Stripe
    """
    session_id = request.GET.get('session_id')
    
    if not session_id:
        messages.error(request, 'Invalid payment session.')
        return redirect('clientLogin')

    try:
        # Retrieve the session from Stripe
        session = stripe.checkout.Session.retrieve(session_id)
        enrollment_id = session.get('client_reference_id') or session.metadata.get('enrollment_id')
        
        if not enrollment_id:
            messages.error(request, 'Could not find enrollment information.')
            return redirect('clientLogin')

        enrollment = Enroll.objects.get(id=enrollment_id)

        # Calculate subscription dates
        membership_prices = {
            "1 month - 1000 Taka": 30,
            "3 month - 2500 Taka": 90,
            "6 month - 4000 Taka": 180,
            "1 year - 6000 Taka": 365,
        }

        duration = membership_prices.get(enrollment.member, 30)
        start_date = timezone.now()
        end_date = start_date + timedelta(days=duration)

        # Update enrollment
        enrollment.paymentStatus = 'Completed'
        enrollment.subscription_start_date = start_date
        enrollment.subscription_end_date = end_date
        enrollment.DueDate = end_date
        enrollment.is_active = True
        enrollment.save()

        # Get the user and log them in if not already logged in
        from django.contrib.auth.models import User
        user = User.objects.get(username=enrollment.client_usrname)
        
        if not request.user.is_authenticated:
            # Log the user in
            from django.contrib.auth import login
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        # Set flag for one-time alert
        request.session['show_payment_alert'] = True
        # Clear pending enrollment
        if 'pending_enrollment_id' in request.session:
            del request.session['pending_enrollment_id']

        messages.success(request, 'Payment successful! Your subscription is now active.')
        return redirect('subscription_success')

    except stripe.error.StripeError as e:
        messages.error(request, f'Stripe error: {str(e)}')
        return redirect('clientLogin')
    except Enroll.DoesNotExist:
        messages.error(request, 'Enrollment not found.')
        return redirect('clientLogin')
    except Exception as e:
        messages.error(request, f'Error processing payment: {str(e)}')
        return redirect('clientLogin')


@login_required(login_url='clientLogin')
def subscription_success(request):
    """
    Show subscription success page with details
    """
    try:
        enrollment = Enroll.objects.get(client_usrname=request.user.username)
        
        # Check if we should show the alert
        show_alert = request.session.pop('show_payment_alert', False)
        
        return render(request, 'subscription_success.html', {
            'enrollment': enrollment,
            'show_alert': show_alert
        })
    except Enroll.DoesNotExist:
        messages.error(request, 'No subscription found.')
        return redirect('enrollment')


@login_required(login_url='clientLogin')
def subscription_info(request):
    """
    Show current subscription information
    """
    try:
        enrollment = Enroll.objects.get(client_usrname=request.user.username)
        
        # Check if subscription is still valid
        if not enrollment.is_subscription_valid():
            enrollment.is_active = False
            enrollment.save()
            messages.warning(request, 'Your subscription has expired.')
            return redirect('enrollment')
        
        return render(request, 'subscription_success.html', {
            'enrollment': enrollment,
            'show_alert': False
        })
    except Enroll.DoesNotExist:
        messages.info(request, 'You do not have an active subscription.')
        return redirect('enrollment')


@login_required(login_url='clientLogin')
def cancel_membership(request):
    """
    Cancel user's membership and return to initial state
    """
    try:
        enrollment = Enroll.objects.get(client_usrname=request.user.username)
        enrollment.delete()
        messages.success(request, 'Your subscription has been cancelled successfully. You can subscribe again anytime from the Enrollment page.')
    except Enroll.DoesNotExist:
        messages.error(request, 'No active membership found.')
    
    return redirect('clientProfile')


def payment_cancelled(request):
    """
    Handle cancelled payment
    """
    messages.warning(request, 'Payment was cancelled. Please try again.')
    return redirect('enrollment')


def success_view(request):
    """Legacy success view - redirect to new subscription success"""
    return redirect('subscription_success')


def cancel_view(request):
    """Legacy cancel view - redirect to payment cancelled"""
    return redirect('payment_cancelled')
