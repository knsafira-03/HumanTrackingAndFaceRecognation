class TrackRegistry:

    def __init__(self):

        self.registry = {}

    def has(self, track_id):

        return track_id in self.registry

    def add(self, track_id, name, confidence):

        self.registry[track_id] = {
            "name": name,
            "confidence": confidence
        }

    def get_name(self, track_id):

        if track_id in self.registry:
            return self.registry[track_id]["name"]

        return None

    def get_confidence(self, track_id):

        if track_id in self.registry:
            return self.registry[track_id]["confidence"]

        return None

    def remove(self, track_id):

        if track_id in self.registry:
            del self.registry[track_id]

    def show(self):

        print("=" * 40)
        print("Track Registry")
        print("=" * 40)

        for track_id, data in self.registry.items():

            print(
                f"{track_id} -> "
                f"{data['name']} "
                f"({data['confidence']:.3f})"
            )