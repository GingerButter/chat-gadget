from django.urls import path
from .views import dashboard, profile_list, profile, dashboardPost, streaming

app_name = "dwitter"

urlpatterns = [
    path("1/", dashboard, name="dashboard"),
    path("2/", dashboard, name="dashboard"),
    path("post/ajax/friend", dashboardPost, name="dashboardPost"),
    path("profile_list/", profile_list, name="profile_list"),
    path("profile/<int:pk>", profile, name="profile"),
    path("sss/", streaming, name="streaming")
]
