import json

from .harness import ADAPTERS, Task, score


def main() -> None:
    task = Task(principal="ada", tool="create_ticket", effect="ticket-42")
    rows = []
    for name, adapter in ADAPTERS.items():
        card = score(adapter, task)
        rows.append({"adapter": name, "kind": "stand-in", **card.__dict__})
    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()
