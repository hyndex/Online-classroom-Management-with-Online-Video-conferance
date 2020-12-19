from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication
from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from .serializers import *
from .permissions import *
import copy
import pytz
from rest_framework import filters
from rest_framework.decorators import action
import json
from rest_framework.parsers import FormParser, MultiPartParser,JSONParser, FileUploadParser
from rest_framework.parsers import JSONParser
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.social_serializers import TwitterLoginSerializer
from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth.registration.views import SocialConnectView
from dj_rest_auth.social_serializers import TwitterConnectSerializer
import razorpay
import json

razorpay_client = razorpay.Client(auth=("rzp_test_UUdDFKZBL7dR4r", "MJTV76lsU8SUjyJXSiK1HHis"))

# Create your views here.


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     search_fields = ['username','email','phone','name']
#     filter_backends = (filters.SearchFilter,)
#     parser_classes=(FormParser, MultiPartParser,JSONParser)

#     serializer_class = UserSerializer
#     permission_classes = [UserPermission]
#     model=serializer_class().Meta().model
#     def get_queryset(self):
#         return UserQuerySet(self.request)


class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    search_fields = ['name']
    filter_backends = (filters.SearchFilter,)
    serializer_class = PlanSerializer
    permission_classes = [PlanPermission]
    model=serializer_class().Meta().model

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    search_fields = ['name']
    filter_backends = (filters.SearchFilter,)
    serializer_class = GroupSerializer
    permission_classes = [GroupPermission]
    model=serializer_class().Meta().model
    def get_queryset(self):
        return GroupQuerySet(self.request)

class GroupJoinLinkViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupJoinLinkSerializer
    permission_classes = [GroupJoinLinkPermission]
    model=serializer_class().Meta().model

    def get_queryset(self):
        return GroupJoinLinkQuerySet(self.request)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.join_link='None'
            instance.save()
            return Response({'success'}, status=204)
        except:
            pass
        return Response(status=400)


from rest_framework.decorators import api_view

@api_view()
def GroupJoinAcceptlink(request,pk):
    try:
        if len(request.user.username)>0:
            group=Group.objects.filter(join_link='pk')
            if group.count()>0:
                group=group[0]
                member=GroupRole.objects.filter(group=group,user=request.user)
                if member.count()==0:
                    if request.user==group.createdBy:
                        return Response({'already member'}, status=200)
                    member=GroupRole.objects.filter(group=group,user=request.user,role='student')
                    return Response({'success'}, status=200)
                else:
                    return Response({'already member'}, status=200)
            return Response({'user not logged in'}, status=401)
        else:
            return Response({"message": 'Internal Server Error'}, status=500)
    except:
        return Response({"message": 'err'})

@api_view()
def selfProfile(request):
    try:
        if len(request.user.username)>0:
            id=User.objects.get(username=str(request.user.username)).id
            return Response({id},status=200)
        else:
            return Response({"message": 'Internal Server Error'}, status=500)
    except:
        return Response({"message": 'err'})

@api_view(['GET', 'POST'])
def pay(request):
    utc=pytz.UTC
    invoice=Invoice.objects.filter(id=request.data['id'])
    if invoice.count()>0:
        razorpay_client = razorpay.Client(auth=("rzp_test_UUdDFKZBL7dR4r", "MJTV76lsU8SUjyJXSiK1HHis"))
        invoice=invoice[0]
        amount = invoice.price
        payment_id = request.data['razorpay_payment_id']
        print("##################level1")
        try:
            razorpay_client.payment.capture(payment_id, str(amount).replace(".",""))    
        except: 
            return Response({'Payment Not Successful'},status=401)  
        profile=invoice.profile
        plan=invoice.plan
        invoice.status='Paid'    
        invoice.save()
        expiry=profile.date_expiry
        print("##################level2")
        if not invoice.plan == invoice.profile.plan:
            profile=Profile.objects.get(user__username=profile.user.username)
            profile.date_expiry=dt.datetime.now()+dt.timedelta(30)
            profile.date_renewed=dt.datetime.now()
            profile.plan=plan
            profile.save()
        print("##################level3")

        if isinstance(expiry, dt.datetime):
            expiryint=int(str(expiry.year)+str(expiry.month)+str(expiry.day))
            todayint=int(str(dt.datetime.now().year)+str(dt.datetime.now().month)+str(dt.datetime.now().day))
            if todayint>expiryint:
                newexipry=dt.datetime.now()+dt.timedelta(30)
            else:
                newexipry=expiry+dt.timedelta(30)
            profile=Profile.objects.get(user__username=profile.user.username)
            profile.date_expiry=newexipry
            profile.date_renewed=dt.datetime.now()
            profile.plan=plan
            profile.save()
            print("##################level4")
        else:
            profile=Profile.objects.grt(user__username=profile.user.username)
            profile.date_expiry=dt.datetime.now()+dt.timedelta(30)
            profile.date_renewed=dt.datetime.now()
            profile.plan=plan
            profile.save()
            print("##################level")
        return Response({"message":"success"},status=200)

    return Response({"message": 'If you did your payment then the amount will be refunded'},status=400)
        


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    search_fields = ['user__username','status']
    filter_backends = (filters.SearchFilter,)
    serializer_class = InvoiceSerializer
    # permission_classes = [GroupPermission]
    model=serializer_class().Meta().model
    # def get_queryset(self):
    #     return GroupQuerySet(self.request)


class GroupRoleViewSet(viewsets.ModelViewSet):
    queryset = GroupRole.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ['group__id']
    serializer_class = GroupRoleSerializer
    permission_classes = [GroupRolePermission]
    model=serializer_class().Meta().model
    def get_queryset(self):
        return GroupRoleQuerySet(self.request)




# class picUploadView(APIView):
#     parser_classes = (MultiPartParser,)

#     def put(self, request, format=None):
#         if request.user.is_authenticated:
#             if (request.user.username == 'admin'):
#                 return Response({"success"},status=204)
#             if request.method in ['PUT','DELETE']:
#                 instance=User.objects.get(username=request.user.username)
#                 instance.media=request.FILES['file']
#                 instance.save()
#                 return Response({"success"},status=204)
#             else:
#                 return Response({"not found"},status=404)

class isAuth(APIView):
    def get(self, request, format=None):
        if request.user.is_authenticated:
            return Response({"success"},status=200)
        else:
            return Response({"not found"},status=401)
class verified(APIView):
    def get(self, request,key, format=None):
        return Response({"success"},status=200)

############################################################################
# SOCIAL MEDIA AUTH
############################################################################


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter



class TwitterLogin(SocialLoginView):
    serializer_class = TwitterLoginSerializer
    adapter_class = TwitterOAuthAdapter


############################################################################
# SOCIAL MEDIA CONNECT
############################################################################


class FacebookConnect(SocialConnectView):
    adapter_class = FacebookOAuth2Adapter

class TwitterConnect(SocialConnectView):
    serializer_class = TwitterConnectSerializer
    adapter_class = TwitterOAuthAdapter