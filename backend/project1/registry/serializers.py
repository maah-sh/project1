from rest_framework import serializers
from .models import Person, PhoneNumber, Address

class PhoneNumberListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        person = instance
        phone_number_ids = set()
        for phone_number_data in validated_data:
            if 'id' in phone_number_data and (phone_number_id := phone_number_data.pop('id')):
                phone_number_ids.add(phone_number_id)
                phone_number = person.phone_numbers.get(id=phone_number_id)
                for attr, value in phone_number_data.items():
                    setattr(phone_number, attr, value)
                phone_number.save()
            else:
                phone_number = PhoneNumber.objects.create(person=person, **phone_number_data)
                phone_number_ids.add(phone_number.id)
        PhoneNumber.objects.filter(person=person).exclude(id__in=phone_number_ids).delete()
        
        return person.phone_numbers


class PhoneNumberSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    class Meta:
        model = PhoneNumber
        fields = ['id', 'phone_number']
        list_serializer_class = PhoneNumberListSerializer


class AddressListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        person = instance
        address_ids = set()
        for address_data in validated_data:
            if 'id' in address_data and (address_id := address_data.pop('id')):
                address_ids.add(address_id)
                address = person.addresses.get(id=address_id)
                for attr, value in address_data.items():
                    setattr(address, attr, value)
                address.save()
            else:
                address = Address.objects.create(person=person, **address_data)
                address_ids.add(address.id)
        Address.objects.filter(person=person).exclude(id__in=address_ids).delete()

        return person.addresses


class AddressSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    class Meta:
        model = Address
        fields = ['id', 'title', 'description']
        list_serializer_class = AddressListSerializer


class PersonSerializer(serializers.ModelSerializer):
    phone_numbers = PhoneNumberSerializer(many=True)
    addresses = AddressSerializer(many=True)

    class Meta:
        model = Person
        fields = ['id', 'first_name', 'last_name', 'gender', 'registration_date', 'phone_numbers', 'addresses']

    def create(self, validated_data):
        phone_numbers_data = validated_data.pop('phone_numbers')
        addresses_data = validated_data.pop('addresses')
        person = Person.objects.create(**validated_data)
        
        phone_number_serializer = PhoneNumberSerializer(data=phone_numbers_data, many=True)
        phone_number_serializer.is_valid()
        phone_number_serializer.save(person = person)

        address_serializer = AddressSerializer(data=addresses_data, many=True)
        address_serializer.is_valid()
        address_serializer.save(person = person)
        
        return person
    
    def update(self, instance, validated_data):
        person = instance
        phone_numbers_data = validated_data.pop('phone_numbers')
        addresses_data = validated_data.pop('addresses')
        
        for attr, value in validated_data.items():
            setattr(person, attr, value)
        person.save()

        phone_number_serializer = PhoneNumberSerializer(instance=person, data=phone_numbers_data, many=True)
        phone_number_serializer.is_valid()
        phone_number_serializer.save()

        address_serializer = AddressSerializer(instance=person, data=addresses_data, many=True)
        address_serializer.is_valid()
        address_serializer.save()

        return person
        


class RegistrationDateReportSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        representation = {
            month: {
                'total_count': 0,
                'weeks': {week : {'male_count': 0, 'female_count': 0} for week in range(1, 5)}
            } for month in range(1,13)
        }
            
        for item in instance:
            month = item.get('month')
            week = item.get('week')
            representation[month]['total_count'] += item.get('total_count', 0)
            representation[month]['weeks'][week] = {
                'male_count': item.get('male_count', 0),
                'female_count': item.get('female_count', 0),
            }
        
        return representation






