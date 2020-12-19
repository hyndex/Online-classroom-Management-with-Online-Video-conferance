from rest_framework import serializers
from rest_framework import exceptions
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import string 
import random 
from hashlib import sha256
from .models import *
from .permissions import *



class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields='__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=('username','email')
        write_only_fields=('password',)



class GroupRoleSerializerforGroup(serializers.ModelSerializer):
    class Meta:
        model = GroupRole
        fields='__all__'
        read_only_fields=('date_updated','group','user')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields=('id','name','description','image','createdBy','date_updated')
        read_only_fields=('date_updated','image','createdBy')
    
    def create(self, validated_data):
        username=self.context['request'].user.username
        teacher = User.objects.get(username=username)
        profileExist=Profile.objects.filter(user__username=username)
        if profileExist.count()==0:
            user=User.objects.get(username=username)
            free=Plan.objects.get(name='Free')
            profile=Profile.objects.create(user=user,plan=free)
                
        group=Group.objects.create(
                    name=validated_data.pop('name'),
                    description=validated_data.pop('description'),
                    createdBy=teacher
                    )
        return group

class GroupJoinLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields=('id','join_link')
        read_only_fields=('join_link',)

    def update(self, instance, validated_data):
        instance.join_link=str(instance.id)+''.join(random.choices(string.ascii_uppercase + string.digits, k = 50))
        instance.save()
        return instance

class InvoiceSerializer(serializers.ModelSerializer):
    planid = serializers.CharField(max_length=None, min_length=None,write_only=True)
    class Meta:
        model = Invoice
        fields=('id','profile','plan','planid','payment_id','price','status','date_created')
        read_only_fields=('profile','plan','price','status','payment_id','date_created')
    
    def create(self, validated_data):
        user=self.context['request'].user
        profile=Profile.objects.get(user = user)
        plan=validated_data.pop('planid')
        plan=Plan.objects.filter(id=plan)[0]            
        price=plan.price
        invoice=Invoice.objects.create(price=price,plan=plan,profile=profile,date_created=dt.datetime.now(),status='Unpaid',payment_id='None')
        return invoice

class GroupRoleSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=None, min_length=None,write_only=True)
    groupid = serializers.CharField(max_length=None, min_length=None,write_only=True)
    group=GroupSerializer(read_only=True)
    user=UserSerializer(read_only=True)
    class Meta:
        model = GroupRole
        fields=('id','username','groupid','group','user','role','date_updated')
        read_only_fields=('date_updated','group','user')
    
    def create(self, validated_data):
        username=self.context['request'].user.username
        user=validated_data.pop('username')
        user=User.objects.filter(username=user)
        group=validated_data.pop('groupid')
        role=validated_data.pop('role')
        if not role.lower() in ['student','teacher']:
            role='student'
        group=Group.objects.filter(id=group , createdBy__username=username)
        if group.count()==1 and user.count()==1:
                exist=GroupRole.objects.filter(group=group[0],user=user[0])
                if exist.count()>0:
                    return exist
                grouprole=GroupRole.objects.create(
                        group=group[0],
                        user=user[0],
                        role=role
                        )
        try:
            return grouprole
        except:
            return GroupRole.objects.none()

