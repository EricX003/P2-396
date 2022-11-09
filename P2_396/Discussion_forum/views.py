from django.shortcuts import render, redirect
from .models import * 
from .forms import * 
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.forms.models import model_to_dict
import datetime
from datetime import date

'''
from django.shortcuts import redirect, render, get_object_or_404
from .models import Author, Category, Post, Comment, Reply
from .utils import update_views
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
'''

def logout(request):
    auth.logout(request)
    return redirect(home)

def goMedia(request):
    allFiles = Media.objects.all()
    context = {"allFiles" : allFiles}
    return render(request,'./media.html', context)

def uploadFiles(request):

    if request.method == 'POST':
        data = request.POST['description']
        files = request.FILES.getlist('files')

        for curfile in files:
            file = Media.objects.create(
                description = data,
                file = curfile
            )
            file.save()

        return redirect(goMedia)

    return render(request, './addFile.html')

def home(request):
    
    if request.user.is_authenticated:
        visitor = NewIndicator.objects.get(user_ID = request.user)
        new = visitor.newPost
        context = {'newPost':new}       
        return render(request,'./home.html', context)
    context = {'newPost':False}  
    return render(request,'./home.html', context)

def goCalendar(request):
    return render(request, './calendar.html')

def goFinance(request):
    form = MakeDepositOrWithdrawl()
    balance = UserProfile.objects.filter(user_ID=request.user)[0].balance

    stockTransactions = StockTransaction.objects.filter(user_ID=request.user)
    propertyTransactions = PropertyTransaction.objects.filter(user_ID=request.user)
    bondTransactions = BondTransaction.objects.filter(user_ID=request.user)

    context = {
        'available' : balance,
        'form' : form,
        'dateForm' : DateForm(),
        'stocks' : stockTransactions,
        'properties' : propertyTransactions,
        'bonds' : bondTransactions,
        'dispGain' : False,
            'gain' : 0
        }
    return render(request, './financeHome.html', context)

def seeTransactionsOnDate(request):
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            balance = UserProfile.objects.filter(user_ID=request.user)[0].balance

            stockTransactions = StockTransaction.objects.filter(user_ID=request.user, transaction_date=form.cleaned_data['date'])
            propertyTransactions = PropertyTransaction.objects.filter(user_ID=request.user, transaction_date=form.cleaned_data['date'])
            bondTransactions = BondTransaction.objects.filter(user_ID=request.user, transaction_date=form.cleaned_data['date'])

            context = {
                'available' : balance, 
                'form' : form,
                'dateForm' : DateForm(),
                'stocks' : stockTransactions,
                'properties' : propertyTransactions,
                'bonds' : bondTransactions,
                'dispGain' : False,
                'gain' : 0
                }
            return render(request, './financeHome.html', context)
    return redirect(goFinance)


def goForum(request):
    visitor = NewIndicator.objects.get(user_ID = request.user)
    visitor.newPost = False
    visitor.save()

    forums=forum.objects.all()

    count=forums.count()

    context={'forums':forums,
              'count':count}
    return render(request,'forum.html',context)

def toPost(request, postID):
    post = forum.objects.get(id = postID)
    post.views = post.views + 1
    post.save()

    forums=forum.objects.all()
    discussions=[]
    for i in forums:
        discussions.append(i.discussion_set.all())
 
    context={'forum':post,
              'discussions':discussions}
    return render(request, 'viewPost.html', context)

def replyPost(request, postID):
    form = CreateInDiscussion()
    if request.method == 'POST':
        form = CreateInDiscussion(request.POST)
        if form.is_valid():
            form.save()
            return redirect(goForum)
    context ={'form':form, 'id':postID}
    return render(request,'./replyPost.html', context)

def makePost(request):
    form = CreateInForum()
    if request.method == 'POST':
        form = CreateInForum(request.POST)
        if form.is_valid():
            form.save()
            unreads = NewIndicator.objects.all()
            for unread in unreads:
                unread.newPost = True
                unread.save()
            return redirect(goForum)

    context ={'form':form}
    return render(request,'./makePost.html',context)

def goTradeAssets(request):
    balance = UserProfile.objects.filter(user_ID=request.user)[0].balance
    context = {'available' : balance, 'stock_form' : MakeStockTransaction(), 'bond_form' : MakeBondTransaction(), 'property_form' : MakePropertyTransaction()}
    return render(request, './tradeAssets.html', context)

def makeDelta():
    if len(delta.objects.filter(date=date.today())) == 0:
        newObject = delta()
        newObject.save()

def goViewLoans(request):
    loans = Loan.objects.order_by('rate')
    return render(request, './viewLoans.html', {'loans' : loans})

def newLoan(request):
    if request.method == "POST":
        form = CreateLoan(request.POST)
        if form.is_valid():
            form.save()
    return redirect(goNewLoan)

def goNewLoan(request):
    context = {'form' : CreateLoan()}
    return render(request, './newLoan.html', context)

def queryGain(request):
    if request.method == "POST":
        form = DateForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            date = form['date']
            gain = delta.objects.filter(date=date)
            if len(gain) > 0:
                gain = gain[0].gl
                form = MakeDepositOrWithdrawl()
                balance = UserProfile.objects.filter(user_ID=request.user)[0].balance

                stockTransactions = StockTransaction.objects.filter(user_ID=request.user)
                propertyTransactions = PropertyTransaction.objects.filter(user_ID=request.user)
                bondTransactions = BondTransaction.objects.filter(user_ID=request.user)
                context = {
                'available' : balance,
                'form' : form,
                'dateForm' : DateForm(),
                'stocks' : stockTransactions,
                'properties' : propertyTransactions,
                'bonds' : bondTransactions,
                'dispGain' : True,
                'gain' : gain
                }
                return render(request, './financeHome.html', context)
    return redirect(goFinance)

def performStockTrade(request):
    balance = UserProfile.objects.filter(user_ID=request.user)[0].balance
    if request.method == 'POST':
        form = MakeStockTransaction(request.POST)
        if form.is_valid():
            makeDelta()
            gain = delta.objects.filter(date=date.today())[0]
            data = form.cleaned_data
            total_price = data['volume'] * data['Stock'].value
            if data['transaction_type'] == 1:
                if total_price > balance:
                    messages.info(request, 'You do not have enough money to make this purchase')
                else:
                    gain.gl -= total_price
                    gain.save()
                    newTransaction = form.save()
                    newTransaction.value = data['Stock'].value
                    newTransaction.save()
                    seller = UserProfile.objects.filter(user_ID=request.user)[0]
                    seller.balance -= total_price
                    seller.save()
                    query = StockOwnership.objects.filter(user_ID=request.user, asset=data['Stock'])
                    if len(query) > 0:
                        single = query[0]
                        single.amount += data['volume']
                        single.save()
                    else:
                        ownership = StockOwnership(
                            user_ID = request.user,
                            amount = data['volume'],
                            asset = data['Stock']
                        )
                        ownership.save()
                        to_update = StockState.objects.filter(asset=data['Stock'])[0]
                        to_update.volume += data['volume']
                        to_update.save()
            else:
                ownership = StockOwnership.objects.filter(user_ID=request.user, asset=data['Stock'])
                if len(ownership) == 0 or ownership[0].amount < data['volume']:
                    messages.info(request, 'You do not own sufficient assets to sell')
                else:
                    gain.gl += total_price
                    gain.save()
                    newTransaction = form.save()
                    newTransaction.value = data['Stock'].value
                    newTransaction.save()
                    ownership = ownership[0]
                    seller = UserProfile.objects.filter(user_ID=request.user)[0]
                    ownership.amount -= data['volume']
                    ownership.save()
                    seller.balance += total_price
                    seller.save()

    return redirect(goTradeAssets)

def performBondTrade(request):
    balance = UserProfile.objects.filter(user_ID=request.user)[0].balance
    if request.method == 'POST':
        form = MakeBondTransaction(request.POST)
        if form.is_valid():
            makeDelta()
            gain = delta.objects.filter(date=date.today())[0]
            data = form.cleaned_data
            total_price = data['volume'] * data['Bond'].value
            if data['transaction_type'] == 1:
                if total_price > balance:
                    messages.info(request, 'You do not have enough money to make this purchase')
                else:
                    gain.gl -= total_price
                    gain.save()
                    newTransaction = form.save()
                    newTransaction.value = data['Bond'].value
                    newTransaction.save()
                    seller = UserProfile.objects.filter(user_ID=request.user)[0]
                    seller.balance -= total_price
                    seller.save()
                    query = BondOwnership.objects.filter(user_ID=request.user, asset=data['Bond'])
                    if len(query) > 0:
                        single = query[0]
                        single.amount += data['volume']
                        single.save()
                    else:
                        ownership = BondOwnership(
                            user_ID = request.user,
                            amount = data['volume'],
                            asset = data['Bond']
                        )
                        ownership.save()
                        to_update = BondState.objects.filter(asset=data['Bond'])[0]
                        to_update.volume += data['volume']
                        to_update.save()
            else:
                ownership = BondOwnership.objects.filter(user_ID=request.user, asset=data['Bond'])
                if len(ownership) == 0 or ownership[0].amount < data['volume']:
                    messages.info(request, 'You do not own sufficient assets to sell')
                else:
                    gain.gl += total_price
                    gain.save()
                    newTransaction = form.save()
                    newTransaction.value = data['Bond'].value
                    newTransaction.save()
                    ownership = ownership[0]
                    seller = UserProfile.objects.filter(user_ID=request.user)[0]
                    ownership.amount -= data['volume']
                    ownership.save()
                    seller.balance += total_price
                    seller.save()

    return redirect(goTradeAssets)

def makeAgentQuery(request):
    if request.method == "POST":
        form = QueryAgent(request.POST)
        
        if form.is_valid():
            agent = form.cleaned_data['agent']
            stocks = Stock.objects.filter(agent=agent)
            bonds = Bond.objects.filter(agent=agent)
            properties = Property.objects.filter(agent=agent)

            context = {
                'form' : QueryAgent(), 
                'stocks' : stocks,
                'bonds' : bonds,
                'properties' : properties,
                'made' : True
                }
            return render(request, './agentQuery.html', context)
    return redirect(goAgentQuery)

def goStockQuery(request):
    if request.method == "POST":
        form = QueryStock(request.POST)
        if form.is_valid():
            form = form.cleaned_data

            stock = form['stock']
            date = form['date']
            state = StockState.objects.filter(date=date, asset=stock)
            if len(state) > 0:
                state = state[0]
                asset = f"Ticker: {stock.ticker}\n Open: {state.open}\n Close: {state.close}\n High: {state.high}\n Volume: {state.volume}"
                context = {
                'stockForm' : QueryStock(), 
                'bondForm' : QueryBond(), 
                'propertyForm' : QueryProperty(), 
                'stockMade' : True,
                'stock' : asset,
                'bondMade' : False,
                'bond' : None,
                'propertyMade' : False,
                'property' : None,
                }
                return render(request, './assetQuery.html', context)

    return redirect(goAssetQuery)

def goPropertyQuery(request):
    if request.method == "POST":
        form = QueryProperty(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            property = form['property']
            asset = f"Address: {property.address}\n Agent: {property.agent}\n Value: {property.value}"
            context = {
            'stockForm' : QueryStock(), 
            'bondForm' : QueryBond(), 
            'propertyForm' : QueryProperty(), 
            'stockMade' : False,
            'stock' : None,
            'bondMade' : False,
            'bond' : None,
            'propertyMade' : True,
            'property' : asset,
            }
            return render(request, './assetQuery.html', context)
            
    return redirect(goAssetQuery)

def goBondQuery(request):
    if request.method == "POST":
        form = QueryBond(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            asset = form['bond']
            asset = f"Issuer: {asset.issuer}\nGrade: {asset.grade}\n Value: {asset.value}\nMaturity: {asset.maturity}\n"
            context = {
            'stockForm' : QueryStock(), 
            'bondForm' : QueryBond(), 
            'propertyForm' : QueryProperty(), 
            'stockMade' : False,
            'stock' : None,
            'bondMade' : True,
            'bond' : asset,
            'propertyMade' : False,
            'property' : None,
            }
            return render(request, './assetQuery.html', context)
            
    return redirect(goAssetQuery)

def goAssetQuery(request):
    context = {
    'stockForm' : QueryStock(), 
    'bondForm' : QueryBond(), 
    'propertyForm' : QueryProperty(), 
    'stockMade' : False,
    'stock' : None,
    'bondMade' : False,
    'bond' : None,
    'propertyMade' : False,
    'property' : None,
    }
    return render(request, './assetQuery.html',context)

def goAgentQuery(request):
    context = {
    'form' : QueryAgent(), 
    'stocks' : None,
    'bonds' : None,
    'properties' : None,
    'made' : False
    }
    return render(request, './agentQuery.html', context)

def performPropertyTrade(request):
    balance = UserProfile.objects.filter(user_ID=request.user)[0].balance
    if request.method == 'POST':
        form = MakePropertyTransaction(request.POST)
        if form.is_valid():
            makeDelta()
            gain = delta.objects.filter(date=date.today())[0]
            data = form.cleaned_data
            total_price = data['volume'] * data['Property'].value
            if data['transaction_type'] == 1:
                if total_price > balance:
                    messages.info(request, 'You do not have enough money to make this purchase')
                else:
                    newTransaction = form.save()
                    newTransaction.value = data['Property'].value
                    newTransaction.save()
                    seller = UserProfile.objects.filter(user_ID=request.user)[0]
                    seller.balance -= total_price
                    seller.save()
                    gain.gl -= total_price
                    gain.save()
                    query = PropertyOwnership.objects.filter(user_ID=request.user, asset=data['Property'])
                    if len(query) > 0:
                        single = query[0]
                        single.amount += data['volume']
                        single.save()
                    else:
                        ownership = PropertyOwnership(
                            user_ID = request.user,
                            amount = data['volume'],
                            asset = data['Property']
                        )
                        ownership.save()
                        to_update = PropertyState.objects.filter(asset=data['Property'])[0]
                        to_update.volume += data['volume']
                        to_update.save()
            else:
                ownership = PropertyOwnership.objects.filter(user_ID=request.user, asset=data['Property'])
                if len(ownership) == 0 or ownership[0].amount < data['volume']:
                    messages.info(request, 'You do not own sufficient assets to sell')
                else:
                    gain.gl += total_price
                    gain.save()
                    newTransaction = form.save()
                    newTransaction.value = data['Property'].value
                    newTransaction.save()
                    ownership = ownership[0]
                    seller = UserProfile.objects.filter(user_ID=request.user)[0]
                    ownership.amount -= data['volume']
                    ownership.save()
                    seller.balance += total_price
                    seller.save()

    return redirect(goTradeAssets)

def changeFunds(request):
    form = MakeDepositOrWithdrawl()
    if request.method == 'POST':
        form = MakeDepositOrWithdrawl(request.POST)
        if form.is_valid():
            form.save()
            all_unfulfilled_deposits = DepositOrWithdrawl.objects.filter(fulfilled=False)
            for unfulfilled in all_unfulfilled_deposits:
                person = UserProfile.objects.get(user_ID=request.user)
                unfulfilled.fulfilled = True
                unfulfilled.save()
                if person.balance < unfulfilled.amount and unfulfilled.type == -1:
                    messages.info(request, "You are trying to withdraw more than you have")
                    return redirect(goFinance)
                person.balance += unfulfilled.type * unfulfilled.amount
                person.save()

            return redirect(goFinance)

    return redirect(goFinance)

def goListAsset(request):
    context = {
            'stock_form' : ListStock(),
            'property_form' : ListProperty(), 
            'bond_form' : ListBond()
            }
    return render(request, './listAssets.html', context)

def goCreateAgent(request):
    context = {'form' : CreateAgent()}
    return render(request, './makeAgent.html', context)

def goNewAgent(request):
    form = CreateAgent()
    if request.method == 'POST':
        form = CreateAgent(request.POST)
        if form.is_valid():
            if len(Agent.objects.filter(username=form.cleaned_data['username'])) > 0:
                messages.info(request, 'Agent with this username already exists')
            else:
                form.save()
    return redirect(goFinance)

def newStock(request):
    if request.method == 'POST':
        form = ListStock(request.POST)
        if form.is_valid():
            newStock = form.save()
            newState = StockState(
                asset = newStock,
                value = form.cleaned_data['value'],
                open = form.cleaned_data['value'],
                close = form.cleaned_data['value'],
                high = form.cleaned_data['value'],
                volume = 0
            )
            newState.save()
    return redirect(goListAsset)

def newProperty(request):
    if request.method == 'POST':
        form = ListProperty(request.POST)
        if form.is_valid():
            newProperty = form.save()
            newState = PropertyState(
                asset = newProperty,
                value = form.cleaned_data['value'],
            )
            newState.save()
    return redirect(goListAsset)

def newBond(request):
    if request.method == 'POST':
        form = ListBond(request.POST)
        if form.is_valid():
            newBond = form.save()
            print(newBond)
            newState = BondState(
                asset = newBond,
                value = form.cleaned_data['value']
            )
            newState.save()

    return redirect(goListAsset)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect(home)
        else:
            messages.info(request, 'Incorrect Username or Password')
            return redirect(login)
    else:
        return render(request, './login.html')

def register(request):
    if request.method == 'POST':
        fname = request.POST['FName']
        lname = request.POST['LName']
        username = request.POST['username']
        password = request.POST['password']
        confirm = request.POST['confirm']

        UserAddress = request.POST['Address']
        UserAge = request.POST['Age']
        UserSex = request.POST['Sex']
        UserOccupation = request.POST['Occupation']

        if password==confirm:

            if User.objects.filter(first_name=fname).exists() and User.objects.filter(last_name=lname).exists() and \
                User.objects.filter(first_name=fname) == User.objects.filter(last_name=lname):

                messages.info(request, 'You Already Have an Account!')
                return redirect(login)
            else:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Username is Taken, Select Another')
                    return redirect(register)
                else:
                    user = User.objects.create_user(username=username, password=password, first_name=fname, last_name=lname)
                    additional = UserProfile(
                        user_ID = user,
                        address = UserAddress,
                        age = UserAge,
                        sex = UserSex,
                        occupation = UserOccupation,
                        balance=0.0,
                        gain=0.0
                    )
                    user.save()
                    additional.save()
                    visited = NewIndicator(user_ID = user, newPost = False)
                    visited.save()
                    
                    return redirect(home)
            
        else:
            messages.info(request, 'Passwords Do Not Match!')
            return redirect(register)
            

    else:
        return render(request, './newAccount.html')