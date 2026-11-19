"""Score who a credential belongs to, not how many tokens a call used.

Each adapter is a stand-in. `run` returns what the integration was able to
bind, revoke, and record for one delegated task. The scorecard only checks
those four properties.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Task:
    principal: str
    tool: str
    effect: str


@dataclass(frozen=True)
class Execution:
    """What the integration actually bound the effect to."""

    credential_subject: str | None
    tools_in_scope: frozenset[str]
    second_call_allowed_after_revoke: bool
    audit_subject: str | None


@dataclass(frozen=True)
class Scorecard:
    scoped_to_principal: bool
    scoped_to_tool: bool
    revoked_mid_task: bool
    audit_names_principal: bool


class Adapter:
    name: str

    def run(self, task: Task) -> Execution:
        raise NotImplementedError


class McpOauth(Adapter):
    """Token minted for one subject and one tool. Revocation stops the next call."""

    name = "mcp_oauth"

    def run(self, task: Task) -> Execution:
        return Execution(
            credential_subject=task.principal,
            tools_in_scope=frozenset({task.tool}),
            second_call_allowed_after_revoke=False,
            audit_subject=task.principal,
        )


class CliToken(Adapter):
    """A process-wide token. The effect is audited as the token owner, not the delegator."""

    name = "cli_token"

    def run(self, task: Task) -> Execution:
        return Execution(
            credential_subject=None,
            tools_in_scope=frozenset({task.tool, "admin"}),
            second_call_allowed_after_revoke=True,
            audit_subject="process-owner",
        )


class SkillCli(Adapter):
    """A skill that shells out to the CLI. It inherits the CLI credential."""

    name = "skill_cli"

    def run(self, task: Task) -> Execution:
        return CliToken().run(task)


ADAPTERS: dict[str, Adapter] = {
    "mcp_oauth": McpOauth(),
    "cli_token": CliToken(),
    "skill_cli": SkillCli(),
}


def score(adapter: Adapter, task: Task) -> Scorecard:
    result = adapter.run(task)
    return Scorecard(
        scoped_to_principal=result.credential_subject == task.principal,
        scoped_to_tool=result.tools_in_scope == frozenset({task.tool}),
        revoked_mid_task=not result.second_call_allowed_after_revoke,
        audit_names_principal=result.audit_subject == task.principal,
    )
