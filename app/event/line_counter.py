import time


class LineCounter:

    def __init__(self):

        # ======================================
        # GARIS PEMBATAS
        # ======================================

        self.line_p1 = (327, 308)
        self.line_p2 = (467, 311)

        # ======================================
        # TOLERANSI GARIS
        # ======================================

        self.cross_threshold = 100

        # ======================================
        # COOLDOWN EVENT
        # ======================================

        self.cooldown = 2

        # ======================================
        # STATE TRACK
        # ======================================

        self.tracker_state = {}

        self.in_count = 0
        self.out_count = 0

    # ==========================================
    # CROSS PRODUCT
    # ==========================================

    def get_cross_product(self, P, Q, S):

        return (
            (S[0] - P[0]) * (Q[1] - P[1])
            -
            (S[1] - P[1]) * (Q[0] - P[0])
        )

    # ==========================================
    # GET SIDE
    # ==========================================

    def get_side(self, foot_point):

        cp = self.get_cross_product(
            self.line_p1,
            self.line_p2,
            foot_point
        )

        if cp > self.cross_threshold:
            return 1

        elif cp < -self.cross_threshold:
            return -1

        else:
            return 0

    # ==========================================
    # UPDATE
    # ==========================================

    def update(self, track_id, current_side):

        # --------------------------------------
        # Titik terlalu dekat dengan garis
        # --------------------------------------

        if current_side == 0:
            return None

        current_time = time.time()

        # ======================================
        # TRACK BARU
        # ======================================

        if track_id not in self.tracker_state:

            self.tracker_state[track_id] = {

                "side": current_side,

                "last_event_time": 0
            }

            print(
                f"[INIT] "
                f"ID {track_id} "
                f"side={current_side}"
            )

            return None

        # ======================================
        # AMBIL STATE SEBELUMNYA
        # ======================================

        previous_side = self.tracker_state[
            track_id
        ]["side"]

        last_event_time = self.tracker_state[
            track_id
        ]["last_event_time"]

        # ======================================
        # TIDAK BERPINDAH SISI
        # ======================================

        if previous_side == current_side:

            return None

        # ======================================
        # COOLDOWN
        # ======================================

        if (
            current_time - last_event_time
            < self.cooldown
        ):

            print(
                f"[COOLDOWN] "
                f"ID {track_id} "
                f"{previous_side} -> {current_side}"
            )

            # PENTING:
            # JANGAN update side di sini.
            #
            # Kalau event sedang cooldown,
            # kita mempertahankan side sebelumnya.
            #
            return None

        # ======================================
        # EVENT
        # ======================================

        event = None

        # ======================================
        # SIDE 1 -> SIDE -1
        # MASUK
        # ======================================

        if (
            previous_side == 1
            and current_side == -1
        ):

            self.in_count += 1

            event = "MASUK"

            print(
                f"[EVENT] "
                f"ID {track_id} "
                f"-> MASUK"
            )

        # ======================================
        # SIDE -1 -> SIDE 1
        # KELUAR
        # ======================================

        elif (
            previous_side == -1
            and current_side == 1
        ):

            self.out_count += 1

            event = "KELUAR"

            print(
                f"[EVENT] "
                f"ID {track_id} "
                f"-> KELUAR"
            )

        # ======================================
        # UPDATE STATE
        # ======================================

        if event is not None:

            self.tracker_state[
                track_id
            ]["side"] = current_side

            self.tracker_state[
                track_id
            ]["last_event_time"] = current_time

        return event