from django.db import models
from authent.models import *

class TrackAssignee(models.Model):
    device_tb_id_fk = models.ForeignKey(Device, on_delete = models.CASCADE, null=True)