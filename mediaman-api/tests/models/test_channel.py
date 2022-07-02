from unittest.mock import MagicMock, patch
from pytest import fixture
from sqlmodel import create_engine, Session, SQLModel

from tests import data
from mediaman_api.models import channel


class TestParseThumbnail:
    def test_it_parses_correctly(self):
        result = channel.parse_thumbnail("default", data.channel_thumbnail["default"])
        expected = channel.ChannelThumbnail(
            size="default",
            url=data.channel_thumbnail["default"]["url"],
            height=data.channel_thumbnail["default"]["height"],
            width=data.channel_thumbnail["default"]["width"],
        )

        assert result == expected


class TestParseThumbnails:
    def test_it_parses_correctly(self):
        result = channel.parse_thumbnails(data.channel_thumbnail)

        assert len(result) == 3
        assert result[0].size == "default"
        assert result[1].size == "medium"
        assert result[2].size == "high"


class TestParseChannel:
    def test_it_parses_correctly(self):
        result = channel.parse(data.channel_info)
        expected = channel.Channel(
            id="UCtKUW8LJK2Ev8hUy9ZG_PPA",
            title="Welker Farms",
            description="Farming is AWESOME!! Seriously...Farming is AMAZING! We make food for MILLIONS! How cool is that!! Come join us as we tell our STORY of FARMING in the 21st Century!\n\nWelker Farms is located in North Central Montana and has been in the family since the homestead of 1912. Third generation farmer, Bob Welker, along with his two sons, Nick and Scott, strive to carry on the family farm legacy. Welker Farms Inc has become a common name throughout the agriculture world by means of popular YouTube videos from our channel. \n\nUltimately we owe everything to our Lord and Savior Jesus Christ.\n\nCheck out our new welkerfarmsinc.com!",
            customUrl="welkerfarmsinc",
            published="2011-06-29T23:37:03Z",
            country="US",
            uploadPlaylist="UUtKUW8LJK2Ev8hUy9ZG_PPA",
            views=132193234,
            subscribers=537000,
            videos=553,
            banner="https://yt3.ggpht.com/6bdF_mPn-gRwTLsE4p1DqByFjZk1nn_PdWhVJt2H2bwkaI9VtQ6CLUmVGTq8t5m_cjupfNrPxg",
            thumbnails=channel.parse_thumbnails(data.channel_thumbnail),
        )

        assert result == expected


class TestGet:
    @fixture
    def db(self):
        yield MagicMock()

    def test_it_gets_the_correct_channel(self, db):
        id = "channel id"

        channel.get(db, id)

        db.get.assert_called_with(channel.Channel, id)


class TestPut:
    @fixture
    def db(self):
        yield MagicMock()

    @fixture
    def data(self):
        yield channel.parse(data.channel_info)

    def test_it_stored_data_to_db(self, db, data):
        channel.put(db, data)

        db.add.assert_called_with(data)

    def test_it_refreshes_the_instance(self, db, data):
        channel.put(db, data)

        db.refresh.assert_called_with(data)

    def test_it_commits_the_changes(self, db, data):
        channel.put(db, data)

        db.commit.assert_called()

    def test_it_returns_the_data(self, db, data):
        result = channel.put(db, data)

        assert result == data


class TestPatch:
    id = "channel id"
    data = {"title": "some new title", "description": "another description"}

    @fixture
    def new_data(self):
        base = channel.parse(data.channel_info)
        base.title = "some new title"
        base.description = "another description"

        yield base

    @fixture
    def db(self):
        yield MagicMock()

    @fixture
    def get(self):
        with patch("mediaman_api.models.channel.get") as mock:
            yield mock

    @fixture
    def put(self):
        with patch("mediaman_api.models.channel.put") as mock:
            yield mock

    def test_it_gets_existing_instances_of_the_data(self, db, get, new_data):
        channel.patch(db, new_data)

        get.assert_called_with(db, new_data.id)

    def test_it_puts_the_updated_values_(self, db, get, put, new_data):
        get.return_value = new_data

        channel.patch(db, new_data)

        put.assert_called_with(db, new_data)

    def test_it_does_not_override_previous_non_default_values(
        self, db, new_data, get, put
    ):
        base = channel.parse(data.channel_info)
        base.following = True
        get.return_value = base

        channel.patch(db, new_data)

        new_data.following = True
        put.assert_called_with(db, new_data)

    def xtest_it_returns_the_updated_value(self, db, get, new_data):
        get.return_value = new_data

        assert channel.patch(db, new_data) == new_data
