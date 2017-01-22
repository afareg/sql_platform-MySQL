from django.db import models

# Create your models here.
class Saltrecord(models.Model):
    user = models.CharField(max_length=30)
    operation = models.CharField(max_length=50)
    jid = models.CharField(max_length=255,db_index=True)
    # Field renamed because it was a Python reserved word.
    return_field = models.TextField(db_column='return')
    create_time = models.DateTimeField()
    class Meta:
        db_table = 'salt_record'