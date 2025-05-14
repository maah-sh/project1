from django.db import models
import jdatetime


class Person(models.Model):
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_CHOICES = [
        (GENDER_MALE, 'Male'), 
        (GENDER_FEMALE, 'Female')
        ]
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.IntegerField(choices=GENDER_CHOICES)
    registration_date = models.DateField()


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        jalali_registration_date = jdatetime.date.fromgregorian(date=self.registration_date)

        JalaliRegistrationDate.objects.update_or_create(
            person=self,
            defaults={
                'year': jalali_registration_date.year,
                'month': jalali_registration_date.month,
                'day': jalali_registration_date.day,
            }
        )


class PhoneNumber(models.Model):
    person = models.ForeignKey(Person, related_name='phone_numbers', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)


class Address(models.Model):
    person = models.ForeignKey(Person, related_name='addresses', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()


class JalaliRegistrationDate(models.Model):
    person = models.ForeignKey(Person, related_name='jalali_registration_date', on_delete=models.CASCADE, primary_key=True)
    year = models.PositiveSmallIntegerField()
    month = models.PositiveSmallIntegerField()
    day = models.PositiveSmallIntegerField()
