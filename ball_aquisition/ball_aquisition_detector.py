# import sys
# sys.path.append('./')
# from utills.bbox_utils import messure_distance,get_center_of_bbox

# class BallAquisitionDetector:
#     def __init__(self):
#         self.position_threshuld=50
#         self.min_number_frames=11
#         self.contaiment_threshold=0.8
#     def get_key_basketball_player_asignment_point(self,player_bbox,ball_center):
#         ball_center_x=ball_center[0]
#         ball_center_y=ball_center[1]
#         x1,y1,x2,y2=player_bbox
#         width=x2-x1
#         height=y2-y1
#         output_points=[]
#         if ball_center_y>y1 and ball_center_y<y2:
#             output_points.append((x1,ball_center_y))
#             output_points.append((x2,ball_center_y))
#         if ball_center_x >x1 and ball_center_x<x2:
#             output_points.append((ball_center_x,y1))
#             output_points.append((ball_center_x,y2))
#         output_points+=[
#             (x1,y1), # top Left conrner
#             (x2,y1), # top right corner with Maximum X and minimum Y
#             (x1,y2), # botom left corner
#             (x2,y2), # botton rigt corner 
#             # TOP center
#             (x1+width//2,y1), # top center 
#             (x2,y1//2,y2), # bottom center 
#             (x1+y1+height//2), #Left center 
#             (x2+y2+height//2) # right center 
#             ]
#         return output_points
#     def find_minmum_distance_to_ball(self,ball_center,player_bbox):
#         key_points=self.get_key_basketball_player_asignment_point(player_bbox,ball_center)
#         # return min(messure_distance(ball_center,key_point) for key_point in key_points) # this the bellow code completely 
#         min=9999
#         for key_point in key_points:
#             distance=messure_distance(ball_center,key_point)
#             if min>distance:
#                 min=distance
#         return min
#     def calculate_ball_containment_ratio(self,playerbbox,ball_box):
#         px1,py1,px2,py2 = playerbbox
#         bx1,by1,bx2,by2= ball_box
#         player_area=(px2-px1) * (py2-py1)

#         ball_area=(bx2-bx1) * (by2-by1) 
#         intersection_x1=max(px1,bx1)
#         intersection_y1=max(py1,by1)
#         intersection_x2=min(px2,bx2)
#         intersection_y2=min(py2,by2)

#         # intersection_area={intersection_x2-intersection_x1} * {intersection_y2 - intersection_y1}
#         intersection_width = max(0, intersection_x2 - intersection_x1)
#         intersection_height = max(0, intersection_y2 - intersection_y1)
#         intersection_area = intersection_width * intersection_height
#         containment_ratio= intersection_area/ball_area

#         return containment_ratio
#     def find_best_condidate_for_position(self,ball_center,player_tracks_frame,ball_bbox):
#         high_containment_player= []
#         regular_distance_player=[]
#         for player_id, player_info in player_tracks_frame.items():
#             player_bbox= player_info.get('box',[])
#             if not player_bbox:
#                 continue
#             containment= self.calculate_ball_containment_ratio(player_bbox,ball_bbox)
#             min_distance=self.find_minmum_distance_to_ball(ball_center,player_bbox)
#             if containment > self.contaiment_threshold:
#                 high_containment_player.append((player_id,containment,containment))
#             else:
#                 regular_distance_player.append((player_id,min_distance))
#             # First Priority high contaiments players
#             if high_containment_player:
#                 best_candidate= max(high_containment_player,key=lambda x:x[1])

#                 return best_candidate[0]
#             # if second priroty
#             if regular_distance_player:
#                 best_candidate=min(regular_distance_player,key=lambda x:x[1])
#                 if best_candidate[1]<self.position_threshuld:
#                     return best_candidate[0]
#             return -1
#     def detect_ball_position(self,player_tracks,ball_tracks):
#         number_frames=len(ball_tracks)
#         posotion_list=[-1] * number_frames
#         consecutive_postion_count={}
#         for frame_number in range(number_frames):
#             ball_info= ball_tracks[frame_number].get(1,{})
#             if not ball_info:
#                 continue
#             ball_bbox=ball_info.get('box',[])
#             if not ball_bbox:
#                 continue
#             ball_center=get_center_of_bbox(ball_bbox)
#             best_player_id= self.find_best_condidate_for_position(ball_center,player_tracks[frame_number],ball_bbox)
            
#             if best_player_id != -1:
#                 number_o_conscutive_frame = consecutive_postion_count.get(best_player_id,0)+1
#                 consecutive_postion_count = {best_player_id: number_o_conscutive_frame}
#                 if consecutive_postion_count[best_player_id]>=self.min_number_frames:
#                     posotion_list[frame_number] =best_player_id
#             else:
#                 consecutive_postion_count={}
#         return posotion_list



# import sys
# sys.path.append('./')
# from utills.bbox_utils import messure_distance,get_center_of_bbox
# class BallAcquisitionDetector:
#     def __init__(self):
#         # Maximum allowed distance between player and ball
#         self.position_threshold = 50

#         # Number of consecutive frames required
#         self.min_number_frames = 11

#         # Required containment ratio
#         self.containment_threshold = 0.8

#     def get_key_basketball_player_assignment_points(
#         self,
#         player_bbox,
#         ball_center
#     ):
#         """
#         Create important points around the player box
#         to measure distance from the ball.
#         """
#         ball_center_x, ball_center_y = ball_center
#         x1, y1, x2, y2 = player_bbox
#         width = x2 - x1
#         height = y2 - y1
#         output_points = []
#         # ---------------------------------------------------
#         # Points aligned horizontally with the ball
#         # ---------------------------------------------------

#         if y1 < ball_center_y < y2:
#             output_points.append((x1, ball_center_y))
#             output_points.append((x2, ball_center_y))

#         # ---------------------------------------------------
#         # Points aligned vertically with the ball
#         # ---------------------------------------------------

#         if x1 < ball_center_x < x2:
#             output_points.append((ball_center_x, y1))
#             output_points.append((ball_center_x, y2))

#         # ---------------------------------------------------
#         # Corners + center points
#         # ---------------------------------------------------

#         output_points += [

#             # Top left
#             (x1, y1),

#             # Top right
#             (x2, y1),

#             # Bottom left
#             (x1, y2),

#             # Bottom right
#             (x2, y2),

#             # Top center
#             (x1 + width // 2, y1),

#             # Bottom center
#             (x1 + width // 2, y2),

#             # Left center
#             (x1, y1 + height // 2),

#             # Right center
#             (x2, y1 + height // 2),
#         ]

#         return output_points

#     def find_minimum_distance_to_ball(
#         self,
#         ball_center,
#         player_bbox
#     ):
#         """
#         Find minimum distance between the ball center
#         and important player points.
#         """
#         key_points = self.get_key_basketball_player_assignment_points(
#             player_bbox,
#             ball_center
#         )
#         min_distance = float('inf')
#         for key_point in key_points:
#             distance = messure_distance(
#                 ball_center,
#                 key_point
#             )
#             if distance < min_distance:
#                 min_distance = distance
#         return min_distance

#     def calculate_ball_containment_ratio(
#         self,
#         player_bbox,
#         ball_bbox
#     ):
#         """
#         Calculate how much of the ball is inside the player box.
#         """
#         px1, py1, px2, py2 = player_bbox
#         bx1, by1, bx2, by2 = ball_bbox

#         # Ball area
#         ball_area = (bx2 - bx1) * (by2 - by1)
#         if ball_area <= 0:
#             return 0
#         # Intersection coordinates
#         intersection_x1 = max(px1, bx1)
#         intersection_y1 = max(py1, by1)

#         intersection_x2 = min(px2, bx2)
#         intersection_y2 = min(py2, by2)
#         # Intersection width & height
#         intersection_width = max(
#             0,
#             intersection_x2 - intersection_x1
#         )

#         intersection_height = max(
#             0,
#             intersection_y2 - intersection_y1
#         )

#         # Intersection area
#         intersection_area = (
#             intersection_width *
#             intersection_height
#         )

#         # Containment ratio
#         containment_ratio = (
#             intersection_area / ball_area
#         )

#         return containment_ratio

#     def find_best_candidate_for_position(
#         self,
#         ball_center,
#         player_tracks_frame,
#         ball_bbox
#     ):
#         """
#         Find the best player candidate for ball possession.
#         """

#         high_containment_players = []

#         regular_distance_players = []
#         for player_id, player_info in player_tracks_frame.items():
#             player_bbox = player_info.get('box', [])
#             if not player_bbox:
#                 continue

#             # Containment ratio
#             containment = self.calculate_ball_containment_ratio(
#                 player_bbox,
#                 ball_bbox
#             )

#             # Distance to player
#             min_distance = self.find_minimum_distance_to_ball(
#                 ball_center,
#                 player_bbox
#             )

#             # High containment players
#             if containment > self.containment_threshold:

#                 high_containment_players.append(
#                     (
#                         player_id,
#                         containment
#                     )
#                 )

#             else:

#                 regular_distance_players.append(
#                     (
#                         player_id,
#                         min_distance
#                     )
#                 )

#         # ---------------------------------------------------
#         # First priority:
#         # High containment players
#         # ---------------------------------------------------

#         if high_containment_players:

#             best_candidate = max(
#                 high_containment_players,
#                 key=lambda x: x[1]
#             )

#             return best_candidate[0]

#         # ---------------------------------------------------
#         # Second priority:
#         # Nearest player
#         # ---------------------------------------------------

#         if regular_distance_players:

#             best_candidate = min(
#                 regular_distance_players,
#                 key=lambda x: x[1]
#             )

#             if best_candidate[1] < self.position_threshold:
#                 return best_candidate[0]

#         return -1

#     def detect_ball_position(
#         self,
#         player_tracks,
#         ball_tracks
#     ):
#         """
#         Detect which player possesses the ball
#         in each frame.
#         """

#         number_frames = len(ball_tracks)

#         position_list = [-1] * number_frames

#         consecutive_position_count = {}

#         for frame_number in range(number_frames):

#             ball_info = ball_tracks[frame_number].get(1, {})

#             if not ball_info:
#                 continue

#             ball_bbox = ball_info.get('box', [])

#             if not ball_bbox:
#                 continue

#             # Ball center
#             ball_center = get_center_of_bbox(ball_bbox)

#             # Find best player
#             best_player_id = self.find_best_candidate_for_position(
#                 ball_center,
#                 player_tracks[frame_number],
#                 ball_bbox
#             )

#             # ---------------------------------------------------
#             # Update consecutive frame count
#             # ---------------------------------------------------

#             if best_player_id != -1:

#                 number_of_consecutive_frames = (
#                     consecutive_position_count.get(
#                         best_player_id,
#                         0
#                     ) + 1
#                 )

#                 consecutive_position_count = {
#                     best_player_id:
#                     number_of_consecutive_frames
#                 }

#                 # Assign only if stable enough
#                 if (
#                     consecutive_position_count[best_player_id]
#                     >= self.min_number_frames
#                 ):

#                     position_list[frame_number] = (
#                         best_player_id
#                     )

#             else:

#                 consecutive_position_count = {}

#         return position_list



import sys
sys.path.append('./')

from utills.bbox_utils import messure_distance, get_center_of_bbox


class BallAquisitionDetector:
    def __init__(self):
        self.position_threshuld = 50
        self.min_number_frames = 11
        self.contaiment_threshold = 0.8

    # -------------------------------
    # Key assignment points for player
    # -------------------------------
    def get_key_basketball_player_asignment_point(self, player_bbox, ball_center):
        ball_center_x, ball_center_y = ball_center
        x1, y1, x2, y2 = player_bbox

        width = x2 - x1
        height = y2 - y1

        output_points = []

        # Ball aligned horizontally
        if y1 < ball_center_y < y2:
            output_points.append((x1, ball_center_y))
            output_points.append((x2, ball_center_y))

        # Ball aligned vertically
        if x1 < ball_center_x < x2:
            output_points.append((ball_center_x, y1))
            output_points.append((ball_center_x, y2))

        # Corners
        output_points += [
            (x1, y1),  # top-left
            (x2, y1),  # top-right
            (x1, y2),  # bottom-left
            (x2, y2),  # bottom-right

            # Centers
            (x1 + width // 2, y1),  # top center
            (x1 + width // 2, y2),  # bottom center
            (x1, y1 + height // 2),  # left center
            (x2, y1 + height // 2),  # right center
        ]

        return output_points

    # -------------------------------
    # Minimum distance to ball
    # -------------------------------
    def find_minmum_distance_to_ball(self, ball_center, player_bbox):
        key_points = self.get_key_basketball_player_asignment_point(
            player_bbox, ball_center
        )

        min_distance = float("inf")

        for key_point in key_points:
            distance = messure_distance(ball_center, key_point)
            if distance < min_distance:
                min_distance = distance

        return min_distance

    # -------------------------------
    # Ball containment ratio
    # -------------------------------
    def calculate_ball_containment_ratio(self, player_bbox, ball_bbox):
        px1, py1, px2, py2 = player_bbox
        bx1, by1, bx2, by2 = ball_bbox

        player_area = (px2 - px1) * (py2 - py1)
        ball_area = (bx2 - bx1) * (by2 - by1)

        intersection_x1 = max(px1, bx1)
        intersection_y1 = max(py1, by1)
        intersection_x2 = min(px2, bx2)
        intersection_y2 = min(py2, by2)

        intersection_width = max(0, intersection_x2 - intersection_x1)
        intersection_height = max(0, intersection_y2 - intersection_y1)

        intersection_area = intersection_width * intersection_height

        if ball_area == 0:
            return 0

        containment_ratio = intersection_area / ball_area
        return containment_ratio

    # -------------------------------
    # Find best candidate player
    # -------------------------------
    def find_best_condidate_for_position(self, ball_center, player_tracks_frame, ball_bbox):

        high_containment_player = []
        regular_distance_player = []

        for player_id, player_info in player_tracks_frame.items():

            player_bbox = player_info.get('box', [])
            if not player_bbox:
                continue

            containment = self.calculate_ball_containment_ratio(
                player_bbox, ball_bbox
            )

            min_distance = self.find_minmum_distance_to_ball(
                ball_center, player_bbox
            )

            # Priority 1: strong containment
            if containment > self.contaiment_threshold:
                high_containment_player.append((player_id, containment))

            # Priority 2: distance
            else:
                regular_distance_player.append((player_id, min_distance))

        # Choose best containment player first
        if high_containment_player:
            best_candidate = max(high_containment_player, key=lambda x: x[1])
            return best_candidate[0]

        # Otherwise choose closest player
        if regular_distance_player:
            best_candidate = min(regular_distance_player, key=lambda x: x[1])

            if best_candidate[1] < self.position_threshuld:
                return best_candidate[0]

        return -1

    # -------------------------------
    # Main tracking function
    # -------------------------------
    def detect_ball_position(self, player_tracks, ball_tracks):

        number_frames = len(ball_tracks)

        position_list = [-1] * number_frames
        consecutive_position_count = {}

        for frame_number in range(number_frames):

            ball_info = ball_tracks[frame_number].get(1, {})
            if not ball_info:
                continue

            ball_bbox = ball_info.get('box', [])
            if not ball_bbox:
                continue

            ball_center = get_center_of_bbox(ball_bbox)

            best_player_id = self.find_best_condidate_for_position(
                ball_center,
                player_tracks[frame_number],
                ball_bbox
            )

            if best_player_id != -1:

                count = consecutive_position_count.get(best_player_id, 0) + 1
                consecutive_position_count[best_player_id] = count

                # reset others (important for switching players)
                for pid in list(consecutive_position_count.keys()):
                    if pid != best_player_id:
                        consecutive_position_count[pid] = 0

                if count >= self.min_number_frames:
                    position_list[frame_number] = best_player_id

            else:
                consecutive_position_count = {}

        return position_list