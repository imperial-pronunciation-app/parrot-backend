from app.admin.analytics import EndpointAnalyticsAdmin
from app.admin.attempt_admin import AttemptAdmin
from app.admin.endpoint_analytics import AnalyticsDashboard
from app.admin.exercise_analytics import ExerciseAnalyticsDashboard
from app.admin.exercise_difficulty_analytics import ExerciseDifficultyDashboard
from app.admin.phoneme_difficulty_analytics import PhonemeDifficultyDashboard

from .leaderboard_user_link_admin import LeaderboardUserLinkAdmin
from .phoneme_admin import PhonemeAdmin
from .recording_admin import RecordingAdmin
from .user_admin import UserAdmin
from .word_admin import WordAdmin
from .word_of_day_admin import WordOfDayAdmin
from .word_phoneme_link_admin import WordPhonemeLinkAdmin


views = [
    AnalyticsDashboard,
    ExerciseAnalyticsDashboard,
    ExerciseDifficultyDashboard,
    PhonemeDifficultyDashboard,
    AttemptAdmin,
    LeaderboardUserLinkAdmin,
    PhonemeAdmin,
    RecordingAdmin,
    UserAdmin,
    WordAdmin,
    WordOfDayAdmin,
    WordPhonemeLinkAdmin,
    EndpointAnalyticsAdmin,
]
