from django.shortcuts import get_object_or_404, render

# Create your views here.
from rest_framework.generics import GenericAPIView
from Booking.models import providerSchedule,ReservationInfo
from my_users.models import provider,Recipient
from .serializer import Service_Info_Serializer, Reservation_Serializer,TimeSlotSerializer 
from rest_framework.response import Response
from rest_framework import status

class RecipientBookedServices(GenericAPIView):
    def get (self,request):
        data = request.data
        Recipient_id = request.data['recipient']
        if not Recipient_id:
            return Response({'error': 'Recipient ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        resipient_instence = Recipient.objects.get(pk=Recipient_id)
        reservations =  ReservationInfo.objects.filter( recipient=resipient_instence)
        serializer = Reservation_Serializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class ListNewService(GenericAPIView):
    serializer_class = Service_Info_Serializer

    def post (self , request ):
        data = request.data 
        
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status = status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,status=status.HTTP_400_BAD_REQUEST
        )
    
class ListNewReservation(GenericAPIView):
    serializer_class = Reservation_Serializer

    def post(self , request ):
        data = request.data

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status = status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,status=status.HTTP_400_BAD_REQUEST
        )
    

    
    """
        """
    
class View_Provider_Booked_times(GenericAPIView):
    
    
    def get(self , request):
        data = request.data
        #serializer = provider_Schedule_Serializer(data=data)
        provider_id = request.data['provider']
        if not provider_id:
            return Response({'error': 'provider ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        #serializer VS request
        provider_instance = provider.objects.get(pk=provider_id)
        provider_schedule_instance = get_object_or_404(providerSchedule, provider=provider_instance)

        time_slots = provider_schedule_instance.TimeSlot.all()
        serializer = TimeSlotSerializer(time_slots, many=True)
        #time_slots = self.get_queryset(provider_instance)
        #serializer = self.get_serializer(time_slots, many=True)
        booked_times = provider_schedule_instance.TimeSlot.all()
        iterator = iter(serializer.data)
        l=[]
        

        while True:
            try:
                time_slot = next(iterator)
                l.append(time_slot)
            except StopIteration:
                break

        return Response(serializer.data, status=status.HTTP_200_OK)

