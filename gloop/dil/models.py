from django.db import models
from django.contrib.auth.models import User


class ComapnyManager(models.Manager):
    def get_company(self, company_login):
        try:
            user = User.objects.get(username=company_login)
            try:
                company=Company.objects.get(base=user)
                return company
            except Company.DoesNotExist:
                return None
        except User.DoesNotExist:
            return None

class Company(models.Model):
    base = models.OneToOneField(User)
    c_name = models.CharField(max_length=20, null=True)
    c_address = models.CharField(max_length=50, null=True)
    c_telephone = models.CharField(max_length=9, null=True)
    objects = ComapnyManager()
    def __unicode__(self):
        return self.base.username # company name later
    
class Client(models.Model):
    base = models.OneToOneField(User)

class Service(models.Model):
    s_owner = models.ForeignKey(Company, related_name='+')
    s_name = models.CharField(max_length=50)
    s_duration = models.IntegerField()
    s_price = models.FloatField() # change spelling later
    def __unicode__(self):
        return str(self.s_name)
