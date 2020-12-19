from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import FormParser, MultiPartParser,JSONParser, FileUploadParser
from rest_framework.decorators import action
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
import datetime as dt


class NotesViewSet(viewsets.ModelViewSet):
    queryset = Notes.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    search_fields = ['title','description','group__id','group__name']
    filterset_fields = ['group__id','group__name']
    ordering_fields = ['title','created_by','date_updated']
    ordering=('-date_updated',)
    # filter_fields = ['name','category','instructor','institute']
    serializer_class = NotesSerializer
    permission_classes = [NotesPermission]
    model=serializer_class().Meta().model
    def get_queryset(self):
        return NotesQuerySet(self.request)

class NotesUploadView(APIView):
    parser_classes = (MultiPartParser,JSONParser)
    def put(self, request, pk, format=None):
        if request.user.is_authenticated:
            if (request.user.username == 'admin'):
                instance=Notes.objects.get(id=pk)
                up_file  = request.FILES['file']
                up_file.name=str(instance.id)+'.'+str(up_file.name).split(".")[-1]
                file=Files.objects.create(file=up_file,created_by=request.user)
                instance.file.add(file)
                instance.save()
                Response({"file":up_file.name},status=204)
            if request.method == 'PUT':
                note=Notes.objects.filter(created_by=request.user,id=pk)  
                if note.count()>0 :
                    if request.method=='PUT':
                        instance=note[0]
                        up_file  = request.FILES['file']
                        up_file.name=str(instance.id)+'.'+str(up_file.name).split(".")[-1]
                        file=Files.objects.create(file=up_file,created_by=request.user)
                        instance.file.add(file)
                        instance.save()
                        return Response({"file":up_file.name},status=204)
                else:
                    return Response({"not found"},status=404)
    def delete(self, request, pk, format=None):
        if request.user.is_authenticated:
            if request.method == 'DELETE':
                instance=Notes.objects.filter(created_by=request.user,file__id=pk)
                if instance.count()>0 :
                    instance=instance[0]
                    delete_instance=Files.objects.get(id=pk)
                    instance.file.remove(delete_instance)
                    delete_instance.delete()
                    return Response({"file":"success"},status=204)
            return Response({"not found"},status=404)
                

                    




class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    search_fields = ['title','description','group__id','group__name','deadline','created_by__username']
    ordering_fields = ['title','created_by','group__id','group__name','date_updated','deadline']
    filterset_fields = ['title','created_by__username','group__id','group__name','date_updated','deadline']
    ordering=('-date_updated',)
    # filter_fields = ['name','category','instructor','institute']
    serializer_class = AssignmentSerializer
    permission_classes = [AssignmentPermission]
    model=serializer_class().Meta().model
    def get_queryset(self):
        return AssignmentQuerySet(self.request)

class AssignmentUploadView(APIView):
    parser_classes = (MultiPartParser,JSONParser)
    
    def put(self, request, pk, format=None):
        if request.user.is_authenticated:
            if (request.user.username == 'admin'):
                instance=Assignment.objects.get(id=pk)
                up_file  = request.FILES['file']
                up_file.name=str(instance.id)+'.'+str(up_file.name).split(".")[-1]
                file=Files.objects.create(file=up_file,created_by=request.user)
                instance.file.add(file)
                instance.save()
                Response({"file":up_file.name},status=204)
            if request.method == 'PUT':
                assignment=Assignment.objects.filter(created_by=request.user,id=pk)
                if assignment.count()>0 :
                    if request.method=='PUT':
                        instance=assignment[0]
                        up_file  = request.FILES['file']
                        up_file.name=str(instance.id)+'.'+str(up_file.name).split(".")[-1]
                        file=Files.objects.create(file=up_file,created_by=request.user)
                        instance.file.add(file)
                        instance.save()
                        return Response({"file":up_file.name},status=204)
                else:
                    return Response({"not found"},status=404)
    def delete(self, request, pk, format=None):
        if request.user.is_authenticated:
            if request.method == 'DELETE':
                instance=Assignment.objects.filter(created_by=request.user,file__id=pk)
                if instance.count()>0 :
                    instance=instance[0]
                    delete_instance=Files.objects.get(id=pk)
                    instance.file.remove(delete_instance)
                    delete_instance.delete()
                    return Response({"file":"success"},status=204)
                return Response({"not found"},status=404)




class AssignmentSubmitViewSet(viewsets.ModelViewSet):
    queryset = AssignmentSubmit.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    search_fields = ['title','description','assignment__id','assignment__group__name','assignment__deadline','assignment__created_by__username','student__username','student__name','student__phone']
    ordering_fields = ['assignment__id','assignment__group__name','assignment__deadline','assignment__created_by__username','date_updated']
    ordering=('-date_updated',)
    # filter_fields = ['name','category','instructor','institute']
    serializer_class = AssignmentSubmitSerializer
    permission_classes = [AssignmentSubmitPermission]
    model=serializer_class().Meta().model
    def get_queryset(self):
        return AssignmentSubmitQuerySet(self.request)


class AssignmentSubmitUploadView(APIView):
    parser_classes = (MultiPartParser,JSONParser)
    def put(self, request, pk, format=None):
        if request.user.is_authenticated:
            if (request.user.username == 'admin'):
                instance=AssignmentSubmit.objects.get(id=pk)
                up_file  = request.FILES['file']
                up_file.name=str(instance.id)+'.'+str(up_file.name).split(".")[-1]
                file=Files.objects.create(file=up_file,created_by=request.user)
                instance.file.add(file)
                instance.save()
                Response({"file":up_file.name},status=204)
            if request.method == 'PUT':
                assignment=AssignmentSubmit.objects.filter(assignment__group__students__username=request.user.username,id=pk)
                if assignment.count()>0 :
                    instance=assignment[0]
                    up_file  = request.FILES['file']
                    up_file.name=str(instance.id)+'.'+str(up_file.name).split(".")[-1]
                    file=Files.objects.create(file=up_file,created_by=request.user)
                    instance.file.add(file)
                    instance.save()
                    Response({"file":up_file.name},status=204)
                else:
                    return Response({"not found"},status=404)
    def delete(self, request, pk, format=None):
        if request.user.is_authenticated:
            if request.method == 'DELETE':
                today=dt.datetime.now()
                today=int(str(today.year)+str(today.month)+str(today.day))
                instance=AssignmentSubmit.objects.filter(created_by=request.user,file__id=pk)
                try:
                    deadline=int(instance.assignment.deadline.replace("-",""))
                except:
                    deadline=today+1
                if instance.count()>0 and (deadline<=today):
                    instance=instance[0]
                    delete_instance=Files.objects.get(id=pk)
                    instance.file.remove(delete_instance)
                    delete_instance.delete()
                    Response({"file":"success"},status=204)
                else:
                    if instance.count()==0:
                        return Response({"Not found"},status=404)
                    else:
                        return Response({"Deadline passed"},status=403)




class OnlineClassRoomViewSet(viewsets.ModelViewSet):

    queryset = OnlineClassRoom.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    search_fields = ['group__id','group__name','status']
    filterset_fields = ['group__id','group__name','status']
    ordering=('-date_updated',)
    serializer_class = OnlineClassRoomSerializer
    permission_classes = [OnlineClassRoomPermission]
    model=serializer_class().Meta().model
    def get_queryset(self):
        return OnlineClassRoomQuerySet(self.request)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.status='close'
            instance.save()
            return Response({'closed'}, status=204)
        except:
            pass
        return Response(status=400)