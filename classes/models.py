from django.db import models
from users.models import *
from uploads.models import *
from django.utils import timezone
import datetime as dt

class Notes(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE,  related_name='NotesOwner')
    title = models.CharField(max_length=150, blank=True, null=True, default='')
    description = models.TextField(max_length=1000, blank=True, null=True, default='')
    file = models.ManyToManyField(Files,blank=True, null=True) 
    date_updated = models.DateTimeField(default=timezone.now(), blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT,  related_name='NotesOwnerCreatedBy', blank=True,null=True)

class Assignment(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE,  related_name='AssignmentGroup')
    title = models.TextField(blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    deadline = models.CharField(max_length=20,blank=True, null=True)#yyyymmdd
    file = models.ManyToManyField(Files,blank=True, null=True) 
    date_updated = models.DateTimeField(default=timezone.now(), blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT,  related_name='AssignmentCreatedBy', blank=True,null=True)

class AssignmentSubmit(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    file = models.ManyToManyField(Files,blank=True, null=True) 
    date_updated = models.DateTimeField(default=timezone.now(), blank=True)
    student = models.ForeignKey(User, on_delete=models.PROTECT, blank=True,null=True)

class OnlineClassRoom(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    link = models.TextField(blank=True, null=True)
    password = models.TextField(blank=True, null=True)
    time = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20,blank=True, null=True)
    date_updated = models.DateTimeField(default=timezone.now(), blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT,  related_name='OnlineClassRoomCreatedBy', blank=True,null=True)

    # jwt = models.TextField(blank=True, null=True)
    # members = models.TextField(blank=True, null=True)
    # frame_details = models.TextField(blank=True, null=True)