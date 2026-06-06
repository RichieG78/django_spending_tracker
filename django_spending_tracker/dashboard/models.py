from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse # Change here

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self): # Change here
        return reverse('post-detail', kwargs={'pk': self.pk}) # Change here to bring the user to the post detail view


    
class Expense(models.Model):
    """Tracks every outgoing payment with the amount, type, and owner."""

    name = models.CharField(max_length=255)
    currency = models.CharField(max_length=3, default='EUR')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    frequency = models.CharField(max_length=20, default='monthly')
    date = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=20, default='fixed')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')

    class Meta:
        db_table = 'expenses'

    def __str__(self):
        return f'{self.name} ({self.amount} {self.currency})'
    
class Income(models.Model):
    """Stores every money-in event so we can compare it with expenses."""

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    currency = models.CharField(max_length=3, default='EUR')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    frequency = models.CharField(max_length=20, default='monthly')
    date = models.DateTimeField(default=timezone.now)
    gross_net = models.CharField(max_length=10, default='net')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incomes')

    class Meta:
        db_table = 'incomes'

    def __str__(self):
        return f'{self.name} ({self.amount} {self.currency})'