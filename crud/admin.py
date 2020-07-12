from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Member)
admin.site.register(Document)
admin.site.register(ContactList)



class CovidAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'start_date','affectedtoday', 'todayRecovered', 'todayDeaths', 'todayTests', 'totalPositive', 'totalRecovered', 'totalDeaths', 'totalTests', 'end_date')
  list_display_links = ('id', 'name')
  search_fields = ('name', 'affectedtoday', 'todayRecovered', 'todayDeaths', 'todayTests', 'totalPositive', 'totalRecovered')
  list_per_page = 30

admin.site.register(CsvUpload, CovidAdmin)



class CovidDistrict(admin.ModelAdmin):
  list_display = ('id', 'start_date', 'SylhetDivision','RangpurDivision', 'RajshahiDivision', 'MymensinghDivision', 'KhulnaDivision', 'DhakaDivision', 'ChittagongDivision', 'BarisalDivision')
  list_display_links = ('id', 'SylhetDivision')
  search_fields = ('id', 'start_date')
  list_per_page = 30

admin.site.register(CsvUploadFile, CovidDistrict)


