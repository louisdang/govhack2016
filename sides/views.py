from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse, HttpResponseServerError
from sides import utils
import json
import logging

log = logging.getLogger(__name__)

def get_optimal_routes(request):
	try:
	    if request.method=='POST':
	    	#if 'data' not in request.POST:
	    		#return HttpResponseBadRequest("No input data received")
	        #received_json_data=json.loads(request.POST['data'])
	        log.info(request.POST)
	        if 'data' in request.POST:
	        	log.info(request.POST['data'])
	        if 'sources' not in request.POST:
	        	return HttpResponseBadRequest("No sources")
	        if 'destinations' not in request.POST:
	        	return HttpResponseBadRequest("No destinations")

	        result = utils.get_optimal_routes(request.POST['sources'], (request.POST['destinations']))
	    	return JsonResponse(result)
	    else:
	        return HttpResponseBadRequest("Only accepts POST for now")
	except Exception as e:
		return HttpResponseServerError("Server erro: {}".format(e))
