import math

from enum import Enum, unique

@unique
class TrackerStatus(Enum):
    NEW = 1 # Belum memenuhi minum frame
    TRACKED = 2 # Utama
    LOST = 3 # Sedang hilang dari frame, tapi masih di track

class EuclideanDistTracker:
    tracked_ever_counter = 0
    
    def __init__(self, tolerance_lost_frame = 25, tolerance_px=50, min_frame_detected=30):
        # Store the center positions of the objects
        self.center_points = {}
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.id_count = 0

        # Mininum frame dia tertrack, hingga akhirnya dia dianggap ada
        self.min_frame_detected = min_frame_detected
        self.frame_detected_counts = {}
        # self.lastObjectCoor = {}

        # Toleransi perubahan jarak px di frame
        self.tolerance_px = tolerance_px

        # Toleransi hilang dari frame sebanyak x frame (Misal bola lewat dari tiang)
        self.lost_frame_counts = {}

        # Seberapa frame suatu objek boleh hilang dan masih ditoleransi
        self.tolerance_lost_frame = tolerance_lost_frame


    def update(self, objects_rect):
        # Objects boxes and ids
        objects_bbs_ids = []

        # Get center point of new object
        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # Find out if that object was detected already
            same_object_detected = False
            dist_mapper = []
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])

                # TODO: Cari delta terdekat
                if dist < self.tolerance_px:
                    dist_mapper.append([id, dist])
                    # self.center_points[id] = (cx, cy)
                    # objects_bbs_ids.append([x, y, w, h, id])
                    # same_object_detected = True
                    # self.frame_detected_counts[id] += 1
                    # break
            dist_mapper.sort(key=lambda it:it[1],reverse=False)
            if len(dist_mapper) >= 1:
                id, _ = dist_mapper[0]
                self.center_points[id] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, id])
                same_object_detected = True
                self.frame_detected_counts[id] += 1
                # self.frame_detected_counts[id] = [x, y]


            # New object is detected we assign the ID to that object
            if same_object_detected is False:
                self.frame_detected_counts[self.id_count] = 1
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1

        # Clean the dictionary by center points to remove IDS not used anymore
        new_center_points = {}

        id_still_tracked = []
        id_lost_still_tolerated = []

        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center
            id_still_tracked.append(object_id)

        for key, val in self.center_points.items():
            if key in id_still_tracked:
                self.lost_frame_counts[key] = 0
            else:
                self.lost_frame_counts[key] += 1

            if self.lost_frame_counts[key] <= self.tolerance_lost_frame:
                id_lost_still_tolerated.append(key)
                new_center_points[key] = self.center_points[key] # Gunakan last known position untuk objek yang hilang
            else:
                # self.lost_frame_counts.pop(key) # Hapus jika sudah lebih dari toleransi
                pass
        
        # Update dictionary with IDs not used removed

        # 
        to_return = []
        for it in objects_bbs_ids:
            _, _, _, _, object_id = it
            if self.frame_detected_counts[object_id] >= self.min_frame_detected:
                it.append(TrackerStatus.TRACKED)
                if object_id in id_lost_still_tolerated:
                    id_lost_still_tolerated.remove(object_id)
                to_return.append(it)
            elif self.frame_detected_counts[object_id] < self.min_frame_detected:
                it.append(TrackerStatus.NEW)
                if object_id in id_lost_still_tolerated:
                    id_lost_still_tolerated.remove(object_id)
                to_return.append(it)

        for id in id_lost_still_tolerated:
            last_known_center = self.center_points[id]
            it = [last_known_center[0], last_known_center[1], 10, 10, id]
            it.append(TrackerStatus.LOST)
            to_return.append(it)

            
        
        self.center_points = new_center_points.copy()
        return to_return