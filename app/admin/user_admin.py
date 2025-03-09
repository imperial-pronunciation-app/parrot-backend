from sqladmin import ModelView

from app.models import User


class UserAdmin(ModelView, model=User): # type: ignore[call-arg]
    column_list = [User.id, User.display_name, User.email, User.language, User.login_streak, User.last_login_date, User.xp_total, User.level, User.new_user, User.is_active, User.is_superuser, User.is_verified, User.created_at, User.leaderboard_entry]
    column_searchable_list = [User.display_name, User.email]
    column_sortable_list = [User.id, User.display_name, User.email, User.login_streak, User.last_login_date, User.xp_total, User.level, User.new_user, User.is_active, User.is_superuser, User.is_verified, User.created_at]
