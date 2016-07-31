import googlemaps
gmaps = googlemaps.Client(key='AIzaSyDPvDQc0_i1cT9sMoT7vnHRUuk8vF3D1CE')
from pulp import LpProblem, LpMinimize, LpInteger, LpVariable, lpSum
import collections
import logging

logging.basicConfig()
log = logging.getLogger(__name__)

def convert_int(x):
    try:
        return int(float(x))
    except ValueError:
        raise


def get_optimal_routes(sources, destinations):
    sources = collections.OrderedDict([(x['id'], x) for x in sources])
    destinations = collections.OrderedDict([(x['id'], x) for x in destinations])

    sources_points = [{'lat': x['lat'], 'lng': x['lng']} for x in sources.values()]
    destinations_points = [{'lat': x['lat'], 'lng': x['lng']} for x in destinations.values()]

    source_ids = [x['id'] for x in sources.values()]
    dest_ids = [x['id'] for x in destinations.values()]

    demand = {x['id']: x['num_students'] for x in sources.values()}
    supply = {x['id']: x['capacity'] for x in destinations.values()}

    log.info("Calling gmaps api...")
    distances = gmaps.distance_matrix(origins=sources_points, destinations=destinations_points, mode='walking')

    costs = {}
    for i, origin in enumerate(distances['rows']):
        origin_costs = {}
        for j, entry in enumerate(origin['elements']):
            origin_costs[dest_ids[j]] = entry['duration']['value']
        costs[source_ids[i]] = origin_costs

    prob = LpProblem("Evaucation Routing for Schools",LpMinimize)
    routes = [(s,d) for s in source_ids for d in dest_ids]
    route_lookup = {'Route_{}_{}'.format(x.replace(' ','_'),y.replace(' ','_')):(x,y) for (x,y) in routes}
    route_vars = LpVariable.dicts("Route",(source_ids,dest_ids),0,None,LpInteger)
    prob += lpSum([route_vars[w][b]*(costs[w][b]**2) for (w,b) in routes])
    for dest in dest_ids:
        prob += lpSum([route_vars[source][dest] for source in source_ids]) <= supply[dest], "Students going to {} is <= {}".format(demand, supply[dest])
    for source in source_ids:
        prob += lpSum([route_vars[source][dest] for dest in dest_ids]) == demand[source], "Students leaving {} is {}".format(source, demand[source])

    log.info("Optimizing routes...")
    prob.solve()

    if prob.status != 1:
        raise Exception("Algorithm could not converge to a solution")

    result = []
    for v in prob.variables():
        src, dst = route_lookup[v.name]
        value = v.value()
        result.append({'src': sources[src], 'dst': destinations[dst], 'value': int(value)})
    return result

if __name__ == '__main__':
    import csv
    import os
    schools = collections.OrderedDict()
    for row in csv.DictReader(open(os.path.expanduser('~/workbook1.csv'))):
        try:
            schools[row['SCHOOL_NAME']] =\
                {'id': row['SCHOOL_NAME'],
                'lat': float(row['LATITUDE']),
                'lng': float(row['LONGITUDE']),
                'num_students': convert_int(row['TOTAL_ENROLMENTS'])}
        except ValueError:
            continue

    sources = schools.values()[:3]
    destinations = schools.values()[4:10]
    results = get_optimal_routes(sources, destinations)