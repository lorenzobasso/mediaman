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
