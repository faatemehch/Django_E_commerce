from django.urls import path
from account_module import views

app_name = 'account_module'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('user-account/', views.UserAccountView.as_view(), name='user-account'),
    path('edit-account/', views.edit_user_info, name='edit-account'),
    path('active-account/<active_code>', views.activation_account_view, name='active_account')
]
