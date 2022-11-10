from django.db import models
import uuid
from datetime import datetime

from insuree.apps import InsureeConfig
from insuree import models as insuree_models
from location import models as location_models

# Create your models here.
class InsureeAuth(models.Model):
    insuree = models.OneToOneField(insuree_models.Insuree, on_delete=models.DO_NOTHING,
                                db_column='InsureeID', blank=True, null=True, related_name="verified_insurees")
    token = models.CharField(max_length=300)
    otp = models.CharField(max_length=10, null=True, blank=True)
    password = models.CharField(max_length=50)

    def __str__(self):
        name = ''
        if self.insuree.other_names:
            name= self.insuree.other_names
        return name

class Notice(models.Model):
    #id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    active = models.BooleanField(default=True)
    created_at =  models.DateTimeField(verbose_name='date added', auto_now_add=True)
    updated_at =   models.DateTimeField(verbose_name='date updated', auto_now_add=True)
    
    def __str__(self):
        return self.title

class HealthFacilityCoordinate(models.Model):
    id = models.AutoField(db_column='hfcId', primary_key=True)
    uuid = models.CharField(db_column='hfcUUID',
                            max_length=36, default=uuid.uuid4, unique=True)
    health_facility = models.ForeignKey(
        location_models.HealthFacility, models.DO_NOTHING, db_column='HFID')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    
def generate_voucher_number():
    return datetime.now().strftime('%Y%m%d%H%M%S')

class VoucherPayment(models.Model):
    insuree = models.ForeignKey(insuree_models.Insuree, on_delete=models.DO_NOTHING,
                                db_column='InsureeID', blank=True, null=True, related_name="voucher_payment_insurees")
    voucher = models.FileField(upload_to="insuree_voucher")
    vocher_id = models.CharField(max_length=50, default=generate_voucher_number()) #this will be always unique
    is_entry = models.BooleanField(default=False)
    created_at =  models.DateTimeField(verbose_name='date added', null=True, auto_now_add=True)
    updated_at =   models.DateTimeField(verbose_name='date updated', null=True, auto_now_add=True)    
    

class Feedback(models.Model):
    fullname = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=15)
    email_address = models.EmailField(max_length=50, unique=False)
    queries = models.CharField(max_length=500)
    created_at =  models.DateTimeField(verbose_name='date added', null=True, auto_now_add=True)

    def __str__(self):
        return self.fullname

class Notification(models.Model):
    insuree = models.ForeignKey(insuree_models.Insuree, on_delete=models.CASCADE, related_name="insuree_nofification")
    chf_id = models.CharField(max_length=100, null=True)
    message = models.CharField(max_length=200)
    created_at =  models.DateTimeField(verbose_name='date added', null=True, auto_now_add=True)

from django.db.models.signals import post_save, post_delete, pre_save

class Profile(models.Model):
    insuree = models.ForeignKey(insuree_models.Insuree, on_delete=models.CASCADE, related_name="self_registration_insuree_profile")
    phone = models.CharField(max_length=15, null=True)
    photo = models.ImageField(upload_to="insuree/photo")
    email = models.EmailField(null=True)
    created_at = models.DateTimeField(verbose_name='date added', null=True, auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='date added', null=True, auto_now_add=True)


class InsureeTempReg(models.Model):
    json = models.TextField()
    is_approved = models.BooleanField(default=False)
    name_of_head = models.CharField(max_length=100, null=True, blank=True)
    card_id = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    is_approved = models.BooleanField(default=False, blank=True)
    is_hold = models.BooleanField(default=False, blank=True)
    is_rejected = models.BooleanField(default=False, blank=True)
    status_message = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='date added', null=True, auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='date added', null=True, auto_now_add=True)


class ChfidTempInsuree(models.Model):
    chfid = models.CharField(max_length=100)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(verbose_name='date added', null=True, auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='date added', null=True, auto_now_add=True)

    def __str__(self):
        return self.chfid

class Config(models.Model):
    key = models.CharField(max_length=150)
    value = models.CharField(max_length=1500)
    def __str__(self):
        return self.chfid


