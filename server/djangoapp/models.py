import datetime
from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30, default='Bmw')
    description = models.CharField(null=False, max_length=300, default='Freude am Fahren')
    def __str__(self):
        return "Name: " + self.name + ", " + \
               "Description: " + self.description


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    BERLINA = 'berlina'
    CROSSOVER = 'crossover'
    STATION = 'station'
    CITY_CAR = 'city_car'
    LUXURY_CAR = 'luxury_car'
    OTHER = 'other'
    CAR_CHOICES = [(BERLINA, "berlina"), (CROSSOVER, 'crossover'), (STATION, 'station'), (CITY_CAR, 'city_car'), (LUXURY_CAR, 'luxury_car'), (OTHER, 'other')]
    carmake = models.ForeignKey(CarMake, null= True, on_delete=models.CASCADE)
    name = models.CharField(null= False, max_length=30, default='Bmw Serie 1')
    dealer_id = models.IntegerField(null=True)
    car_type = models.CharField(
        null=False, max_length=15, choices=CAR_CHOICES, default=BERLINA)

    YEAR_SELECT = []
    for r in range(1969, (datetime.datetime.now().year+1)):
        YEAR_SELECT.append((r, r))

    year = models.IntegerField(
        ('year'), choices=YEAR_SELECT, default=datetime.datetime.now().year)

    def __str__(self):
        return self.name + ", " + str(self.year) + ", " + self._type

    def __str__(self):
        return 'Name ' + self.name


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip
    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
