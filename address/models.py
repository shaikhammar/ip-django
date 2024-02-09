from django.db import models
import cities_light
from cities_light.abstract_models import (AbstractCity, AbstractRegion,
            AbstractSubRegion, AbstractCountry, BaseManager)
from cities_light.receivers import connect_default_signals
from cities_light.settings import ICity


class Country(AbstractCountry):
    def __str__(self):
        display_name = getattr(self, 'name', None)
        if display_name:
            return display_name
        return self.name
connect_default_signals(Country)

class Region(AbstractRegion):
    
    def __str__(self):
        display_name = getattr(self, 'name', None)
        if display_name:
            return display_name
        return self.name
    
    
connect_default_signals(Region)

class SubRegion(AbstractSubRegion):
    def __str__(self):
        display_name = getattr(self, 'name', None)
        if display_name:
            return display_name
        return self.name
connect_default_signals(SubRegion)

class City(AbstractCity):
    modification_date = models.CharField(max_length=40)
    def __str__(self):
        display_name = getattr(self, 'name', None)
        if display_name:
            return display_name
        return self.name
connect_default_signals(City)



# def set_city_fields(sender, instance, items, **kwargs):
#     instance.modification_date = items[ICity.modificationDate]
# cities_light.signals.city_items_post_import.connect(set_city_fields)