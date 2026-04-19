from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    # ── Auth ──────────────────────────────────────────────────────────
    path('token/',         TokenObtainPairView.as_view(), name='token_obtain'),
    path('token/refresh/', TokenRefreshView.as_view(),   name='token_refresh'),
    path('register/',      views.register_view,          name='register'),
    path('me/',            views.me_view,                name='me'),

    # ── Shelters (новое) ─────────────────────────────────────────────
    path('shelters/',      views.ShelterListView.as_view(), name='shelters'),
    path('assistant/',     views.assistant_view,            name='assistant'),

    # ── Swipe & Matches ───────────────────────────────────────────────
    path('swipe-cards/',   views.swipe_cards,            name='swipe_cards'),
    path('swipe/',         views.swipe_view,             name='swipe'),
    path('matches/',       views.MatchListView.as_view(), name='matches'),

    # ── Submit animal (новое) ─────────────────────────────────────────
    path('animals/submit/', views.submit_animal,         name='animal_submit'),

    # ── Pets ──────────────────────────────────────────────────────────
    path('pets/',          views.PetListCreateView.as_view(),  name='pet_list'),
    path('pets/<int:pk>/', views.PetDetailView.as_view(),      name='pet_detail'),

    # ── Admin ─────────────────────────────────────────────────────────
    path('admin/users/',   views.AdminUserListView.as_view(),   name='admin_users'),
    path('admin/animals/', views.AdminAnimalListView.as_view(), name='admin_animals'),
    path('admin/pets/',    views.AdminPetCreateView.as_view(),  name='admin_pets'),

    # ── Health Records ────────────────────────────────────────────────
    path('health-records/',          views.HealthRecordListCreateView.as_view(), name='health_list'),
    path('health-records/<int:pk>/', views.HealthRecordDetailView.as_view(),     name='health_detail'),

    # ── Reminders ─────────────────────────────────────────────────────
    path('reminders/',          views.ReminderListCreateView.as_view(), name='reminder_list'),
    path('reminders/<int:pk>/', views.ReminderDetailView.as_view(),     name='reminder_detail'),
]
