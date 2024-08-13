from http import client
import pytest


@pytest.mark.asyncio
async def test_get_cities_by_state_valid_code():
    state_code = "SP" 
    expected_cities = [
        {"city_id": 1, "name": "São Paulo"},
        {"city_id": 2, "name": "Campinas"}
    ]
    
    response = await client.get(f"/cities/state/{state_code}")

    assert response.status_code == 200
    assert response.json() == {"cities": expected_cities}

@pytest.mark.asyncio
async def test_get_cities_by_state_invalid_code():
    state_code = "ZZ"  
    
    response = await client.get(f"/cities/state/{state_code}")

    assert response.status_code == 404
    assert response.json() == {"detail": "State not found."}

@pytest.mark.asyncio
async def test_get_cities_by_state_missing_code():
    state_code = ""  
    
    response = await client.get(f"/cities/state/{state_code}")

    assert response.status_code == 422  
    assert "detail" in response.json()

@pytest.mark.asyncio
async def test_get_cities_by_state_no_cities():
    state_code = "XX" 

    response = await client.get(f"/cities/state/{state_code}")

    assert response.status_code == 404
    assert response.json() == {"detail": "State not found."}