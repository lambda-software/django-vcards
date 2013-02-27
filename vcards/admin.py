from django import forms
from django.contrib import admin
from models import VCards
from django.core.urlresolvers import reverse

class VCardsAdmin(admin.ModelAdmin):
    list_display = ('vcf_name', 'firstname', 'lastname','email','default')
    readonly_fields = ['view_vcard_url']
    save_as = True
    
    def save_model(self, request, obj, form, change):
        if obj.default == True:
            objects=VCards.objects.all()
            for object in objects:
                object.default=False;
                object.save()
            obj.default=True   
        obj.save()
        obj.view_vcard_url=reverse('view_vcard', args=[obj.vcf_name])
        obj.save()

admin.site.register(VCards,VCardsAdmin)
