from django.contrib import admin
from .models import Action, PartyType, States, TransitionManager , workevents , workflowitems , SignList 
# Register your models here.
from django.conf import settings



class CustomAdminModel(admin.ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        return obj is None or obj.pk != 1


class customadminforsign(admin.ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        return obj is None or obj.pk != 0
    

admin.site.register(TransitionManager)
admin.site.register(Action , CustomAdminModel )
admin.site.register(States)
admin.site.register(PartyType)
admin.site.register(SignList , customadminforsign)
admin.site.register(workflowitems)
admin.site.register(workevents)