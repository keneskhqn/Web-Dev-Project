from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Animal, Shelter, Swipe, Match, Pet, HealthRecord, Reminder


class UserSerializer(serializers.ModelSerializer):
    is_staff = serializers.BooleanField(read_only=True)

    class Meta:
        model  = User
        fields = ['id', 'username', 'email', 'is_staff']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model  = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )


class ShelterSerializer(serializers.ModelSerializer):
    animal_count = serializers.SerializerMethodField()

    class Meta:
        model = Shelter
        fields = ['id', 'name', 'address', 'phone', 'latitude', 'longitude',
                  'telegram', 'instagram', 'website', 'animal_count']

    def get_animal_count(self, obj):
        return obj.animals.filter(is_adopted=False).count()


class AnimalSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
    shelter_detail = ShelterSerializer(source='shelter', read_only=True)

    class Meta:
        model = Animal
        fields = [
            'id', 'shelter', 'shelter_detail', 'name', 'species', 'breed', 'age',
            'photo', 'is_vaccinated', 'is_neutered', 'is_adopted', 'likes_count',
        ]

    def get_likes_count(self, obj):
        return obj.likes_count()

    def get_photo(self, obj):
        request = self.context.get('request')
        if obj.photo and request:
            return request.build_absolute_uri(obj.photo.url)
        return obj.photo_url or ''


class AnimalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ['shelter', 'name', 'species', 'breed', 'age',
                  'photo', 'photo_url', 'is_vaccinated', 'is_neutered']

    def create(self, validated_data):
        request = self.context.get('request')
        return Animal.objects.create(submitted_by=request.user, **validated_data)


class SwipeSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Swipe
        fields = ['id', 'animal', 'is_like', 'created_at']


class MatchSerializer(serializers.ModelSerializer):
    animal = AnimalSerializer(read_only=True)

    class Meta:
        model  = Match
        fields = ['id', 'animal', 'created_at']


class PetSerializer(serializers.ModelSerializer):
    animal = AnimalSerializer(read_only=True)
    animal_id = serializers.PrimaryKeyRelatedField(
        queryset=Animal.objects.all(), source='animal', write_only=True
    )
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True, required=False
    )

    class Meta:
        model = Pet
        fields = ['id', 'animal', 'animal_id', 'user', 'user_id', 'name', 'birth_date', 'weight']


class HealthRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model  = HealthRecord
        fields = ['id', 'pet', 'record_type', 'title', 'description', 'date', 'next_due_date']


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Reminder
        fields = ['id', 'pet', 'title', 'date_time', 'is_completed']
