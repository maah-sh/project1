from rest_framework import serializers
from .models import Person, PhoneNumber, Address
from registry.services.registry_service import RegistryService


class PhoneNumberSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    class Meta:
        model = PhoneNumber
        fields = ['id', 'phone_number']


class AddressSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    class Meta:
        model = Address
        fields = ['id', 'title', 'description']


class PersonSerializer(serializers.ModelSerializer):
    phone_numbers = PhoneNumberSerializer(many=True)
    addresses = AddressSerializer(many=True)

    class Meta:
        model = Person
        fields = ['id', 'first_name', 'last_name', 'gender', 'registration_date', 'phone_numbers', 'addresses']

    def create(self, validated_data):
        person = RegistryService.create_person_from_serialized_data(serialized_data=validated_data)
        return person
    
    def update(self, instance, validated_data):
        person = RegistryService.update_person_from_serialized_data(person=instance, serialized_data=validated_data)
        return person
        







