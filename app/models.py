from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.contrib.postgres.fields import ArrayField
import json
from django.contrib.postgres.fields.jsonb import JSONField as JSONBField


# Create your models here.
def upload_path(instance , filename):
    path = '/'.join(['covers',filename])
    path = ''.join([ path , '.jpg'])
    return path
class CustomArrayField(models.TextField):
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return json.loads(value)

    def to_python(self, value):
        if isinstance(value, list):
            return value
        if value is None:
            return value
        return json.loads(value)

    def get_prep_value(self, value):
        if value is None:
            return value
        return json.dumps(value)



def upload_video(instance , filename):
    path = '/'.join(['video',filename])
    path = ''.join([ path , '.mp4'])
    return path

def upload_file(instance , filename):
    path = '/'.join(['pdf',filename])
    
    return path



class category_book (models.Model) : 
    title = models.TextField()
    description = models.TextField()
    def __str__(self):
        return self.title 


class book_cat (models.Model) : 
    title = models.TextField()
    description = models.TextField()
    def __str__(self):
        return self.title 


class book(models.Model):
    name = models.TextField()
    author = models.TextField()
    description = models.TextField()
    pdfPrice =  models.FloatField(null=True ,blank=True)
    paperPrice =  models.FloatField(null=True ,blank=True)
    cover = models.ImageField(upload_to=upload_path, blank=True)
    category =  models.ForeignKey(book_cat, on_delete=models.CASCADE,null=True,blank=True)
    file = models.FileField(upload_to=upload_file, blank=True)
    def __str__(self):
        return self.name 


class about_page_table (models.Model) :
    desc = models.TextField()
    content = JSONBField(default=list,null=True,blank=True) 


class cour_category_app (models.Model) :
    name = models.TextField()
    description = models.TextField()
    def __str__(self):
        return self.name

class side_page (models.Model) :
    name = models.TextField()
# content = ArrayField(models.CharField(max_length=50), blank=True, null=True)

class the_content (models.Model) :
    name = models.TextField()
    library = models.ForeignKey(cour_category_app, on_delete=models.CASCADE,null=True,blank=True)
    as_sidepage = models.ForeignKey(side_page, on_delete=models.CASCADE,null=True,blank=True)
    content = JSONBField(default=list,null=True,blank=True) 
    def __str__(self):
        return self.name

class page_comment (models.Model) : 
    page =  models.ForeignKey(the_content, on_delete=models.CASCADE,null=True,blank=True)
    user =  models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    comment = models.TextField()
    date = models.DateField(("Date"), default=date.today)

class quizeHistory (models.Model) : 
    user =  models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    page =  models.ForeignKey(the_content, on_delete=models.CASCADE,null=True,blank=True)
    line = models.IntegerField(blank=True,null=True)
    answer = JSONBField(default=list,null=True,blank=True) 
    

class social_media_link (models.Model):
    whatsapp = models.TextField()
    insta = models.TextField()
    youtube = models.TextField()
    gmail = models.TextField()
    facebook = models.TextField()



class profile (models.Model):
    name = models.TextField()
    description = models.TextField(blank=True,null=True)
    picture = models.ImageField(upload_to=upload_path, blank=True)





class userDetails (models.Model):
    picture =  models.ImageField(upload_to=upload_path, blank=True)
    auth = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
    desc = models.TextField(null=True,blank=True)
    frenchCourse = models.BooleanField(default=False)
    job = models.TextField(null=True,blank=True)
    # email = models.EmailField(unique=True)
    
class pubPermission(models.Model) :
    profile = models.OneToOneField(userDetails ,  on_delete=models.CASCADE , null=True,blank=True )
    date = models.DateField(("Date"), default=date.today)



class Galery (models.Model) : 
    picture = models.ImageField(upload_to=upload_path, blank=True)

class PDF_library (models.Model) :
    file = models.FileField(upload_to=upload_file, blank=True)

    