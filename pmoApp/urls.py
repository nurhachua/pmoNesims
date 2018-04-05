# pmoApp/urls.py
from django.conf.urls import url, include
from pmoApp import views
from rest_framework import routers
from django.contrib.auth import views as auth_views

# We are adding a URL called /home
router = routers.DefaultRouter()
router.register(r'justificationID', views.JustificationReportViewSet)
router2 = routers.DefaultRouter()
router2.register(r'authorizationID', views.AuthorizationReportViewSet)
urlpatterns = [
    url(r'^$', views.home, name='home'),
	url(r'^createpost/$', views.createpost, name='createpost'),
	url(r'^liveUpdate/$', views.liveUpdate, name='liveUpdate'),
	url(r'^currentCrisis/$', views.currentCrisis, name='currentCrisis'),
	url(r'^crisis/$', views.crisis, name='crisis'),
	url(r'^historicalCrisis/$', views.historicalCrisis, name='historicalCrisis'),
	url(r'^broadcast/$', views.broadcast, name='broadcast'),
	url(r'^home/$', views.home, name='home'),
	url(r'^justification/$', views.justification, name='justification'),
	url(r'^api/jReport/', include(router.urls)),
	url(r'^api/aReport/', include(router2.urls)),
	url(r'^logout/',views.logout,name='logout'),
    url(r'^otp/', views.otp,name='otp'),
	url(r'^resendOTP/$',views.resendOTP,name='resendOTP'),
    url(r'^otpAuthentication/$',views.otpAuthentication,name='otpAuthentication')

   
]