import datetime

from flask import redirect, url_for, request, jsonify
from flask_classful import route
from flask_login import current_user, login_required

from app.helpers.formaters import parse_date

from app.models.daily_plans import DailyPlan
from app.models.daily_plan_has_recipes import DailyPlanHasRecipes
from app.models.diets import Diet
from app.models.recipes import Recipe

from app.controllers.extended_flask_view import ExtendedFlaskView


class DailyPlansView(ExtendedFlaskView):
    decorators = [login_required]

    def index(self):
        return redirect(url_for("DailyPlansView:show", date=datetime.date.today()))

    def show(self, date):
        date = parse_date(date)
        date_before = date + datetime.timedelta(days=-1)
        date_after = date + datetime.timedelta(days=1)
        self.dates = {"active": date, "previous": date_before, "next": date_after}

        self.daily_plan = DailyPlan.load_by_date(date)
        if self.daily_plan is None:
            self.daily_plan = DailyPlan(date=date, author=current_user)
            self.daily_plan.save()

        self.daily_recipes = self.daily_plan.has_recipes

        return self.template(diets=current_user.active_diets)

    @route("/add_recipe", methods=["POST"])
    def add_recipe_AJAX(self,):
        recipe_id = request.form["recipe_id"]
        recipe = Recipe.load(recipe_id)

        date = request.form["date"]

        daily_plan = DailyPlan.load_by_date(date)

        dphr = DailyPlanHasRecipes()
        dphr.recipes_id = recipe.id
        dphr.daily_plans_id = daily_plan.id
        dphr.amount = request.form["amount"]
        dphr.save()

        return redirect(url_for("DailyPlansView:show", date=date))

    @route("/load_recipes_AJAX", methods=["POST"])
    def load_recipes_AJAX(self):
        diet_id = request.json["diet_id"]
        recipes = Diet.load(diet_id).recipes

        json_recipes = []
        for recipe in recipes:
            json_recipes.append(recipe.json)

        return jsonify(json_recipes)