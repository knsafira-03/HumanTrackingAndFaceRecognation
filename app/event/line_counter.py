class LineCounter:

    def __init__(self):

        self.line_p1 = (50, 240)
        self.line_p2 = (590, 240)

        self.cross_threshold = 100

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

        # Abaikan jika tepat di garis
        if current_side == 0:
            return

        # ID baru
        if track_id not in self.tracker_state:

            self.tracker_state[track_id] = {
                "side": current_side,
                "counted": False
            }

            return

        previous_side = self.tracker_state[track_id]["side"]

        # Tidak ada perubahan sisi
        if previous_side == current_side:
            return

        if previous_side == 1 and current_side == -1:

            self.in_count += 1

            print(f"[EVENT] ID {track_id} -> MASUK")

        elif previous_side == -1 and current_side == 1:

            self.out_count += 1

            print(f"[EVENT] ID {track_id} -> KELUAR")

        # Update sisi terakhir
        self.tracker_state[track_id]["side"] = current_side