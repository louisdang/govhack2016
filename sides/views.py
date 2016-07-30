from django.http import HttpResponseBadRequest, JsonResponse
from sides import utils
import json

def get_optimal_routes(request):
    if request.method=='GET':
    	if 'data' not in request.GET:
    		return HttpResponseBadRequest("No input data received")
        received_json_data=json.loads(request.GET['data'])
        result = utils.get_optimal_routes(received_json_data)
        return JsonResponse(result)
    else:
        return HttpResponseBadRequest("Only accepts GET for now")

