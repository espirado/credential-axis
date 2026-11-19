import unittest

from credential_axis.harness import ADAPTERS, Task, score


class HarnessTest(unittest.TestCase):
    def test_stand_ins_separate_delegation_from_the_interface_name(self) -> None:
        task = Task(principal="ada", tool="create_ticket", effect="ticket-42")
        cards = {name: score(adapter, task) for name, adapter in ADAPTERS.items()}

        self.assertTrue(cards["mcp_oauth"].scoped_to_principal)
        self.assertTrue(cards["mcp_oauth"].scoped_to_tool)
        self.assertTrue(cards["mcp_oauth"].revoked_mid_task)
        self.assertTrue(cards["mcp_oauth"].audit_names_principal)

        for name in ("cli_token", "skill_cli"):
            self.assertFalse(cards[name].scoped_to_principal)
            self.assertFalse(cards[name].scoped_to_tool)
            self.assertFalse(cards[name].revoked_mid_task)
            self.assertFalse(cards[name].audit_names_principal)

        self.assertEqual(cards["cli_token"], cards["skill_cli"])


if __name__ == "__main__":
    unittest.main()
