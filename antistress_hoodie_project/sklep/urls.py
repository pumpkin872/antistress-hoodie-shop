from django.urls import path, include
from . import views

urlpatterns = [
#    path("welcome/", views.welcome_view),
    path('people/', views.person_list),
    path('people/<int:pk>/', views.person_detail),
    path('positions/', views.position_list),
    path('positions/<int:pk>/', views.position_detail),

    path('html/people/', views.person_list_html, name='people-list'),
    path('html/person/<int:id>/', views.person_detail_html, name='person-details'),
    path('html/person/add/', views.person_create_html, name='person-create'),
    path('html/person/add_django/', views.person_create_django_form, name='person-create-django'),


    path('html/positions/', views.position_list_html, name='positions-list'),
    path('html/position/<int:id>/', views.position_detail_html, name='position-details'),
    path('html/position/add/', views.position_create_django_form, name='position-create-django'),
]