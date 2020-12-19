from rest_framework import serializers
from rest_framework import exceptions
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import string 
import random 
from hashlib import sha256
import datetime as dt
from .models import *
from .permissions import *
from users.serializers import *


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields='__all__'


class NotesSerializer(serializers.ModelSerializer):
    file=FileSerializer(read_only=True, many=True)
    group=GroupSerializer(read_only=True)
    groupid=serializers.CharField(write_only=True)
    class Meta:
        model = Notes
        fields=('id','groupid','group','title','description','file')
        read_only_fields=('date_updated','group','created_by','file')
        
    def create(self, validated_data):
        username = self.context['request'].user.username
        group = validated_data.pop('groupid')
        date_updated=str(dt.datetime.now())
        user=User.objects.get(username=username)
        group=Group.objects.get(id=group)
        notes = Notes.objects.create(created_by=user,group=group,date_updated=date_updated,**validated_data)
        return notes

    def update(self, instance, validated_data):
        instance.title=validated_data.get('title',instance.title)
        instance.description=validated_data.get('description',instance.description)
        instance.date_updated=dt.datetime.now()
        instance.save()
        return instance

class AssignmentSerializer(serializers.ModelSerializer):
    file=FileSerializer(read_only=True, many=True)
    group=GroupSerializer(read_only=True)
    groupid=serializers.CharField(write_only=True)
    class Meta:
        model = Assignment
        fields=('id','groupid','group','title','description','deadline','file','created_by','date_updated')
        read_only_fields=('date_updated','created_by','file')

    def create(self, validated_data):
        username = self.context['request'].user.username
        group = validated_data.pop('groupid')
        date_updated=str(dt.datetime.now())
        user=User.objects.get(username=username)
        group=Group.objects.get(id=group)
        assignment = Assignment.objects.create(created_by=user,date_updated=date_updated,group=group,**validated_data)
        return assignment

    def update(self, instance, validated_data):
        instance.title=validated_data.get('title',instance.title)
        instance.description=validated_data.get('description',instance.description)
        instance.deadline=validated_data.get('deadline',instance.deadline)
        instance.date_updated=dt.datetime.now()
        instance.save()
        return instance

class AssignmentSubmitSerializer(serializers.ModelSerializer):
    file=FileSerializer(read_only=True, many=True)
    assignment=AssignmentSerializer(read_only=True)
    assignmentid=serializers.CharField(write_only=True)
    class Meta:
        model = AssignmentSubmit
        fields=('id','assignmentid','assignment','title','description','file','student','date_updated')
        read_only_fields=('date_updated','student','file')
    
    def create(self, validated_data):
        username = self.context['request'].user.username
        assignment = validated_data.pop('assignmentid')
        user=User.objects.get(username=username)
        assignment=Assignment.objects.get(id=assignment)
        #################################################
        # group=assignment.group
        # member=GroupRole.objects.filter(group=group,user=user)
        # if member.count()<1:
        #     return 
        #################################################
        date_updated=dt.datetime.now()
        instance=AssignmentSubmit.objects.filter(student=user,assignment=assignment)
        if instance.count()>0:
            instance=instance[0]
            instance.title=validated_data.get('title',instance.title)
            instance.description=validated_data.get('description',instance.description)
            instance.save()
            return instance
        ass_submit = AssignmentSubmit.objects.create(date_updated=date_updated,student=user,assignment=assignment,**validated_data)
        return ass_submit

    def update(self, instance, validated_data):
        instance.title=validated_data.get('title',instance.title)
        instance.description=validated_data.get('description',instance.description)
        instance.date_updated=dt.datetime.now()
        instance.save()
        return instance





class OnlineClassRoomSerializer(serializers.ModelSerializer):
    group=GroupSerializer(read_only=True)
    groupid=serializers.CharField(write_only=True)
    class Meta:
        model = OnlineClassRoom
        fields=('id','groupid','group','link','password','time','status','created_by','date_updated')
        read_only_fields=('date_updated','link','password','time','status','created_by','group')

    def create(self, validated_data):
        username = self.context['request'].user.username
        group = validated_data.pop('groupid')
        time=str(dt.datetime.now().year)+str(dt.datetime.now().month)+str(dt.datetime.now().day)+str(dt.datetime.now().hour)+str(dt.datetime.now().minute)
        user=User.objects.get(username=username)
        password = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 50))
        link = sha256((str(dt.datetime.now())+str(username)+str(password)).encode('utf-8')).hexdigest()
        group=Group.objects.get(id=group)
        existingRoom=OnlineClassRoom.objects.filter(created_by=user,status='open').update(status='close')
        room = OnlineClassRoom.objects.create(created_by=user,status='open',time=time,link=link,group=group,password=password)
        return room

