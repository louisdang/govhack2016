from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse
from sides import utils
import json

def get_optimal_routes(request):
    if request.method=='POST':
    	if 'data' not in request.POST:
    		return HttpResponseBadRequest("No input data received")
        received_json_data=json.loads(request.POST['data'])
        result = utils.POST_optimal_routes(received_json_data['sources'], received_json_data['destinations'])
        if 'callback' in request.REQUEST:
                # a jsonp response!
                resp_text = '%s(%s);' % (request.REQUEST['callback'], json.dumps(result))
            	return HttpResponse(resp_text, "text/javascript")
        else:
        	return JsonResponse(result)
    else:
        return HttpResponseBadRequest("Only accepts POST for now")

