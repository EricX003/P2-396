from django.forms import ModelForm
from .models import *
from django import forms
from django.forms import Form

class CreateInForum(ModelForm):
    class Meta:
        file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
        model = forum
        fields = "__all__"

class CreateInMedia(ModelForm):
    class Meta:
        model = Media
        fields = ['description', 'file']

class CreateInDiscussion(ModelForm):
    class Meta:
        model = Discussion
        fields = "__all__"

class MakeDepositOrWithdrawl(ModelForm):
    class Meta:
        model = DepositOrWithdrawl
        exclude = ['fulfilled']

class CompleteProfile(ModelForm):
    class Meta:
        model = UserProfile
        fields = "__all__"

class ListBond(ModelForm):
    class Meta:
        model = Bond
        fields = "__all__"
        widgets = {'maturity' : forms.SelectDateWidget}

class ListProperty(ModelForm):
    class Meta:
        model = Property
        fields = "__all__"

class ListStock(ModelForm):
    class Meta:
        model = Stock
        fields = "__all__"

class MakeStockTransaction(ModelForm):
    class Meta:
        model = StockTransaction
        exclude = ['transaction_ID', 'transaction_date', 'value']

class MakeBondTransaction(ModelForm):
    class Meta:
        model = BondTransaction
        exclude = ['transaction_ID', 'transaction_date', 'value']

class MakePropertyTransaction(ModelForm):
    class Meta:
        model = PropertyTransaction
        exclude = ['transaction_ID', 'transaction_date', 'value']

class CreateAgent(ModelForm):
    class Meta:
        model = Agent
        exclude = ['agent_ID']

class DateForm(Form):
    date = forms.DateField(widget=forms.SelectDateWidget)

class QueryAgent(ModelForm):
    class Meta:
        model = AgentQuery
        fields = "__all__"

class QueryBond(ModelForm):
    class Meta:
        model = BondQuery
        fields = "__all__"

class QueryStock(ModelForm):
    class Meta:
        model = StockQuery
        fields = "__all__"
        widgets = {'date' : forms.SelectDateWidget}

class QueryProperty(ModelForm):
    class Meta:
        model = PropertyQuery
        fields = "__all__"

class CreateLoan(ModelForm):
    class Meta:
        model = Loan
        fields = "__all__"