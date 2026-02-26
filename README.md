🚗 Smart Route Fuel Optimizer API

An optimized Django REST API that:

Calculates driving routes within the USA

Determines cost-effective fuel stops (500 mile max range)

Computes total fuel cost assuming 10 MPG efficiency

Minimizes external routing API calls

Returns simplified route geometry for fast responses

🏗 Tech Stack

Django 5.x

OpenRouteService (Routing API)

OpenStreetMap (Map Data)

Shapely (Geometry Processing)

U.S. Energy Information Administration (Fuel Pricing Data)

✨ Features

✅ Single routing API call per request

✅ Production-grade greedy fuel optimization

✅ Simplified route geometry for fast responses

✅ Deterministic fuel cost calculation

✅ Local CSV-based fuel pricing (no repeated external calls)

📁 Project Structure
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
🔐 Environment Variables (.env)

Create a .env file in the project root:

EIA_API_KEY=your_eia_api_key
ORS_API_KEY=your_openrouteservice_key
⛽ Fuel Data Format (fuel_prices.csv)
station_id,latitude,longitude,state,price
1,32.7767,-96.7970,TX,3.25
2,39.7392,-104.9903,CO,3.50

station_id → Unique ID

latitude → Station latitude

longitude → Station longitude

state → 2-letter state code

price → Price per gallon

⚙️ Installation
1️⃣ Create Virtual Environment
python -m venv venv
2️⃣ Activate Environment

Windows:

venv\Scripts\activate

Mac/Linux:

source venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Run Migrations
python manage.py migrate
5️⃣ Start Server
python manage.py runserver
🚀 API Endpoint
POST http://127.0.0.1:8000/api/route/
📥 Sample Request
{
  "start": "Dallas, TX",
  "finish": "Denver, CO"
}
📤 Sample Response Structure
{
  "total_distance_miles": 798.67,
  "fuel_stops": [
    {
      "latitude": 35.701148,
      "longitude": -102.295104,
      "price": 3.25,
      "mile_marker": 428.33
    }
  ],
  "total_fuel_cost": 1512.43,
  "route_geojson": {
    "type": "LineString",
    "coordinates": [...]
  }
}
🧠 Fuel Optimization Logic

Vehicle Assumptions:

Max Range: 500 miles

Fuel Efficiency: 10 MPG

Algorithm:

Call OpenRouteService once.

Decode and simplify route geometry.

Identify fuel stations along route corridor.

Apply greedy selection:

Choose cheapest reachable station within 500 miles.

Refill to full range.

Continue until destination.

Calculate total gallons and total cost.

⚡ Performance Characteristics

Route geometry simplified before returning.

Only optimized fuel stops returned.

CSV fuel data loaded locally (no repeated API calls).

Single external routing API call per request.

Suitable for caching (Redis recommended for production).

🔮 Future Enhancements

Real-time station-level fuel pricing

Traffic-aware routing

Electric vehicle charging optimization

Cost vs time optimization modes

Spatial indexing for large fuel datasets
