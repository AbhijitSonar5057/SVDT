from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserLoginSerializer, UserRegistrationSerializer, UserlogoutSerializer,ProjectSerializer,PartSerializer,TaskSerializer,TimesheetSerializer
from django.contrib.auth import authenticate, logout
from rest_framework_simplejwt.tokens import RefreshToken
from account.models import *
from datetime import datetime
from django.http import JsonResponse


# Create your views here.

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({'msg':'Registration Success'}, status=status.HTTP_201_CREATED)
        
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserLoginView(APIView):
    def post(self, request, format=None):
        try:
            obj =  User.objects.all()
            for j in obj:
                serializer = UserLoginSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    username = serializer.data.get('username')
                    password = serializer.data.get('password')
                    
                    if j.username in username:
                        j.is_active=True
                        j.save()
                        user = authenticate(username=username, password=password)
                        token = get_tokens_for_user(j)

                        if user is not None:
                            return Response({'token':token,'msg':'Login Success','username':username}, status=status.HTTP_200_OK)
                        else:
                            print("&&&&&&&&&&&")
                            return Response({'non_field_errors':'name or password is not valid'}, status=status.HTTP_404_NOT_FOUND)
        except:
            print("Something else went wrong")

            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserLogoutView(APIView):
    def post(self, request, format=None):
        serializer = UserlogoutSerializer(data=request.data)
        obj =  User.objects.all()
        for i in obj:
            print(i.username)
            if serializer.is_valid(raise_exception=True):
                user = serializer.data.get('username')
                
                if i.username in user:

                    print(i,'~~~~~~~~~~>user')
                    i.is_active=False


                    i.save()
                    return Response({"msg":"log out"})

            else:
                return Response({'errors':{'non_field_errors':['name or password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
            
        return Response(status=status.HTTP_200_OK)


class ProjectView(APIView):
    def get(self,request, format=None):
        serializer = ProjectSerializer(data=request.data)
        obj=Project_db.objects.all()
        user = request.user
        # print(user,'~~~~~~~~~~~')
        for i in obj:
            for j in  i.emp.all():
                if j == user:
                    project_name=(i.project_name)

        return Response({'project_name':project_name}, status=status.HTTP_201_CREATED)

    def post(self, request, format=None):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.save()
            return Response({'msg':'Projects deatails add'}, status=status.HTTP_201_CREATED)
        
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PartsView(APIView):
    def post(self, request, format=None):
        serializer = PartSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.save()
            return Response({'msg':'Parts deatails add'}, status=status.HTTP_201_CREATED)
        
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskView(APIView):
    def post(self, request, format=None):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.save()
            return Response({'msg':'Parts deatails add'}, status=status.HTTP_201_CREATED)
        
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TaskView(APIView):
    def post(self, request, format=None):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.save()
            return Response({'msg':'Parts deatails add'}, status=status.HTTP_201_CREATED)
        
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TimesheetView(APIView):

    def post(self, request, format=None):
        check_in =  request.data.get("check_in")
        check_out =  request.data.get("check_out")
        check_in = datetime.strptime(check_in, '%y-%m-%d %H:%M:%S')
        check_out = datetime.strptime(check_out, '%y-%m-%d %H:%M:%S')

        # time = str(check_out - check_in)
        print(type(check_in),'~~~~~~~~~')
        user = request.user
        time_spent = 9
        user_id=User.objects.get(id=user.id)
        obj=Project_db.objects.all()
        obj1 = Task_db.objects.all()
        obj2 = Timesheet_db.objects.all()
        for i in obj:
            for j in  i.emp.all():
                if user == j:
                    project_id = (i.id)
                    project_obj = Project_db.objects.get(id=project_id)
        for i in obj1:
            # print(i.emp_id)
            if i.emp_id == user:
                parts_id = i.parts_id
                task_id = i.id
                task_obj = Task_db.objects.get(id =task_id )
                print(task_obj)
        
        data = {
            'punch_in':check_in,
            'project_id':project_obj,
            'task_id':task_obj,
            'time_spent':time_spent,
            'punch_out':check_out
            
        }
        
        # for data in obj2:
        #     data.emp_id = user_id
        #     data.projet_id = project_id
        #     data.parts_id = task_id
        # Timesheet_db(emp_id=user_id,projet_id=project_obj,parts_id=parts_id,task_id=task_obj,time_spent=time_spent,check_in=check_in,check_out=check_out).save()

        # for i in obj:
        #     if i in user_id:

        #         print(i.id)
        # for j in obj:
        #     if j.is_active:

        #         print('i am',j.username)
        # serializer = TimesheetSerializer(data=request.data)
        # if serializer.is_valid(raise_exception=True):
        #     data = serializer.save()
        #     return Response({'msg':'Parts deatails add'}, status=status.HTTP_201_CREATED)
        
        
        return Response( {'msg':'data added succusfully'}  ,status=status.HTTP_201_CREATED)