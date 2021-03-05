

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import uuid


class User(AbstractUser):
    pass

class Transaction(models.Model):
    uuid = models.CharField(default=uuid.uuid4, editable=True, unique=True, max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created  = models.DateTimeField(editable=True, default=timezone.now)
    modified  = models.DateTimeField(editable=True, default=timezone.now)
    category = models.CharField(max_length=200, default="")
    debit = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    description = models.CharField(max_length=200, default="")

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Transaction, self).save(*args, **kwargs)

