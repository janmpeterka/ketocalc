# from flask import redirect, url_for
from flask import render_template as template

from flask_classful import FlaskView

# from flask_login import current_user

from app.auth import admin_required


class MailsView(FlaskView):
    decorators = [admin_required]

    # def index(self):
    #     import glob
    #     import os
    #     from pathlib import Path

    #     path = os.getcwd() + "/app/templates/mails"

    #     files = glob.glob(path + "/**/*.html.j2", recursive=True)
    #     file_names = []

    #     for file in files:
    #         file_names.append(Path(file).name)

    #     return ",".join(file_names)

    def template(self, template_name, folder="onboarding"):
        return template("mails/{}/{}.html.j2".format(folder, template_name))