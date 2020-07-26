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

# RFE stands for robot framework front end
from . import home
from . import RFE
from . import planning

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'^$', home.home),
    url(r'^expire$', home.home_error),
    url(r'^RFE$', RFE.initial_load, name="RFE"),
    url(r'^RFETS$', RFE.load_test_suite, name="TS"),
    url(r'^RFERUN$', RFE.run_instance, name="Run"),
    url(r'^RFEABORT$', RFE.abort_instance, name="Abort"),
    url(r'^RFERUNSTATUS$', RFE.run_stat, name="run_stat"),
    url(r'^RFELOADSTATUS$', RFE.log_stat, name="load_stat"),
    url(r'^RFERUNWITHMETA$', RFE.load_meta_run_with, name="load_meta_run_with"),
    url(r'^RFEEDITOR$', RFE.core_editor, name="editor"),
    url(r'^GETSERVERNOW$', RFE.get_time, name="ctime"),
    url('GETALLSUITES$', RFE.get_all_files, name="all_files"),
    url('MANAGEFEAT$', RFE.manage_feat, name="manage_feat"),
    url('PLAN$', planning.suite_plan, name="suite_plan"),
    url('EXEC$', planning.suite_execution, name="")
    #path(r'^App1/',Test.test1, name="index")
]
