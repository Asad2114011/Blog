from django.contrib import admin
from .import models
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug' :('name',)}

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',)}
    
admin.site.register(models.catagory,CategoryAdmin)
admin.site.register(models.Tag,TagAdmin)
