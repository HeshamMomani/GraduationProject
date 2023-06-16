from datetime import datetime
from django.db import IntegrityError
from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from .models import service_Info, ReservationInfo, providerSchedule

from my_users.models import provider, Recipient
class Reservation_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationInfo
        fields = '__all__'

    def create(self, validated_data):
        service_id = validated_data.get('service_Info')
        recipient_id = validated_data.get('recipient')
        start_time = validated_data.get('start_time')
        end_time = validated_data.get('end_time')

        service_instance = service_Info.objects.get(pk=service_id.id)
        provider_instance = service_instance.provider
        start_time = start_time.strftime("%Y-%m-%dT%H:%M:%S")
        end_time = end_time.strftime("%Y-%m-%dT%H:%M:%S")

        if service_id and recipient_id:
            recipient_instance = Recipient.objects.get(pk=recipient_id.id)
            validated_data['service_Info'] = service_instance
            validated_data['recipient'] = recipient_instance
        else:
            raise serializers.ValidationError(
                "No ID (provider/recipient) was given.")

        # Check for overlapping reservations
        overlapping_reservations = ReservationInfo.objects.filter(
            service_Info__provider=provider_instance,
            start_time__lt=end_time,
            end_time__gt=start_time,
        )
        if overlapping_reservations.exists():
            raise serializers.ValidationError(
                "The requested time conflicts with a booked time.")

        try:
            reservation_info = ReservationInfo.objects.create(**validated_data)
            provider_schedule, _ = providerSchedule.objects.get_or_create(provider=provider_instance)
            provider_schedule.time_slots.create(start_time=start_time, end_time=end_time)
        except IntegrityError:
            raise serializers.ValidationError(
                "An error occurred while creating the reservation info.")

        return reservation_info
