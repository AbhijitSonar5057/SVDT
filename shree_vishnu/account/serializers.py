from rest_framework import serializers
from account.models import User,Project_db,Parts_db,Task_db,Timesheet_db




class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password','password2']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password is not same")
        
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    class Meta:
        model = User
        fields = ['username', 'password']


class UserlogoutSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    class Meta:
        model = User
        fields = ['username']

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project_db
        fields = '__all__'

class PartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parts_db
        fields = '__all__'



class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task_db
        fields = '__all__'

class TimesheetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Timesheet_db
        fields = '__all__'