class PersonTracker:

    def __init__(self):

        self.tracker_name = "bytetrack.yaml"

    def track(self,
              detector,
              frame):

        return detector.model.track(
            frame,
            persist=True,
            tracker=self.tracker_name,
            classes=[0],
            conf=0.35,
            verbose=False
        )