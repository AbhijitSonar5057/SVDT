from django.urls import path, include
from account.views import UserRegistrationView, UserLoginView, UserLogoutView, ProjectView,PartsView,TaskView,TimesheetView,Get_All_User

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('project/', ProjectView.as_view(), name='project'),
    path('parts/', PartsView.as_view(), name='parts'),
    path('task/', TaskView.as_view(), name='task'),
    path('timesheet/',TimesheetView.as_view(),name='timesheet'),
    path('get_all_users/',Get_All_User.as_view()),


]
