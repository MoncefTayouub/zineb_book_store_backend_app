from dataclasses import fields
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class profileSER(serializers.ModelSerializer):
    class Meta :
        fields = '__all__'
        model = profile

class UserSER(serializers.ModelSerializer):
    class Meta :
        fields = '__all__'
        model = User

class cour_categorySER(serializers.ModelSerializer):
    class Meta :
        fields = '__all__'
        model = cour_category_app

class page_contenteSER(serializers.ModelSerializer):
    class Meta :
        fields = '__all__'
        model = the_content


class social_media_linkSER(serializers.ModelSerializer):
    class Meta :
        fields = '__all__'
        model = social_media_link 

class GalerySER(serializers.ModelSerializer):
    class Meta :
        fields = '__all__'
        model = Galery 

class book_categorySER(serializers.ModelSerializer):
    class Meta :
        fields = '__all__'
        model = category_book

class booksSER(serializers.ModelSerializer):
    class Meta :
        fields = '__all__'
        model = book 

    

class userProfileSER(serializers.ModelSerializer):
    class Meta :
        fields = '__all__'
        model = userDetails  

 

class pubPermissionSER(serializers.ModelSerializer):
    class Meta :
        fields = '__all__'
        model = pubPermission  

class book_catSER(serializers.ModelSerializer):
    class Meta :
        fields = '__all__'
        model = book_cat  
    
class quizeHistorySER(serializers.ModelSerializer):
    class Meta :
        fields = '__all__'
        model = quizeHistory  

class page_commentSER(serializers.ModelSerializer):
    class Meta :
        fields = '__all__'
        model = page_comment 

class side_pageSER(serializers.ModelSerializer):
    class Meta :
        fields = '__all__'
        model = side_page  

class about_pageSER(serializers.ModelSerializer):
    class Meta :
        fields = '__all__'
        model = about_page_table  