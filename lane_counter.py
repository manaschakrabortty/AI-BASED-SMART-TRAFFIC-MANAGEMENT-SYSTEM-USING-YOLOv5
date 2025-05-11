
# LaneCounter handles vehicle counting per lane
class LaneCounter:
    def __init__(self, lane_id):
        self.lane_id = lane_id
        self.vehicle_count = 0

    def count_vehicles(self, boxes):
        # Only count vehicle types
        self.vehicle_count = len([box for box in boxes if box[-1] in ['car', 'bus', 'truck']])
        return self.vehicle_count
