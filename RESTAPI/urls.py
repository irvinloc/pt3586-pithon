from django.urls import path
from .views import UserListView, UserDetailListView,UserDetailView,UserDetailDetailView

urlpatterns = [
    path('user/', UserListView.as_view(), name="user_list"),
    path('user_detail/', UserDetailListView.as_view(), name="user_detail_list"),
    path('user/<int:pk>', UserDetailView.as_view(),name="user"),
    path('user_detail/<int:pk>', UserDetailDetailView.as_view(),name="user_detail"),
]