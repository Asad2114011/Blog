from django.contrib import admin
from .models import Question,Answer
# Register your models here.

class questionAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('title',)}

admin.site.register(Question,questionAdmin)
admin.site.register(Answer)
