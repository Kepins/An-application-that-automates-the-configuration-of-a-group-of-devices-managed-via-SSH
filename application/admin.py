from django.contrib import admin
from .models import Script


class ScriptAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


admin.site.register(Script, ScriptAdmin)
