from app.recognition.track_registry import TrackRegistry

registry = TrackRegistry()

registry.add(25, "khalisa", 0.144)

registry.add(31, "aqil", 0.213)

registry.show()

print()

print(registry.get_name(25))

print(registry.get_name(31))