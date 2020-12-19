from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.permissions import BasePermission
from django.db.models import Q
from users.models import *

class GroupPermission(BasePermission):
    message='You are not authorized to this data'
    def has_permission(self, request, view):
        SAFE_METHOD = ['GET','POST','PUT','DELETE']
        if request.method not in SAFE_METHOD:
            return False
        if (request.user.username == 'admin'):
                return True
        if request.user.is_authenticated:
            if request.method == 'POST':
                groups=Group.objects.filter(createdBy=request.user)
                profileExist=Profile.objects.filter(user=request.user)
                if profileExist.count()==0:
                    user=User.objects.get(username=request.user.username)
                    free=Plan.objects.get(name='Free')
                    profile=Profile.objects.create(user=user,plan=free)
                    return True
                else:
                    profile=profileExist[0]
                    groups=Group.objects.filter(createdBy=request.user)
                    if profile.plan.max_group >= groups.count():
                        return True
                return False
            if request.method in ['GET','DELETE','PUT']:
                return True
        return False
    def has_object_permission(self, request, view, obj):
        if request.user.username=='admin':
            return True
        if request.method == 'GET':
            return True  
        if request.method in ['DELETE','PUT']:
            if obj.createdBy == request.user:
                return True            
        return False

def GroupQuerySet(request):
    if (request.user.username == 'admin'):
        return Group.objects.all()
    
    grouprole=GroupRole.objects.filter(user=request.user)
    if grouprole.count()>0:
        queries = [Q(id=member.group.id) for member in grouprole]
        query = queries.pop()
        for item in queries:
            query |= item
        group=Group.objects.filter(Q(createdBy=request.user) | query)
    else:
        group=Group.objects.filter(Q(createdBy=request.user))

    if request.method == 'GET':
        return group
    if request.method in ['PUT','DELETE']:
        return group.filter(createdBy=request.user)
    return Group.objects.none()

class PlanPermission(BasePermission):
    message='You are not authorized to this data'
    def has_permission(self, request, view):
        SAFE_METHOD = ['GET']
        if request.method not in SAFE_METHOD:
            return False
        if request.method == 'GET':
            return True
        return False

class InvoicePermission(BasePermission):
    message='You are not authorized to this data'
    def has_permission(self, request, view):
        SAFE_METHOD = ['GET','PUT','DELETE']
        if request.method not in SAFE_METHOD:
            return False
        if request.user.is_authenticated:
            if (request.user.username == 'admin'):
                return True
            if request.method in ['POST']:
                try:
                    plan=request.data["plainid"]
                    plan=Plan.objects.filter(id=plan)
                    if plan.count()>0:
                        return True
                except:
                    self.message='No Plans exist by this id'
                    return False
            if request.method=='GET':
                return True
        return False

def InvoiceQuerySet(request):
    if (request.user.username == 'admin'):
        return Invoice.objects.all()
    if request.method in ['GET']:
        return Invoice.objects.filter(profile__user__username=request.user.username)
    return Invoice.objects.none()

class GroupJoinLinkPermission(BasePermission):
    message='You are not authorized to this data'
    def has_permission(self, request, view):
        SAFE_METHOD = ['GET','PUT','DELETE']
        if request.method not in SAFE_METHOD:
            return False
        if request.user.is_authenticated:
            if (request.user.username == 'admin'):
                return True
            if request.method in ['GET','DELETE','PUT']:
                return True
        return False
    def has_object_permission(self, request, view, obj):
        if request.user.username=='admin':
            return True
        if request.method in ['GET','DELETE','PUT']:
            if obj.createdBy == request.user:
                return True            
        return False

def GroupJoinLinkQuerySet(request):
    if (request.user.username == 'admin'):
        return Group.objects.all()
    if request.method in ['GET','PUT','DELETE']:
        return Group.objects.filter(createdBy=request.user)
    return Group.objects.none()



class GroupRolePermission(BasePermission):
    message='You are not authorized to this data'
    def has_permission(self, request, view):
        SAFE_METHOD = ['GET','POST','PUT','DELETE']
        if request.method not in SAFE_METHOD:
            return False
        if request.user.is_authenticated:
            if (request.user.username == 'admin'):
                return True
            if request.method in ['GET','DELETE']:
                return True
            if request.method == 'POST':
                try:
                    groupid=request.data["groupid"]
                    group=Group.objects.filter(id=groupid)
                    if group.count()>0:
                        group=group[0]
                        if group.createdBy == request.user:
                            members=GroupRole.objects.filter(group=group).count()
                            profileExist=Profile.objects.filter(user=request.user)
                            if profileExist.count()==0:
                                user=User.objects.get(username=request.user.username)
                                try:
                                    free=Plan.objects.get(name='Free')
                                except:
                                    free=Plan.objects.create(name='Free',price=float(0),max_group=5,max_group_member=30)
                                profile=Profile.objects.create(user=user,plan=free)
                                return True
                            else:
                                profile=profileExist[0]
                                if profile.plan.max_group_member >= members:
                                    return True
                                
                            return True
                        else:
                            return False
                    else:
                        return False
                except:
                    return False                
            else:
                return False
        return False
    def has_object_permission(self, request, view, obj):
        if request.user.username=='admin':
            return True
        if request.method in ['DELETE','GET']:
            if obj.group.createdBy.user == request.user:
                return True         
            elif obj.user == request.user:
                return True   
        return False

def GroupRoleQuerySet(request):
    if (request.user.username == 'admin'):
        return GroupRole.objects.all()

    if request.method in ['GET','DELETE']:
        group=GroupRole.objects.filter(Q(group__createdBy=request.user) | Q(user=request.user))
        return group
    return GroupRole.objects.none()