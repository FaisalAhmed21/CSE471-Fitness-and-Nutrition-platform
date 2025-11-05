from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    #path('', views.homepage, name='home'),
    path('', views.clientLogin, name='clientLogin'),
    path('client-register/', views.clientRegister, name='clientRegister'),
    path('client-login/', views.clientLogin, name='clientLogin'),
    path('trainer-login/', views.trainerLogin, name='trainerLogin'),
    path('owner-login/', views.ownerLogin, name='ownerLogin'),
    path('owner-profile/', views.ownerProfile, name='ownerProfile'),
    path('client-profile/', views.clientProfile, name='clientProfile'),
    path('trainer-profile/', views.trainerProfile, name='trainerProfile'),
    path('logout/', views.logoutUser, name='logoutUser'),
    path('delete-account', views.delete_account, name = "delete_account"),
    path('edit-profile/', views.editProfile, name='editProfile'),
    path('enroll/', views.enrollment_view, name='enrollment'),
    path('process-enrollment/', views.process_enrollment, name='process_enrollment'),
    path('bkash-payment/', views.bkash_payment, name='bkash_payment'),
    path('stripe-checkout/', views.stripe_checkout, name='stripe_checkout'),
    path('stripe-success/', views.stripe_success, name='stripe_success'),
    path('subscription-success/', views.subscription_success, name='subscription_success'),
    path('subscription-info/', views.subscription_info, name='subscription_info'),
    path('payment-cancelled/', views.payment_cancelled, name='payment_cancelled'),
    path('cancel-membership/', views.cancel_membership, name="cancel_membership"),
    
    # Legacy routes for backward compatibility
    path('create-checkout-session/', views.stripe_checkout, name='create_checkout_session'),
    path('success/', views.success_view, name='success'),
    path('cancel/', views.cancel_view, name='cancel'),
    
    
    path('premium-content/', views.premium_content, name='client-premium-content'),

    


    path('trainer-plan-view/', views.TrainerPlanView, name='TrainerPlanView'),
    # path('plan-view/', views.planView, name='planView'),
    path('add-plan/', views.addPlan, name='addPlan'),
    path('plan-content/<str:plan_id>/', views.planContent, name='planContent'),
    path('add-plan-content/<str:plan_id>/', views.addPlanContent, name='addPlanContent'),
    path('client-plan-view/', views.planviewClient, name='planviewClient'),
    path('client-plan-content/<str:plan_id>/', views.planContentviewClient, name='planContentviewClient'),


    path('trainer-wplan-view/', views.wplanView, name='wplanView'),
    path('add-wplan/', views.addwPlan, name='addwPlan'),
    path('wplan-content/<str:wplan_id>/', views.wplanContent, name='wplanContent'),
    path('add-wplan-content/<str:wplan_id>/', views.addwPlanContent, name='addwPlanContent'),
    path('client-wplan-view/', views.wplanviewClient, name='wplanviewClient'),
    path('client-wplan-content/<str:wplan_id>/', views.wplanContentviewClient, name='wplanContentviewClient'),

    path('index', views.index, name='index'),
    path('owner-profile/custom_message/', views.custom_message, name='custom_message'),

    path('post-discussion/', views.postDiscussion, name='postDiscussion'),
    path('discussion-client-view/', views.discussionClientView, name='discussionClientView'),
    path('discussion-trainer-view/', views.discussionTrainerView, name='discussiontrainerView'),
    path('discussion/<int:discussion_id>/', views.discussionDetail, name='discussionDetail'),
    path('discussion/<int:discussion_id>/upvote/', views.upvoteDiscussion, name='upvoteDiscussion'),
    path('discussion/<int:discussion_id>/delete/', views.deleteDiscussion, name='deleteDiscussion'),

    path('password-reset/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('password-reset-sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    path('support&faq/', views.support_view, name='Support&FAQ'),

    path('bmi/', views.bmi_page, name='bmi_page'),

    path('workout/', views.workout_options, name='workout_options'),
    path('workout/arms/beginner/', views.arms_beginner, name='arms_beginner'),
    path('workout/arms/intermediate/', views.arms_intermediate, name='arms_intermediate'),
    path('workout/arms/advanced/', views.arms_advanced, name='arms_advanced'),
    path('workout/chest/beginner/', views.chest_beginner, name='chest_beginner'),
    path('workout/chest/intermediate/', views.chest_intermediate, name='chest_intermediate'),
    path('workout/chest/advanced/', views.chest_advanced, name='chest_advanced'),
    path('workout/abs/beginner/', views.abs_beginner, name='abs_beginner'),
    path('workout/abs/intermediate/', views.abs_intermediate, name='abs_intermediate'),
    path('workout/abs/advanced/', views.abs_advanced, name='abs_advanced'),
    path('workout/legs/beginner/', views.legs_beginner, name='legs_beginner'),
    path('workout/legs/intermediate/', views.legs_intermediate, name='legs_intermediate'),
    path('workout/legs/advanced/', views.legs_advanced, name='legs_advanced'),

    path('tracker/', views.tracker, name='tracker'),
    
    # Chatbot endpoint
    path('chatbot-response/', views.chatbot_response, name='chatbot_response'),

] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#path('', views.homepage, name='home'),