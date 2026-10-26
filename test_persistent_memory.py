
from core.persistent_memory import PersistentMemory

memory = PersistentMemory()

memory.remember("response_style", "concise")

print("Saved:", memory.recall("response_style"))
print("All memories:", memory.get_all())

memory.forget("response_style")
print("After deletion:", memory.recall("response_style"))
