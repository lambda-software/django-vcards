from django.db import models

class VCards(models.Model):
    vcf_name = models.CharField(max_length=200,verbose_name="VCARD Name") 
    firstname = models.CharField(max_length=200,verbose_name="First Name") 
    lastname = models.CharField(max_length=200, blank=True,verbose_name="Last Name") 
    title = models.CharField(max_length=200, blank=True,verbose_name="Title") 
    company = models.CharField(max_length=200, blank=True) 
    phone = models.CharField(max_length=20, blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    fax = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=200, blank=True)
    url = models.URLField("Website", blank=True)
    facebook = models.CharField(max_length=200, blank=True) 
    twitter = models.CharField(max_length=200, blank=True) 
    googleplus = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=200, blank=True) 
    postal_code = models.CharField(max_length=200, blank=True,verbose_name="Postal Code") 
    city = models.CharField(max_length=200, blank=True) 
    province = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="vcards/",blank=True)
    default=models.BooleanField(blank=True,verbose_name="Default VCARD")
    view_vcard_url=models.URLField("VIEWCARD", blank=True,)
    
    class Meta:
        ordering = ["vcf_name"]
        verbose_name_plural = "VCARDS"  
        verbose_name = "VCARD"   
    
    def __unicode__(self):
        return u"%s" % (self.vcf_name)
