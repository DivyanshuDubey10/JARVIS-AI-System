
import json
from pathlib import Path


class PersistentMemory:
    def __init__(self, file_path=None):
        if file_path is None:
            project_root = Path(__file__).resolve().parent.parent
            file_path = project_root / "memory.json"

        self.file_path = Path(file_path)
        self.memories = {}
        self._load()

    def _load(self):
        if not self.file_path.exists():
            self._save()
            return

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                self.memories = json.load(file)

            if not isinstance(self.memories, dict):
                raise ValueError("Memory file must contain a JSON object.")

        except (json.JSONDecodeError, ValueError) as error:
            raise ValueError(
                f"Could not load memory file: {self.file_path}"
            ) from error

    def _save(self):
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(
                self.memories,
                file,
                indent=4,
                ensure_ascii=False,
            )

    def remember(self, key, value):
        self.memories[key] = value
        self._save()

    def recall(self, key):
        return self.memories.get(key)

    def get_all(self):
        return self.memories.copy()

    def forget(self, key):
        if key in self.memories:
            del self.memories[key]
            self._save()
            return True

        return False

    def clear(self):
        self.memories.clear()
        self._save()
