from django.contrib.auth import get_user_model

from rest_framework import serializers

from drf_writable_nested import WritableNestedModelSerializer

from core.models import Profile, Address, Education, Gig


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = (
            'id',
            'address_line1',
            'address_line2',
            'city',
            'province',
            'post_code',
            'country'
        )
        read_only_fields = ('id',)


class EducationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Education
        fields = (
            'id',
            'degree',
            'university',
            'faculty',
            'start_year',
            'graduation_year'
        )
        read_only_fields = ('id',)


class ProfileSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):

    address = AddressSerializer(many=False)
    education = EducationSerializer(many=False)

    class Meta:
        model = Profile
        fields = (
            'id',
            'phone',
            'profession',
            'ratings',
            'bio',
            'profile_photo',
            'user',
            'address',
            'education'
        )
        read_only_fields = ('id', 'user')


class GigSerializer(serializers.ModelSerializer):

    freelancer = serializers.PrimaryKeyRelatedField(
        queryset=Profile.objects.all() 
    )

    class Meta:
        model = Gig
        fields = (
            'id',
            'title',
            'description',
            'min_price',
            'thumbnail',
            'thumbnail_2',
            'thumbnail_3',
            'freelancer'
        )
        read_only_fields = ('id',)