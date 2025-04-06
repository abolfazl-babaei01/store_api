from django.contrib import admin
from .models import Ticket, TicketMessage

# Register your models here.

admin.site.register(Ticket)
admin.site.register(TicketMessage)
