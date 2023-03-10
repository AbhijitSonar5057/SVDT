from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserLoginSerializer, UserRegistrationSerializer, UserlogoutSerializer,ProjectSerializer,PartSerializer,TaskSerializer,TimesheetSerializer
from django.contrib.auth import authenticate, logout,login
from account.models import *
from datetime import datetime
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class UserRegistrationView(APIView):
    """ 
        Register User....
    """
    serializer_class = UserRegistrationSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        username = request.data['username']
        password= request.data['password']
        if serializer.is_valid():
            user=serializer.save()
            authenticate(username=username, password=password)
            login(request,user)
            token = Token.objects.get_or_create(user=user)[0].key
            # resfresh = RefreshToken.for_user(user)
            # response_data = {'refresh':str(resfresh),'access':str(resfresh.access_token), "token": AuthToken.objects.create(user)[1]}
            response={
                    'token':token,
                    'msg':'User Registered Successfully',
                    'status':True
                }
            return Response(response,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        




class UserLoginView(APIView):
    """ 
        Login User....
    """
    def post(self, request, format=None):
        obj =  User.objects.all()
        # for j in obj:
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.data.get('username')
            password = serializer.data.get('password')
            user_username=User.objects.filter(username=username).first()
            if user_username:
                    user_username.is_active=True
                    user_username.save()
                    user = authenticate(username=username, password=password)
                    # User.is_active = True
                    # token = get_tokens_for_user(j)
                    token = Token.objects.get_or_create(user=user)[0].key
                    if user :
                        response={
                                'token':token,
                                'msg':'Login Success',
                                'status':True
                            }
                        return Response(response, status=status.HTTP_200_OK)
                    
                    else:
                        return Response({'errors':{'non_field_errors':['name or password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
            else:
                # Response("Something went wrong",status=status.HTTP_400_BAD_REQUEST)

                Response("Add valid Username",status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self, request, format=None):
        request.user.auth_token.delete()
        logout(request)
        return Response('User Logged out successfully')
      

class ProjectView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request, format=None):
        serializer = ProjectSerializer(data=request.data)
        obj=Project_db.objects.all()
        user = request.user
        for i in obj:
            for j in  i.emp.all():
                if j == user:
                    project_name=(i.project_name)

        return Response({'project_name':project_name}, status=status.HTTP_201_CREATED)

    def post(self, request, format=None):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # serializer.save()
            response={
                'msg':'Projects deatails add',
                 'data':serializer.data,
                'status':True
            }
            return Response(response, status=status.HTTP_201_CREATED)
        
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PartsView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self, request, format=None):
        serializer = PartSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response={
                'msg':'Parts deatails add',
                'data':serializer.data,
                'status':True
            }
            return Response(response, status=status.HTTP_201_CREATED)
        
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self, request, format=None):
       
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.save()
            response={
                'msg':'Task assigned successfully',
                'data':serializer.data,
                'status':True
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class Get_All_User(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self,request):
        check_in=request.data.get('check_in')
        check_out=request.data.get('check_out')
        if request.user.is_authenticated:
            print(request.user)
            # "check_in":"21-02-2021 18:46:00",
            # "check_out":"23-02-2021 18:46:00"
        
        check_in = datetime.strptime(check_in, "%d-%m-%Y %H:%M:%S")
        check_out = datetime.strptime(check_out, "%d-%m-%Y %H:%M:%S")

        hours_difference = abs(check_out - check_in).total_seconds() / 3600.0
        
        return Response("DONE")

class TimesheetView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    
    def post(self,request):
        try:
            #get current user
            current_user=request.user.id
            check_in_time=request.data.get('check_in')
            check_out_time=request.data.get('check_out')
            
            #convert check-in check-out in str to datetime object
            if check_in_time:
                check_in_str = datetime.strptime(str(check_in_time), "%Y-%m-%d %H:%M:%S")
            if check_out_time:
                check_out_str = datetime.strptime(str(check_out_time), "%Y-%m-%d %H:%M:%S")
        
            if check_in_time and not check_out_time:
                try:
                    time_sheet_obj=Timesheet_db.objects.get(check_in_time__contains=check_in_str.date())
                    if time_sheet_obj:
                        response={
                        'msg':'You Have Already Check In....',
                        'status':True
                    }
                    return Response(response)
                except:
                    time_sheet=Timesheet_db(check_in_time=check_in_time)
            if check_out_time: 
                try:
                    time_sheet=Timesheet_db.objects.get(check_in_time__contains=check_out_str.date())
                    if time_sheet:
                        #hours_for_the_day  
                        check_in_str = datetime.strptime(str(time_sheet.check_in_time)[:19], "%Y-%m-%d %H:%M:%S")
                        hours_difference = abs(check_in_str - check_out_str).total_seconds() / 3600.0
                        if int(hours_difference) < 9:
                            response={
                                'msg':'Please Complete Your working Hour  ....',
                                'status':False
                            }
                            return Response(response,status=status.HTTP_400_BAD_REQUEST)
                        time_sheet.check_out_time=check_out_time
                        time_sheet.hours_for_the_day=hours_difference
                except Exception:
                    response={
                        'msg':'Please Check In....',
                        'status':True
                    }
                    return Response(response,status=status.HTTP_400_BAD_REQUEST)
            time_sheet.save()
            time_sheet_obj=Timesheet_db.objects.get(id=time_sheet.id)
            # #add user
            user_obj=User.objects.get(id=current_user)
            if user_obj:
                time_sheet_obj.emp_id=user_obj
            
            # #add project data of employee
            project_obj=Project_db.objects.filter(emp__id=user_obj.id)
            if project_obj:
                for i in project_obj:
                    pr_obj=Project_db.objects.get(id=i.id)
                    if pr_obj:
                        time_sheet_obj.projet_id.add(pr_obj.id)
            #add parts data of employee
            parts_obj=Parts_db.objects.filter(emp_id__id=user_obj.id)
            if parts_obj:
                for i in parts_obj:
                    part_obj=Parts_db.objects.get(id=i.id)
                    if part_obj:
                        time_sheet_obj.parts_id.add(part_obj.id)
            # add task data of employee
            tasks_obj=Task_db.objects.filter(emp_id__id=user_obj.id)
            if task_obj:
                for i in tasks_obj:
                    task_obj=Task_db.objects.get(id=i.id)
                    if task_obj:
                        time_sheet_obj.task_id.add(task_obj.id)
            time_sheet_obj.save()
        
            response={
                'msg':"Timesheet added Sucessfully",
                'status':True
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response={
                'msg':"Something went wrong",
                'status':False
            } 
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
        
        
        
        
        
        
        
        
        #   obj2 = Timesheet_db.objects.filter()
        
        
    