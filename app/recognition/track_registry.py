class TrackRegistry:

    def __init__(self, confirmation_required=3):

        self.registry = {}

        # Jumlah recognition konsisten yang diperlukan
        # sebelum identitas dikunci
        self.confirmation_required = confirmation_required

    # ======================================
    # CHECK
    # ======================================

    def has(self, track_id):

        return track_id in self.registry

    def is_locked(self, track_id):

        return (
            self.has(track_id)
            and self.registry[track_id]["locked"]
        )

    def is_recognized(self, track_id):

        return (
            self.has(track_id)
            and self.registry[track_id]["recognized"]
        )

    # ======================================
    # UPDATE RECOGNITION
    # ======================================

    def update(self, track_id, name, confidence):

        # ==================================
        # TRACK BARU
        # ==================================

        if not self.has(track_id):

            self.registry[track_id] = {
                "name": "Unknown",
                "confidence": 999,
                "recognized": False,
                "locked": False,

                "candidate_name": None,
                "candidate_count": 0
            }

        data = self.registry[track_id]

        # ==================================
        # SUDAH LOCKED
        # ==================================

        if data["locked"]:

            # Identitas yang sudah dikunci
            # tidak boleh diubah lagi
            return

        # ==================================
        # UNKNOWN
        # ==================================

        if name == "Unknown":

            # Jangan menghapus candidate
            # hanya karena satu frame gagal
            return

        # ==================================
        # CANDIDATE SAMA
        # ==================================

        if data["candidate_name"] == name:

            data["candidate_count"] += 1

        # ==================================
        # CANDIDATE BERUBAH
        # ==================================

        else:

            data["candidate_name"] = name
            data["candidate_count"] = 1

        # ==================================
        # CHECK CONFIRMATION
        # ==================================

        if data["candidate_count"] >= self.confirmation_required:

            data["name"] = name
            data["confidence"] = confidence
            data["recognized"] = True
            data["locked"] = True

            print(
                f"[LOCK] "
                f"Track {track_id} "
                f"-> {name}"
            )

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

    def get_candidate(self, track_id):

        if not self.has(track_id):
            return None

        return self.registry[track_id]["candidate_name"]

    def get_candidate_count(self, track_id):

        if not self.has(track_id):
            return 0

        return self.registry[track_id]["candidate_count"]

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

        print("=" * 60)
        print("Track Registry")
        print("=" * 60)

        for track_id, data in self.registry.items():

            print(
                f"Track {track_id} | "
                f"Name: {data['name']} | "
                f"Candidate: {data['candidate_name']} | "
                f"Count: {data['candidate_count']} | "
                f"Locked: {data['locked']} | "
                f"Distance: {data['confidence']:.3f}"
            )