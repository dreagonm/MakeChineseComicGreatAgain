from django.conf.urls import url
from Login import views

urlpatterns = [
    url(r"^register/$", views.UserRegister.as_view()),
    url(r"^login/$", views.UserLogin.as_view()),
    url(r"^email/vary/$", views.EmailVaryView.as_view()),
    url(r"^email/find/$", views.EmailFindView.as_view()),

]

