from app.auth import admin_required

from app.helpers.base_view import BaseView
from app.models import Recipe, User, DailyPlan, Ingredient, ImageFile, RequestLog


class AdminView(BaseView):
    decorators = [admin_required]
    template_folder = "admin"

    def index(self):
        from app.helpers.general import created_recently, created_at_date
        from datetime import datetime
        from datetime import timedelta

        self.days = 30

        self.share_recipe_toggles = created_recently(
            RequestLog.load_by_like(attribute="url", pattern="recipes/toggle_shared"),
            days=self.days,
        )

        return self.template()
