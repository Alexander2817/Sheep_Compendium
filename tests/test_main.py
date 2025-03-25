#Import TestClient to simulate API requests
from fastapi.testclient import TestClient

#Import the FastAPI app instance from the controller module
from main import app

#Create a TestClient instance for the FastAPI app
client = TestClient(app)

#Define a test function for reading a specific sheep
def test_read_sheep():
    #Send a GET request to the endpoint "/sheep/1"
    response = client.get("/sheep/1")

    #Assert that the response status code is 200(OK)
    assert response.status_code == 200

    #Assert that the response JSON matches the expected data
    assert response.json() == {
        #Expceted JSON structure
        "id": 1,
        "name": "Spice",
        "breed": "Gotland",
        "sex": "ewe"
    }

#Define a test function for adding a new sheep
def test_add_sheep():

    #TODO: Prepare the new sheep data in a dictionary format
    new_sheep_data = {
        "id": 10,
        "name": "Chowder",
        "breed": "Suffolk",
        "sex": "ewe"
    }

    #TODO: Send a POST request to the endpoint "/sheep" with the new sheep data.
    #Arguments should be your endpoint and new sheep data
    response = client.post("/sheep", json=new_sheep_data)

    #TODO: Assert that the response status code is 201 (Created)
    assert response.status_code == 201

    #TODO: Assert that the response JSON matches the new sheep data
    assert response.json() == new_sheep_data

    #TODO: Verify that the sheep was actually added to the database by retrieving the new sheep by ID
    get_response = client.get(f"/sheep/{new_sheep_data['id']}")

    # Include an assert statement to see if the new sheep data can be retrieved.
    assert get_response.status_code == 200

def test_delete_sheep():
    sheep_data = {
        "id": 11,
        "name": "Naruto",
        "breed": "Border Leicester",
        "sex": "ram"
    }
    client.post("/sheep", json=sheep_data)

    response = client.delete(f"/sheep/{sheep_data['id']}")
    assert response.status_code == 204

    get_response = client.get(f"/sheep/{sheep_data['id']}")
    assert get_response.status_code == 404

def test_update_sheep():
    sheep_data = {
        "id": 12,
        "name": "Luffy",
        "breed": "Suffolk",
        "sex": "ram"
    }
    client.post("/sheep", json=sheep_data)

    update_data = {
        "id": 1,
        "name": "Spice",
        "breed": "Gotland",
        "sex": "ewe"
    }

    response = client.put(f"/sheep/{sheep_data['id']}", json=update_data)

    assert response.status_code == 200
    assert response.json() == update_data

    get_response = client.get(f"/sheep/{sheep_data['id']}")

    assert get_response.status_code == 200
    assert response.json() == update_data

def test_read_all_sheep():
    client.post("/sheep", json={"id": 13, "name": "Zoro", "breed": "Suffolk", "sex": "ram"})
    client.post("/sheep", json={"id": 14, "name": "Sanji", "breed": "Suffolk", "sex": "ram"})

    response = client.get("/sheep")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    # Makes sure that more than 1 sheep are returned
    assert len(response.json()) > 1