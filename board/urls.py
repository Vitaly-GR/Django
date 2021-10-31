from django.urls import path
from .views import index, other_page, by_category
from .views import BbCreateView, BbLoginView, profile, BbLogoutView, ChangeUserInfoView, BbPasswordChange
app_name = 'board'

urlpatterns = [
    path('', index, name='index'),
    path(' <str:page>/', other_page, name='other'),
    path('<int:category_id>/', by_category, name='by_category'),
    path('add/', BbCreateView.as_view(), name='add'),
    path('accounts/login/', BbLoginView.as_view(), name='login'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/logout/', BbLogoutView.as_view(), name='logout'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/password/change/', BbPasswordChange.as_view(), name='password_change')
]
