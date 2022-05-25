from wtforms import StringField, SubmitField
from wtforms import validators

from flask_wtf import FlaskForm

from app.controllers.forms.custom import ComaFloatField


class DietForm(FlaskForm):
    name = StringField(
        "Název diety", [validators.InputRequired("Název musí být vyplněn")]
    )
    calorie = ComaFloatField(
        "Množství (kJ) kalorií / den",
        [validators.InputRequired("Množství musí být vyplněno")],
    )
    protein = ComaFloatField(
        "Množství (g) bílkovin / den",
        [validators.InputRequired("Množství musí být vyplněno")],
    )
    sugar = ComaFloatField(
        "Množství (g) sacharidů / den",
        [validators.InputRequired("Množství musí být vyplněno")],
    )
    fat = ComaFloatField(
        "Množství (g) tuku / den",
        [validators.InputRequired("Množství musí být vyplněno")],
    )
    submit = SubmitField("Přidat dietu")
