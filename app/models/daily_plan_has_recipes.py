import datetime
from app import db

from app.models.base_mixin import BaseMixin


class DailyPlanHasRecipes(db.Model, BaseMixin):
    __tablename__ = "daily_plan_has_recipes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipes_id = db.Column(db.ForeignKey("recipes.id"), nullable=False, index=True)
    daily_plans_id = db.Column(
        db.ForeignKey("daily_plans.id"), nullable=False, index=True
    )

    amount = db.Column(db.Float, nullable=False)
    added_at = db.Column(db.DateTime, nullable=True, default=datetime.datetime.now)

    daily_plan = db.relationship("DailyPlan")
    recipes = db.relationship("Recipe")
