class FaceMatcher:

    def match(self, person_box, face_box):

        px1, py1, px2, py2 = person_box
        fx1, fy1, fx2, fy2 = face_box

        # Titik tengah wajah
        cx = (fx1 + fx2) / 2
        cy = (fy1 + fy2) / 2

        return (
            px1 <= cx <= px2 and
            py1 <= cy <= py2
        )