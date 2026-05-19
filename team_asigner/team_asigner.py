from PIL import Image
from transformers import CLIPProcessor,CLIPModel
import cv2
class teamAssiner:
    def __init__(self,team_1_className='white shirt',team_2_classname='blue shirt'):
        self.team_1_className=team_1_className
        self.team_2_classname=team_2_classname
        self.player_team_dic={}
    def LoadModel(self):
        self.mpdel = CLIPModel.from_pretrained("patrickjohncyh/fashion-clip")
        self.processor  = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")
    def get_player_color(self,frame,bbox):
        # The bellow format is used to crop image 
        # The Box --> x1,y1,x2,y2 so the first two parameters is for height and second other paramerts is for width

        image=frame[int(bbox[1]):int(bbox[3]),int(bbox[0]):int(bbox[2])]
        rgb_Image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        PILImage=Image.fromarray(rgb_Image)
        classes=[self.team_1_className,self.team_2_classname]
        inputs=self.processor(text=classes,images=PILImage,return_tensor='pt',padding=True)
        outPuts=self.mpdel(**inputs)
        logits_perImage= outPuts.logits_per_image # this is the image text similarity score 
        probs=logits_perImage.softmax(dim=1)
        class_name=probs.argmax(dim=1)[0]
        return class_name
    def get_player_team(self,frame,playerbbox,playerId):
        if playerId in self.player_team_dic[playerId]:
            return self.player_team_dic[playerId]
        player_color=self.get_player_color(frame,playerbbox)
        team_id=True
        if player_color==self.team_1_className:
            team_id=1
        self.player_team_dic[playerId]=team_id
        return team_id
    def get_player_team_across_fames(self,video_frames,playerTrack,read_fromStub=False,stubPath=None):
        self.LoadModel()
        player_assignment=[]
        for frame_number,traks in enumerate(playerTrack):
            player_assignment.append({})
            if frame_number %50==0:
                self.player_team_dic={}
            for player_id,track in playerTrack.items():
                team=self.get_player_team(video_frames[frame_number],track['box'],player_id)
                player_assignment[frame_number][player_id]=team
        return player_assignment


