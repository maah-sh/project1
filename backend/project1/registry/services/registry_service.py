from registry.models import Person, PhoneNumber, Address

class RegistryService():
    
    @staticmethod
    def create_person_from_serialized_data(serialized_data):
        phone_numbers_data = serialized_data.pop('phone_numbers')
        addresses_data = serialized_data.pop('addresses')
        person = Person.objects.create(**serialized_data)
        
        for phone_number_data in phone_numbers_data:
            PhoneNumber.objects.create(person=person, **phone_number_data)

        for address_data in addresses_data:
            Address.objects.create(person=person, **address_data)
        
        return person
    
    @staticmethod
    def update_person_from_serialized_data(person, serialized_data):
        phone_numbers_data = serialized_data.pop('phone_numbers')
        addresses_data = serialized_data.pop('addresses')
        
        for attr, value in serialized_data.items():
            setattr(person, attr, value)
        person.save()

        phone_number_ids = set()
        address_ids = set()

        for phone_number_data in phone_numbers_data:
            if 'id' in phone_number_data and (phone_number_id := phone_number_data.pop('id')):
                phone_number_ids.add(phone_number_id)
                phone_number = person.phone_numbers.get(id=phone_number_id)
                for attr, value in phone_number_data.items():
                    setattr(phone_number, attr, value)
                phone_number.save()
            else:
                phone_number = PhoneNumber.objects.create(person=person, **phone_number_data)
                phone_number_ids.add(phone_number.id)

        for address_data in addresses_data:
            if 'id' in address_data and (address_id := address_data.pop('id')):
                address_ids.add(address_id)
                address = person.addresses.get(id=address_id)
                for attr, value in address_data.items():
                    setattr(address, attr, value)
                address.save()
            else:
                address = Address.objects.create(person=person, **address_data)
                address_ids.add(address.id)

        PhoneNumber.objects.filter(person=person).exclude(id__in=phone_number_ids).delete()
        Address.objects.filter(person=person).exclude(id__in=address_ids).delete()

        return person