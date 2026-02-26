from django.shortcuts import render
# Create your views here.
import os
import requests
import polyline
import pandas as pd
from shapely.geometry import LineString, Point
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings

VEHICLE_RANGE_MILES = 500
MPG = 10

# Load fuel CSV once
FUEL_DF = pd.read_csv("fuel_prices.csv")
FUEL_DF["point"] = FUEL_DF.apply(lambda r: Point(r["longitude"], r["latitude"]), axis=1)

class RouteFuelAPIView(APIView):

    def post(self, request):
        start = request.data.get("start")
        finish = request.data.get("finish")
        if not start or not finish:
            return Response({"error": "start and finish required"}, status=400)

        # 1️ Geocode start/finish
        coords = self.geocode_locations(start, finish)

        # 2️ Call OpenRouteService once
        ors_url = "https://api.openrouteservice.org/v2/directions/driving-car"
        headers = {"Authorization": settings.ORS_API_KEY, "Content-Type": "application/json"}
        body = {"coordinates": coords}
        r = requests.post(ors_url, headers=headers, json=body)
        if r.status_code != 200:
            return Response({"error": "Routing API failed"}, status=500)

        data = r.json()
        geometry = data["routes"][0]["geometry"]
        distance_meters = data["routes"][0]["summary"]["distance"]
        total_miles = distance_meters * 0.000621371
        route_coords = polyline.decode(geometry)
        route_line = LineString([(lng, lat) for lat, lng in route_coords])

        # 3️ Filter fuel stations near route
        buffer_miles = 10 / 69
        route_buffer = route_line.buffer(buffer_miles)
        stations_near_route = FUEL_DF[FUEL_DF["point"].apply(lambda p: route_buffer.contains(p))].copy()

        # 4️ Project stations to route miles
        def project_station(point):
            nearest = route_line.interpolate(route_line.project(point))
            dist = route_line.project(nearest)
            return (dist / route_line.length) * total_miles
        stations_near_route["mile_marker"] = stations_near_route["point"].apply(project_station)
        stations_near_route = stations_near_route.sort_values("mile_marker")

        # 5️ Production-grade greedy fuel optimization
        fuel_stops = []
        current_pos = 0
        tank_capacity = VEHICLE_RANGE_MILES
        fuel_remaining = tank_capacity
        total_cost = 0
        last_price = 0

        while current_pos < total_miles:
            max_reach = current_pos + fuel_remaining
            if max_reach >= total_miles:
                gallons_needed = (total_miles - current_pos) / MPG
                total_cost += gallons_needed * last_price
                break

            reachable = stations_near_route[
                (stations_near_route["mile_marker"] > current_pos) &
                (stations_near_route["mile_marker"] <= current_pos + tank_capacity)
            ]
            if reachable.empty:
                return Response({"error": "No reachable fuel station. Trip impossible."}, status=400)

            cheapest = reachable.sort_values("price").iloc[0]
            distance_to_station = cheapest["mile_marker"] - current_pos
            fuel_remaining -= distance_to_station
            gallons_to_fill = tank_capacity - fuel_remaining
            cost_here = gallons_to_fill * cheapest["price"]
            total_cost += cost_here
            fuel_remaining = tank_capacity
            current_pos = cheapest["mile_marker"]
            last_price = cheapest["price"]
            fuel_stops.append({
                "latitude": cheapest["latitude"],
                "longitude": cheapest["longitude"],
                "price": cheapest["price"],
                "mile_marker": round(current_pos, 2)
            })
        simplified_line = route_line.simplify(0.01)
        route_line = LineString([(lng, lat) for lat, lng in route_coords])

        # Simplify the route to reduce points (~1 mile tolerance)
        simplified_line = route_line.simplify(0.09)  # adjust 0.01 as needed

        # Convert to coordinates for JSON
        simplified_coords = [(lng, lat) for lng, lat in simplified_line.coords]
        return Response({
            "total_distance_miles": round(total_miles, 2),
            "fuel_stops": fuel_stops,
            "total_fuel_cost": round(total_cost, 2),
            "route_geojson": {
                "type": "LineString",
                "coordinates": simplified_coords
                # "coordinates": [
                #     (c[0], c[1]) if isinstance(c, tuple) else (c.x, c.y)
                #     for c in simplified_line.coords
                # ]
            }
        })

    def geocode_locations(self, start, finish):
        url = "https://api.openrouteservice.org/geocode/search"
        headers = {"Authorization": settings.ORS_API_KEY}

        def get_coords(place):
            r = requests.get(url, headers=headers, params={"text": place})
            return r.json()["features"][0]["geometry"]["coordinates"]

        return [get_coords(start), get_coords(finish)]