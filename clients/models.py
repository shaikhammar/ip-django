from django.db import models
from django.utils.translation import gettext_lazy as _

class Client(models.Model):
    client_date_created = models.DateField(_("date created"), auto_now_add=True)
    client_date_modified = models.DateField(_("date modified"), auto_now=True)
    client_name = models.CharField(_("name"), max_length=150, default='', blank=True)
    client_address_1 = models.CharField(_("address line 1"), max_length=150, default='', blank=True)
    client_address_2 = models.CharField(_("address line 2"), max_length=150, default='', blank=True)
    client_city = models.ForeignKey("address.City", verbose_name=_("city"), on_delete=models.SET_NULL, null=True, blank=True)
    client_state = models.ForeignKey("address.Region", verbose_name=_("state/province"), on_delete=models.SET_NULL, null=True, blank=True)
    client_country = models.ForeignKey("address.Country", verbose_name=_("country"), on_delete=models.SET_NULL, null=True, blank=True)
    client_zip = models.CharField(_("zip"), max_length=100, default='', blank=True)
    client_phone = models.CharField(_("phone"), max_length=100, default='', blank=True)
    client_fax = models.CharField(_("fax"), max_length=100, default='', blank=True)
    client_mobile = models.CharField(_("mobile"), max_length=100, default='', blank=True)
    client_email = models.EmailField(_("email"), max_length=254, default='', blank=True)
    client_web = models.CharField(_("website"), max_length=200, default='', blank=True)
    client_currency = models.CharField(_("currency"), max_length=50)
    client_active = models.BooleanField(_("active"))
    

    def __str__(self):
        return self.client_name

    def __unicode__(self):
        return self.client_name

