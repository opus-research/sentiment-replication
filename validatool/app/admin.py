from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Validation)
admin.site.register(Participation)
admin.site.register(Item)
admin.site.register(Answer)