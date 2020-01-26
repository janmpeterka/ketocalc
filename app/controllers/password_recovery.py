from werkzeug import MultiDict

from flask import redirect, url_for, request, session, flash
from flask import render_template as template
from flask import current_app as application

from flask_classful import FlaskView, route
from flask_login import current_user

from app.auth.routes import generate_new_password_token

from app.controllers.forms.password_recovery import NewPasswordForm, GetNewPasswordForm
from app.helpers.mail import send_email
from app.models.users import User


class PasswordRecoveryView(FlaskView):
    def before_request(self, name):
        if current_user.is_authenticated:
            return redirect(url_for("IndexView:index"))

    def show(self):
        form_data = None
        if session.get("formdata") is not None:
            form_data = MultiDict(session.get("formdata"))
            session.pop("formdata")
        if form_data:
            form = GetNewPasswordForm(form_data)
            form.validate()
        else:
            form = GetNewPasswordForm()
        return template("auth/get_new_password.html.j2", form=form)

    def post(self):
        form = GetNewPasswordForm(request.form)
        if not form.validate_on_submit():
            session["formdata"] = request.form
            return redirect(url_for("PasswordRecoveryView:show"))

        user = User.load(form.username.data, load_type="username")
        if user is None:
            session["formdata"] = request.form
            # TODO: This does nothing - form is not saved
            form.username.errors = ["Uživatel s tímto emailem neexistuje"]
            # for now...
            flash("Uživatel s tímto emailem neexistuje", "error")
            return redirect(url_for("PasswordRecoveryView:show"))

        html_body = template(
            "auth/mails/_new_password_email.html.j2",
            token=generate_new_password_token(user),
        )
        send_email(
            subject="Nové heslo",
            sender="ketocalc.jmp@gmail.com",
            recipients=[user.username],
            text_body="",
            html_body=html_body,
        )

        flash("Nové heslo vám bylo zasláno do emailu", "success")
        return redirect(url_for("LoginView:show"))

    def show_token(self):
        token = request.args["token"]
        form_data = None
        if session.get("formdata") is not None:
            form_data = MultiDict(session.get("formdata"))
            session.pop("formdata")
        if form_data:
            form = NewPasswordForm(form_data)
            form.validate()
        else:
            form = NewPasswordForm()

        user = User.load(token, load_type="new_password_token")
        if user is None:
            flash("tento token již není platný", "error")
            return redirect(url_for("LoginView:show"))

        return template(
            "auth/new_password.html.j2", form=form, username=user.username, token=token
        )

    @route("/post_token", methods=["POST"])
    def post_token(self):
        token = request.args["token"]
        form = NewPasswordForm(request.form)
        user = User.load(token, load_type="new_password_token")

        print(user)
        if not form.validate_on_submit():
            session["formdata"] = request.form
            return redirect(url_for("PasswordRecoveryView:show_token", token=token))

        if user is None:
            flash("nemůžete změnit heslo", "error")
            print("nemůžete změnit heslo")
        else:
            user.set_password_hash(form.password.data.encode("utf-8"))
            user.password_version = application.config["PASSWORD_VERSION"]
            user.new_password_token = None
            user.edit()
            flash("heslo bylo změněno", "success")
            print("heslo bylo změněno")

        return redirect(url_for("LoginView:show"))