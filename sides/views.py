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
	
def get_bushfire_cat(school_code):
	bush_fire_risk = ""
	
	finders.find('NSW-Government-Schools-by-Bushfire-Category.txt')
	searched_locations = finders.searched_locations
	#print searched_locations
	file_path = os.path.join(searched_locations[-1],'NSW-Government-Schools-by-Bushfire-Category.txt')
	print file_path
	
	with open(file_path) as f:
		f.readline()
		lines = f.readlines()
		
		for each_line in lines:
			cols = each_line.split("\t")
			
			doe_school_code = cols[0].rstrip("\r\n")
			
			if(doe_school_code == school_code):
				print school_code
				
				bush_fire_risk = cols[2].rstrip("\r\n")
				break
			else:
				bush_fire_risk = "No_risk"
			
			print bush_fire_risk
			
	return bush_fire_risk		
	

def search_postcode(request):
	
	if 'postcode' in request.GET:
		postcode = request.GET['postcode']
	
		
		json_array = []
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
					
				school_code = cols[0].rstrip("\r\n")
				school_name_col = cols[2].rstrip("\r\n")
				postcode_col = cols[19].rstrip("\r\n")
				total_enrollments = cols[10].rstrip("\r\n")
				lat = cols[20].rstrip("\r\n")
				long = cols[21].rstrip("\r\n")
					
				if(str(postcode) == postcode_col):
					
					bush_fire_cat = get_bushfire_cat(school_code)

					print "---------------------"
					print postcode_col
					print school_name_col
					print total_enrollments
					print lat
					print long
					print bush_fire_cat
					
					data = {
					'json_school_name' : school_name_col,
					'json_total_enrollments' : total_enrollments,
					'lat' : lat,
					'long' : long,
					'bush_fire_cat' : bush_fire_cat
					}
			
			
					json_school_output = json.dumps(data)
					json_array.append(json_school_output)
		
		
		
	#return HttpResponse("POST CODE.")
	return JsonResponse({'json_array': json_array})
	#return render(request, 'search_postcode.html',{'json_array': json_array})

