{% extends "base.tpl" %}
{% block title %}
    {{ texts.recipe_print_all }}
{% endblock %}

{% block style %}
    <style type="text/css" media="screen">
		.totals {
			background-color: var(--bgcolor-totals);
		}      

		@media print {
			body {
                -webkit-print-color-adjust: exact;
            }
			.totals {
				background-color: var(--bgcolor-totals);
			}
		}
    </style>
{% endblock %}

{% block script %}{% endblock %}

{% block content %}
    <div class="container">
        <div class="col-12 d-print-flex">
            {% for recipe in recipes: %}
                <h2>{{ recipe.name }}</h2>
                {% if recipe.size == "small" %}
                    <h5>{{ texts.meal_size_small }} ({{ recipe.diet.small_size }}%)</h5>
                {% elif recipe.size == "big" %}
                    <h5>{{ texts.meal_size_small }} ({{ recipe.diet.big_size }}%)</h5> 
                {% endif %}
                <table id="ingredients" class="table">
                    <tr>
                        <th><strong>{{ texts.title }}</strong></th>
                        <th><strong>{{ texts.protein_simple }}</strong></th>
                        <th><strong>{{ texts.fat_simple }}</strong></th>
                        <th><strong>{{ texts.sugar_simple }}</strong></th>
                        <th><strong>{{ texts.amount_simple }}</strong></th>
                        <th></th>
                    </tr>


                    {% for ingredient in recipe.ingredients: %}
                        <tr>
                            <td><strong>{{ ingredient.name }}</strong></td>
                            <td>{{ ingredient.protein|round(2,'common') }}</td>
                            <td>{{ ingredient.fat|round(2,'common') }}</td>
                            <td>{{ ingredient.sugar|round(2,'common') }}</td>
                            <td>{{ ingredient.amount|round(2,'common') }}</td>
                            <td></td>
                        </tr>
                    {% endfor %}

                    <tr class="totals">
                        <td><strong>{{ texts.total }}</strong></td>
                        <td>{{ recipe.show_totals.protein|round(2,'common') }}</td>
                        <td>{{ recipe.show_totals.fat|round(2,'common') }}</td>
                        <td>{{ recipe.show_totals.sugar|round(2,'common') }}</td>
                        <td>{{ recipe.show_totals.amount|round(2,'common') }}</td>
                        <td>{{ recipe.show_totals.ratio }} : 1</td>
                    </tr>

                </table>
            {% endfor %}
        </div>
    </div>
{% endblock %}

