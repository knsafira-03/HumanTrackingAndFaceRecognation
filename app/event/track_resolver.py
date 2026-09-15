import time


class TrackIdentityResolver:
    """
    ByteTrack kadang memberi track_id BARU ke orang yang SAMA saat terjadi
    oklusi (occlusion), ganti pose, atau 2 orang berpapasan. Kalau ID
    berubah, line_counter.py dan recognition_service.py menganggapnya
    "orang baru" -- garis IN/OUT dihitung ulang dari nol dan identitas
    wajah yang sudah locked hilang.

    Class ini menjembatani itu: kalau track_id baru muncul di posisi yang
    (cukup) berdekatan dengan track_id lama yang baru saja hilang,
    track_id baru itu "diadopsi" jadi ID lama yang sama.

    PENTING -- dipakai per FRAME, bukan per deteksi satu-satu:
    Panggil resolve_frame() SEKALI tiap frame dengan daftar SEMUA orang
    yang terdeteksi di frame itu. Ini supaya "tandai ID lama hilang" dan
    "coba sambungkan ID baru" terjadi dalam satu langkah yang sama --
    kalau dipisah jadi resolve() dipanggil per orang lalu mark_missing()
    di akhir frame (versi sebelumnya), ada jeda 1 frame yang bikin ID
    yang berubah PERSIS di frame yang sama gagal tersambung (karena ID
    lama belum sempat ditandai "hilang" saat ID baru sedang dicari
    pasangannya) -- ini yang menyebabkan IN/OUT kehitung dobel kemarin.

    DUA TINGKAT TOLERANSI (sama seperti sebelumnya):
    - Identitas yang SUDAH TERKUNCI (locked): toleransi LONGGAR.
    - Identitas yang BELUM terkunci: toleransi KETAT.
    """

    def __init__(
        self,
        is_locked_fn=None,
        max_distance=150,
        max_age=2.5,
        locked_max_distance=350,
        locked_max_age=8.0,
    ):

        self.is_locked_fn = is_locked_fn or (lambda stable_id: False)

        self.max_distance = max_distance
        self.max_age = max_age

        self.locked_max_distance = locked_max_distance
        self.locked_max_age = locked_max_age

        self.active = {}  # stable_id -> {"pos": (x, y), "last_seen": t}
        self.lost = {}    # stable_id -> {"pos": (x, y), "lost_at": t, "locked": bool}

    def resolve_frame(self, detections):
        """
        detections: list berisi (raw_track_id, position) untuk SEMUA
        orang yang terdeteksi di frame ini.

        Return: dict {raw_track_id: stable_id} untuk frame ini.
        """

        now = time.time()

        raw_ids_this_frame = {raw_id for raw_id, _ in detections}

        # ==================================
        # LANGKAH 1: tandai active yang TIDAK muncul di frame ini
        # sebagai "baru saja hilang" -- SEBELUM mencoba menyambungkan
        # id baru manapun, supaya id yang hilang & id baru yang
        # menggantikannya di frame YANG SAMA tetap bisa ketemu.
        # ==================================

        for stable_id in list(self.active.keys()):

            if stable_id not in raw_ids_this_frame:

                self.lost[stable_id] = {
                    "pos": self.active[stable_id]["pos"],
                    "lost_at": now,
                    "locked": self.is_locked_fn(stable_id),
                }

                del self.active[stable_id]

        # ==================================
        # LANGKAH 2: proses tiap deteksi di frame ini
        # ==================================

        result = {}

        for raw_track_id, position in detections:

            # raw_track_id ini sudah dikenal sebagai stable_id aktif
            if raw_track_id in self.active:

                self.active[raw_track_id]["pos"] = position
                self.active[raw_track_id]["last_seen"] = now

                result[raw_track_id] = raw_track_id
                continue

            # cari kandidat di daftar "lost" (termasuk yang baru saja
            # ditandai hilang di Langkah 1 di atas, frame yang sama)
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

                result[raw_track_id] = best_match

            else:

                # memang track baru sungguhan
                self.active[raw_track_id] = {"pos": position, "last_seen": now}
                result[raw_track_id] = raw_track_id

        # ==================================
        # LANGKAH 3: buang entri "lost" yang sudah kelamaan
        # ==================================

        for stable_id in list(self.lost.keys()):

            info = self.lost[stable_id]
            age_limit = self.locked_max_age if info["locked"] else self.max_age

            if now - info["lost_at"] > age_limit:
                del self.lost[stable_id]

        return result