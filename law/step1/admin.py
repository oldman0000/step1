from django.contrib import admin # type: ignore
from .models import Venue, MyclubUser, Event
#from django.contrib.auth.models import Group # type: ignore



# Register your models here.

#admin.site.register(Venue)
admin.site.register(MyclubUser)
#admin.site.register(Event)


#admin.site.unregister(Group)



@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone')
    ordering = ('name',)
    search_fields = ('name', 'address')
    
    
    

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (('name', 'venue'), 'event_date', 'description', 'manager', 'approved')
    list_display = ('name', 'event_date', 'venue')
    list_filter = ('event_date', 'venue')
    ordering = ('event_date',)
   
    