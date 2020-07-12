from django.conf.urls import url


from .views import (
    # StatusListSearchAPIView,
    CovidAPIView,
    ListingAPIDetailView,
    # StatusCreateAPIView,
    # StatusDetailAPIView,
    # StatusUpdateAPIView,
    # StatusDeleteAPIView,
    DistrictAndDivisionAPIView,
    DistrictAndDivisionDetailAPI,
)
urlpatterns = [
    url(r'^$', CovidAPIView.as_view()),
    url(r'^(?P<id>\d+)/$', ListingAPIDetailView.as_view()),

    url(r'^district/$', DistrictAndDivisionAPIView.as_view()),
    url(r'^district/(?P<id>\d+)/$', DistrictAndDivisionDetailAPI.as_view()),

    # url(r'^create/$', StatusCreateAPIView.as_view()),
    # url(r'(?P<id>\d+)/$', StatusDetailAPIView.as_view()),


    # url(r'^(?P<pk>\d+)/update/$', StatusUpdateAPIView.as_view()),
    # url(r'^(?P<pk>\d+)/delete/$', StatusDeleteAPIView.as_view()),

]