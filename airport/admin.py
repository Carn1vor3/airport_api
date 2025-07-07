from django.contrib import admin

from airport.models import (
    Airport,
    Route,
    Crew,
    AirplaneType,
    Airplane,
    Order,
    Ticket,
    Flight,
)


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = [TicketInline]


admin.site.register(Airport)
admin.site.register(Route)
admin.site.register(Crew)
admin.site.register(AirplaneType)
admin.site.register(Airplane)
admin.site.register(Order, OrderAdmin)
admin.site.register(Ticket)
admin.site.register(Flight)
