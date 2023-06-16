from .views import ListNewService,ListNewReservation,View_Provider_Booked_times,RecipientBookedServices

from django.urls import path

urlpatterns = [
    # path(book),
    path('newService', ListNewService.as_view() ),
    path('newReservation', ListNewReservation.as_view() ), 
    path('providebooked',View_Provider_Booked_times.as_view()),
    path ('returnRecipintReservations',RecipientBookedServices.as_view() )
    
]
