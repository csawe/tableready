from django.urls import path
from .views import waitlist_view, waitlist_create, WaitlistUpdateView, message_view ,home 
app_name = 'main'

urlpatterns = [
    path('', home, name='home-view'),
    
    path('waitlist/', waitlist_view, name='waitlist-list'),
    path('waitlist_create/', waitlist_create, name='waitlist-create'),
    path('waitlist_update/<int:id>', WaitlistUpdateView.as_view(), name='waitlist-update' ),
        
    path('settings/', message_view, name='message-view'),
]

