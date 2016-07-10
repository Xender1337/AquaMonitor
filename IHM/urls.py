from django.conf.urls import url

from IHM import views

urlpatterns = [
        url(r'^index$',                                          view=views.index,      name='index'),
        url(r'^index$',                                          view=views.index,      name='index'),
        url(r'^settings$',                                          view=views.settings,      name='settings'),
        url(r'^json$',                                          view=views.get_json,      name='json'),
]
