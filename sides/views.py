from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse, HttpResponseServerError
from sides import utils
import json
import logging
from django.shortcuts import render
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib.staticfiles import finders
import os
import urllib2  # the lib that handles the url stuff
import json
from django.http import JsonResponse

log = logging.getLogger(__name__)
logging.basicConfig(filename='/home/ec2-user/log')

def get_optimal_routes(request):
	try:
	    if request.method=='POST':
	    	data = json.loads(request.body)	    	
	        log.info(request.POST)

	        result = utils.get_optimal_routes(data['sources'], (data['destinations']))
	    	return JsonResponse(result, safe=False)
	    else:
	        return HttpResponseBadRequest("Only accepts POST for now")
	except Exception as e:
		return HttpResponseServerError("Server error: {}".format(e))


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

# Create your views here.

def search_form(request):
	#return HttpResponse("search_form.")
	#return render(request, 'search_form.html')
	return render(request, 'index.html')
	
def search_postcode(request):
	
	if 'postcode' in request.GET:
		postcode = request.GET['postcode']
	
		json_array = []
			
		#url_file = static('Government-School-Locations.txt')
		#print url_file
		
		#data = urllib2.urlopen('https://github.com/ronniels92372/govhack2016/blob/master/Government-School-Locations.txt')
		
		 
		finders.find('Government-School-Locations.txt')
		searched_locations = finders.searched_locations
		#print searched_locations
		file_path = os.path.join(searched_locations[-1],'Government-School-Locations.txt')
		print file_path
		
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
					
					data = {
					'json_school_name' : school_name_col,
					'json_total_enrollments' : total_enrollments,
					'lat' : lat,
					'long' : long
					}
			
					json_school_output = json.dumps(data)
					json_array.append(json_school_output)
		
		
		
	#return HttpResponse("POST CODE.")
	return JsonResponse({'json_array': json_array})
	#return render(request, 'search_postcode.html',{'json_array': json_array})

