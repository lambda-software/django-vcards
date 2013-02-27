# -*- coding: utf-8 -*-
from django.template import Template
from django.template import loader, Context
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import logout
from django.shortcuts import render_to_response
from django.conf import settings
from models import *
import base64, imghdr
import re
from time import gmtime, strftime

#Very simple function to detect if the remote browser is iphone or ipad.
#Based on simple mobile support http://djangosnippets.org/snippets/2228/
def mobile(request):
    device = ""
    ua = request.META.get('HTTP_USER_AGENT', '').lower()
    
    if ua.find("iphone") > 0:
        device = "iphone"
        
    elif ua.find("ipad") > 0:
        device = "ipad"
        
    elif ua.find("android") > 0:
        device = "android"
        
    elif ua.find("blackberry") > 0:
        device = "blackberry"
        
    elif ua.find("windows phone os 7") > 0:
        device['winphone7'] = "winphone7"
        
    elif ua.find("iemobile") > 0:
        device['winmo'] = "winmo"
        
    else:  # either desktop
        device = "desktop"
    
    return device

def viewcard(request,vcf_name):
    try:
        vcard=VCards.objects.get(vcf_name=vcf_name)
        #Create the QR if it not exists
        if not os.path.exists(settings.MEDIA_ROOT + "/" + vcard.vcf_name + ".jpg"):
            #Creating vcard due an error in PIL creating vcard with qrcode python lib
            ## System execution of qrencode command
            command="qrencode -o %s/%s.jpg %s%s.vcf " %(settings.MEDIA_ROOT,vcard.vcf_name,request.build_absolute_uri("/vcards/"),vcard.vcf_name)
            os.system(command)
            ## QRCode to creating vcard on demand
            #qr = QRCode()
            #qr.add_data()
            #qr.make() # Generate the QRCode itself
            #im = qr.make_image()
            #im.save(settings.MEDIA_ROOT + "/" + vcard.vcf_name + ".jpg")
    except:
        vcard=False   
        
    data ={ 
           'vcard': vcard,
           'site_url':request.build_absolute_uri("/")
          }
    return render_to_response('viewcard.html',
                            data, 
                            context_instance=RequestContext(request))

def download(request,vcf_name=""):
    try:
        vcard=VCards.objects.get(vcf_name=vcf_name)
    except:
        vcard=VCards.objects.get(default=True) 
    
    VCARD="BEGIN:VCARD\n"
    VCARD+="N:%s;%s;;\n"  % (vcard.lastname, vcard.firstname)
    VCARD+="FN:%s %s;;;\n"  % (vcard.firstname, vcard.lastname)
    
    if vcard.address:
        VCARD+="ADR;INTL;PARCEL;WORK:;;%s;%s;%s;%s;%s\n" % (vcard.address,vcard.city,vcard.province,vcard.postal_code,vcard.country)
    if vcard.email:
        VCARD+="EMAIL;INTERNET: %s\n" % (vcard.email)
    if vcard.title:
        VCARD+="TITLE: %s\n" % (vcard.title)    
    if vcard.company:
        VCARD+="ORG: %s\n" % (vcard.company)
    if vcard.phone:
        VCARD+="TEL;WORK:%s\n" % (vcard.phone)
    if vcard.fax:
        VCARD+="TEL;FAX;WORK:%s\n" % (vcard.fax)
    if vcard.mobile:
        VCARD+="TEL;CELL:%s\n" % (vcard.mobile)
    if vcard.url:
        VCARD+="URL;WORK:%s\n" % (vcard.url)
    if vcard.image:
        print vcard.image.__dict__
        ImageFile=vcard.image
        type=imghdr.what(ImageFile.path).upper()
        image= base64.b64encode(ImageFile.read())
        VCARD+="PHOTO;ENCODING=BASE64;TYPE=%s:%s\n" % (type, image)
    VCARD+="END:VCARD"
    VCARD=VCARD.encode("UTF-8")
    ##For Iphone / Ipad, VCARD will be embeded into ICS calendar
    
    VCAL=""
    VCAL+="BEGIN:VCALENDAR\n"
    VCAL+="VERSION:2.0\n"
    VCAL+="BEGIN:VEVENT\n"
    VCAL+="SUMMARY:Click attached contact below to save to your contacts\n"
    VCAL+="DTSTART;TZID=Europe/London:%s\n" % (strftime("%Y%m%dT%H%M%S",gmtime()))
    VCAL+="DTEND;TZID=Europe/London:%s\n" % (strftime("%Y%m%dT%H%M%S",gmtime()))
    VCAL+="DTSTAMP:%sZ\n" % (strftime("%Y%m%dT%H%M%S",gmtime()))
    #Embedding vcard in ICS
    VCAL+="ATTACH;VALUE=BINARY;ENCODING=BASE64;FMTTYPE=text/directory;\n"
    VCAL+=" X-APPLE-FILENAME=%s.vcf:\n" % (vcard.vcf_name)
    #We need to split each 76 lines de Base64 according to RFC2045
    #Alse we need ident 1 space for the iphone / ipad / and ICalendar
    VCARDIPHONE='\n'.join(base64.b64encode(VCARD)[pos:pos+76] for pos in xrange(0, len(base64.b64encode(VCARD)), 76))
    VCAL+=re.sub("(.+)", " \\1", VCARDIPHONE.encode())
    VCAL+="\n"
    VCAL+="END:VEVENT\n"
    VCAL+="END:VCALENDAR\n"
    
    device=mobile(request)
    mimetype="application/octet-stream"
    #Decide to serve ICS or VCF depending of the device
    if device == "iphone" or device == "ipad":
        response = HttpResponse(VCAL,mimetype=mimetype)
        response['Content-Type'] = 'text/x-vCalendar; charset=utf-8'
        response['Content-Disposition'] = 'attachment; filename=iphonecontact.ics'
    else:
        response = HttpResponse(VCARD, mimetype=mimetype)
        response['Content-Disposition'] = 'attachment; filename=%s.vcf' % (vcard.vcf_name)
    
    return response


