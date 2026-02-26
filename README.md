# 🚗 Smart Route Fuel Optimizer API

> An optimized Django REST API that calculates driving routes within the USA, determines cost-effective fuel stops, and computes total fuel cost.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Tech Stack](#-tech-stack)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Environment Variables](#-environment-variables)
- [Fuel Data Format](#-fuel-data-format)
- [Installation](#-installation)
- [API Usage](#-api-usage)
- [Fuel Optimization Logic](#-fuel-optimization-logic)
- [Performance](#-performance-characteristics)
- [Future Enhancements](#-future-enhancements)

---

## 🌐 Overview

The **Smart Route Fuel Optimizer** helps drivers plan cost-effective road trips across the USA by:

- Calculating driving routes using OpenRouteService
- Identifying the cheapest fuel stops along the route (within a 500-mile max range)
- Computing total fuel cost based on a **10 MPG** vehicle efficiency assumption
- Minimizing external API calls for fast, reliable responses

---

## 🏗 Tech Stack

| Tool | Purpose |
|------|---------|
| **Django 5.x** | Backend web framework |
| **OpenRouteService** | Routing API |
| **OpenStreetMap** | Map data |
| **Shapely** | Geometry processing |
| **U.S. Energy Information Administration (EIA)** | Fuel pricing data |

---

## ✨ Features

- ✅ Single routing API call per request
- ✅ Production-grade greedy fuel optimization
- ✅ Simplified route geometry for fast responses
- ✅ Deterministic fuel cost calculation
- ✅ Local CSV-based fuel pricing (no repeated external calls)

---

## 📁 Project Structure

```
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
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
EIA_API_KEY=your_eia_api_key
ORS_API_KEY=your_openrouteservice_key
```

> 🔑 Get your **ORS API Key** at [openrouteservice.org](https://openrouteservice.org/)  
> 🔑 Get your **EIA API Key** at [eia.gov/opendata](https://www.eia.gov/opendata/)

---

## ⛽ Fuel Data Format

The `fuel_prices.csv` file should be placed in the project root with the following structure:

```csv
station_id,latitude,longitude,state,price
1,32.7767,-96.7970,TX,3.25
2,39.7392,-104.9903,CO,3.50
```

| Column | Description |
|--------|-------------|
| `station_id` | Unique station identifier |
| `latitude` | Station latitude |
| `longitude` | Station longitude |
| `state` | 2-letter state code |
| `price` | Price per gallon (USD) |

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/smart-route-fuel-optimizer.git
cd smart-route-fuel-optimizer
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
```

### 3️⃣ Activate the Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Configure Environment Variables

```bash
cp .env.example .env
# Then edit .env with your API keys
```

### 6️⃣ Run Migrations

```bash
python manage.py migrate
```

### 7️⃣ Start the Server

```bash
python manage.py runserver
```

---

## 🚀 API Usage

### Endpoint

```
POST http://127.0.0.1:8000/api/route/
```

### Request

```json
{
  "start": "Dallas, TX",
  "finish": "Denver, CO"
}
```

### Response

```json
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
    "coordinates": ["..."]
  }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `total_distance_miles` | float | Total route distance in miles |
| `fuel_stops` | array | List of optimized fuel stop objects |
| `fuel_stops[].latitude` | float | Stop latitude |
| `fuel_stops[].longitude` | float | Stop longitude |
| `fuel_stops[].price` | float | Price per gallon at this stop |
| `fuel_stops[].mile_marker` | float | Distance from start at this stop |
| `total_fuel_cost` | float | Total estimated fuel cost in USD |
| `route_geojson` | object | Simplified GeoJSON LineString of the route |

---

## 🧠 Fuel Optimization Logic

### Vehicle Assumptions

| Parameter | Value |
|-----------|-------|
| Max Range | 500 miles |
| Fuel Efficiency | 10 MPG |
| Tank Capacity | 50 gallons |

### Algorithm

```
1. Call OpenRouteService API once to get the full route.
2. Decode and simplify route geometry using Shapely.
3. Identify all fuel stations within a corridor along the route.
4. Apply greedy selection:
   a. From current position, find all reachable stations (≤ 500 miles).
   b. Select the cheapest station among them.
   c. Refuel to full range.
   d. Repeat until destination is within range.
5. Calculate total gallons consumed and total cost.
```

### Greedy Selection Diagram

```
Start ──► [Cheap Stop 1] ──► [Cheap Stop 2] ──► ... ──► Destination
           ↑ within 500mi      ↑ within 500mi
           cheapest available   cheapest available
```

---

## ⚡ Performance Characteristics

| Characteristic | Detail |
|----------------|--------|
| External API calls | **1 per request** (OpenRouteService only) |
| Fuel data source | Local CSV (no repeated API calls) |
| Geometry handling | Simplified before returning |
| Response payload | Only optimized stops returned |
| Caching | Redis recommended for production |

---

## 🔮 Future Enhancements

- [ ] Real-time station-level fuel pricing
- [ ] Traffic-aware routing
- [ ] Electric vehicle (EV) charging optimization
- [ ] Cost vs. time optimization modes
- [ ] Spatial indexing for large fuel datasets
- [ ] Redis caching layer
- [ ] Dockerized deployment

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
