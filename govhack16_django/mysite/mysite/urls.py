from django.conf.urls import include, url
from django.contrib import admin

from django.contrib import admin
#from search_recipes.views import search_recipes_form, search_recipes, get_full_recipe
from polls.views import search_form,search_postcode
from django.conf import settings

urlpatterns = [
    url(r'^polls/', include('polls.urls')),
    url(r'^admin/', admin.site.urls),
	url(r'^search_form/', search_form),
	url(r'^search_postcode/', search_postcode),
]