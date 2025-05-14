from django.db.models import Count, Q, F
from registry.models import Person, JalaliRegistrationDate
from registry.decorators import log_function_run_time


class ReportService():
    
    @log_function_run_time
    @staticmethod
    def list_of_jalali_years():
        years = JalaliRegistrationDate.objects.values_list('year', flat=True).distinct().order_by('year')
        return list(years)
    
    @log_function_run_time
    @staticmethod
    def gender_counts():
        gender_counts = Person.objects.aggregate(
            male_count=Count('id', filter=Q(gender=0)),
            female_count=Count('id', filter=Q(gender=1)),
        )
        return gender_counts
    
    @log_function_run_time
    @staticmethod
    def count_of_registrations_by_month_and_week(year):
        registraions_by_month_and_week = (
            JalaliRegistrationDate.objects
            .filter(year=year) 
            .annotate(week=((F('day') - 1) / 7 + 1))
            .values('month', 'week')
            .annotate(
                total_count=Count('person'),
                male_count=Count('person', filter=Q(person__gender=0)),
                female_count=Count('person', filter=Q(person__gender=1)),
            )
        )

        result = {}
        for month in range(1, 13):
            result[month] = {
                'total_count': 0,
                'weeks': {
                    1: {'male_count': 0, 'female_count': 0},
                    2: {'male_count': 0, 'female_count': 0},
                    3: {'male_count': 0, 'female_count': 0},
                    4: {'male_count': 0, 'female_count': 0},
                }
            }
            
        for item in registraions_by_month_and_week:
            month = item['month']
            week = item['week']

            result[month]['total_count'] += item['total_count']

            result[month]['weeks'][week] = {
                'male_count': item['male_count'],
                'female_count': item['female_count'],
            }

        return result