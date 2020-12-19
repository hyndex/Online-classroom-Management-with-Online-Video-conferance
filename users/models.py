from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime as dt


class Plan(models.Model):
    price = models.DecimalField(max_digits=6, decimal_places=2,default=0)
    name = models.CharField(max_length=20, blank=True, null=True)
    max_group = models.IntegerField(default=0)
    max_group_member = models.IntegerField(default=0)
    date_created = models.DateTimeField(default=timezone.now(), blank=True)
    
    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.OneToOneField(Plan, on_delete=models.PROTECT,blank=True, null=True)
    phone = models.CharField(max_length=20, blank=False, null=True, default = '')
    subscribed = models.CharField(max_length=20, blank=False, null=True, default = 'False')
    image = models.ImageField(upload_to='User/',blank=True, null=True)
    date_renewed = models.DateTimeField(blank=True,null=True)
    date_expiry = models.DateTimeField(blank=True,null=True)
    
    def __str__(self):
        return self.user.username

class Invoice(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100, blank=False, null=True,default='None')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, blank=False, null=True, default = 'Unpaid')
    date_created = models.DateTimeField(default=timezone.now(), blank=True)
    date_updated = models.DateTimeField(default=timezone.now(), blank=True)
    
class Group(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='Group/',blank=True, null=True)
    students=models.ManyToManyField(User,related_name='GroupStudents')
    join_link = models.TextField(blank=True, null=True)
    date_updated = models.DateTimeField(default=timezone.now(), blank=True)
    createdBy = models.ForeignKey(User,on_delete=models.PROTECT)
    
    def __str__(self):
        return self.name


class GroupRole(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    group = models.ForeignKey(Group,on_delete=models.CASCADE)
    role = models.TextField(default='student')
    date_updated = models.DateTimeField(default=timezone.now(), blank=True)
    
    def __str__(self):
        return self.user.username

class GroupInvitation(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    group = models.ForeignKey(Group,on_delete=models.CASCADE)
    role = models.TextField(default='student')
    joined = models.TextField(default='false') # if reject then delete the instance
    date_updated = models.DateTimeField(default=timezone.now(), blank=True)
    
    def __str__(self):
        return self.user.username


