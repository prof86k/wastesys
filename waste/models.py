from django.db import models
from accounts import models as acmdl
# Create your models here.

class WasteLocation(models.Model):
    ''' 
    @ the administrator add places they can collect waste from
    @ The location of the waste can be found (chamba east) and some digital address
    '''
    location        = models.CharField(verbose_name='Waste Location:',max_length=255,null=True,blank=True)
    digital_address = models.CharField(verbose_name='Digital Address:',max_length=255,null=True,blank=True)
    gps_latitude    = models.CharField(verbose_name='Gps Latitude:',max_length=255,null=True,blank=True)
    gps_longitude   = models.CharField(verbose_name='Gps Longitude:',max_length=255,null=True,blank=True)
    date_created    = models.DateTimeField(auto_now_add=True)
    date_updated    = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.location

    class Meta:
        managed = True
        verbose_name = 'WasteLocation'
        verbose_name_plural = 'WasteLocations'

class WasteType(models.Model):
    '''
    @ the administrator adds the type of waste they can collect
    @ What type of waste we collect
    '''
    title       = models.CharField(verbose_name='Waste Type:',max_length=255,null=True,blank=True) #liquid,plastic etc
    date_created    = models.DateTimeField(auto_now_add=True)
    date_updated    = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        managed = True
        verbose_name = 'WasteType'
        verbose_name_plural = 'WasteTypes'

class DustBin(models.Model):
    ''' 
    @ The container of the waste bin
    @ A user goes fill up the bin with
    @ location
    @ and the type of waste
    @ filled and ready bin are turned on by the user and a notification is sent to the administrator
    @ the administrator collects the bin and marks it collected
    @ the administrator returns the bin and marks it return and the bin is ready to collect next waste
    @ the user add the gps location of the bin.
    @ the bin is collected if the payment has been made.
    '''
    user            = models.ForeignKey(acmdl.User,on_delete=models.CASCADE,related_name='user_waste_locations')
    location        = models.ForeignKey(WasteLocation,on_delete=models.CASCADE,related_name='waste_dustbins')
    waste_type      = models.ForeignKey(WasteType,on_delete=models.CASCADE,related_name='waste_types')
    bin_label       = models.CharField(verbose_name='Bin Label:',max_length=255,null=True,blank=True)
    digital_address = models.CharField(verbose_name='Digital Address:',max_length=255,null=True,blank=True)
    gps_latitude    = models.CharField(verbose_name='Gps Latitude:',max_length=255,null=True,blank=True)
    gps_longitude   = models.CharField(verbose_name='Gps Longitude:',max_length=255,null=True,blank=True)
    bin_ready       = models.BooleanField(default=False)
    bin_collected   = models.BooleanField(default=False)
    payment_made    = models.BooleanField(default=False)
    empty_bin       = models.BooleanField(default=True)
    date_created    = models.DateTimeField(auto_now_add=True)
    date_updated    = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.bin_label

    class Meta:
        managed = True
        verbose_name = 'Dustbin'
        verbose_name_plural = 'Dustbins'


class WasteSettings(models.Model):
    '''
    @ The administrator gives the price of waste collection by
    @ general payment of waste collection
    @ the location price
    @ the waste type price
    '''
    location        = models.OneToOneField(WasteLocation,on_delete=models.CASCADE,related_name='location_setting')
    waste_type      = models.OneToOneField(WasteType,on_delete=models.CASCADE,related_name='waste_type_setting')
    settings_title  = models.CharField(verbose_name='Setting Title:',max_length=255,default='Waste Payment Plan')
    dues            = models.DecimalField(verbose_name='Amount Payable:',max_digits=20,decimal_places=2)
    date_created    = models.DateTimeField(auto_now_add=True)
    date_updated    = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.settings_title

    class Meta:
        managed = True
        verbose_name = 'WasteSetting'
        verbose_name_plural = 'WasteSettings'
