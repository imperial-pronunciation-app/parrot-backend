from .analytics.analytics import EndpointAnalyticsAdmin
from .analytics.endpoint_analytics import AnalyticsDashboard
from .analytics.exercise_analytics import ExerciseAnalyticsDashboard
from .analytics.exercise_difficulty_analytics import ExerciseDifficultyDashboard
from .analytics.phoneme_difficulty_analytics import PhonemeDifficultyDashboard
from .attempt_admin import AttemptAdmin
from .basic_lesson_admin import BasicLessonAdmin
from .exercise_admin import ExerciseAdmin
from .exercise_attempt_admin import ExerciseAttemptAdmin
from .exercise_attempt_phoneme_link_admin import ExerciseAttemptPhonemeLinkAdmin
from .language_admin import LanguageAdmin
from .leaderboard_user_link_admin import LeaderboardUserLinkAdmin
from .lesson_admin import LessonAdmin
from .phoneme_admin import PhonemeAdmin
from .phoneme_respelling_admin import PhonemeRespellingAdmin
from .recap_lesson_admin import RecapLessonAdmin
from .recording_admin import RecordingAdmin
from .unit_admin import UnitAdmin
from .user_admin import UserAdmin
from .word_admin import WordAdmin
from .word_of_day_admin import WordOfDayAdmin
from .word_of_day_attempt_admin import WordOfDayAttemptAdmin
from .word_phoneme_link_admin import WordPhonemeLinkAdmin


_analytics_dashboards = [
    AnalyticsDashboard,
    ExerciseAnalyticsDashboard,
    ExerciseDifficultyDashboard,
    PhonemeDifficultyDashboard,
]


views = _analytics_dashboards + [
    AttemptAdmin,
    BasicLessonAdmin,
    ExerciseAdmin,
    ExerciseAttemptAdmin,
    ExerciseAttemptPhonemeLinkAdmin,
    LanguageAdmin,
    LeaderboardUserLinkAdmin,
    LessonAdmin,
    PhonemeAdmin,
    PhonemeRespellingAdmin,
    RecapLessonAdmin,
    RecordingAdmin,
    UnitAdmin,
    UserAdmin,
    WordAdmin,
    WordOfDayAdmin,
    WordOfDayAttemptAdmin,
    WordPhonemeLinkAdmin,
    EndpointAnalyticsAdmin,
]
