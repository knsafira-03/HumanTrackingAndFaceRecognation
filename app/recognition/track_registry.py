class TrackRegistry:

    def __init__(self):

        self.registry = {}

    # ======================================
    # CHECK
    # ======================================

    def has(self, track_id):

        return track_id in self.registry

    # ======================================
    # ADD / UPDATE
    # ======================================

    def update(self, track_id, name, confidence):

        self.registry[track_id] = {
            "name": name,
            "confidence": confidence,
            "recognized": name != "Unknown"
        }

    # ======================================
    # GET
    # ======================================

    def get_name(self, track_id):

        if not self.has(track_id):
            return None

        return self.registry[track_id]["name"]

    def get_confidence(self, track_id):

        if not self.has(track_id):
            return None

        return self.registry[track_id]["confidence"]

    def is_recognized(self, track_id):

        if not self.has(track_id):
            return False

        return self.registry[track_id]["recognized"]

    # ======================================
    # REMOVE
    # ======================================

    def remove(self, track_id):

        if self.has(track_id):
            del self.registry[track_id]

    # ======================================
    # DEBUG
    # ======================================

    def show(self):

        print("=" * 50)
        print("Track Registry")
        print("=" * 50)

        for track_id, data in self.registry.items():

            print(
                f"{track_id} -> "
                f"{data['name']} | "
                f"{data['confidence']:.3f} | "
                f"{data['recognized']}"
            )