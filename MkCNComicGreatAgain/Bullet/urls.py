from django.conf.urls import url
from Bullet import views

urlpatterns = [
    url(r"^bullet/$", views.BulletMessage.as_view()),
    url(r"^inform/$", views.Inform.as_view()),


]

