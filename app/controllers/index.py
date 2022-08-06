from flask import redirect, url_for
from flask import render_template as template

from flask_classful import FlaskView, route
from flask_login import current_user


class IndexView(FlaskView):
    route_base = "/"

    def index(self):
        if current_user.is_authenticated:
            return redirect(url_for("DashboardView:index"))
        else:
            return template("index/index.html.j2")

    @route("about")
    @route("about/")
    @route("o-kalkulacce")
    @route("o-kalkulacce/")
    def about(self):
        return template("index/index.html.j2")

    @route("kalkulacka")
    @route("kalkulacka/")
    def simple_calculator(self):
        return redirect(url_for("SimpleCalculatorView:index"))

    @route("kucharka")
    @route("kucharka/")
    def public_cookbook(self):
        return redirect(url_for("CookbookView:public_index"))

    @route("terms")
    def terms(self):
        return redirect(url_for("SupportView:terms"))

    @route("privacy")
    def privacy(self):
        return redirect(url_for("SupportView:privacy"))
