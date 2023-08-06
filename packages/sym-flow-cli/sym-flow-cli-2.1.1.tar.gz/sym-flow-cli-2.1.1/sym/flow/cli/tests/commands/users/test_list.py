from unittest.mock import patch

import pytest

from sym.flow.cli.commands.users.list import get_user_data
from sym.flow.cli.helpers.utils import human_friendly, utc_to_local
from sym.flow.cli.tests.factories.users import UserFactory


class TestUsersList:
    @pytest.fixture
    def users(self):
        yield [
            UserFactory.create(),
            UserFactory.create(is_admin=True),
            UserFactory.create(),
        ]

    @pytest.fixture(autouse=True)
    def patchypatch(self, users):
        with patch("sym.flow.cli.helpers.api.SymAPI.get_users", return_value=users):
            yield

    def test_get_user_data(self, users, global_options):
        table_data = get_user_data(global_options.sym_api)

        assert table_data.pop(0) == ["Email", "Role", "Created At"]
        for i, row in enumerate(table_data):
            assert row == [
                users[i].sym_identifier,
                "admin" if users[i].is_admin else "",
                human_friendly(utc_to_local(users[i].created_at)),
            ]
