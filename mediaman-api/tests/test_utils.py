import json
from unittest.mock import mock_open, patch
from pytest import fixture

from mediaman_api.utils import load_json, dump_json

data = {
    "some": ["structured", "data", True],
    "to": "test",
    "the": 1,
    "loader": None,
}


@fixture(autouse=True)
def file_open():
    json_data = json.dumps(data)
    with patch("mediaman_api.utils.open", mock_open(read_data=json_data)) as mock:
        yield mock


class TestLoadJson:
    def test_it_opens_the_correct_file(self, file_open):
        load_json("some file")

        file_open.assert_called_with("some file")

    def test_it_returns_the_parsed_json_as_dict(self):
        assert load_json("some file") == data


class TestDumpJson:
    def test_it_opens_the_correct_file(self, file_open):
        dump_json(data, "some file")

        file_open.assert_called_with("some file", "w")

    def test_it_writes_the_correct_data_to_file(self, file_open):
        with patch("mediaman_api.utils.json") as mock:
            dump_json(data, "some file")

            mock.dump.assert_called_with(
                data,
                file_open().__enter__.return_value,
                indent=4,
                sort_keys=False,
            )

    def test_it_allows_indent_to_be_set(self, file_open):
        with patch("mediaman_api.utils.json") as mock:
            dump_json(data, "some file", indent=2)

            mock.dump.assert_called_with(
                data,
                file_open().__enter__.return_value,
                indent=2,
                sort_keys=False,
            )

    def test_it_allows_keys_to_be_sorted(self, file_open):
        with patch("mediaman_api.utils.json") as mock:
            dump_json(data, "some file", sort_keys=True)

            mock.dump.assert_called_with(
                data,
                file_open().__enter__.return_value,
                indent=4,
                sort_keys=True,
            )
