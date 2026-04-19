from django.contrib.auth.models import User
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Animal, Shelter, Swipe, Match, Pet, HealthRecord, Reminder
from .serializers import (
    RegisterSerializer, UserSerializer,
    AnimalSerializer, AnimalCreateSerializer, ShelterSerializer,
    SwipeSerializer, MatchSerializer,
    PetSerializer, HealthRecordSerializer, ReminderSerializer,
)


# ── Auth ──────────────────────────────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def me_view(request):
    return Response(UserSerializer(request.user).data)


# ── Shelters ──────────────────────────────────────────────────────────────────

class ShelterListView(generics.ListAPIView):
    serializer_class = ShelterSerializer
    queryset = Shelter.objects.all()


# ── Assistant ─────────────────────────────────────────────────────────────────

@api_view(['POST'])
def assistant_view(request):
    message = (request.data.get('message') or '').strip()
    normalized = message.lower()

    if not message:
        return Response({
            'reply': 'Напишите вопрос о платформе, приютах, матчах или профиле — и я подскажу.',
            'suggestions': [
                'Как работает мэтчинг?',
                'Как связаться с приютом?',
                'Что есть в профиле?',
            ]
        })

    shelters = list(Shelter.objects.all())
    shelter_names = [shelter.name for shelter in shelters]

    if any(word in normalized for word in ['матч', 'мэтч', 'matching', 'свайп', 'лайк']):
        reply = (
            'Мэтч создаётся не после каждого лайка. Система учитывает интерес к питомцу: '
            'нужно поставить лайк животному, которое уже понравилось другим пользователям '
            'или набрало достаточно симпатий. Тогда оно попадает в раздел «Матчи».'
        )
    elif any(word in normalized for word in ['приют', 'shelter', 'телефон', 'позвон', 'связаться']):
        shelters_text = '; '.join(
            f'{shelter.name}: {shelter.phone or "телефон не указан"}'
            for shelter in shelters[:4]
        ) or 'Список приютов пока пуст.'
        reply = (
            'На странице «Приюты» можно открыть карточку приюта, посмотреть адрес, контакты и карту. '
            f'Сейчас доступны: {shelters_text}.'
        )
    elif any(word in normalized for word in ['профиль', 'аккаунт', 'кабинет']):
        reply = (
            'В профиле можно посмотреть свои данные, быстрые ссылки на свайпы, матчи и питомцев, '
            'а также задать вопрос AI-помощнику. Для администратора там доступен блок управления питомцами.'
        )
    elif any(word in normalized for word in ['питом', 'pet', 'животн', 'добавить']):
        reply = (
            'Питомцы — это животные, закреплённые за пользователем. Обычный пользователь видит своих питомцев, '
            'а администратор может назначать питомцев другим пользователям через специальный блок в профиле.'
        )
    elif any(word in normalized for word in ['платформ', 'сайт', 'pawmatch']):
        reply = (
            'PawMatch помогает находить животных из приютов, свайпать анкеты, получать мэтчи, '
            'связываться с приютами и вести информацию о питомцах в личном кабинете.'
        )
    else:
        matching_shelter = next(
            (name for name in shelter_names if name.lower() in normalized),
            None
        )
        if matching_shelter:
            shelter = next(item for item in shelters if item.name == matching_shelter)
            reply = (
                f'По приюту {shelter.name}: адрес — {shelter.address}. '
                f'Телефон — {shelter.phone or "не указан"}. '
                'Открыть все контакты можно на странице «Приюты».'
            )
        else:
            reply = (
                'Я могу подсказать по платформе PawMatch, приютам, мэтчам, профилю и питомцам. '
                'Например: «Как работает мэтчинг?» или «Как связаться с приютом?».'
            )

    return Response({
        'reply': reply,
        'suggestions': [
            'Как работает мэтчинг?',
            'Как связаться с приютом?',
            'Что можно делать в профиле?',
        ]
    })


# ── Swipe ─────────────────────────────────────────────────────────────────────

@api_view(['GET'])
def swipe_cards(request):
    already_swiped = Swipe.objects.filter(user=request.user).values_list('animal_id', flat=True)
    animals = Animal.objects.filter(is_adopted=False).exclude(id__in=already_swiped)
    serializer = AnimalSerializer(animals, many=True, context={'request': request})
    return Response(serializer.data)


def _should_create_match(animal, user):
    likes_count = Swipe.objects.filter(animal=animal, is_like=True).exclude(user=user).count()
    popular_animal = likes_count >= 2
    even_card_bonus = animal.id % 2 == 0 and likes_count >= 1
    return popular_animal or even_card_bonus


@api_view(['POST'])
def swipe_view(request):
    animal_id = request.data.get('animal_id')
    is_like = request.data.get('is_like', False)

    try:
        animal = Animal.objects.get(id=animal_id)
    except Animal.DoesNotExist:
        return Response({'error': 'Животное не найдено'}, status=404)

    swipe, created = Swipe.objects.get_or_create(
        user=request.user,
        animal=animal,
        defaults={'is_like': is_like}
    )
    if not created:
        swipe.is_like = is_like
        swipe.save()

    if is_like and _should_create_match(animal, request.user):
        match, _ = Match.objects.get_or_create(user=request.user, animal=animal)
        match_data = MatchSerializer(match, context={'request': request}).data
        return Response({'status': 'matched', 'match': match_data})

    if not is_like:
        Match.objects.filter(user=request.user, animal=animal).delete()

    return Response({'status': 'swiped'})


# ── Matches ───────────────────────────────────────────────────────────────────

class MatchListView(generics.ListAPIView):
    serializer_class = MatchSerializer

    def get_queryset(self):
        return Match.objects.filter(user=self.request.user).select_related('animal', 'animal__shelter')


# ── Submit animal ─────────────────────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def submit_animal(request):
    serializer = AnimalCreateSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    animal = serializer.save()
    return Response(
        AnimalSerializer(animal, context={'request': request}).data,
        status=status.HTTP_201_CREATED
    )


# ── Pets ──────────────────────────────────────────────────────────────────────

class PetListCreateView(generics.ListCreateAPIView):
    serializer_class = PetSerializer

    def get_queryset(self):
        return Pet.objects.filter(user=self.request.user).select_related('animal', 'animal__shelter')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PetDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PetSerializer

    def get_queryset(self):
        return Pet.objects.filter(user=self.request.user)


# ── Admin Pets ────────────────────────────────────────────────────────────────

class AdminUserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all().order_by('username')


class AdminAnimalListView(generics.ListAPIView):
    serializer_class = AnimalSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Animal.objects.filter(is_adopted=False).select_related('shelter').order_by('name')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class AdminPetCreateView(generics.ListCreateAPIView):
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Pet.objects.all().select_related('user', 'animal', 'animal__shelter').order_by('-id')

    def perform_create(self, serializer):
        serializer.save()


# ── Health Records ────────────────────────────────────────────────────────────

class HealthRecordListCreateView(generics.ListCreateAPIView):
    serializer_class = HealthRecordSerializer

    def get_queryset(self):
        pet_id = self.request.query_params.get('pet_id')
        qs = HealthRecord.objects.filter(pet__user=self.request.user)
        if pet_id:
            qs = qs.filter(pet_id=pet_id)
        return qs


class HealthRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HealthRecordSerializer

    def get_queryset(self):
        return HealthRecord.objects.filter(pet__user=self.request.user)


# ── Reminders ─────────────────────────────────────────────────────────────────

class ReminderListCreateView(generics.ListCreateAPIView):
    serializer_class = ReminderSerializer

    def get_queryset(self):
        pet_id = self.request.query_params.get('pet_id')
        qs = Reminder.objects.filter(pet__user=self.request.user)
        if pet_id:
            qs = qs.filter(pet_id=pet_id)
        return qs


class ReminderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReminderSerializer

    def get_queryset(self):
        return Reminder.objects.filter(pet__user=self.request.user)
