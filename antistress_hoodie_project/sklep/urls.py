from django.urls import path, include
from . import views

urlpatterns = [
    path('people/', views.person_list),
    path('people/<int:pk>/', views.person_detail),
]