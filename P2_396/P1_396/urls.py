"""P1_396 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.urls import path
from Discussion_forum.views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('forum/', goForum, name='forum'),
    path('forum/makePost/',makePost,name='makePost'),
    path(r'forum/replyPost/<postID>/',replyPost,name='replyPost'),
    path('logout/', logout, name='logout'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path(r'forum/toPost/<postID>/', toPost, name='toPost'),
    path('media/', goMedia, name='goMedia'),
    path('media/addMedia', uploadFiles, name='uploadFiles'),
    path('calendar/', goCalendar, name='goCalendar'),
    path('finance/changeFunds/', changeFunds, name='changeFunds'),
    path('finance/seeTransactionsOnDate', seeTransactionsOnDate, name='seeTransactionOnDate'),
    path('finance/', goFinance, name='goFinance'),
    path('finance/listAsset', goListAsset, name = 'goListAsset'),
    path('finance/newStock', newStock, name='newStock'),
    path('finance/newProperty', newProperty, name='newProperty'),
    path('finance/newBond', newBond, name='newBond'),
    path('finance/tradeAssets', goTradeAssets, name='goTradeAssets'),
    path('finance/newAgent', goCreateAgent, name='newAgent'),
    path('finance/newAgent/create', goNewAgent, name='newAgent'),
    path('finance/tradeAssets/performStockTrade', performStockTrade, name='performStockTrade'),
    path('finance/tradeAssets/performBondTrade', performBondTrade, name='performBondTrade'),
    path('finance/tradeAssets/performPropertyTrade', performPropertyTrade, name='performPropertyTrade'),
    path('finance/agentQuery/', goAgentQuery, name='goAgentQuery'),
    path('finance/agentQuery/made/', makeAgentQuery, name='makeAgentQuery'),
    path('finance/assetQuery/', goAssetQuery, name='goAssetQuery'),
    path('finance/assetQuery/madeStock', goStockQuery, name='goStockQuery'),
    path('finance/assetQuery/madeBond', goBondQuery, name='goBondQuery'),
    path('finance/assetQuery/madeProperty', goPropertyQuery, name='goPropertyQuery'),
    path('finance/queryGain', queryGain, name='queryGain'),
    path('finance/goNewLoan', goNewLoan, name='goNewLoan'),
    path('finance/goNewLoan/newLoan', newLoan, name='newLoan'),
    path('finance/viewLoans', goViewLoans, name='goViewLoans'),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
