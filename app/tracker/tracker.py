class PersonTracker:

    def __init__(self, detector):

        self.detector = detector

    def track(self, frame, confidence, person_class, tracker):

        results = self.detector.model.track(
            frame,
            persist=True,
            tracker=tracker,
            classes=[person_class],
            conf=confidence,
            verbose=False
        )

        return results