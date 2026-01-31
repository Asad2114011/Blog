from django.contrib import admin
from .import models
# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',)}

admin.site.register(models.Author,AuthorAdmin)