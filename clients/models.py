from django.db import models
from django.utils.translation import gettext_lazy as _

class Client(models.Model):
    client_date_created = models.DateField(_("date created"), auto_now_add=True)
    client_date_modified = models.DateField(_("date modified"), auto_now=True)
    client_name = models.CharField(_("client name"), max_length=150, default='', blank=False)
    client_address = models.TextField(_("Address"), max_length=500, default='', blank=True)
    client_phone = models.CharField(_("phone"), max_length=100, default='', blank=True)
    client_fax = models.CharField(_("fax"), max_length=100, default='', blank=True)
    client_mobile = models.CharField(_("mobile"), max_length=100, default='', blank=True)
    client_email = models.EmailField(_("email"), max_length=254, default='', blank=True)
    client_web = models.CharField(_("website"), max_length=200, default='', blank=False)
    client_currency = models.CharField(_("currency"), max_length=50)
    client_active = models.BooleanField(_("active"))
    

    def __str__(self):
        return self.client_name + " - " + self.client_currency

    def __unicode__(self):
        return self.client_name