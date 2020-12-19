from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime as dt
from users.models import *

class Files(models.Model):
    file=models.FileField(upload_to='files/')
    created_by=models.ForeignKey(User,on_delete=models.PROTECT)
    def __str__(self):
        return self.media