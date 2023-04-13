from django.urls import path 
from . import views 


urlpatterns = [
    path('zinebprofile', views.prof ) ,
    path('selfdev', views.persDev ) ,  
    path('bookdetails/<int:id>', views.bookDetails ) ,
    path('bookdetails/edit', views.bookEdit ) ,
    path('bookdetails/rm', views.bookDelete ) ,

    path('add_book/', views.Add_book ) ,
    path('add_category/', views.Add_Video_category ) ,
    path('add_category/edite', views.Edit_Video_category ) ,
    path('add_category/delete', views.delete_Video_category ) ,

    path('about_page', views.about_page ) ,   

    path('add_page_cat', views.add_page_cat ) ,
    path('add_page_cat/delete', views.rm_page_cat ) ,
    path('add_page', views.add_page ) ,
    path('add_page/delete', views.delete_page ) ,
    path('add_page/register_picture', views.register_picture ) ,
    path('add_page/register_pdf', views.register_PDF ) ,

    path('general/pages_indexing', views.pages_indexing ) ,
    path('general/book_category/<int:id>', views.book_category ) ,
    path('general/page_content/', views.get_page_content ) ,

    path('register_quiz_answers', views.register_quiz_answers ) ,
    path('register_user_comment', views.register_user_comment ) ,
    path('register_side_table', views.register_side_table ) ,
    path('edit_side_table', views.edit_side_table ) ,
    path('delete_side_table', views.delete_side_table ) ,
    path('register_quiz_correction', views.register_quiz_correction ) ,


    path('profile/edit', views.EditProfile ) ,
    path('profile/updatekey', views.updateKey ) ,
    
    path('video/add', views.userProfile ) ,


    path('profile_register/', views.profile_register ) ,
    path('set_permission/', views.setPermission ) ,
    path('prof_rm_perm/', views.profile_rm_perm ) ,

    path('check_perm/', views.userState ) ,
    path('permission_data/', views.get_data_permission ) ,
    path('permission_accept/', views.permission_accept ) ,
    path('setlinks/', views.set_links ) ,

    path('sign/', views.signIn ) ,
    path('login/', views.logIn ) ,
    path('authorization/', views.checkAuthen ) ,
    path('for_footer/', views.for_footer ) ,


]      