from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import requests
import string
from django.http import JsonResponse


# Create your views here.
@csrf_exempt
def homepage(request):
    if request.method == 'POST':
        api_key = "U9uh3A0yoBtn4AsGATf8k9rGWSANYDuN"
        vlat = request.POST.get('var_lat')
        vlon = request.POST.get('var_lon')
        locationurl = "https://api.tomtom.com/search/2/reverseGeocode/" + vlat + "%2C" + vlon + "+json?key=" + api_key
        location_info = requests.get(locationurl)
        location_info = location_info.json()
        location_state = location_info['addresses'][0]['address']['countrySubdivision']
        location_city = location_info['addresses'][0]['address']['countrySecondarySubdivision']
        corona_stats_url = "https://api.covid19india.org/state_district_wise.json"
        corona_info = requests.get(corona_stats_url)
        corona_info = corona_info.json()
        location_state = string.capwords(location_state)
        location_city = string.capwords(location_city)
        active = corona_info[location_state]['districtData'][location_city]['active']
        confirmed = corona_info[location_state]['districtData'][location_city]['confirmed']
        died = corona_info[location_state]['districtData'][location_city]['deceased']
        recovered = corona_info[location_state]['districtData'][location_city]['recovered']
        corona_stats = {
            "city": location_city,
            "state": location_state,
            "active": active,
            "confirmed": confirmed,
            "died": died,
            "recovered": recovered
        }
        return JsonResponse(corona_stats, safe=False)
    return render(request, 'index.html')
