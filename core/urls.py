from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('upload_resume',views.resume_upload, name='upload_resume'),
    path('suggestions',views.suggestions, name='suggestions'),
    path('composemail',views.composemail, name='composemail')
]