from django.urls import path, include

from rest_framework.routers import DefaultRouter

from freelancer import views


router = DefaultRouter()

router.register('myprofile', views.MyProfileViewSet)
router.register('editmyprofile', views.EditMyProfileViewSet, basename='editmyprofile')
router.register('freelancers', views.ListAllProfilesViewSet)
router.register('mygigs', views.MyGigsViewSet)
router.register('gigs', views.ListAllGigsViewSet)


app_name = 'freelancer'

urlpatterns = [
    path('', include(router.urls))
]
