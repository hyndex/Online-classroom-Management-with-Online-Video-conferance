from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.permissions import BasePermission
from django.db.models import Q
from hashlib import sha256
import datetime as dt
from .models import *


class NotesPermission(BasePermission):
    message='You are not authorized to this data'
    def has_permission(self, request, view):
        SAFE_METHOD = ['GET','POST','PUT','DELETE']
        if request.method not in SAFE_METHOD:
            return False
        if request.user.is_authenticated:
            if request.method == 'POST':
                try:
                    groupid=request.data["groupid"]
                    membership=GroupRole.objects.filter(group__id=groupid,user=request.user,role='teacher')
                    owner=Group.objects.filter(id=groupid,createdBy=request.user)
                    if owner.count()>0 or membership.count()>0 :
                        return True
                    return False
                except:
                    pass
                return False
            if (request.user.username == 'admin'):
                return True
            if request.method in ['GET','DELETE','PUT']:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method=='GET':
            return True
        if request.user.username=='admin':
            return True
        if request.method in ['DELETE','PUT']:
            if obj.created_by == request.user:
                return True            
        return False

def NotesQuerySet(request):
    if (request.user.username == 'admin'):
        return Notes.objects.all()
    
    membership=GroupRole.objects.filter(user=request.user,role='student')
    if membership.count()>0:
        queries = [Q(group__id=member.group.id) for member in membership]
        query = queries.pop()
        for item in queries:
            query |= item
        notes=Notes.objects.filter(Q(created_by=request.user) | query)
    else:
        notes=Notes.objects.filter(created_by=request.user)

    if request.method == 'GET':
        return notes
    if request.method in ['PUT','DELETE']:
        return notes.filter(created_by=request.user)
    return Notes.objects.none()

class AssignmentPermission(BasePermission):
    message='You are not authorized to this data'
    def has_permission(self, request, view):
        SAFE_METHOD = ['GET','POST','PUT','DELETE']
        if request.method not in SAFE_METHOD:
            return False
        if request.user.is_authenticated:
            if request.method == 'POST':
                try:
                    groupid=request.data["groupid"]
                    membership=GroupRole.objects.filter(group__id=groupid,user=request.user,role='teacher')
                    owner=Group.objects.filter(id=groupid,createdBy=request.user)
                    if owner.count()>0 or membership.count()>0 :
                        return True
                    return False
                except:
                    pass
                return False
            if (request.user.username == 'admin'):
                return True
            if request.method in ['GET','DELETE','PUT']:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method=='GET':
            return True
        if request.user.username=='admin':
            return True
        if request.method == 'GET':
            return True
        if request.method in ['DELETE','PUT']:
            if obj.created_by == request.user:
                return True            
        return False

def AssignmentQuerySet(request):
    if (request.user.username == 'admin'):
        return Assignment.objects.all()

    membership=GroupRole.objects.filter(user=request.user,role='student')
    if membership.count()>0:
        queries = [Q(group__id=member.group.id) for member in membership]
        query = queries.pop()
        for item in queries:
            query |= item

        assignment=Assignment.objects.filter(Q(created_by=request.user) | query)
    else:
        assignment=Assignment.objects.filter(created_by=request.user)
    if request.method == 'GET':
        return assignment
    if request.method in ['PUT','DELETE']:
        return assignment.filter(created_by=request.user)
    return Assignment.objects.none()


class AssignmentSubmitPermission(BasePermission):
    message='You are not authorized to this data'
    def has_permission(self, request, view):
        SAFE_METHOD = ['GET','POST','PUT','DELETE']
        if request.method not in SAFE_METHOD:
            return False
        if request.user.is_authenticated:
            if request.method == 'POST':
                try:
                    assignmentid=request.data["assignmentid"]
                    group=Assignment.objects.filter(id=assignmentid).group
                    membership=GroupRole.objects.filter(group=group,user=request.user)
                    if membership.count()>0:
                        return True
                    else:
                        return False
                except:
                    return False####################or True
                assignment=Assignment.objects.filter(id=assignmentid)
                if not assignment.count()>0:
                    return False
                assignment=assignment[0]
                group=assignment.group.id
                if GroupRole.objects.filter(user=request.user,group__id=group).count()>0:
                    deadline=int(assignment.deadline.replace("-",""))
                    today=dt.date.today()
                    if int(str(today.year)+str(today.month)+str(today.day)) > deadline:
                        return False
                    return True
            if (request.user.username == 'admin'):
                return True
            if request.method in ['GET','DELETE','PUT']:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method=='GET':
            return True
        if request.method in ['DELETE','PUT']:
            if obj.student.user == request.user:
                deadline=obj.assignment.deadline.replace("-","")
                today=dt.date.today()
                if  int(str(today.year)+str(today.month)+str(today.day)) < int(deadline):
                    return True            
        return False


def AssignmentSubmitQuerySet(request):
    if (request.user.username == 'admin'):
        return AssignmentSubmit.objects.all()
    assignment=AssignmentSubmit.objects.filter(Q(student=request.user) | Q(assignment__created_by=request.user))
    if request.method in ['PUT','DELETE']:
        return assignment.filter(student=request.user)
    if request.method == 'GET':
        return assignment
    return AssignmentSubmit.objects.none()



class OnlineClassRoomPermission(BasePermission):
    message='You are not authorized to this data'
    def has_permission(self, request, view):
        SAFE_METHOD = ['GET','POST','PUT','DELETE']
        if request.method not in SAFE_METHOD:
            return False
        if request.user.is_authenticated:
            if request.method == 'POST':
                try:
                    groupid=request.data["groupid"]
                    membership=GroupRole.objects.filter(group__id=groupid,user=request.user,role='teacher')
                    owner=Group.objects.filter(id=groupid,createdBy=request.user)
                    if owner.count()>0 or membership.count()>0 :
                        return True
                    return False
                except:
                    pass
                return False
            if (request.user.username == 'admin'):
                return True
            if request.method in ['GET','DELETE']:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.username=='admin':
            return True
        if request.method == 'GET':
            return True
        if request.method in ['DELETE']:
            if obj.created_by == request.user or obj.group.createdBy == request.user:
                return True            
            group=obj.group
            membership=GroupRole.objects.filter(role='teacher',group=group,user=request.user)
            if membership.count()>0:
                time=int(obj.time)
                now=str(dt.datetime.now().year)+str(dt.datetime.now().month)+str(dt.datetime.now().day)+str(dt.datetime.now().hour)+str(dt.datetime.now().minute)
                now=int(now)
                if time + 300 < now:
                    return True
        return False

def OnlineClassRoomQuerySet(request):
    if (request.user.username == 'admin'):
        return OnlineClassRoom.objects.all()

    membership=GroupRole.objects.filter(user=request.user,role='student')
    if membership.count()>0:
        queries = [Q(group__id=member.group.id) for member in membership]
        query = queries.pop()
        for item in queries:
            query |= item

        room=OnlineClassRoom.objects.filter(Q(created_by=request.user) | query)
    else:
        room=OnlineClassRoom.objects.filter(created_by=request.user)
    if request.method == 'GET':
        return room
    if request.method == 'DELETE':
        return room
        # return room.filter(created_by=request.user)
    return OnlineClassRoom.objects.none()
