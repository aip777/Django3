from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Member)
admin.site.register(Document)
admin.site.register(ContactList)



class CovidAdmin(admin.ModelAdmin):
  list_display = ('id', 'name','affectedtoday', 'todayRecovered', 'todayDeaths', 'todayTests', 'totalPositive', 'totalRecovered', 'totalDeaths', 'totalTests')
  list_display_links = ('id', 'name')
  search_fields = ('name', 'affectedtoday', 'todayRecovered', 'todayDeaths', 'todayTests', 'totalPositive', 'totalRecovered')
  list_per_page = 25

admin.site.register(CsvUpload, CovidAdmin)

