import time


class TrackIdentityResolver:
   
    def __init__(
        self,
        is_locked_fn=None,
        max_distance=150,
        max_age=2.5,
        locked_max_distance=350,
        locked_max_age=8.0,
    ):

        # kalau tidak dikasih, anggap semua track "belum locked" --
        # otomatis pakai toleransi ketat untuk semuanya
        self.is_locked_fn = is_locked_fn or (lambda stable_id: False)

        self.max_distance = max_distance
        self.max_age = max_age

        self.locked_max_distance = locked_max_distance
        self.locked_max_age = locked_max_age

        self.active = {}  # stable_id -> {"pos": (x, y), "last_seen": t}
        self.lost = {}    # stable_id -> {"pos": (x, y), "lost_at": t, "locked": bool}

    def resolve(self, raw_track_id, position):

        now = time.time()

        # raw_track_id ini sudah dikenal sebagai stable_id yang aktif
        if raw_track_id in self.active:
            self.active[raw_track_id]["pos"] = position
            self.active[raw_track_id]["last_seen"] = now
            return raw_track_id

        # raw_track_id BARU -> cek apakah ada stable_id yang baru saja
        # hilang di posisi yang berdekatan (toleransi beda tergantung
        # apakah stable_id itu sudah locked atau belum)
        best_match = None
        best_dist = None

        for stable_id, info in self.lost.items():

            if info["locked"]:
                dist_limit = self.locked_max_distance
                age_limit = self.locked_max_age
            else:
                dist_limit = self.max_distance
                age_limit = self.max_age

            if now - info["lost_at"] > age_limit:
                continue

            dx = position[0] - info["pos"][0]
            dy = position[1] - info["pos"][1]
            dist = (dx ** 2 + dy ** 2) ** 0.5

            if dist > dist_limit:
                continue

            if best_dist is None or dist < best_dist:
                best_dist = dist
                best_match = stable_id

        if best_match is not None:

            was_locked = self.lost[best_match]["locked"]

            del self.lost[best_match]
            self.active[best_match] = {"pos": position, "last_seen": now}

            print(
                f"[REID] track_id baru {raw_track_id} "
                f"diadopsi jadi stable_id={best_match} "
                f"(jarak={best_dist:.0f}px, locked={was_locked})"
            )

            return best_match

        # tidak ada yang cocok -> memang track baru sungguhan
        self.active[raw_track_id] = {"pos": position, "last_seen": now}

        return raw_track_id

    def mark_missing(self, seen_stable_ids):
        """
        Panggil SEKALI tiap frame, dengan set/list semua stable_id
        (hasil resolve()) yang terlihat di frame ini. stable_id yang
        aktif tapi TIDAK ada di frame ini dipindah ke daftar "lost",
        siap diadopsi kalau track_id baru muncul dekat posisinya.
        Status "locked" dicek & disimpan SAAT INI JUGA (bukan nanti),
        karena begitu track hilang dari frame kita tidak akan tahu lagi
        apakah dia sempat locked atau tidak kalau tidak dicatat sekarang.
        """

        now = time.time()

        for stable_id in list(self.active.keys()):

            if stable_id not in seen_stable_ids:

                self.lost[stable_id] = {
                    "pos": self.active[stable_id]["pos"],
                    "lost_at": now,
                    "locked": self.is_locked_fn(stable_id),
                }

                del self.active[stable_id]

        # buang yang sudah kelamaan hilang -- kalau tidak, dict ini
        # bisa terus membesar selama program jalan
        for stable_id in list(self.lost.keys()):

            info = self.lost[stable_id]
            age_limit = self.locked_max_age if info["locked"] else self.max_age

            if now - info["lost_at"] > age_limit:
                del self.lost[stable_id]