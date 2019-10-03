"""App1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
# RFE stands for robot framework front end
from . import Test
from . import RFE

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'^$', Test.home),
    url(r'^expire$', Test.home_error),
    url(r'^RFE$', RFE.InitialLoad, name="RFE"),
    url(r'^RFETS$', RFE.LoadTestSuite, name="TS"),
    url(r'^RFERUN$', RFE.Run_instance, name="Run"),
    url(r'^RFEABORT$', RFE.Abort_instance, name="Abort"),
    url(r'^RFERUNSTATUS$', RFE.Run_stat, name="run_stat"),
    url(r'^RFELOADSTATUS$', RFE.Log_stat, name="load_stat"),
    url(r'^RFERUNWITHMETA$', RFE.load_meta_run_with, name="load_meta_run_with"),
    url(r'^RFEEDITOR$', RFE.Core_Editor, name="editor"),
    url(r'^GETSERVERNOW$', RFE.get_time, name="ctime"),
    url('GETALLSUITES$', RFE.GetAllSuites, name="get_all"),
    url('MANAGEFEAT$', RFE.manage_feat, name="manage_feat")
    #path(r'^App1/',Test.test1, name="index")
]
