import uuid
from unittest.mock import patch

from sym.flow.cli.symflow import symflow as click_command


class TestDomains:
    @patch("sym.flow.cli.helpers.api.SymAPI.add_domain")
    def test_domains_add(self, _, click_setup):
        with click_setup() as runner:
            result = runner.invoke(
                click_command,
                ["domains", "add", "test.invalid"],
            )
            assert result.exit_code == 0
            assert result.output == "test.invalid successfully added as a domain.\n"

    @patch("sym.flow.cli.helpers.api.SymAPI.remove_domain")
    def test_domains_remove(self, _, click_setup):
        with click_setup() as runner:
            result = runner.invoke(
                click_command,
                ["domains", "remove", "test.invalid"],
            )
            assert result.exit_code == 0
            assert result.output == "test.invalid successfully removed as a domain.\n"

    def test_domains_list(self, click_setup):
        mock_org = {
            "id": str(uuid.uuid4()),
            "slug": "test",
            "domains": ["test.invalid", "blah.symops.com"],
        }
        with patch(
            "sym.flow.cli.helpers.api.SymAPI.get_current_organization",
            return_value=mock_org,
        ):
            with click_setup() as runner:
                result = runner.invoke(
                    click_command,
                    ["domains", "list"],
                )
                assert result.exit_code == 0
                assert "- test.invalid\n- blah.symops.com\n" in result.output
