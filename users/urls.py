from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView, TemplateView
from allauth.account.views import ConfirmEmailView
from dj_rest_auth.registration.views import VerifyEmailView, RegisterView
from dj_rest_auth.registration.views import ( SocialAccountListView, SocialAccountDisconnectView )



from .views import *

# Create a router and register our viewsets with it.
router = DefaultRouter()
# router.register(r'profile', ProfileViewSet)
router.register(r'group', GroupViewSet)
router.register(r'add', GroupRoleViewSet)
router.register(r'joinlink', GroupJoinLinkViewSet)
router.register(r'invoice', InvoiceViewSet)
router.register(r'plan', PlanViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    # path('upload/', picUploadView.as_view()),
    path('join/<pk>', GroupJoinAcceptlink),
    path('self/', selfProfile),
    path('pay/', pay),
    path('auth/', include('dj_rest_auth.urls')),
    
    url("auth/registration/account-confirm-email/(?P<key>[\s\d\w().+-_',:&]+)/$", VerifyEmailView.as_view(template_name="verify.html"), name='account_confirm_email'),
    re_path(r'^auth/registration/account-confirm-email/', VerifyEmailView.as_view(template_name='verify.html'),name='account_email_verification_sent'),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    path('auth/twitter/', TwitterLogin.as_view(), name='twitter_login'),
    path('auth/facebook/connect/', FacebookConnect.as_view(), name='fb_connect'),
    path('auth/twitter/connect/', TwitterConnect.as_view(), name='twitter_connect'),
    path('auth/socialaccounts/', SocialAccountListView.as_view(), name='social_account_list'),
    path('auth/socialaccounts/<int:pk>/disconnect/', SocialAccountDisconnectView.as_view(), name='social_account_disconnect'),
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)