from django.shortcuts import render
from unicodedata import category
from django.shortcuts import render
from django.shortcuts import render
from .models import * 
from rest_framework.response import *
from rest_framework.decorators import *
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.renderers import * 
from django.core.files.images import ImageFile
from django.core.mail import *
from django.conf import settings 
from django.contrib.auth import *
import random
import string  
from django.contrib.auth.models import User
from calendar import *
from .Manipulation import *
import json  
from .serializable import * 
from datetime import * 
from rest_framework_jwt.views import ObtainJSONWebToken
import jwt
from .forms import * 
from django.contrib import messages
from django.http import JsonResponse
# Create your views here.

# error table 
# 1 success 
# 11 
# 
# 
# 
# 
# 
# 









@api_view(['GET'])
def checkAuthen(request):
    try:
        auth_header = request.headers['Authorization']
        token = auth_header.split(" ")[1]
        payload = jwt.decode(token, settings.SECRET_KEY)
        user_id = payload['id']
        user = User.objects.get(pk=user_id)
        return Response({'user': user.email})
    except jwt.ExpiredSignatureError:
        return Response({'error': 'Token expired'}, status=401)
    except jwt.DecodeError:
        return Response({'error': 'Token invalid'}, status=401)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)


@api_view(['POST'])
def logIn(request):
    if request.method == 'POST' :
        username = User.objects.filter(email= request.POST.get('email'))
        if username.count() == 1 :
            username = User.objects.get(email= request.POST.get('email')).username
            user = authenticate( username=username, password=request.POST.get('password'))
            if user is not None : 
                payload = {
                    'id': user.pk,
                    'email': user.email,
                }
                jwt_token = {'token': jwt.encode(payload, settings.SECRET_KEY)}  

                return Response(jwt_token)  
            else :
                return Response(0) 
        else : 
            return Response(-1) 
   
    return Response(-1)
@api_view(['POST'])
def signIn(request):
    # email must be unique 
    # check if there is another username 
    if request.method == 'POST' :

        if User.objects.filter(email = request.POST.get('email')).exists() :
            return Response(-1) 
        else :
            username = fistName = lastName = ''
            if " " in request.POST.get('name') :
                username = request.POST.get('name').replace(' ','_')
                fistName = setUsername(request.POST.get('name'))[0]
                lastName = setUsername(request.POST.get('name'))[1]
            else :
                username = request.POST.get('name')  
            sufix = '' 
            while User.objects.filter(username = (username+sufix)).exists() :
                sufix = get_random_string()
            username = username+sufix
            
            user = authenticate(request, username=username, password=request.POST.get('password'))
            if user is None : 
                form = RegistrationForm({'username' : username, 'email' : request.POST.get('email') ,'password' : request.POST.get('password') , 'first_name' : fistName ,'last_name': lastName  })
                if (form.is_valid()):
                    form.save()   
                    return Response(1)
            else :  
                return Response(0)
    return Response(0)   


@api_view(['GET'])
def prof(request):    
    if request.method == 'GET' :
        # arr = []
        re = profile.objects.first()
        zineb_desc = about_page_table.objects.first().desc
        profl = profileSER(re).data
        profl['description'] = zineb_desc 

        # books = book.objects.filter(category = 'zinebBooks')
        # selfDef = book.objects.filter(category = 'selfdev')
        um = social_media_link.objects.all()
        if um.count() > 0 :
            um = um[0]
            um = social_media_linkSER(um).data
        else :
            um = None
        

       
        book_category = book_cat.objects.all()
        bookPack = []
        for s in book_category :
            books = book.objects.filter(category = s)
            if books.count() :
                bookPack.append ({
                    'cat' :book_catSER(s).data ,
                    'books' : booksSER(books , many=True).data ,
                })
        return Response ({
            'zinebProf' : profl ,
            'books' : bookPack ,
            'links' : um
        })
    return Response()

@api_view(['GET'])
def bookDetails(request,id):
    s = book.objects.get(id=id)
    sRET = book.objects.filter(id=id)
    books = book.objects.all().exclude(id = id)
    
    return Response({
        'theBook': booksSER(sRET,many=True).data , 
        'otherbooks' : booksSER(books,many=True).data , 

    })      
        
@api_view(['GET','POST'])
def bookDelete(request):

    if request.method == 'POST' :
        bk = book.objects.get(id=request.POST.get('id'))
        bk.delete()
        return Response(1)

    return Response('')  


@api_view(['GET','POST'])
def bookEdit(request):
    if request.method == 'POST' :
        cat = book_cat.objects.get(id=request.POST.get('category'))
        bk = book.objects.get(id = request.POST.get('id'))
        bk.name = request.POST.get('name')
        bk.author = request.POST.get('author')
        bk.description = request.POST.get('description')
        bk.pdfPrice = request.POST.get('pdfPrice')
        bk.paperPrice = request.POST.get('paperPrice')
        bk.category = cat
        if (request.FILES != {}) :
            bk.cover = request.FILES['picture']
            bk.file = request.FILES['file']
        bk.save()
       
    return Response()

@api_view(['GET'])
def persDev(request):  
    books = book.objects.filter(category = 'selfdev')
    return Response({
        'books' : booksSER(books,many=True).data
    })   

@api_view(['GET'])
def zinebPage(request): 
    re = profile.objects.all()
    books = book.objects.filter(category = 'zinebBooks')
    return Response({ 'zinebProf' : profileSER(re,many=True).data,
                    'zinebBooks' : booksSER(books,many=True).data
        }) 
# Create your views here.      




@api_view(['POST'])
def Edit_Video_category(request):

    cat = book_cat.objects.get(id = request.POST.get('id'))
    cat.title = request.POST.get('name')
    cat.description = request.POST.get('desc')
    cat.save()
    return Response(1)

@api_view(['POST'])
def delete_Video_category(request):
    cat = book_cat.objects.get  (id = request.POST.get('id'))
    cat.delete()
    return Response()




@api_view(['POST'])
def Add_Video_category(request):

    rq = book_cat.objects.create()
    rq.title = request.POST.get('name')
    rq.description = request.POST.get('desc')
    rq.save()
    return Response() 

@api_view(['POST'])    
def rm_page_cat(request):
    rm = cour_category_app.objects.filter(id= int(request.POST.get('id')) )
    if rm.count() :
        rm.delete()
    return Response ()


@api_view(['POST','GET'])    
def add_page_cat(request):
    if request.method == 'POST' :

        if int(request.POST.get('edit')) == 0 : 
            rq = cour_category_app.objects.create()
        else :
            rq = cour_category_app.objects.get( id = int(request.POST.get('id')) )
        rq.name = request.POST.get('name')
        rq.description = request.POST.get('desc')    
        rq.save()
        return Response(1)   
    if request.method == 'GET' : 
        side_table = side_page.objects.all()
        tables_pack = side_pageSER(side_table,many = True).data 
        for s in tables_pack :
            rt = the_content.objects.filter(as_sidepage = s['id'])
            s['tables'] = page_contenteSER( rt , many=True ).data
        about = about_page_table.objects.first()
        
        return Response({
            'category_list' : cour_categorySER(cour_category_app.objects.all() , many = True).data ,
            'side_table' : tables_pack , 
            'about' : about_pageSER(about).data ,     
        })
    return Response(0)


@api_view(['POST'])    
def delete_page(request):
    rq = the_content.objects.filter(id = request.POST.get('id'))
    if rq.count() :
        rq = the_content.objects.get(id = request.POST.get('id'))
        rq.delete()
    return Response()


@api_view(['POST','GET'])    
def add_page(request):
    if request.method == 'POST' :

        if int(request.POST.get('page_type')) == 2 :
            check = about_page_table.objects.all()
            if check.count() == 0 :
                rq = about_page_table.objects.create() 
                rq.desc = request.POST.get('desc')
                rq.content = json.loads(request.POST.get('content'))
                rq.save()
            else :
                rq = about_page_table.objects.first()
                rq.desc = request.POST.get('desc')
                rq.content = json.loads(request.POST.get('content'))
                rq.save()
        else :
            fr_resp = json.loads(request.POST.get('edit_state'))

            if fr_resp == False : 
                rk = the_content.objects.create()
            else : 
                rk = the_content.objects.get(id = fr_resp['id'] )
            rk.name = request.POST.get('page_title')
            rk.content = json.loads(request.POST.get('content'))
            if int(request.POST.get('page_type')) == 0 :
                rk.library =  cour_category_app.objects.get(id = request.POST.get('category'))
            elif int(request.POST.get('page_type')) == 1 :
                rk.as_sidepage = side_page.objects.get(id = request.POST.get('category'))
            rk.save()  

    return Response()      


@api_view(['POST'])        
def Add_book(request):
    data = request.POST
    cat = book_cat.objects.get(id=data.get('category'))
    rq = book.objects.create()
    rq.name = data.get('name')   
    rq.author = data.get('author')
    rq.pdfPrice = data.get('pdfPrice')
    rq.paperPrice = data.get('paperPrice')
    rq.category = cat
    rq.description = data.get('description')
    if (request.FILES != {}) :
        rq.cover =  request.FILES['picture']
        rq.file = request.FILES['file']
    rq.save()

    return Response(rq.id)

@api_view(['GET','POST'])    
def userState(request):
    try:
        auth_header = request.headers['Authorization']
        token = auth_header.split(" ")[1]
        payload = jwt.decode(token, settings.SECRET_KEY)
        user_id = payload['id']
        user = User.objects.get(pk=user_id)
        rk = userDetails.objects.filter(auth = user)
        if rk.count() > 0 :
            userP = userDetails.objects.get(auth = user)
            mk = pubPermission.objects.filter(profile = userP)
            if userP.frenchCourse :
                return Response({
                    'profile' : True ,
                    'permission' : False ,
                    'permissionSet' : True ,
                    'data' : {
                        'picture' : str(userP.picture) ,
                        'id_p' :  userP.id ,
                        'full_name' : user.get_full_name() ,
                        'job' : userP.job
                    }
                })
            if (mk.count() > 0) :
                return Response({
                    'profile' : True ,
                    'permission' : True , 
                    'permissionSet' : False ,
                    'data' : {
                        'picture' : str(userP.picture) ,
                        'id_p' :  userP.id ,
                        'full_name' : user.get_full_name() ,
                        'job' : userP.job
                    }
                })
            else : 
                return Response({
                    'profile' : True ,
                    'permission' : False , 
                    'permissionSet' : False ,
                    'data' : {}
                })
        else :
            return Response({
                    'profile' : False ,
                    'permission' : False , 
                    'permissionSet' : False ,
                    'data' : {}
                })    

        # return Response({'user': user.email})
    except jwt.ExpiredSignatureError:
        return Response({'error': 'Token expired'}, status=401)
    except jwt.DecodeError:
        return Response({'error': 'Token invalid'}, status=401)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    return Response()



@api_view(['GET','POST'])    
def profile_register(request):
    if request.method == 'POST' :

        token = request.POST.get('jwt')
        payload = jwt.decode(token, settings.SECRET_KEY)
        user_id = payload['id']
        rq = userDetails.objects.create()
        rq.picture = request.FILES['picture']
        rq.auth = User.objects.get(id = user_id)
        rq.desc = request.POST.get('desc')
        rq.job = request.POST.get('job')
        rq.save()
        return Response(1)
    return Response()

@api_view(['GET','POST'])    
def setPermission(request):
    if request.method == 'POST' :
        token = request.POST.get('jwt')
        payload = jwt.decode(token, settings.SECRET_KEY)
        user_id = payload['id']
        thUser = User.objects.get(id = user_id)
        userP = userDetails.objects.filter( auth = thUser)

        if (userP.count()>0) :
            userP = userDetails.objects.get(auth = thUser)
            check = pubPermission.objects.filter(profile = userP)
            if (check.count() == 0) :
                rq  = pubPermission.objects.create()
                rq.profile = userP
                rq.save() 
            
            return Response({
                'job' : userP.job ,
                'picture' : str(userP.picture) ,
                'full_name' : userP.auth.get_full_name() ,
                'id_p' : userP.id , 
            })
            
            
            
        else :
            return Response(0)
    return Response()


@api_view(['POST'])    
def register_quiz_correction(request):
    rq = quizeHistory.objects.filter(id = request.POST.get('pk'))
    if rq.count() :
        rq = quizeHistory.objects.get(id = request.POST.get('pk'))
        for s in rq.answer :
            if s['q_index'] == int(request.POST.get('q_index') ):
                s['comment'] = request.POST.get('comment')
                rq.save()
    return Response()

@api_view(['GET','POST'])    
def get_data_permission(request):
    if (request.method == 'POST') :
        token = request.POST.get('jwt')
        payload = jwt.decode(token, settings.SECRET_KEY)
        user_id = payload['id']
        user = User.objects.get(pk=user_id)
        
        um = profile.objects.all()
        if um.count() > 0 :
            um = um[0].picture
        else :
            um = ''

        books_ = book.objects.all()
        cat = book_cat.objects.all() 

        if (user.is_staff) :

            rk = pubPermission.objects.all().order_by('date')
            package = []
            for p in rk :
                package.append({
                    'name' : p.profile.auth.get_full_name() ,
                    'picture' : str(p.profile.picture) , 
                    'job' : p.profile.job ,
                    'id' : p.id ,
                })
            us = userDetails.objects.filter(frenchCourse = True)
            users_package = []
           
            profObj = {}
            generalProfile = profile.objects.all()
            if generalProfile.count() > 0  :
                profObj = profileSER(generalProfile[0]).data
            linkers = social_media_link.objects.all()
            linksObj = {}
            if linkers.count() > 0 :
                linksObj = social_media_linkSER(linkers[0]).data

            cour_category_tab = cour_category_app.objects.all() 
            cour_category_package = []
            for s in cour_category_tab :
                page_pack = []
                pages = page_contenteSER(the_content.objects.filter(library = s),many=True).data
            
                cour_category_package.append({
                    'category' : cour_categorySER(s).data ,
                    'pages' : pages ,
                })

            quizes = quizeHistory.objects.all()
            quiz_pack = []
            for s in quizes :
                page = s.page.content[s.line]['content']
                
                user = userD(s.user.id) 
                questions_pack = []
                for m in s.answer : 
                    q =  s.page.content[s.line]['content']['list'][m['q_index']]
                    
                    if int(q['type']) == 0 :
                        questions_pack.append({
                            'question' : q['question'] ,
                            'answer' : m['answer'] ,
                            'comment' : m['comment'] , 
                            'pk' : s.id ,
                            'q_index' : m['q_index'] , 
                        })
                quiz_pack.append({
                    'name' : user['name'] ,
                    'cover' : user['cover'] ,
                    'quiz_name' : page['title'] ,
                    'page_title' : s.page.name ,
                    'ques' : questions_pack ,
                }) 
                    
            

#  question - user answer - field for comment correction  
            
            


            return Response({
                'permission' : package ,
                'users' : users_package ,
                'picture' : str(um) ,   
                'books' : booksSER(books_ , many = True).data ,
                'categories' : book_categorySER(cat , many = True ).data ,
                'generalProfile' : profObj ,
                'links' : linksObj ,
                'pages_cat' : cour_category_package ,
                'quizes' : quiz_pack ,

            })
        else :
            return Response(None)
    return Response(None)
   
@api_view(['GET','POST'])    
def permission_accept(request):
    if request.method == 'POST' :
        check = pubPermission.objects.filter(id  = request.POST.get('id'))
        if check.count() > 0 :
            perm = pubPermission.objects.get(id  = request.POST.get('id'))
            userP = perm.profile

            if int(request.POST.get('resp')) == 1 :
                userP.frenchCourse = True 
                userP.save()
                perm.delete()
                return Response(1)
            else : 
                userP.frenchCourse = False 
                userP.save()
                perm.delete()
                return Response(1)
        else : 
            return Response(0)
    return Response()



@api_view(['GET','POST'])    
def profile_rm_perm (request) :
    if request.method == 'POST' :
        check = userDetails.objects.filter(id=request.POST.get('id'))
        if check.count() > 0 :
            userP = userDetails.objects.get(id=request.POST.get('id'))
            userP.frenchCourse = False 
            userP.save()
            return Response(1)
        
    return Response()

@api_view(['GET','POST'])    
def about_page (request) :
    # if request.method == 'POST' :
        # check = about_page_table.objects.all()
        # if check.count() == 0 :
        #     rq = about_page_table.objects.create() 
        #     rq.desc = request.POST.get('desc')
        #     rq.content = json.loads(request.POST.get('content'))
        #     rq.save()
        # else :
        #     rq = about_page_table.objects.first()
        #     rq.desc = request.POST.get('desc')
        #     rq.content = json.loads(request.POST.get('content'))
        #     rq.save()

    sk = about_page_table.objects.first()

    return Response(about_pageSER(sk).data)



@api_view(['GET','POST'])    
def userProfile(request):
    if request.method == 'GET' :
        auth_header = request.headers['Authorization']
        token = auth_header.split(" ")[1]
        payload = jwt.decode(token, settings.SECRET_KEY)
        user_id = payload['id']
        us = User.objects.get(id = user_id)
        profile = userDetails.objects.get(auth = us)
        
        package = []
      
        select_cat = []
        vid_package = []
        select_PL = []     
       
        
   
        
        return Response({
            'playLists' : package ,
            'videos' : vid_package ,
            'select_playlist' : select_PL ,
            'select_cat' : select_cat ,
            'playlist_update' : [] ,
            'userProfile' : userProfileSER(profile).data ,
            'username' : us.get_full_name() ,
        })
 


    






@api_view(['GET','POST'])    
def EditProfile(request):
    if request.method == 'POST' :
        token = request.POST.get('jwt')
        payload = jwt.decode(token, settings.SECRET_KEY)
        user_id = payload['id']
        user = User.objects.get(pk=user_id)
        usernane = request.POST.get('username')

        user.first_name = setUsername(usernane)[0]
        user.last_name = setUsername(usernane)[1]
        user.save()
        rq = userDetails.objects.get(auth= user)
        rq.desc = request.POST.get('desc')
        rq.job = request.POST.get('job')
        if (request.FILES != {}) :
            rq.picture = request.FILES['picture']
        rq.save()
        return Response(1)
    return Response(0)


@api_view(['GET','POST'])    
def updateKey(request):
    if request.method == 'POST' :
        token = request.POST.get('jwt')
        payload = jwt.decode(token, settings.SECRET_KEY)
        user_id = payload['id']
        user = User.objects.get(pk=user_id) 
        auth = authenticate(request, username=user.username , password=request.POST.get('curr_password'))

        if auth is not None: 
            user.set_password(request.POST.get('new_password'))
            user.save() 
            return Response (1)
        else :
            return Response(-1)
    return Response(0)  




@api_view(['GET','POST'])    
def set_links(request):
    if request.method == 'POST' :
        rq = profile.objects.all()
        if rq.count() > 0 :
            row = rq[0]
            row.description = request.POST.get('desc')
            if (request.FILES != {}) :
                row.picture = request.FILES['picture']
            row.save()
        else :
            row = profile.objects.create()
            row.name = 'El Kadri Zineb'
            row.description = request.POST.get('desc')
            if (request.FILES != {}) :
                row.picture = request.FILES['picture']
            row.save()
        rf = social_media_link.objects.all()
        if rf.count() > 0 :
            row = rf[0]
            row.whatsapp = request.POST.get('whatsapp')
            row.insta = request.POST.get('instagram')
            row.youtube = request.POST.get('youtube')
            row.gmail = request.POST.get('gmail')
            row.facebook = request.POST.get('facebook')
            row.save()
        else :    
            row = social_media_link.objects.create()
            row.whatsapp = request.POST.get('whatsapp')
            row.insta = request.POST.get('instagram')
            row.youtube = request.POST.get('youtube')
            row.gmail = request.POST.get('gmail')
            row.facebook = request.POST.get('facebook')
            row.save()
        return Response(1)
    return Response(0)


@api_view(['POST'])    
def register_picture(request):
    if (request.FILES != {}) :
        rq = Galery.objects.create()
        rq.picture = request.FILES['picture']
        rq.save()        
        return Response(str(rq.picture))
    return Response(0)

@api_view(['POST'])    
def register_PDF(request):
    if (request.FILES != {}) :
        rq = PDF_library.objects.create()
        rq.file = request.FILES['file']
        rq.save()        
        return Response(str(rq.file))
    return Response(0)

@api_view(['GET'])
def pages_indexing(request):
    books_cat = book_cat.objects.all()
    pack = []
    for s in books_cat :
        books = book.objects.filter ()
        if books.count() :
            pack.append(book_catSER(s).data)
    pages_pack =[]
    pages = cour_category_app.objects.all()
    for k in pages : 
        list_pages = []
        pages_cat =  the_content.objects.filter(library=k)
        if pages_cat.count() :
            pages_pack.append({
                'category' : k.name ,
                'pages' : page_contenteSER(pages_cat,many=True).data ,
            })
    return Response({
        'books' : pack ,
        'pages' : pages_pack , 
    })

@api_view(['GET'])
def book_category(request,id):

    tr = book_cat.objects.filter(id=id) 
    if tr.count():
        tr = book_cat.objects.get(id=id) 
        books = book.objects.filter(category = id) 
        other_books = book.objects.all().exclude(category = id)[:8]
        return Response({
            'category' : book_catSER(tr).data , 
            'books' : booksSER(books , many=True).data , 
            'other_books' : booksSER(other_books , many=True).data
        })

    return Response ()

@api_view(['POST'])
def get_page_content(request):
    page_row = the_content.objects.filter(id=request.POST.get('id'))
    token = request.POST.get('jwt')
    answers_pack = []

    if page_row.count() : 
        page_row = the_content.objects.get(id=request.POST.get('id'))  
        answers_pack = None
        side_table = side_page.objects.all()
        tables_pack = []
        for s in side_table :
            rt = the_content.objects.filter(as_sidepage = s)
            
            if rt.count() :
                tables_pack.append({
                    'id' : s.id ,
                    'name' : s.name ,
                    'tables' :  page_contenteSER( rt , many=True ).data ,
                })

        if token != 'null' :
            payload = jwt.decode(token, settings.SECRET_KEY)
            user_id = payload['id']

            rq_answers = quizeHistory.objects.filter(
                user =  user_id ,
                page = page_row )
            answers_pack = quizeHistorySER(rq_answers , many = True ).data
        this_page_comments = page_comment.objects.filter(page = page_row)
        comments_pack = page_commentSER(this_page_comments , many = True).data
        for s in comments_pack :
            user = User.objects.get(id = s['user'] )
            userProfile = userDetails.objects.filter(auth=user)
            pic = ''
            if userProfile.count() :
                pic = str(userDetails.objects.get(auth=user).picture)
            s['user'] = user.get_full_name()
            s['picture'] = pic

        return Response ({
            'content' : page_contenteSER(page_row).data , 
            'quiz_answer' : answers_pack ,
            'comments' : comments_pack , 
            'side_table' : tables_pack ,
        })
        
    return Response (0)


@api_view(['POST'])
def register_quiz_answers(request):
    token = request.POST.get('jwt')
    payload = jwt.decode(token, settings.SECRET_KEY)
    user_id = payload['id']
    answer = json.loads(request.POST.get('answers'))
    the_page = the_content.objects.get(id = request.POST.get('page'))
    quiz = the_page.content[int(request.POST.get('line'))]['content']['list']
    for s in answer :
        the_question = quiz[int(s['q_index'])]
        
        if ( the_question['type'] == 1 ) :
            if the_question['answer'] == s['answer'] :
                s['result'] = 1 
            else :
                s['result'] = 0 
                

    row = quizeHistory.objects.filter(
        user = user_id,
        page=request.POST.get('page'),
        line = request.POST.get('line')  )
    if row.count() == 1:
        row = row[0] 
        row.answer = json.loads(request.POST.get('answers'))
        row.save()
    else :
        rq = quizeHistory.objects.create()
        rq.user = User.objects.get(id = user_id) 
        rq.page = the_content.objects.get(id=request.POST.get('page'))
        rq.line = int(request.POST.get('line'))    
        rq.answer = json.loads(request.POST.get('answers'))
        rq.save()
    return Response()


@api_view(['POST'])
def register_user_comment(request):
    token = request.POST.get('jwt')
    payload = jwt.decode(token, settings.SECRET_KEY)
    user_id = payload['id']
    rq = page_comment.objects.create()
    rq.page = the_content.objects.get(id=request.POST.get('page'))
    rq.user = User.objects.get(id = user_id) 
    rq.comment = request.POST.get('comment')
    rq.save()
    return Response()



@api_view(['POST'])
def register_side_table(request):
    rq = side_page.objects.create()
    rq.name = request.POST.get('table_name')
    rq.save()
    return Response()


@api_view(['POST'])
def edit_side_table(request):
    rq = side_page.objects.filter(id = request.POST.get('id'))
    if rq.count() :
        rq = side_page.objects.get(id = request.POST.get('id'))
        rq.name = request.POST.get('table_name')
        rq.save()
    return Response()



@api_view(['POST'])
def delete_side_table(request):
    rq = side_page.objects.filter(id = request.POST.get('id'))
    if rq.count() :
        rq = side_page.objects.get(id = request.POST.get('id'))
        rq.delete()
    return Response()

@api_view(['GET'])
def for_footer(request):
    social = social_media_link.objects.first()
    
    return Response({
        'links' : social_media_linkSER(social).data
    })