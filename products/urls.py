from django.urls import path, include

from . import views

app_name = 'products'


bucket_urls = [
    path('', views.BucketHome.as_view(), name='bucket'),
    path('delete_obj/<str:key>', views.DeleteBucketObject.as_view(),
                                                name='bucket_obj_delete'),
    path('download_obj/<str:key>', views.DownloadBucketObject.as_view(),
                                                name='bucket_obj_download'),
    path('upload_obj/', views.UploadBucketObject.as_view(),
                                                name='bucket_obj_upload')
]


urlpatterns = [
    path('', views.ProductsListView.as_view(), name='products_list'),
    path('category/<slug:cat_slug>/', views.ProductsListView.as_view(), name='cat_filter'),
    path('bucket/', include(bucket_urls)),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]
