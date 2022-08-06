import math
import types
from flask_login import current_user

from app import db
from app.models.base_mixin import BaseMixin


class DailyPlan(db.Model, BaseMixin):
    __tablename__ = "daily_plans"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)

    user_id = db.Column(db.ForeignKey(("users.id")), nullable=False, index=True)
    author = db.relationship("User", uselist=False, back_populates="daily_plans")

    daily_recipes = db.relationship("DailyPlanHasRecipes", back_populates="daily_plan")
    # recipes = db.relationship("Recipe", secondary="daily_plan_daily_recipes")

    @staticmethod
    def load_by_date(date):
        date_plan = DailyPlan.query.filter_by(
            date=date, user_id=current_user.id
        ).first()
        return date_plan

    @staticmethod
    def load_by_date_or_create(date):
        daily_plan = DailyPlan.load_by_date(date)
        if daily_plan is None:
            daily_plan = DailyPlan(date=date, author=current_user)
            daily_plan.save()

        return daily_plan

    @property
    def totals(self):
        totals = types.SimpleNamespace()

        metrics = ["calorie", "sugar", "fat", "protein"]
        for metric in metrics:
            setattr(totals, metric, 0)

        totals.amount = 0

        for daily_recipe in self.daily_recipes:
            recipe = daily_recipe.recipe
            recipe.amount = daily_recipe.amount

            for metric in metrics:
                value = getattr(totals, metric)
                recipe_value = getattr(recipe.values, metric)
                setattr(totals, metric, value + recipe_value)
            totals.amount += recipe.amount

        try:
            totals.ratio = (
                math.floor((totals.fat / (totals.protein + totals.sugar)) * 100) / 100
            )
        except ZeroDivisionError:
            totals.ratio = 0
        return totals

    @property
    def is_active(self):
        return len(self.daily_recipes) > 0
