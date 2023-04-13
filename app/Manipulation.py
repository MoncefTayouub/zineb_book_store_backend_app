from .models import * 
from django.contrib.auth.models import User
from .serializable import * 
import random
import string

def nb_video_category (catId) :
    cat = CoursCategory.objects.get(id = catId)
    plays = playlist.objects.filter(category=cat)
    total = 0
    for s in plays :
        total += videoPlay.objects.filter(playlist = s).count()
    return total  

def get_random_string():
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(4))
    return result_str

def VideoDetails (id) :
    video = videoPlay.objects.get(id=id)
    user = User.objects.get(id= video.playlist.madeBy.auth.id )
    prof = userDetails.objects.get(auth=user)
    nbPlayList = playlist.objects.filter(madeBy= prof )
    nbVideo = 0
    for s in nbPlayList :
        nbVideo += videoPlay.objects.filter(playlist = s).count()
    
    return ({
        'owner' : {    
            'name' : video.playlist.madeBy.auth.get_full_name()  , 
            'picture' :  str(video.playlist.madeBy.picture) ,
            'number_of_playlist' : nbPlayList.count() ,
            'video_nb' : nbVideo,
            
        }, 
        'video' : videoPlaySER(videoPlay.objects.filter(id = video.id),many= True).data,
    })   
    
def cat_3_videos (id) :
    arr = []
    cat = CoursCategory.objects.get(id = id )
    nbVideos = 0 
    playLists = playlist.objects.filter(category=cat)
    nbPlayList = playLists.count()
    total_video = 0
    # for s in playLists : 
    #     total_video += videoPlay.objects.filter(playlist=s).count()
    
    
    
    for s in playLists :
        vid = videoPlay.objects.filter(playlist = s)
        for k in vid :
            if (nbVideos < 3) :
                arr.append(VideoDetails(k.id))
                nbVideos += 1 
            else :
                return arr
    return arr

    

def play_3_video (id):
    curr_playList =  playlist.objects.get(id=id)
    vds = videoPlay.objects.filter(playlist = curr_playList)[:3]
    arr = []
    nbVd = 0
    for s in vds :
        arr.append(VideoDetails(s.id))
           
    return arr

def setUsername (username) :
    arr = username.split(' ')
    firstName = arr[0]
    secondName = ''
    if len(arr) > 1  :
        for k in range(1 , len(arr)) :
            secondName += ' ' + arr[k]
    return [firstName , secondName]


def userD (id) :
    user = User.objects.filter(id = id )
    if user.count() : 
        user = User.objects.get(id = id )
        full_name = user.get_full_name()
        pic_table = userDetails.objects.filter(auth = user )
        cover = ''
        if pic_table.count() :
            pic_table = userDetails.objects.get(auth = user )
            cover =str( pic_table.picture)

        return { 'name' : full_name , 'cover' : cover}
    else :
        return None



# def get_question (page , line , q_index) :
#     rm = page.content[line]['content']['list'][q_index]['question']

#     return 0 