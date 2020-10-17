import datetime

from flask import redirect, url_for, request, jsonify, abort
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
        if not isinstance(date, datetime.date):
            date = parse_date(date)

        date_before = date + datetime.timedelta(days=-1)
        date_after = date + datetime.timedelta(days=1)
        self.dates = {"active": date, "previous": date_before, "next": date_after}

        self.daily_plan = DailyPlan.load_by_date_or_create(date)
        self.daily_recipes = self.daily_plan.daily_recipes

        return self.template(diets=current_user.active_diets)

    def remove_daily_recipe(self, id, date):
        daily_recipe = DailyPlanHasRecipes.load(id)
        if daily_recipe:
            daily_recipe.remove()
        return redirect(url_for("DailyPlansView:show", date=date))

    @route("/add_recipe", methods=["POST"])
    def add_recipe(self):
        recipe_id = request.form["recipe_id"]

        recipe = Recipe.load(recipe_id)
        if not recipe.can_current_user_add:
            abort(403)
        date = request.form["date"]

        recipe_percentage = float(request.form["recipe_percentage"])
        amount = round(recipe.totals.amount * (recipe_percentage / 100), 2)

        daily_plan = DailyPlan.load_by_date(date)

        # TODO this calls for renaming
        dphr = DailyPlanHasRecipes(
            recipes_id=recipe_id, daily_plans_id=daily_plan.id, amount=amount
        )
        dphr.save()

        return redirect(url_for("DailyPlansView:show", date=date))

    @route("/load_recipes_AJAX", methods=["POST"])
    def load_recipes_AJAX(self):
        diet_id = request.json["diet_id"]

        diet = Diet.load(diet_id)
        if not diet.is_author(current_user):
            abort(403)

        recipes = Diet.load(diet_id).recipes

        json_recipes = [recipe.json for recipe in recipes]

        return jsonify(json_recipes)
