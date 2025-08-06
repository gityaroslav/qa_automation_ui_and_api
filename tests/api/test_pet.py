import random
import pytest
from tenacity import retry, stop_after_attempt, wait_fixed


@retry(stop=stop_after_attempt(5), wait=wait_fixed(1))
def get_pet_with_retries(pet_api_client, pet_id):
    get_response = pet_api_client.get_pet_by_id(pet_id)
    assert get_response.status_code == 200
    return get_response


@pytest.mark.xfail(reason="API returns 404 on GET for a recently created pet, indicating a consistency issue.")
def test_get_pet_by_id_is_successful(pet_api_client, created_pet_id):
    get_response = get_pet_with_retries(pet_api_client, created_pet_id)
    assert get_response.json()['id'] == created_pet_id


def test_get_pet_by_status_is_successful(pet_api_client):
    pet_status = "available"
    get_response = pet_api_client.get_pet_by_status(pet_status)
    assert get_response.status_code == 200
    get_response_json = get_response.json()
    for pet in get_response_json:
        assert pet["status"] == pet_status


def test_get_pet_by_invalid_id_fails(pet_api_client):
    get_response = pet_api_client.get_pet_by_id('')
    assert get_response.status_code == 405


def test_create_pet_with_valid_data_is_successful(pet_api_client):
    pet_id = random.randint(1000000, 9999999)
    pet_name = f"TestPet_{pet_id}"
    pet_status = "available"
    pet_data = {
        "id": pet_id,
        "name": pet_name,
        "status": pet_status
    }
    create_response = pet_api_client.create_pet(pet_data)
    assert create_response.status_code == 200
    response_json = create_response.json()
    assert response_json['id'] == pet_id
    assert response_json['name'] == pet_name
    assert response_json['status'] == pet_status
    pet_api_client.delete_pet(pet_id)


@pytest.mark.xfail(reason="API returns 200 instead of 400 when 'name' is missing")
def test_create_pet_with_missing_required_field_fails(pet_api_client):
    pet_id = random.randint(1000000, 9999999)
    pet_status = "available"
    pet_data = {
        "id": pet_id,
        "status": pet_status
    }
    create_response = pet_api_client.create_pet(pet_data)
    assert create_response.status_code == 400
    pet_api_client.delete_pet(pet_id)


@pytest.mark.xfail(reason="API accepts string for 'id' instead of integer, returning 200 OK.")
def test_create_pet_with_invalid_id_type_fails(pet_api_client):
    pet_id = random.randint(1000000, 9999999)
    pet_name = f"TestPet_{pet_id}"
    pet_status = "available"
    pet_data = {
        "id": str(pet_id),
        "name": pet_name,
        "status": pet_status
    }
    create_response = pet_api_client.create_pet(pet_data)
    assert create_response.status_code == 400
    pet_api_client.delete_pet(pet_id)


@pytest.mark.xfail(reason="API Update (PUT) does not reflect changes, or takes too long to reflect.")
def test_update_existing_pet_is_successful(pet_api_client, created_pet_id):
    update_pet_name = f"UpdatedPet_{created_pet_id}"
    update_pet_data = {
        "id": created_pet_id,
        "name": update_pet_name,
        "status": "sold"
    }
    update_response = pet_api_client.update_pet(update_pet_data)
    update_response_json = update_response.json()
    assert update_response.status_code == 200
    assert update_response_json['id'] == created_pet_id
    assert update_response_json['name'] == update_pet_name
    assert update_response_json['status'] == update_pet_data["status"]
    get_response = get_pet_with_retries(pet_api_client, created_pet_id)
    get_response_json = get_response.json()
    assert get_response_json['id'] == created_pet_id
    assert get_response_json['name'] == update_pet_name
    assert get_response_json['status'] == update_pet_data["status"]


@pytest.mark.xfail(
    reason="API returns 404 on DELETE for a recently created/retrieved pet, indicating a consistency issue.")
def test_delete_existing_pet_is_successful(pet_api_client):
    pet_id = random.randint(1000000, 9999999)
    pet_name = f"TestPet_{pet_id}"
    pet_status = "available"
    pet_data = {
        "id": pet_id,
        "name": pet_name,
        "status": pet_status
    }
    create_response = pet_api_client.create_pet(pet_data)
    assert create_response.status_code == 200
    response_json = create_response.json()
    assert response_json['id'] == pet_id
    assert response_json['name'] == pet_name
    assert response_json['status'] == pet_status

    get_before_delete_response = get_pet_with_retries(pet_api_client, pet_id)
    assert get_before_delete_response.status_code == 200

    delete_response = pet_api_client.delete_pet(pet_id)
    assert delete_response.status_code == 200

    get_after_delete_response = pet_api_client.get_pet_by_id(pet_id)
    assert get_after_delete_response.status_code == 404
