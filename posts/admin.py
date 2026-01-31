from django.contrib import admin
from .import models
# Register your models here.
class postAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('title',)}
    
admin.site.register(models.Post,postAdmin)
admin.site.register(models.Comment)
admin.site.register(models.Like)
admin.site.register(models.Bookmark)