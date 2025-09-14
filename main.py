from fastapi import FastAPI, HTTPException, Query, Path
from typing import Dict, List, Optional
from uuid import UUID
from datetime import datetime

import socket
from models.health import Health
from models.city import CityCreate, CityRead, CityUpdate
from models.restaurant import RestaurantCreate, RestaurantRead, RestaurantUpdate

app = FastAPI(title="City/Restaurant API", version="0.1.0")

cities: Dict[UUID, CityRead] = {}
restaurants: Dict[UUID, RestaurantRead] = {}

# ----------------- Health Endpoint -----------------
def make_health(echo: Optional[str], path_echo: Optional[str] = None) -> Health:
    return Health(
        status=200,
        status_message="OK",
        timestamp=datetime.utcnow().isoformat() + "Z",
        ip_address=socket.gethostbyname(socket.gethostname()),
        echo=echo,
        path_echo=path_echo
    )
@app.get("/health", response_model=Health)
def get_health_no_path(echo: str | None = Query(None, description="Optional echo string")):
    return make_health(echo=echo)

@app.get("/health/{path_echo}", response_model=Health)
def get_health_with_path(
    path_echo: str = Path(..., description="Required echo in the URL path"),
    echo: str | None = Query(None, description="Optional echo string"),
):
    return make_health(echo=echo, path_echo=path_echo)

# ----------------- City Endpoints -----------------
@app.post("/cities", response_model=CityRead, status_code=201)
def create_city(city: CityCreate):
    city_read = CityRead(**city.model_dump())
    cities[city_read.id] = city_read
    return city_read

@app.get("/cities", response_model=List[CityRead])
def list_cities(
    name: Optional[str] = Query(None, description="Filter by city name"),
    country: Optional[str] = Query(None, description="Filter by country"),
    min_population: Optional[int] = Query(None, description="Filter by minimum population"),
    max_population: Optional[int] = Query(None, description="Filter by maximum population"),
):
    results = list(cities.values())
    if name is not None:
        results = [c for c in results if c.name == name]
    if country is not None:
        results = [c for c in results if c.country == country]
    if min_population is not None:
        results = [c for c in results if c.population and c.population >= min_population]
    if max_population is not None:
        results = [c for c in results if c.population and c.population <= max_population]
    return results

@app.get("/cities/{city_id}", response_model=CityRead)
def get_city(city_id: UUID):
    if city_id not in cities:
        raise HTTPException(status_code=404, detail="City not found")
    return cities[city_id]

@app.put("/cities/{city_id}", response_model=CityRead)
def update_city(city_id: UUID, city_update: CityCreate):
    if city_id not in cities:
        raise HTTPException(status_code=404, detail="City not found")
    cities[city_id] = CityRead(id=city_id, **city_update.model_dump())
    return cities[city_id]

@app.delete("/cities/{city_id}", status_code=204)
def delete_city(city_id: UUID):
    if city_id not in cities:
        raise HTTPException(status_code=404, detail="City not found")
    del cities[city_id]
    return

# ----------------- Restaurant Endpoints -----------------
@app.post("/restaurants", response_model=RestaurantRead, status_code=201)
def create_restaurant(restaurant: RestaurantCreate):
    if restaurant.city_id not in cities:
        raise HTTPException(status_code=400, detail="City does not exist")
    restaurant_read = RestaurantRead(**restaurant.model_dump())
    restaurants[restaurant_read.id] = restaurant_read
    return restaurant_read

@app.get("/restaurants", response_model=List[RestaurantRead])
def list_restaurants(
    name: Optional[str] = Query(None, description="Filter by restaurant name"),
    cuisine: Optional[str] = Query(None, description="Filter by cuisine type"),
    city_id: Optional[UUID] = Query(None, description="Filter by city UUID"),
    min_rating: Optional[float] = Query(None, description="Filter by minimum rating"),
    max_rating: Optional[float] = Query(None, description="Filter by maximum rating"),
):
    results = list(restaurants.values())
    if name is not None:
        results = [r for r in results if r.name == name]
    if cuisine is not None:
        results = [r for r in results if r.cuisine == cuisine]
    if city_id is not None:
        results = [r for r in results if r.city_id == city_id]
    if min_rating is not None:
        results = [r for r in results if r.rating and r.rating >= min_rating]
    if max_rating is not None:
        results = [r for r in results if r.rating and r.rating <= max_rating]
    return results

@app.get("/restaurants/{restaurant_id}", response_model=RestaurantRead)
def get_restaurant(restaurant_id: UUID):
    if restaurant_id not in restaurants:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurants[restaurant_id]

@app.put("/restaurants/{restaurant_id}", response_model=RestaurantRead)
def update_restaurant(restaurant_id: UUID, restaurant_update: RestaurantCreate):
    if restaurant_id not in restaurants:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    restaurants[restaurant_id] = RestaurantRead(id=restaurant_id, created_at=datetime.utcnow(), updated_at=datetime.utcnow(), **restaurant_update.model_dump())
    return restaurants[restaurant_id]

@app.delete("/restaurants/{restaurant_id}", status_code=204)
def delete_restaurant(restaurant_id: UUID):
    if restaurant_id not in restaurants:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    del restaurants[restaurant_id]
    return

@app.get("/")
def root():
    return {"message": "Welcome to the City/Restaurant API. See /docs for OpenAPI UI."}


if __name__ == "__main__":
    import os
    import uvicorn

    port = int(os.environ.get("FASTAPIPORT", 8001))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
