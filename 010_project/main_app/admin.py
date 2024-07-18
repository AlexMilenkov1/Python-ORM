from django.contrib import admin
from main_app.models import Car


# Register your models here.
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['model', 'year', 'owner']

    @staticmethod
    def car_details(car: Car):
        try:
            owner_name = car.owner.name
        except AttributeError:
            owner_name = 'No owner'

        try:
            registration_number = car.registration.registration_number
        except AttributeError:
            registration_number = 'No registration number'

        return f"Owner: {owner_name}, Registration: {registration_number}"

    car_details.short_description = 'Car Details'
