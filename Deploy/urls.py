"""MiaDB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from views import *

urlpatterns = [

    url(r'GetDeployPlans/$',GetDeployPlans,name="GetDeployPlans"),
    url(r'GetDeployments/$',GetDeployments,name="GetDeployments"),

    url(r'GetDeployPlanByName/(?P<DeployPlanName>\w+)/$', GetDeployPlanByName, name="GetDeployPlan"),
    url(r'GetDeploymentByName/(?P<DeploymentByName>\w+)/$', GetDeploymentByName, name="GetDeploymentByName"),

    url(r'Deploy/$',Deploy,name="Deploy"),
    url(r'StartDeployment/$',StartDeployment,name="StartDeployment"),

    url(r'RemoveDeployment/$',RemoveDeployment,name="RemoveDeployment"),
    url(r'StopDeployment/$',StopDeployment,name="StopDeployment"),

    url(r'ScaleUP/$',ScaleUP,name="ScaleUP")
]
