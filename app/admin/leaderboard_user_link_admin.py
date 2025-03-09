from sqladmin import ModelView

from app.models import LeaderboardUserLink


class LeaderboardUserLinkAdmin(ModelView, model=LeaderboardUserLink): # type: ignore[call-arg]
    column_list = [LeaderboardUserLink.id, LeaderboardUserLink.user_id, LeaderboardUserLink.league, LeaderboardUserLink.xp, LeaderboardUserLink.created_at, LeaderboardUserLink.updated_at]
    column_searchable_list = [LeaderboardUserLink.league]
    column_sortable_list = [LeaderboardUserLink.id, LeaderboardUserLink.user_id, LeaderboardUserLink.league, LeaderboardUserLink.xp, LeaderboardUserLink.created_at, LeaderboardUserLink.updated_at]
    can_edit = False
