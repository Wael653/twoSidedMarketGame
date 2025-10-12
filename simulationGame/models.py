from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class Supplier(models.Model):
    supplier_id = models.IntegerField()
    willingness_to_pay = models.FloatField(validators=[MinValueValidator(8), MaxValueValidator(30)])
    preference = models.CharField(max_length=1)
    travel_cost_to_A = models.FloatField(default=10, validators= [MinValueValidator(5),
            MaxValueValidator(100)])
    travel_cost_to_B = models.FloatField(default=10, validators= [MinValueValidator(5),
            MaxValueValidator(100)])

    def __str__(self):
        return f"ID:{self.supplier_id}, ZB:{self.willingness_to_pay}, Präferenz:{self.preference}"
    
class Buyer(models.Model):
    buyer_id = models.IntegerField()
    willingness_to_pay = models.FloatField(validators=[MinValueValidator(4), MaxValueValidator(15)])
    preference = models.CharField(max_length=1)
    out_door_pf = models.IntegerField(
           validators=[
            MinValueValidator(0),
            MaxValueValidator(13)
           ]
    )
    in_door_pf = models.IntegerField( default=0,
           validators=[
            MinValueValidator(0),
            MaxValueValidator(13)
           ]
    )

    def __str__(self):
        return f"ID:{self.buyer_id}, ZB:{self.willingness_to_pay}, Präferenz:{self.preference}"
