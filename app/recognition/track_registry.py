from collections import deque


class TrackRegistry:
    
    def __init__(self, votes_required=3, history_size=6):

        self.registry = {}

        self.votes_required = votes_required
        self.history_size = history_size

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

        # disamakan dengan is_locked -- begitu locked, otomatis
        # dianggap "recognized" juga (sama seperti perilaku asli)
        return self.is_locked(track_id)

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
                "locked": False,

                "history": deque(maxlen=self.history_size),
            }

        data = self.registry[track_id]

        # ==================================
        # SUDAH LOCKED
        # ==================================

        if data["locked"]:

            # Identitas & status locked tidak boleh berubah lagi, tapi
            # kalau ada bacaan baru untuk nama yang SAMA dengan distance
            # (confidence) yang LEBIH BAIK (lebih kecil), boleh dipakai
            # supaya angka confidence yang tampil makin akurat.
            if (
                name == data["name"]
                and confidence < data["confidence"]
            ):
                data["confidence"] = confidence

            return

        # ==================================
        # UNKNOWN
        # ==================================

        if name == "Unknown":

            # Jangan dimasukkan ke history & jangan hapus history yang
            # sudah terkumpul -- 1 frame buram tidak membatalkan
            # progres voting sebelumnya.
            return

        # ==================================
        # CATAT KE HISTORY
        # ==================================

        data["history"].append((name, confidence))

        # ==================================
        # HITUNG VOTE
        # ==================================

        counts = {}

        for hist_name, _ in data["history"]:
            counts[hist_name] = counts.get(hist_name, 0) + 1

        top_name = max(counts, key=counts.get)
        top_count = counts[top_name]

        print(
            f"[VOTE] "
            f"Track {track_id} -> {name} "
            f"(top saat ini: {top_name} "
            f"{top_count}/{len(data['history'])})"
        )

        # ==================================
        # CHECK LOCK
        # ==================================

        if top_count >= self.votes_required:

            # Ambil confidence TERBAIK (distance terkecil) di antara
            # semua vote untuk nama pemenang ini
            best_confidence = min(
                c for n, c in data["history"] if n == top_name
            )

            data["name"] = top_name
            data["confidence"] = best_confidence
            data["locked"] = True

            print(
                f"[LOCK] "
                f"Track {track_id} -> {top_name} "
                f"(vote {top_count}/{len(data['history'])})"
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

        if not self.has(track_id) or not self.registry[track_id]["history"]:
            return None

        counts = {}

        for name, _ in self.registry[track_id]["history"]:
            counts[name] = counts.get(name, 0) + 1

        return max(counts, key=counts.get)

    def get_candidate_count(self, track_id):

        if not self.has(track_id) or not self.registry[track_id]["history"]:
            return 0

        counts = {}

        for name, _ in self.registry[track_id]["history"]:
            counts[name] = counts.get(name, 0) + 1

        return max(counts.values())

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
                f"Locked: {data['locked']} | "
                f"History: {list(data['history'])} | "
                f"Confidence: {data['confidence']:.3f}"
            )