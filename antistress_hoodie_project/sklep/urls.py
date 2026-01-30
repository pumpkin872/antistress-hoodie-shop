from django.urls import path, include
from . import views

urlpatterns = [
    path('people/', views.PersonList.as_view()),
    path('people/<int:pk>/', views.PersonDetail.as_view()),
]