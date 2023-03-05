from django.db import models

# Create your models here.
class SSID(models.Model):
    name = models.CharField(max_length=100)
    network = models.CharField(max_length=50)
    authentication = models.CharField(max_length=100)
    encryption = models.CharField(max_length=20)
    max_signal = models.IntegerField(null=True)
    is_connected = models.BooleanField(null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-is_connected', '-max_signal']

class BSSID(models.Model):
    BSSID = models.CharField(max_length=20)
    signal = models.IntegerField()
    radio = models.CharField(max_length=50)
    band = models.CharField(max_length=50)
    channel = models.IntegerField()
    SSID = models.ForeignKey(SSID, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.SSID.name + self.BSSID
