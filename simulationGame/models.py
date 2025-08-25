from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class Supplier(models.Model):
    supplier_id = models.IntegerField()
    willingness_to_pay = models.FloatField()
    preference = models.CharField(max_length=1)
    travel_cost_to_A = models.FloatField(default=10, validators= [MinValueValidator(5),
            MaxValueValidator(30)])
    travel_cost_to_B = models.FloatField(default=10, validators= [MinValueValidator(5),
            MaxValueValidator(30)])

    def __str__(self):
        return f"ID:{self.supplier_id}, ZB:{self.willingness_to_pay}, Präferenz:{self.preference}"
    
class Buyer(models.Model):
    buyer_id = models.IntegerField()
    willingness_to_pay = models.FloatField()
    preference = models.CharField(max_length=1)
    out_door_pf = models.IntegerField(
           validators=[
            MinValueValidator(0),
            MaxValueValidator(8)
           ]
    )
    in_door_pf = models.IntegerField( default=0,
           validators=[
            MinValueValidator(0),
            MaxValueValidator(8)
           ]
    )

    def __str__(self):
        return f"ID:{self.buyer_id}, ZB:{self.willingness_to_pay}, Präferenz:{self.preference}"
