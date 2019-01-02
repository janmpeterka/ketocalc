{% extends "base.tpl" %}
{% block title %}
    Nový recept
{% endblock %}

{% block style %}{% endblock %}

{% block script %}
	<script type="text/javascript">
            var prerecipe__ingredient_array = [];
            var recipe__ingredient_array = [];
            var recipe__ingredient_dietID = "";

            Array.prototype.empty = function(){
                this.length = 0
            }

            /// On ready - change visibility to default
            $(document).ready(function() {
                allIngredients = $(".prerecipe__add-ingredient__form__select").html();
                $(".recipe__right").hide();
                $(".recipe__wrong").hide();
                $(".recipe__loader").hide();
                // prerecipe__calc__form__empty();
                prerecipe__ingredient_array.empty();
                $('#prerecipe__add-ingredient__form__select').select2();
            });

            // ingredient select to default
            function prerecipe__addIngredient__form__select__renew(){
                $('.prerecipe__add-ingredient__form__select').empty();
                $('.prerecipe__add-ingredient__form__select').append(allIngredients);
            }

            // ingredient select to actual
            function prerecipe__addIngredient__form__select__refresh(){
                prerecipe__addIngredient__form__select__renew()

                for (var i = 0; i < prerecipe__ingredient_array.length; i++) {
                    $('.prerecipe__add-ingredient__form__select option[value="' + prerecipe__ingredient_array[i].id + '"]').remove(); // wip
                }
            }

            // add ingredient html to table of ingredients (prerecipe)
            function prerecipe__selectedIngredients__table__add(ingredient_data){
                $('.prerecipe__selected-ingredients__table').append(ingredient_data);
            }


            // add ingredient to recipe
            function recipe__right__form__addIngredient(ingredient){
                recipe__ingredient_array.push(ingredient)
            }

            // remove prerecipe__form ingredient
            function prerecipe__calc__form__ingredients__remove(id){
                for (let i = 0; i < prerecipe__ingredient_array.length; i++) {
                    if (prerecipe__ingredient_array[i].id == id){
                        prerecipe__ingredient_array.splice(i, 1);
                        break;
                    }
                }
            }

            // add prerecipe__form ingredient
            function prerecipe__calc__form__ingredients__add(ingredient){
                // if already at least one ingredient in array/table
                if (prerecipe__ingredient_array.length > 0) {
                    var hasMain = false;
                    for (let i = 0; i < prerecipe__ingredient_array.length; i++) {
                        if (prerecipe__ingredient_array[i]['main']){
                            hasMain = true;
                        }
                    }

                    if (! hasMain){
                        prerecipe__ingredient_array[0]['main'] = true;
                        setMainIngredient(prerecipe__ingredient_array[0]['id']);
                    }
                }

                prerecipe__ingredient_array.push({'id': ingredient.id, 'name': ingredient.name, 'fixed': false, 'main': false, 'amount': 0});
            }


            // visibility
            function recipe__loader__show(){
                $(".recipe__loader").show();
                $(".recipe__right").hide();
                $(".recipe__wrong").hide();
            }

            function recipe__wrong__show(){
                $(".recipe__loader").hide();
                $(".recipe__wrong").show();
                $(".recipe__right").hide();
            }

            function recipe__right__show(){
                $(".recipe__loader").hide();
                $(".recipe__wrong").hide();
                $(".recipe__right").show();
            }

            function recipe__hideAll(){
                $(".recipe__loader").hide();
                $(".recipe__wrong").hide();
                $(".recipe__right").hide();
            }

            // Save recipe AJAX
            $(document).on("submit", ".recipe__right__form", function(e){
                $.ajax({
                        type: 'POST',
                        url: '/saveRecipeAJAX',
                        data: JSON.stringify({
                            'ingredients' : recipe__ingredient_array,
                            'dietID' : recipe__ingredient_dietID,
                            'name' : $('[name="recipe__right__form__name-input"]').val(),
                            'size' : $('[name="recipe__right__form__size-select"]').val()
                        }),
                        contentType: 'application/json;charset=UTF-8',
                        success: function(response){
                            var pathname = window.location.pathname.split("/")[0];
                            window.location.replace(pathname + response);
                        },
                        error: function(error) {
                            // console.log(error);
                        }
                });
                e.preventDefault();
            });

            $(document).on("submit", ".prerecipe__calc__form", function(e) {

                    // check conditions - ingredients types count
                    main_count = 0;
                    fixed_count = 0;
                    variable_count = 0;
                    for (var i = 0; i < prerecipe__ingredient_array.length; i++) {
                        if (prerecipe__ingredient_array[i].fixed == true){
                            fixed_count++;
                        } else if (prerecipe__ingredient_array[i].main == true){
                            main_count++;
                        } else {
                            variable_count++;
                        }
                    }
                    // main to variable if necessary
                    if (variable_count == 2 && main_count == 1){
                        for (var i = 0; i < prerecipe__ingredient_array.length; i++) {
                            if (prerecipe__ingredient_array[i].main == true){
                                prerecipe__ingredient_array[i].main = false;
                                main_count--;
                                variable_count++;
                        }
                      }
                    }

                    //nefixních (počítaná + hlavní) > 4
                    if (variable_count + main_count > 4){
                        bootbox.alert("Příliš mnoho počítaných surovin - počítané suroviny musí být právě 3");
                        $(".recipe__loader").hide();

                        return false;
                    }
                    //počítaná > 3
                    if (variable_count > 3){
                        bootbox.alert("Příliš mnoho počítaných surovin - počítané suroviny musí být právě 3");
                        $(".recipe__loader").hide();
                        return false;
                    }
                    //málo počítaných surovin
                    if (variable_count + main_count < 3){
                        bootbox.alert("Příliš málo počítaných surovin - počítané suroviny musí být právě 3");
                        $(".recipe__loader").hide();
                        return false;
                    }

                    // values for fixed
                    for (var i = 0; i < prerecipe__ingredient_array.length; i++) {
                        if (prerecipe__ingredient_array[i].fixed) {
                            prerecipe__ingredient_array[i].amount = parseFloat(prompt("Množství suroviny " + prerecipe__ingredient_array[i].name + "v gramech :","").replace(",","."));
                        }
                    }

                    $.ajax({
                        type: 'POST',
                        url: '/calcRecipeAJAX',
                        data: JSON.stringify({
                            'ingredients' : prerecipe__ingredient_array,
                            'dietID' : $('.select-diet').val()
                        }),
                        contentType: 'application/json;charset=UTF-8',
                        success: function(response){
                            var ingredients = response.ingredients;
                            var template_data = response.template_data;
                            console.log(template_data);

                            if (response == "False"){
                                recipe__wrong__show();
                                return;
                            }
                            
                            // // empty recipe all
                            recipe__ingredient_array.empty();

                            // fill with html
                            $('#recipe__right').html(template_data);

                            var mySlider = $("#slider").slider();

                            // ingredients to inputs
                            for (let i = 0; i < ingredients.length; i++ ){
                                recipe__right__form__addIngredient(ingredients[i]);
                            }

                            // diet ID
                            recipe__ingredient_dietID = response.diet.id

                            // change visibility
                            recipe__right__show();

                        },
                        error: function(error) {
                            // console.log(error);
                        }
                    });
                    e.preventDefault();
                });

            /// Adding ingredient from select to list of selected ingredients
            $(document).on("submit", ".prerecipe__add-ingredient__form", function(e) {
                // Empty select
                if ($('[name="prerecipe__add-ingredient__form__select"]').val() == null){
                    return false;
                }
                else{
                    $.ajax({
                        type: 'POST',
                        url: '/addIngredientAJAX',
                        data: $(this).serialize(),
                        data: JSON.stringify({
                            'ingredient_id' : $('[name="prerecipe__add-ingredient__form__select"]').val()},
                            null, '\t'),
                        contentType: 'application/json;charset=UTF-8',
                        success: function(response) {
                            var ingredient = response['ingredient'];
                            var template_data = response['template_data'];

                            prerecipe__calc__form__ingredients__add(ingredient);
                            prerecipe__addIngredient__form__select__refresh();
                            
                            $('.prerecipe__selected-ingredients__table').append(template_data);
                            recipe__hideAll();
                        },
                        error: function(error) {
                            console.log(error);
                        }
                    });
                    e.preventDefault();
                }
            });


            /// Removing ingredient from list of selected ingredients
            $(function(){
                  $('.prerecipe__selected-ingredients__table').on('click','tr i.remove',function(e){
                     e.preventDefault();

                    // remove from list
                    prerecipe__calc__form__ingredients__remove($(this).parents('tr').attr('id_value'));

                    // remove table line
                    $(this).parents('tr').remove();

                    // Refresh selection
                    prerecipe__addIngredient__form__select__refresh();

                    // Hide recipe form (discard)
                    $(".recipe__right").hide();
                  });
            });

            /// Setting main ingredient
            $(function(){
                  $('.prerecipe__selected-ingredients__table').on('click','tr i.set_main',function(e){
                     e.preventDefault();

                    // set main
                    setMainIngredient($(this).parents('tr').attr('id_value'));
                  });
            });

            /// Setting fixed ingredients
            $(function(){
                  $('.prerecipe__selected-ingredients__table').on('click','tr i.set_fixed',function(e){
                     e.preventDefault();

                    // toggle fixes
                    toggleFixedIngredient($(this).parents('tr').attr('id_value'));
                  });
            });


            /// Running loader animation
            $(document).on("click", ".prerecipe__calc__form__submit", function() {
                recipe__loader__show();
            });


            /// Recalculating amounts
            $(document).on("slideStop", "#slider", function(e) {
                recipe__loader__show();

                $.ajax({
                        type: 'POST',
                        url: '/recalcRecipeAJAX',
                        data: JSON.stringify({
                            'dietID'       : recipe__ingredient_dietID,
                            'ingredients'  : prerecipe__ingredient_array,
                            'slider'       : $('#slider').val()},
                            null, '\t'), // wip not sure why
                        contentType: 'application/json;charset=UTF-8',

                        success: function(response) {

                            if (response == "False"){
                                recipe__wrong__show();
                                return;
                            }

                            // ingredients
                            for (var i = 0; i < response.ingredients.length; i++) {
                                $('#amount_'+response.ingredients[i].id).text(response.ingredients[i].amount+" g");
                                $('#calorie_'+response.ingredients[i].id).text(response.ingredients[i].calorie);
                                $('#fat_'+response.ingredients[i].id).text(response.ingredients[i].fat);
                                $('#protein_'+response.ingredients[i].id).text(response.ingredients[i].protein);
                                $('#sugar_'+response.ingredients[i].id).text(response.ingredients[i].sugar);
                            }
                            recipe__ingredient_array = response.ingredients

                            // new totals
                            $('#totalFat').text(response.totals.fat);
                            $('#totalSugar').text(response.totals.sugar);
                            $('#totalProtein').text(response.totals.protein);
                            $('#totalCalorie').text(response.totals.calorie);
                            $('#totalWeight').text(response.totals.amount);
                            $('#totalRatio').text(response.totals.ratio);
                            recipe__right__show();

                        },
                        error: function(error) {
                        }

                    });
                    e.preventDefault();
            });

            function setMainIngredient(id){
                for (var i = 0; i < prerecipe__ingredient_array.length; i++) {
                    if (prerecipe__ingredient_array[i].id == id) {
                        prerecipe__ingredient_array[i].main = true;
                        prerecipe__ingredient_array[i].fixed = false;
                    } else {
                        prerecipe__ingredient_array[i].main = false;
                    }
                }

                $('.prerecipe__selected-ingredients__table tr').removeClass('tr-mainIngredient');
                $('.prerecipe__selected-ingredients__table').find('tr[id_value = "' + id +'"] ').addClass('tr-mainIngredient')
                $('.prerecipe__selected-ingredients__table').find('tr[id_value = "' + id +'"] ').removeClass('tr-fixedIngredient')
            }

            function toggleFixedIngredient(id){
                for (var i = 0; i < prerecipe__ingredient_array.length; i++) {
                    if (prerecipe__ingredient_array[i].id == id) {
                        if (prerecipe__ingredient_array[i].fixed){
                            prerecipe__ingredient_array[i].fixed = false;
                            $('.prerecipe__selected-ingredients__table').find('tr[id_value = "' + id +'"] ').removeClass('tr-fixedIngredient');
                        } else {
                            prerecipe__ingredient_array[i].fixed = true;
                            prerecipe__ingredient_array[i].main = false;
                            $('.prerecipe__selected-ingredients__table').find('tr[id_value = "' + id +'"] ').addClass('tr-fixedIngredient');
                            $('.prerecipe__selected-ingredients__table').find('tr[id_value = "' + id +'"] ').removeClass('tr-mainIngredient');

                        }
                    }
                }
            }

            function trialSaveConfirm(){
                r = confirm("Pokud si chcete recept uložit, musíte se zaregistrovat")
                if (r == true){
                    var win = window.open('/register');
                }
                return;
            }
        </script>
{% endblock %}

{% block content %}
    {% if not trialrecipe %}
	   {% include('navbar.tpl') %}
    {% else %}
        {% include('navbar_login.tpl')%}
    {% endif %}
        <div class="container-fluid container__main">
            <div class="row">
                <div class="prerecipe col-lg-6 col-md-12">

                    <div class="prerecipe__add-ingredient col-12">
                        <form class="prerecipe__add-ingredient__form form-inline">
                            <select class="prerecipe__add-ingredient__form__select form-control"
                            name="prerecipe__add-ingredient__form__select" id="prerecipe__add-ingredient__form__select">
                            {% for ingredient in ingredients: %}
                                <option name='{{ingredient.name}}' value="{{ingredient.id}}">{{ingredient.name}}</option>
                            {% endfor %}
                            </select>
                            <input type="submit" class="btn btn-primary add-ingredient-btn" value="Přidat surovinu" />
                        </form>
                    </div>

                    <div class="prerecipe__selected-ingredients col-11">
                        <form class="form-group">
                            <table class="prerecipe__selected-ingredients__table table">
                                <tr>
                                    <th>Název</th>
                                    <th>Kalorie</th>
                                    <th>Bílk.</th>
                                    <th>Tuk</th>
                                    <th>Sach.</th>
                                    <th></th>
                                </tr>
                            </table>
                        </form>
                    </div>

                    <div class="prerecipe__calc col-12">
                        <form class="prerecipe__calc__form form-inline">
                            <label for="select-diet">Název diety</label>
                            <select name="select-diet" class="select-diet form-control">
                            {% for diet in diets: %}
                                <option value="{{diet.id}}">{{ diet.name }}</option>
                            {% endfor %}
                            </select>
                            <input type="submit" class=" prerecipe__calc__form__submit btn btn-primary" value="Spočítat množství!" />
                        </form>
                    </div>

                </div>

                <div class="recipe col-lg-6 col-md-12">

                    <div class="recipe__loader"></div>

                    <div class="recipe__wrong">
                        <span>Recept nelze vytvořit</span>
                    </div>

                    <div class="recipe__right" id="recipe__right">
                    </div>
                </div>
            </div>
        </div>
{% endblock %}
