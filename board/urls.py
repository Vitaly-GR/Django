from django.urls import path
from .views import index, other_page, by_category, bb_change, bb_delete
from .views import bb_create, BbLoginView, profile, BbLogoutView, ChangeUserInfoView, BbPasswordChange
from .views import RegisterUserView, RegisterDoneView, user_activate, DeleteUserView, detail

app_name = 'board'

urlpatterns = [
    path('', index, name='index'),
    path(' <str:page>/', other_page, name='other'),
    path('acoounts/profile/change/<str:slug>/', bb_change, name='bb_change'),
    path('accounts/profile/delete/<str:slug>/', bb_delete, name='bb_delete'),
    path('add/', bb_create, name='add'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/login/', BbLoginView.as_view(), name='login'),

    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),

    path('accounts/profile/', profile, name='profile'),
    path('accounts/logout/', BbLogoutView.as_view(), name='logout'),
    path('<str:category_slug>/<str:slug>/', detail, name='detail'),
    path('<str:category_slug>/', by_category, name='by_category'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/password/change/', BbPasswordChange.as_view(), name='password_change'),
    path('accounts/profile/delete/', DeleteUserView.as_view(), name='profile_delete')
]
