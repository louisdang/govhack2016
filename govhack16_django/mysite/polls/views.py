from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib.staticfiles import finders
import os
import urllib2  # the lib that handles the url stuff

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

# Create your views here.

def search_form(request):
	#return HttpResponse("search_form.")
	return render(request, 'search_form.html')
	
def search_postcode(request):	
	if 'postcode' in request.GET:
		postcode = request.GET['postcode']
	
		print "school function"
		#print postcode
			
		#url_file = static('Government-School-Locations.txt')
		#print url_file
		
		#data = urllib2.urlopen('https://github.com/ronniels92372/govhack2016/blob/master/Government-School-Locations.txt')
		 
		result = finders.find('Government-School-Locations.txt')
		searched_locations = finders.searched_locations
		#print searched_locations
		file_path = os.path.join(searched_locations[1],'Government-School-Locations.txt')
		
		with open(file_path) as f:
			first_line = f.readline()
			print first_line
			
			first_line = f.readline()
			lines = f.readlines()
				
			for each_line in lines:
				cols = each_line.split("\t")
					
				school_name_col = cols[2]
				postcode_col = cols[19]
				total_enrollments = cols[10]
				lat = cols[20]
				long = cols[21]
					
				
				if(str(postcode) == postcode_col):
					print "---------------------"
					print postcode_col
					print school_name_col
					print total_enrollments
					print lat
					print long
					
		
		
	return HttpResponse("POST CODE.")
	#return render(request, 'search_form.html')

