from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse, HttpResponseServerError
from sides import utils
import json
import logging

log = logging.getLogger(__name__)
logging.basicConfig(filename='/home/ec2-user/log')

def get_optimal_routes(request):
	try:
	    if request.method=='POST':
	    	data = request.body
	    	#if 'data' not in request.POST:
	    		#return HttpResponseBadRequest("No input data received")
	        #received_json_data=json.loads(request.POST['data'])
	        log.info(request.POST)

	        result = utils.get_optimal_routes(data['sources'], (data['destinations']))
	    	return JsonResponse(result)
	    else:
	        return HttpResponseBadRequest("Only accepts POST for now")
	except Exception as e:
		return HttpResponseServerError("Server erro: {}".format(e))
