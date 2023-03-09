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
# @api_view(["POST"])
# @permission_classes([AllowAny])
class UserRegistrationView(APIView):
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
            response_data={"msg":"register Success","token":token}
            return Response(response_data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        




class UserLoginView(APIView):
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
                        
                        return Response({'token':token,'msg':'Login Success'}, status=status.HTTP_200_OK)
                    
                    else:
                        return Response({'errors':{'non_field_errors':['name or password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
            else:
                # Response("Something went wrong",status=status.HTTP_400_BAD_REQUEST)

                Response("Add valid Username",status=status.HTTP_204_NO_CONTENT)

            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self, request, format=None):
        request.user.auth_token.delete()
        logout(request)
        return Response('User Logged out successfully')
      

class ProjectView(APIView):
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
    
    def post(self, request, format=None):
        check_in =  request.data.get("check_in")
        check_out =  request.data.get("check_out")
        user = request.user
        time_spent = ""
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
                
        if check_out:
            print("check_out",check_out)
            timeobj = Timesheet_db.objects.all()
            for i in timeobj:
                if user_id == i.emp_id:
                    d = i.check_in
                    datetime_str = str(d)
                    old_format = '%Y-%m-%d %H:%M:%S'
                    new_format = '%d-%m-%Y %H:%M:%S'
                    new_datetime_str = datetime.strptime(datetime_str, old_format).strftime(new_format)
                    checkout_datetime_str = datetime.strptime(check_out, old_format).strftime(new_format)
                    check_in_str = datetime.strptime(new_datetime_str, "%d-%m-%Y %H:%M:%S")
                    check_out_str = datetime.strptime(checkout_datetime_str, "%d-%m-%Y %H:%M:%S")
                    hours_difference = abs(check_out_str -check_in_str).total_seconds() / 3600.0
                    print(hours_difference,'gjhgjgjhgjhgg')
                    if hours_difference >= 9:
                        print(" i am 9")
                        i.check_out = check_out
                        i.time_spent = hours_difference
                        i.save()  
                        return Response ( {'msg':f'{user} Your check out  '}  ,status=status.HTTP_201_CREATED)
                    else:
                        print("i am esle")
                        return Response ( {'msg':f'{user} Your check out time is not done '}  ,status=status.HTTP_201_CREATED)
            print("i am check_out")

        if check_in:
            print(" i am in check_in")
            for i in obj2:
                # print(" i am in check_in 1qqqqqqqqq", i.emp_id)
                print("i am else for if ",user_id,i.emp_id)

                user_emp =  i.emp_id
                if user_id not in user_emp:
                    pass
                    # print("i am else for if ",user_id,i.emp_id)
                    # Timesheet_db(emp_id=user_id,projet_id=project_obj,parts_id=parts_id,task_id=task_obj,time_spent=time_spent,check_in=check_in,check_out=check_out).save()

                if user_id == i.emp_id:
                    # print(" i am check value 1" , user_id,i.emp_id)

                    if i.check_in != None:
                        i.check_in = check_in
                        i.save()
                        # print(" i am check value")
                    else:
                        # print("i am mahesh esle")
                        # i.emp_id = user_id
                        # i.projet_id = project_obj
                        # i.parts_id = parts_id
                        # i.task_id =task_obj
                        # i.time_spent = time_spent
                        i.check_in = check_in
                        # i.check_out = check_out
                        i.save()
                        # Timesheet_db(emp_id=user_id,projet_id=project_obj,parts_id=parts_id,task_id=task_obj,time_spent=time_spent,check_in=check_in,check_out=check_out).save()
                # if user_id != i.emp_id:
                #     print("i am else for if ")
                #     Timesheet_db(emp_id=user_id,projet_id=project_obj,parts_id=parts_id,task_id=task_obj,time_spent=time_spent,check_in=check_in,check_out=check_out).save()
                # break
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
        
        
        return Response( {'msg':f'{user} Check_in'}  ,status=status.HTTP_201_CREATED)