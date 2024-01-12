from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    user_company = models.CharField(_("Company"), max_length=100, default='')
    user_address_1 = models.CharField(_("Address Line 1"), max_length=100, default='', blank=True)
    user_address_2 = models.CharField(_("Address Line 2"), max_length=100, default='', blank=True)
    user_city = models.ForeignKey("address.City", verbose_name=_("city"), on_delete=models.SET_NULL, null=True, blank=True)
    user_state = models.ForeignKey("address.Region", verbose_name=_("state/province"), on_delete=models.SET_NULL, null=True, blank=True)
    user_country = models.ForeignKey("address.Country", verbose_name=_("country"), on_delete=models.SET_NULL, null=True, blank=True)
    user_zip = models.CharField(_("zip"), max_length=100, default='', blank=True)
    user_phone = models.CharField(_("phone"), max_length=100, default='', blank=True)
    user_fax = models.CharField(_("fax"), max_length=100, default='', blank=True)
    user_mobile = models.CharField(_("mobile"), max_length=100, default='', blank=True)
    user_date_modified = models.DateTimeField(_("date modified"), auto_now=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
    
    @property
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()
    
    @property
    def user_type(self):
        """
        Return the type of user.
        """
        if self.is_staff == True: 
            user_type = "Administrator"
        else:
            user_type = "Basic User"
        return user_type
    
    # @user_type.setter
    # def user_type(self, user_type):
    #     if user_type == "Administrator": 
    #         self.is_staff = "1"
    #     else:
    #         self.is_staff = "0"