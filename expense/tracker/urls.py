from django.urls import path
from tracker.views import *

urlpatterns = [
    path('', index, name ="index"),
    path('registration/',registration,name="registration"),
    path('login/',login_page,name="login"),
    path('logout/',logout_page,name="login"),
    path('delete-transaction/<uid>/',deleteTransaction, name ="deleteTransaction")
]