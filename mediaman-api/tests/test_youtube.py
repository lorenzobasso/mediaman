from unittest.mock import MagicMock, patch
from pytest import fixture

from mediaman_api.youtube import (
    create_yt_session,
    get_api_key,
    get_channel_info,
    secrets_file,
    channel_parts,
)
from tests import data


class TestGetApiKey:
    @fixture
    def open(self):
        with patch("mediaman_api.youtube.load_json") as mock:
            yield mock

    def test_get_api_key_opens_the_correct_file(self, open):
        get_api_key()

        open.assert_called_with(secrets_file)

    def test_get_api_key_returns_the_correct_data(self, open):
        open.return_value = {"ytApiKey": "the api key"}

        assert get_api_key() == "the api key"


class TestCreateYtSession:
    @fixture
    def key(self):
        with patch("mediaman_api.youtube.get_api_key") as mock:
            mock.return_value = "api key"
            yield mock

    def test_it_creates_the_correct_session(self, key):
        with patch("mediaman_api.youtube.googleapiclient") as api:
            create_yt_session()

            api.discovery.build.assert_called_with(
                "youtube", "v3", developerKey="api key"
            )


class TestGetChannelInfo:
    id = "channel id"

    @fixture
    def yt(self):
        mock = MagicMock()
        mock.channels().list().execute.return_value = data.raw_channel_info

        yield mock

    def test_it_creates_the_correct_request(self, yt):
        get_channel_info(self.id, yt)

        yt.channels().list.assert_called_with(
            part=",".join(channel_parts),
            id=self.id,
            maxResults=50,
        )

    def test_it_executes_the_request(self, yt):
        get_channel_info(self.id, yt)

        yt.channels().list().execute.assert_called

    def test_it_only_returns_the_channel_data(self, yt):
        assert get_channel_info(self.id, yt) == data.channel_info
