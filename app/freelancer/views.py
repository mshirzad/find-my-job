from django.db.models.query_utils import Q

from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Profile, Gig

from freelancer import serializers


class BaseListAttr(viewsets.GenericViewSet, 
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class ListAllProfilesViewSet(BaseListAttr):
    
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    def get_queryset(self):
        queryset = self.queryset
        keyword = self.request.query_params.get('keyword')

        if keyword:
            queryset = queryset.filter(
                Q(user__name__icontains=keyword) | 
                Q(profession__icontains=keyword) | 
                Q(bio__icontains=keyword)
            )

        return queryset


class ListAllGigsViewSet(BaseListAttr):

    queryset = Gig.objects.all()
    serializer_class = serializers.GigSerializer

    def get_queryset(self):
        queryset = self.queryset
        keyword = self.request.query_params.get('keyword')

        if keyword:
            queryset = queryset.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword)).order_by('min_price')
            
        return queryset
    


class MyProfileViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user

        if not Profile.objects.filter(user=user):
            serializer.save(user=user)
        else:
            return Response(
                serializer.errors,
                status.HTTP_400_BAD_REQUEST
            )


class EditMyProfileViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ProfileSerializer

    def get_object(self):
        return Profile.objects.get(user=self.request.user)


class MyGigsViewSet(viewsets.ModelViewSet):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Gig.objects.all()
    serializer_class = serializers.GigSerializer

    def get_queryset(self):
        user = self.request.user
        current_freelancer = Profile.objects.get(user=user)

        return self.queryset.filter(freelancer__profile__id=current_freelancer.id)