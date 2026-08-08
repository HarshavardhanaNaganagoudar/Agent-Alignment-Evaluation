import json
from pathlib import Path

from models import BusinessState, Reply


class Memory:

    def __init__(self, path: str = "data/state.json"):
        self.path = Path(path)

        # Ensure directory exists
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def save(self, state: BusinessState):

        self.path.write_text(
            state.model_dump_json(indent=4)
        )

    def load(self) -> BusinessState:

        if not self.path.exists():
            return BusinessState()

        return BusinessState.model_validate_json(
            self.path.read_text()
        )


class ReplyLog:

    def __init__(self, path: str = "data/replies.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, reply: Reply):
        replies = self.load()
        replies.append(reply)

        self.path.write_text(
            json.dumps(
                [r.model_dump() for r in replies],
                indent=4,
            )
        )

    def load(self) -> list[Reply]:
        if not self.path.exists():
            return []

        raw = json.loads(self.path.read_text())
        return [Reply.model_validate(r) for r in raw]