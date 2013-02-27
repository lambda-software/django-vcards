from django.conf.urls.defaults import *
from vcards import views

urlpatterns = patterns('',               
    url(r'view/(?P<vcf_name>[-\w]+)$', 'vcards.views.viewcard',name="view_vcard"),
    url(r'(?P<vcf_name>[-\w]+).vcf$', 'vcards.views.download', name="vcard_url"),
)
