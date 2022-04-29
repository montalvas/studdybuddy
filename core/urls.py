from django.urls import path
from . import views


app_name = 'core'

urlpatterns = [
    # USER 
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('register/', views.register_page, name='register'),
        
    path('', views.home, name='home'),
    
    # CRUD ROOM
    path('room/<int:pk>', views.room, name='room'),
    path('create-room/', views.create_room, name='create-room'),
    path('update-room/<int:pk>', views.update_room, name='update-room'),
    path('delete-room/<int:pk>', views.delete_room, name='delete-room'),
    
    # MESSAGE
    path('delete-message/<int:pk>', views.delete_message, name='delete-message'),
]