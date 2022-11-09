import uuid
from django.db import models 
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.db.models import Model
import datetime

'''
from django_resized import ResizedImageField
from tinymce.models import HTMLField
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from taggit.managers import TaggableManager
from django.shortcuts import reverse
'''

User = get_user_model()

class Agent(Model):

    agent_ID = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    firm = models.CharField(max_length=50, default='None')
    username = models.CharField(max_length=50, default='None')

    def __str__(self):
        return str(self.username)

class Bond(Model):

    choices = [
        (10 ,'AAA'),
        (9 ,'AA'),
        (8 ,'A'),
        (7 ,'BBB'),
        (6 ,'BB'),
        (5 ,'B'),
        (4 ,'CCC'),
        (3 ,'CC'),
        (2 ,'C'),
        (0 ,'D')
    ]

    agent = models.ForeignKey(Agent, on_delete = models.CASCADE)
    issuer = models.CharField(max_length=50, default='None')
    maturity = models.DateField(editable=True)
    grade = models.IntegerField(choices=choices, default=0)
    value = models.FloatField(default=0.0, blank=False)

    def __str__(self):
        return f'BOND: {str(self.issuer)}: ${str(self.value)}({str(self.grade)})'

class Stock(Model):

    ticker = models.CharField(max_length=5, default='NONE')
    value = models.FloatField(default=0.0, blank=False)
    agent = models.ForeignKey(Agent, on_delete = models.CASCADE)
    def __str__(self):
        return f'STOCK: {str(self.ticker)}: ${str(self.value)}'

class Property(Model):

    address = models.CharField(max_length=300, default='None')
    agent = models.ForeignKey(Agent, on_delete = models.CASCADE)
    value = models.FloatField(default=0.0, blank=False)

    def __str__(self):
        return f'PROPERTY: {str(self.address)}: ${str(self.value)}'

class delta(Model):
    date = models.DateField(auto_now=True)
    gl = models.FloatField(default=0)

class Loan(Model):
    bank = models.CharField(max_length = 100, default = 'None')
    rate = models.FloatField(default = 0, blank = False, null = False)
    amount = models.FloatField(default = 0, blank = False, null = False)

    def __str__(self):
        return f'Issued by: {str(self.bank)} for ${str(self.amount)} at a rate of {str(self.rate)}'

class StockState(Model):

    asset = models.ForeignKey(Stock, on_delete=models.CASCADE)
    value = models.FloatField(default=0)
    open = models.FloatField(default = 0)
    close = models.FloatField(default = 0)
    high = models.FloatField(default = 0)
    volume = models.FloatField(default = 0)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f'STOCK: {str(self.asset.ticker)}: ${str(self.value)}'

class PropertyState(Model):

    asset = models.ForeignKey(Property, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    value = models.FloatField(default = 0)

class BondState(Model):

    asset = models.ForeignKey(Bond, on_delete=models.CASCADE, blank=False, null=False)
    date = models.DateField(auto_now=True)
    value = models.FloatField(default=0)

class StockOwnership(Model):

    user_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    asset = models.ForeignKey(Stock, on_delete=models.CASCADE)

class BondOwnership(Model):

    user_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    asset = models.ForeignKey(Bond, on_delete=models.CASCADE)

class PropertyOwnership(Model):

    user_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    asset = models.ForeignKey(Property, on_delete=models.CASCADE)

class StockTransaction(Model):

    choices = [
        (1, 'Buy'),
        (-1 ,'Sell')
    ]
    transaction_type = models.IntegerField(choices=choices, blank=False, null=False, default=1)
    transaction_ID = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    asset = models.ForeignKey(Stock, on_delete=models.CASCADE, name='Stock')
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    volume = models.IntegerField(default=0)
    value = models.FloatField(default=0.0)
    transaction_date = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.volume} of {str(self.Stock.ticker)} on {str(self.transaction_date)} at {str(self.value)} per unit'

class PropertyTransaction(Model):

    choices = [
        (1, 'Buy'),
        (-1 ,'Sell')
    ]
    transaction_type = models.IntegerField(choices=choices, blank=False, null=False, default=1)
    asset = models.ForeignKey(Property, on_delete=models.CASCADE, name = 'Property')
    transaction_ID = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    volume = models.IntegerField(default=0)
    value = models.FloatField(default=0.0)
    transaction_date = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.volume} of {str(self.Property.address)} on {str(self.transaction_date)} at {str(self.value)} per unit'

class AgentQuery(Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)

class StockQuery(Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField()

class BondQuery(Model):
    bond = models.ForeignKey(Bond, on_delete=models.CASCADE)

class PropertyQuery(Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

class BondTransaction(Model):

    choices = [
        (1, 'Buy'),
        (-1 ,'Sell')
    ]
    transaction_type = models.IntegerField(choices=choices, blank=False, null=False, default=1)
    transaction_ID = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    transaction_date = models.DateField(auto_now=True)
    asset = models.ForeignKey(Bond, on_delete=models.CASCADE, name='Bond')
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.FloatField(default=0.0)
    volume = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.volume} of {str(self.Bond.issuer)} on {str(self.transaction_date)} at {str(self.value)} per unit'

class DepositOrWithdrawl(Model):

    choices = [
        (1, 'Deposit'),
        (-1 ,'Withdraw')
    ]
    type = models.IntegerField(choices=choices, blank = False, default=1)
    amount = models.FloatField(null=False, blank=False, default=0)
    fulfilled = models.BooleanField(default=False)

class UserProfile(Model):

    user_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=300, default='None')
    age = models.IntegerField(default = 0)
    sex = models.CharField(max_length=300, default='None')
    occupation = models.CharField(max_length=300, default='None')
    balance = models.FloatField(default=0)
    gain = models.FloatField(default=0)

class NewIndicator(Model):

    user_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    newPost = models.BooleanField(default=False)

class forum(Model):
    
    views = models.IntegerField(default = 0, editable = False)
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE, blank = False, default = "Anonymous")
    topic = models.CharField(max_length=300, default='Untitled')
    description = models.CharField(max_length=1000, default = '')
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.topic)

class Discussion(Model):

    user_ID = models.ForeignKey(User, on_delete=models.CASCADE, blank = False, default = "Anonymous")
    forum = models.ForeignKey(forum, on_delete=models.CASCADE,  blank = False)
    comment = models.CharField(max_length = 500)
    disc_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self):
        return str(self.forum)

class Media(Model):

    file = models.FileField(null=False, blank=False)
    description = models.TextField()
    media_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.description