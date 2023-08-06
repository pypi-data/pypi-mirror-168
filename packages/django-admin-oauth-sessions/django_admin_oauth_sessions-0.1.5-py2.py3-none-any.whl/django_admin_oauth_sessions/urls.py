from django.urls import path
from . import views
urlpatterns  = [
    path("denied/" , views.access_denied_view , name = "access_denied"),
]