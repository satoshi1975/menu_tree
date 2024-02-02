from django.urls import path
from main import views

urlpatterns = [
    path('menu-item/<str:section_name>', views.any_section )
    
]
