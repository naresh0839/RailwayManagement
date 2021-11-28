"""lorax URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from django.contrib import admin
from django.urls import path
from railway import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.home),
    url(r'^admin/', admin.site.urls),
    url(r'^signup/', views.signup),
    url(r'^login/', views.login_user),
    url(r'^home/', views.home),    
    url(r'^logout/', views.logout_user),
    url(r'^traininfo/', views.traininfo),
    url(r'^findtrains/', views.findtrains),
    url(r'^ticket/', views.ticket),
    url(r'^dashboard/', views.dashboard),
    url(r'^download_ticket/', views.download_ticket),
    url(r'^aboutus/', views.aboutus),
    url(r'^listtrains/',views.list_trains),
    url(r'^addtrain/',views.add_train),
    url(r'^liststations/',views.list_stations),
    url(r'^writefeedback/',views.write_feedback),
    url(r'^listfeedback/',views.show_feedback),
    url(r'^activation/',views.activation)
]
