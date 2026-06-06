from django.contrib import admin
from .models import Expense, Income

# Register your models here.
admin.site.register(Income)
admin.site.register(Expense)

