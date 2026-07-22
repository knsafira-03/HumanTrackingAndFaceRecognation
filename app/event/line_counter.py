class LineCounter:

    def __init__(self,
                 line_p1,
                 line_p2,
                 threshold):

        self.line_p1 = line_p1
        self.line_p2 = line_p2

        self.threshold = threshold

        self.tracker_state = {}

        self.in_count = 0

        self.out_count = 0

    def get_cross_product(self,
                          point):

        return (
            (point[0] - self.line_p1[0]) *
            (self.line_p2[1] - self.line_p1[1])
            -
            (point[1] - self.line_p1[1]) *
            (self.line_p2[0] - self.line_p1[0])
        )

    # count_in()
    # count_out()