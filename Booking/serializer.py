from datetime import datetime
from django.db import IntegrityError
from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from .models import TimeSlot, service_Info, ReservationInfo, providerSchedule
from my_users.models import provider, Recipient


class Service_Info_Serializer(serializers.ModelSerializer):
    class Meta:
        model = service_Info
        fields = '__all__'

    def create(self, validated_data):
        provider_id = validated_data.get('provider')
        if provider_id:
            provider_con = provider.objects.get(pk=provider_id.id)
            validated_data['provider'] = provider_con
        else:
            raise serializers.ValidationError("No ID was given.")

        try:
            service_info = service_Info.objects.create(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                "An error occurred while creating the service info.")
        return service_info

    def validate(self, attrs):
        if not attrs.get('price'):
            raise serializers.ValidationError("Price must be greater than 0.")
        return attrs


class Reservation_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationInfo
        fields = '__all__'

    def create(self, validated_data):

        service_id = validated_data.get('service_Info')
        recipient_id = validated_data.get('recipient')
        start_time = validated_data.get('start_time')
        end_time = validated_data.get('end_time')
        service_instence = service_Info.objects.get(pk=service_id.id)
        provider_id = service_instence.provider.id
        provider_instance = provider.objects.get(pk=provider_id)
        #start_time = start_time.strftime("%Y-%m-%dT%H:%M:%S")
        #end_time = end_time.strftime("%Y-%m-%dT%H:%M:%S")
        # start_time
        # end_time

        if service_id and recipient_id:
            service_instence = service_Info.objects.get(pk=service_id.id)
            recipient_instance = Recipient.objects.get(pk=recipient_id.id)
            validated_data['service_Info'] = service_instence
            validated_data['recipient'] = recipient_instance
        else:
            raise serializers.ValidationError(
                "No ID (provider/recipient) was given.")

        try:
            reservationInfo = ReservationInfo.objects.create(**validated_data)
            provider_schedule = providerSchedule.objects.get(provider=provider_instance)
            provider_schedule.TimeSlot.create(start_time=start_time, end_time=end_time,schedule=provider_schedule)

            """
            provider_id = service_instence.provider.id            
            providerSchedule.objects.get(
                provider=provider_instence).booked_time.append([start_time, end_time])
            providerSchedule.objects.get(provider=provider_instence).save()"""

        except IntegrityError:
            raise serializers.ValidationError(
                "An error occurred while creating the reservation Info.")
        return reservationInfo

    def validate(self, attrs):
        # validate time => check for schadual
        # start_time = validated_data.get('start_time')
        # end_time = validated_data.get('end_time')
        start_time = attrs.get('start_time')
        end_time = attrs.get('end_time')
        service_id = attrs.get('service_Info')
        service_instence = service_Info.objects.get(pk=service_id.id)
        provider_id = service_instence.provider.id
        provider_instence = provider.objects.get(pk=provider_id)
        # service_info = service_Info.objects.create(**validated_data)

        start_time = start_time.strftime("%Y-%m-%dT%H:%M:%S")
        end_time = end_time.strftime("%Y-%m-%dT%H:%M:%S")
        
        try:
            provider_schedule = providerSchedule.objects.get(provider=provider_instence)
            booked_times = provider_schedule.TimeSlot.all()
        except providerSchedule.DoesNotExist:
            provider_schedule = providerSchedule.objects.create(provider=provider_instence)
            provider_schedule.save()
                
        try:
                booked_times = provider_schedule.TimeSlot.all()
                if booked_times.count :
                    pass
                else : raise IndexError
                first_time_slot = booked_times.first()
        except : raise IndexError    

        # compare  now the start and end time with booked time
        booked_times = provider_schedule.time_slots.all()
        iterator = iter(booked_times)

        while True:
            try:
                time_slot = next(iterator)
                booked_start_time = time_slot.start_time.strftime("%Y-%m-%dT%H:%M:%S")
                booked_end_time =time_slot.end_time.strftime("%Y-%m-%dT%H:%M:%S")
                if start_time < booked_end_time and end_time > booked_start_time:
                    raise serializers.ValidationError("The requested time is not available.")
            except StopIteration:
                break
        
        """""
        for booked_time in booked_times:
            
            booked_start_time = booked_time.start_time.strftime("%Y-%m-%dT%H:%M:%S")

            booked_end_time =booked_time.end_time.strftime("%Y-%m-%dT%H:%M:%S")

            if start_time < booked_end_time and end_time > booked_start_time:
                raise serializers.ValidationError("The requested time is not available.")
"""
        
        
        return attrs
    

    '''
        '''
    '''


    existing_reservations = ReservationInfo.objects.filter(
            service_Info=service_instence,
            start_time__lte=end_time,
            end_time__gte=start_time
        )
        if existing_reservations.exists():
            raise serializers.ValidationError("The requested time conflicts with an existing reservation.")
    bus = Bus.objects.get(id=request.data['travel_id']
    def create(self, validated_data):
        return service_Info.objects.create(**validated_data)
    
    
    def validate(self, attrs):
        return super().validate(attrs)

        def create(self, validated_data):
        provider = self.context['request'].user  # Get the current user as the provider
        validated_data['provider'] = provider  # Set the provider field with the current user
        try:
            booking = service_Info.objects.create(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError("An error occurred while creating the booking.")
        return booking

        def create(self, validated_data):
        provider = self.context['request'].user  # Get the current user as the provider
        validated_data['provider'] = provider  # Set the provider field with the current user
        service_info = service_Info.objects.create(**validated_data)
        return service_info

        
        def create(self, validated_data):
        validated_data['provider'] = None  # Set the provider field to None
        service_info = service_Info.objects.create(**validated_data)
        return service_info


        def create(self, validated_data):
        provider_id = self.context['request'].data.get('provider_id')  # Get the provider_id from the request data
        if provider_id:
            validated_data['provider_id'] = provider_id  # Set the provider_id field with the value from the request
        else: raise  serializers.ValidationError("no id was given ")   
        try:
            booking = service_Info.objects.create(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError("An error occurred while creating the booking.")
        return booking


        def create(self, validated_data):
        provider_id = validated_data.get('provider_id')  # Get the provider_id from the validated data
        if provider_id:
            validated_data['provider_id'] = provider_id  # Set the provider_id field with the value from the validated data
        else:
            raise serializers.ValidationError("No ID was given.")
        
        try:
            service_info = service_Info.objects.create(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError("An error occurred while creating the service info.")
        return service_info

         def create(self, validated_data):
        service_id = validated_data.get('service_Info')

        if service_id:
            service_con = service_Info.objects.get(pk=service_id)
            validated_data['service_Info'] = service_con
        else:
            raise serializers.ValidationError("No ID was given.")
        try:
            reservation_info = ReservationInfo.objects.create(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                "An error occurred while creating the reservation info.")
        return reservation_info



        def create(self, validated_data):
        service_instance = validated_data.get('service_Info')
        if service_instance:
            service_id = service_instance.id
            validated_data['service_Info'] = service_id
        else:
            raise serializers.ValidationError("No ID was given.")
        try:
            reservation_info = ReservationInfo.objects.create(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError("An error occurred while creating the reservation info.")
        return reservation_info


        def create(self, validated_data):
        service_instance = validated_data.pop('service_Info')
        if service_instance:
            validated_data['service_Info_id'] = service_instance.id
        else:
            raise serializers.ValidationError("No service_Info was given.")
        try:
            reservation_info = ReservationInfo.objects.create(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError("An error occurred while creating the reservation info.")
        return reservation_info
    
    def validate(self, attrs):
        return attrs

    '''


class TimeSlotSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimeSlot
        fields = '__all__'

""""


class provider_Schedule_Serializer(serializers.ModelSerializer):
    TimeSlot = TimeSlotSerializer(many=True)

    class Meta:
        model = providerSchedule
        fields = '__all__'

class Resrevation2Serializer(serializers.ModelSerializer):

    class Meta :
        model = ReservationInfo

                fields = "__all__"
                """