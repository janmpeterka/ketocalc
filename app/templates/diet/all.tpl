{% extends "base.tpl" %}
{% block title %}
    {{ texts.diet_all }}
{% endblock %}

{% block style %}
    <style type="text/css" media="screen">
    .inactive {
        background-color: var(--bgcolor_inactive);
        color: var(--color_inactive);
    }
    .inactive a{
        color: var(--color_inactive);
        
    }
    </style>
{% endblock %}

{% block script %}{% endblock %}

{% block content %}
    {% include('navbar.tpl') %}
    <div class="container">
        <div class="col-12">
            <table id="diets" class="table">
                <tr>
                    <th>{{ texts.title }}</th>
                    <th>{{ texts.protein_100 }}</th>
                    <th>{{ texts.fat_100 }}</th>
                    <th>{{ texts.sugar_100 }}</th>
                    <th>{{ texts.diet_active }}</th>
                    <th>{{ texts.diet_recipes_count }}</th>
                </tr>
                {% for diet in diets: %}
                    <tr class= {% if diet.active%} active {% else %} inactive {% endif %}>                        
                        <td><a href="/diet={{diet.id}}">{{ diet.name }}</a></td>
                        <td>{{ diet.protein }}</td>
                        <td>{{ diet.fat }}</td>
                        <td>{{ diet.sugar }}</td>
                        <td>
                            {% if diet.active %}
                                {{ texts.yes }}
                            {% else %}
                                {{ texts.no }}
                            {% endif %}
                        </td>
                        <td>{{ diet.recipes|length }}</td>
                    </tr>
                {% endfor %}
            </table>
            
            <a href="/newdiet" target="_blank"><button class="btn btn-secondary">{{ texts.diet_add }}</button></a>
        </div>    
    </div>
{% endblock %}
