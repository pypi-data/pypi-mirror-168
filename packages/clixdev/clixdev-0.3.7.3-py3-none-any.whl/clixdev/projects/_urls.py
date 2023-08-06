from django.urls import path

from API.views import *

urlpatterns = [
	path('users/all/<d>', rcxxday),
]