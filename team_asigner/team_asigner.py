# from PIL import Image
# from transformers import CLIPProcessor,CLIPModel
# import cv2
# import sys
# sys.path.append('./')
# from utills.stubs_utils import ReadSub,Write_sub
# class teamAssiner:
#     def __init__(self,team_1_className='white shirt',team_2_classname='blue shirt'):
#         self.team_1_className=team_1_className
#         self.team_2_classname=team_2_classname
#         self.player_team_dic={}
#     def LoadModel(self):
#         self.mpdel = CLIPModel.from_pretrained("patrickjohncyh/fashion-clip")
#         self.processor  = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")
#     def get_player_color(self,frame,bbox):
#         # The bellow format is used to crop image 
#         # The Box --> x1,y1,x2,y2 so the first two parameters is for height and second other paramerts is for width

#         image=frame[int(bbox[1]):int(bbox[3]),int(bbox[0]):int(bbox[2])]
#         rgb_Image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
#         PILImage=Image.fromarray(rgb_Image)
#         classes=[self.team_1_className,self.team_2_classname]
#         inputs=self.processor(text=classes,images=PILImage,return_tensor='pt',padding=True)
#         outPuts=self.mpdel(**inputs)
#         logits_perImage= outPuts.logits_per_image # this is the image text similarity score 
#         probs=logits_perImage.softmax(dim=1)
#         class_name=probs.argmax(dim=1)[0]
#         return class_name
#     def get_player_team(self,frame,playerbbox,playerId):
#         if playerId in self.player_team_dic[playerId]:
#             return self.player_team_dic[playerId]
#         player_color=self.get_player_color(frame,playerbbox)
#         team_id=True
#         if player_color==self.team_1_className:
#             team_id=1
#         self.player_team_dic[playerId]=team_id
#         return team_id
#     def get_player_team_across_fames(self,video_frames,playerTrack,read_fromStub=False,stubPath=None):
#         player_assignment=ReadSub(read_fromStub,stubPath)
#         if player_assignment is not None:
#             if len(player_assignment)==len(video_frames):
#                 return player_assignment
#         self.LoadModel()
#         player_assignment=[]
#         for frame_number,traks in enumerate(playerTrack):
#             player_assignment.append({})
#             if frame_number %50==0:
#                 self.player_team_dic={}
#             for player_id,track in playerTrack.items():
#                 team=self.get_player_team(video_frames[frame_number],track['box'],player_id)
#                 player_assignment[frame_number][player_id]=team
#         Write_sub(stubPath,player_assignment)
#         return player_assignment


from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import cv2
import sys
sys.path.append('./')
from utills.stubs_utils import ReadSub, Write_sub
class teamAssiner:
    def __init__(
        self,
        team_1_className='white shirt',
        team_2_classname='blue shirt'
    ):
        self.team_1_className = team_1_className
        self.team_2_classname = team_2_classname
        self.player_team_dic = {}
        self.model = None
        self.processor = None
    def LoadModel(self):
        self.model = CLIPModel.from_pretrained(
            "patrickjohncyh/fashion-clip"
        )
        self.processor = CLIPProcessor.from_pretrained(
            "openai/clip-vit-large-patch14"
        )
    def get_player_color(self, frame, bbox):
        x1, y1, x2, y2 = map(int, bbox)
        # Prevent invalid crop
        if x2 <= x1 or y2 <= y1:
            return None
        image = frame[y1:y2, x1:x2]
        # Prevent empty image
        if image.size == 0:
            return None
        # Convert BGR -> RGB
        rgb_Image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Convert numpy image -> PIL image
        PILImage = Image.fromarray(rgb_Image)
        classes = [
            self.team_1_className,
            self.team_2_classname
        ]
        inputs = self.processor(
            text=classes,
            images=PILImage,
            return_tensors='pt',
            padding=True
        )

        outputs = self.model(**inputs)
        logits_perImage = outputs.logits_per_image
        probs = logits_perImage.softmax(dim=1)
        # Get class index
        class_name = probs.argmax(dim=1).item()
        return class_name
    def get_player_team(self, frame, playerbbox, playerId):
        # Check cached result
        if playerId in self.player_team_dic:
            return self.player_team_dic[playerId]
        player_color = self.get_player_color(
            frame,
            playerbbox
        )
        # If crop failed
        if player_color is None:
            return None
        # Class 0 -> Team 1
        if player_color == 0:
            team_id = 1
        else:
            team_id = 2
        # Save result
        self.player_team_dic[playerId] = team_id
        return team_id
    def get_player_team_across_fames(
        self,
        video_frames,
        playerTrack,
        read_fromStub=False,
        stubPath=None
    ):

        # Try reading saved stub
        player_assignment = ReadSub(
            read_fromStub,
            stubPath
        )

        if player_assignment is not None:

            if len(player_assignment) == len(video_frames):
                return player_assignment

        # Load CLIP model
        self.LoadModel()
        player_assignment = []
        # Loop over all frames
        for frame_number, tracks in enumerate(playerTrack):
            player_assignment.append({})
            # Reset cache every 50 frames
            if frame_number % 50 == 0:
                self.player_team_dic = {}

            # Loop over all players in current frame
            for player_id, track in tracks.items():
                if 'box' not in track:
                    continue
                team = self.get_player_team(
                    video_frames[frame_number],
                    track['box'],
                    player_id
                )
                player_assignment[frame_number][player_id] = team
        # Save stub
        Write_sub(
            stubPath,
            player_assignment
        )
        return player_assignment