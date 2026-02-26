Smart Route Fuel Optimizer API
An optimized Django REST API that calculates driving routes within the USA, determines cost-effective fuel stops (500 mile max range), and computes total fuel cost assuming 10 MPG efficiency.
Tech Stack
- Django 5.x
- OpenRouteService (Routing API)
- OpenStreetMap (Map Data)
- Shapely (Geometry Processing)
- U.S. Energy Information Administration (Fuel Pricing Data)
Features
• Single routing API call per request
• Production-grade greedy fuel optimization
• Simplified route geometry for fast responses
• Deterministic cost calculation
• Local CSV-based fuel pricing (no repeated external calls)
Project Structure
smart_route/
│
├── smart_route/
│   └── settings.py
│
├── routeapp/
│   ├── views.py
│   ├── urls.py
│   ├── models.py
│
├── fuel_prices.csv
├── .env
├── requirements.txt
└── manage.py
Environment Variables (.env)
EIA_API_KEY=your_eia_api_key
ORS_API_KEY=your_openrouteservice_key
Fuel Data Format (fuel_prices.csv)
station_id,latitude,longitude,state,price
1,32.7767,-96.7970,TX,3.25
2,39.7392,-104.9903,CO,3.50
Installation Steps
1. Create virtual environment
2. Activate virtual environment
3. pip install -r requirements.txt
4. python manage.py migrate
5. python manage.py runserver
API Endpoint
POST http://127.0.0.1:8000/api/route/
Sample Request Body
{
  "start": "Dallas, TX",
  "finish": "Denver, CO"
}
Sample Response Fields
- total_distance_miles
- fuel_stops (optimized cheapest stops within 500 mile range)
- total_fuel_cost
- route_geojson (simplified LineString geometry)
Fuel Optimization Logic
• Vehicle max range: 500 miles
• Efficiency: 10 MPG
• Greedy selection of cheapest reachable station
• Refill to full tank at each stop
• Continue until destination reached
Production Notes
• Route geometry simplified to reduce payload size
• Only optimized stops returned
• Single routing API call
• Suitable for caching layer (Redis recommended)
Future Enhancements
• Real-time gas station pricing
• Traffic-aware routing
• EV charging optimization
• Cost vs Time optimization mode
