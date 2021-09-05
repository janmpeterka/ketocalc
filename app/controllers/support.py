import os

from flask import redirect, request, flash, url_for, send_file
from flask import render_template as template

from flask_classful import FlaskView, route
from flask_login import current_user, login_required

from app.handlers.mail import MailSender

from app.controllers.forms.feedback import FeedbackForm


class SupportView(FlaskView):
    @route("/google3748bc0390347e56.html")
    def googleVerification(self):
        return template("support/google3748bc0390347e56.html")

    @route("/feedback", methods=["GET", "POST"])
    @login_required
    def feedback(self):
        from werkzeug.datastructures import CombinedMultiDict

        form = FeedbackForm(CombinedMultiDict((request.files, request.form)))
        if request.method == "GET":
            return template("support/feedback.html.j2", form=form)
        elif request.method == "POST":
            if not form.validate_on_submit():
                return template("support/feedback.html.j2", form=form)

            attachments = [form.feedback_file.data] if form.feedback_file.data else []
            MailSender().send_email(
                subject="[ketocalc] [{}]".format(form.option.data),
                sender="ketocalc",
                recipient_mails=["ketocalc.jmp+feedback@gmail.com"],
                text_body="Message: {}\n Send by: {} [user: {}]".format(
                    form.message.data, form.email.data, current_user.username
                ),
                html_body=None,
                attachments=attachments,
            )

            flash("Vaše připomínka byla zaslána na vyšší místa.", "success")
            return redirect(url_for("DashboardView:index"))

    @route("changelog")
    @login_required
    def changelog(self):
        return template("support/changelog.html.j2")

    @route("help")
    def help(self):
        return template("support/help.html.j2")

    @route("download/<filename>/", methods=["GET"])
    def download(self, filename):
        PATH = os.path.dirname(os.path.realpath(__file__))
        FILES_PATH = os.path.join(PATH, "../public/files/")
        return send_file(
            os.path.join(FILES_PATH, filename), attachment_filename=filename,
        )

    @route("terms")
    def terms(self):
        return template("support/terms.html.j2")

    @route("privacy")
    def privacy(self):
        return template("support/privacy.html.j2")

    @route("unsupported_browser")
    def unsupported_browser(self):
        return template("support/unsupported_browser.html.j2")

    @route("facebook")
    def facebook_redirect(self):
        return redirect("https://www.facebook.com/ketokalkulacka")
