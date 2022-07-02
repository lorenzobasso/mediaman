from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from pytest import fixture

from mediaman_api.main import app
from mediaman_api.routes.channel import yt_session, db_session
from mediaman_api.models import channel
from tests import data

channel_id = "UCtKUW8LJK2Ev8hUy9ZG_PPA"
endpoint = lambda id: f"/search-channel?id={id}"


@fixture
def yt():
    return MagicMock()


@fixture
def db():
    return MagicMock()


@fixture
def client(yt, db):
    def override_yt():
        yield yt

    def override_db():
        yield db

    _client = TestClient(app)
    app.dependency_overrides[yt_session] = override_yt
    app.dependency_overrides[db_session] = override_db

    yield _client

    app.dependency_overrides.clear()


@fixture(autouse=True)
def channel_info():
    with patch("mediaman_api.routes.channel.get_channel_info") as mock:
        mock.return_value = data.channel_info
        yield mock


@fixture(autouse=True)
def channel_patch():
    with patch("mediaman_api.routes.channel.channel.patch") as mock:
        mock.return_value = channel.parse(data.channel_info)
        yield mock


def test_endpoint_returns_successfully(client: TestClient):
    response = client.post(endpoint(channel_id))

    assert response.status_code == 200


def test_endpoint_returns_400_if_id_not_specified(client: TestClient):
    response = client.post(endpoint(""))

    assert response.status_code == 400
    assert response.json() == dict(detail="You need to specify a channel id")


def test_endpoint_returns_404_if_channel_not_found(client: TestClient, channel_info):
    channel_info.side_effect = KeyError
    response = client.post(endpoint(channel_id))

    assert response.status_code == 404
    assert response.json() == dict(detail=f"No channel with id={channel_id}")


def test_it_fetches_new_channel_info(client: TestClient, yt, channel_info):
    client.post(endpoint(channel_id))

    channel_info.assert_called_with(channel_id, yt)


def test_it_stores_the_new_data(client: TestClient, db, channel_patch):
    new_data = channel.parse(data.channel_info)
    client.post(endpoint(channel_id))

    channel_patch.assert_called_with(db, new_data)


def test_it_returns_the_new_data(client: TestClient):
    expected = channel.parse(data.channel_info).dict()
    response = client.post(endpoint(channel_id))

    assert response.json() == expected
