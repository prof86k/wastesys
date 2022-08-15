from django.urls import path


from . import views as vi 


app_name = 'accounts'
urlpatterns = [  
    path('',vi.user_login,name='user_login'),
    path('create-account',vi.user_account_creation,name='create_account'),
    path('dashboard',vi.dashboard,name='dashboard'),
    path('my/dashboard',vi.users_dashboard,name='user_dashboard'),
    path('profile/<int:user_id>',vi.profile,name='profile'),
    path('update/profile/<int:user_id>',vi.update_profile,name='update_profile'),
    path('all-users',vi.display_all_users,name='show_users'),
    path('delete/user/<int:user_id>',vi.delete_user_account,name='delete_user'),
    path('logout-user',vi.user_logout,name='user_logout')
]