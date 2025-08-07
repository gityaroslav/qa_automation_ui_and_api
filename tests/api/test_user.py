import random
import pytest
from tenacity import retry, stop_after_attempt, wait_fixed


@retry(stop=stop_after_attempt(10), wait=wait_fixed(1))
def get_user_with_retries(user_api_client, username):
    get_response = user_api_client.get_user_by_username(username)
    assert get_response.status_code == 200
    return get_response


@pytest.mark.xfail(reason="API returns 404 on DELETE during cleanup after user creation, indicating a consistency "
                          "issue.")
def test_create_user_with_valid_data_is_successful(user_api_client):
    user_id = random.randint(1000000, 9999999)
    user_data = {
        "id": user_id,
        "username": f"Test_Name_{user_id}",
        "firstName": f"Test_First_{user_id}",
        "lastName": f"Test_Second_{user_id}",
        "email": f"mail_{user_id}@test.com",
        "password": user_id,
        "phone": f"093{user_id}",
        "userStatus": 0
    }
    create_user_response = user_api_client.create_user(user_data)
    assert create_user_response.status_code == 200
    create_user_response_json = create_user_response.json()
    assert create_user_response_json["code"] == 200
    assert create_user_response_json["type"] == "unknown"

    delete_user_response = user_api_client.delete_user(user_data["username"])
    assert delete_user_response.status_code == 200


def test_get_user_is_successful(user_api_client, created_username):
    get_user_response = get_user_with_retries(user_api_client, created_username)
    assert get_user_response.status_code == 200
    response_json = get_user_response.json()
    assert response_json['username'] == created_username


@pytest.mark.xfail(reason="API Update (PUT) does not reflect changes, or takes too long to reflect.")
def test_update_existing_user_is_successful(user_api_client, created_username):
    get_user_response_before_update = get_user_with_retries(user_api_client, created_username)
    assert get_user_response_before_update.status_code == 200
    original_user_data = get_user_response_before_update.json()
    updated_user_data = {
        "id": original_user_data["id"],
        "username": created_username,
        "firstName": f"Updated_First_{original_user_data["id"]}",
        "lastName": f"Updated_Second_{original_user_data["id"]}",
        "email": f"Updated_mail_{original_user_data["id"]}@test.com",
        "password": original_user_data["id"],
        "phone": f"093{original_user_data["id"]}",
        "userStatus": 0
    }
    update_user_response = user_api_client.update_user_by_username(created_username, updated_user_data)
    assert update_user_response.status_code == 200

    get_user_response_after_update = get_user_with_retries(user_api_client, created_username)
    assert get_user_response_after_update.status_code == 200
    get_user_response_after_update_json = get_user_response_after_update.json()
    assert get_user_response_after_update_json["username"] == updated_user_data["username"]
    assert get_user_response_after_update_json["firstName"] == updated_user_data["firstName"]
    assert get_user_response_after_update_json["lastName"] == updated_user_data["lastName"]
    assert get_user_response_after_update_json["email"] == updated_user_data["email"]


@pytest.mark.xfail(reason="API returns 404 on DELETE for a recently created/retrieved user")
def test_delete_user_is_successful(user_api_client):
    user_id = random.randint(1000000, 9999999)
    user_data = {
        "id": user_id,
        "username": f"Test_Name_{user_id}",
        "firstName": f"Test_First_{user_id}",
        "lastName": f"Test_Second_{user_id}",
        "email": f"mail_{user_id}@test.com",
        "password": user_id,
        "phone": f"093{user_id}",
        "userStatus": 0
    }
    create_user_response = user_api_client.create_user(user_data)
    assert create_user_response.status_code == 200
    create_user_response_json = create_user_response.json()
    assert create_user_response_json["code"] == 200
    assert create_user_response_json["type"] == "unknown"
    get_before_delete_response = get_user_with_retries(user_api_client, user_data["username"])
    assert get_before_delete_response.status_code == 200

    delete_user_response = user_api_client.delete_user(user_data["username"])
    assert delete_user_response.status_code == 200

    get_after_delete_response = user_api_client.get_user_by_username(user_data["username"])
    assert get_after_delete_response.status_code == 404
