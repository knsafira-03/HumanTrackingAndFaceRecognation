import time


class LineCounter:

    def __init__(self):

        # Garis pembatas
        self.line_p1 = (50, 240)
        self.line_p2 = (590, 240)

        # Toleransi jarak dari garis
        self.cross_threshold = 100

        # Cooldown antar event (detik)
        self.cooldown = 2

        # Menyimpan state tiap track
        self.tracker_state = {}

        self.in_count = 0
        self.out_count = 0

    def get_cross_product(self, P, Q, S):

        return (
            (S[0] - P[0]) * (Q[1] - P[1])
            -
            (S[1] - P[1]) * (Q[0] - P[0])
        )

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

    def update(self, track_id, current_side):

        # Tepat di atas garis
        if current_side == 0:
            return None

        current_time = time.time()

        # Track baru
        if track_id not in self.tracker_state:

            self.tracker_state[track_id] = {
                "side": current_side,
                "last_event_time": 0
            }

            return None

        previous_side = self.tracker_state[track_id]["side"]

        # Tidak berpindah sisi
        if previous_side == current_side:
            return None

        # Cooldown
        last_event_time = self.tracker_state[track_id]["last_event_time"]

        if current_time - last_event_time < self.cooldown:

            # tetap update side supaya sinkron
            self.tracker_state[track_id]["side"] = current_side

            return None

        event = None

        # Atas -> bawah
        if previous_side == 1 and current_side == -1:

            self.in_count += 1
            event = "MASUK"

            print(f"[EVENT] ID {track_id} -> MASUK")

        # Bawah -> atas
        elif previous_side == -1 and current_side == 1:

            self.out_count += 1
            event = "KELUAR"

            print(f"[EVENT] ID {track_id} -> KELUAR")

        # Update state
        self.tracker_state[track_id]["side"] = current_side
        self.tracker_state[track_id]["last_event_time"] = current_time

        return event