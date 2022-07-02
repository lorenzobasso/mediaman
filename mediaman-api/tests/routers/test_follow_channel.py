from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from pytest import fixture

from mediaman_api.main import app
from mediaman_api.routes.channel import yt_session, db_session
from mediaman_api.models import channel
from tests import data

channel_id = "UCtKUW8LJK2Ev8hUy9ZG_PPA"
endpoint = lambda id: f"/follow-channel?id={id}"


@fixture
def db():
    return MagicMock()


@fixture
def client(db):
    def override_db():
        yield db

    _client = TestClient(app)
    app.dependency_overrides[db_session] = override_db

    yield _client

    app.dependency_overrides.clear()


@fixture(autouse=True)
def get():
    with patch("mediaman_api.models.channel.get") as mock:
        yield mock


@fixture(autouse=True)
def put():
    with patch("mediaman_api.models.channel.put") as mock:
        yield mock


def test_it_returns_200(client: TestClient):
    response = client.patch(endpoint(channel_id))

    assert response.status_code == 200


def test_it_returns_400_if_id_not_given(client: TestClient):
    response = client.patch(endpoint(""))

    assert response.status_code == 400


def test_it_gets_the_right_channel_from_database(client: TestClient, db, get):
    client.patch(endpoint(channel_id))

    get.assert_called_with(db, channel_id)


def test_it_trims_whitespace_in_id(client: TestClient, db, get):
    client.patch(endpoint(f"\t  {channel_id}\n\r\t    "))

    get.assert_called_with(db, channel_id)


def test_it_returns_404_if_channel_not_found(client: TestClient, get):
    get.return_value = None

    response = client.patch(endpoint(channel_id))

    assert response.status_code == 404


def test_it_returns_true_if_not_following_before(client: TestClient, get):
    channel_data = channel.parse(data.channel_info)
    get.return_value = channel_data

    response = client.patch(endpoint(channel_id))

    assert response.json() == True


def test_it_returns_false_if_following_before(client: TestClient, get):
    channel_data = channel.parse(data.channel_info)
    channel_data.following = True
    get.return_value = channel_data

    response = client.patch(endpoint(channel_id))

    assert response.json() == False


def test_it_puts_the_right_data_in_the_db(client: TestClient, db, get, put):
    channel_data = channel.parse(data.channel_info)
    channel_data.following = True
    get.return_value = channel_data

    client.patch(endpoint(channel_id))

    put.assert_called_with(db, channel_data)
