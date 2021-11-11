from django.urls import path, include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

app_name = 'insects'

urlpatterns = [
    path('insect/<slug>', views.insect_slug, name='slug'),
    path('', views.home, name='home'),
    path('image/<str:image>', views.image, name="image"),
    path('get_all_insect/', views.getAllInsect, name='get_all_insect'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('users/', views.getAllUser, name='get_user'),
    path('logout/', views.logout_view, name='logout'),
    path('import_data/', views.import_data_view, name='import_data'),
    path('search_tool/', views.search_tool, name='search_tool'),
    path('classification-insect/', views.ClassificationInsect, name='ClassificationInsect'),
    path('get_taxonomy_tree', views.get_taxonomy_tree, name='get_taxonomy_tree'),
    path('detail/<name>', views.detail_insect_view, name='detail_insect_view'),
    path('getfiles/<insect_slug>', views.getfiles, name='getfiles'),
    path('get-insect-images', views.getInsectImage, name='get-insect-images'),
    path('crawl-image/', views.crawl_image, name='craw_image'),
    path('import-new/', views.import_new, name='import_new'),
    path('export-excel/', views.export_excel, name='export_excel'),
    path('import-excel/', views.import_excel, name='import_excel'),
    path('get-crawled-urls/', views.get_current_urls, name='get_current_urls'),
    path('compare-img/', views.compare_url_image, name='compare_url_image'),
    path('upload-new-img/', views.upload_new_image, name='upload_new_image'),
    path('download-new-img/', views.DownloadImageFromUrl, name='DownloadImageFromUrl'),
    path('get-new-img/', views.getNewImageToDraw, name='getNewImageToDraw'),
    path('draw-boundingbox/', views.draw_bbox, name='draw_bbox'),
    path('test/', views.getNewImg, name='getNewImg'),
    path('get-new-img-rect/', views.getNewImgRect, name='getNewImgRect'),
    path('save-rect-new-image/', views.saveRectNewImg, name='saveRectNewImg'),
    path('auto-bbox/', views.autoBBox, name='autoBBox'),
    
]

urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
