from http import client
import pytest


@pytest.mark.asyncio
async def test_get_cities_by_state_valid_code():
    state_code = "SP"  # Exemplo de código de estado válido
    expected_cities = [
        {"city_id": 1, "name": "São Paulo"},
        {"city_id": 2, "name": "Campinas"}
    ]
    
    # Simule uma chamada GET para a rota
    response = await client.get(f"/cities/state/{state_code}")

    assert response.status_code == 200
    assert response.json() == {"cities": expected_cities}

@pytest.mark.asyncio
async def test_get_cities_by_state_invalid_code():
    state_code = "ZZ"  # Exemplo de código de estado inválido
    
    # Simule uma chamada GET para a rota
    response = await client.get(f"/cities/state/{state_code}")

    assert response.status_code == 404
    assert response.json() == {"detail": "State not found."}

@pytest.mark.asyncio
async def test_get_cities_by_state_missing_code():
    state_code = ""  # Código de estado ausente
    
    # Simule uma chamada GET para a rota
    response = await client.get(f"/cities/state/{state_code}")

    assert response.status_code == 422  # Código de status para validação inválida
    assert "detail" in response.json()

# Caso de teste para estado que não possui cidades
@pytest.mark.asyncio
async def test_get_cities_by_state_no_cities():
    state_code = "XX"  # Código de estado que não possui cidades

    # Simule uma chamada GET para a rota
    response = await client.get(f"/cities/state/{state_code}")

    assert response.status_code == 404
    assert response.json() == {"detail": "State not found."}