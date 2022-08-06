Stimulus.register("new-recipe", class extends Controller {
  static get targets() {
    return [
      "baseSelect",
      "presetIngredientIds",
      "select", "ingredientTable", "selectDiet",

      "loader", "wrongRecipe",

      "recipeName", "recipeDiet",
      "recipe", "recipeIngredientTable"
      ]
    }

      connect() {
        this.recipe__hideAll()
        this._load_preset_ingredients()
      }

      _load_preset_ingredients(){
        var ingredient_ids = this._string_to_list(this.presetIngredientIdsTarget.value)
        for (let i = 0, ingredient_id; ingredient_id = ingredient_ids[i]; i++) {
          this.add_ingredient_by_id(ingredient_id)
        }
      }

      _refresh_select(){
        this.selectTarget.innerHTML = this.baseSelectTarget.innerHTML;

        for (let i = 0, ingredient; ingredient = this._get_currently_selected()[i]; i++) {
          let option = this.selectTarget.querySelector("option[value='" + ingredient.id + "']");
          try {
            option.remove();
          } catch(err) {
            // console.log(err);
          }
        }
      }

      add_ingredient_by_id(ingredient_id){
          fetch("{{ url_for('RecipeCreatorView:addIngredientAJAX') }}",{
            method: 'POST',
            body: JSON.stringify({'ingredient_id' : ingredient_id}),
            headers: {'Content-Type': 'application/json,charset=UTF-8'}}
          ).then((response) => { return response.json(); }
          ).then((response) => {
            $(this.ingredientTableTarget).append(response['template_data']);
            this._set_main_ingredient_if_missing();
            this._refresh_select();
            this.recipe__hideAll();
          });
      }

      add_ingredient(e){
        e.preventDefault();

        if (this.selectTarget.value == false){return false;}
        else {this.add_ingredient_by_id(this.selectTarget.value);}
      }

      copy_ingredient(event){
        var old_ingredient_id = event.target.dataset.id

        // create copy of ingredient (AJAX), get back new id
        fetch("{{ url_for('IngredientView:duplicateAJAX') }}", {
          method: 'POST',
          body: JSON.stringify({
            'ingredient_id' : old_ingredient_id,
          }),
          headers: {'Content-Type': 'application/json,charset=UTF-8'},}
        ).then((response) => { return response.json(); }
        ).then((response) => {
          this.replace_ingredient_by_ids(old_ingredient_id, response['ingredient_id'])
          this._set_main_ingredient_if_missing();
          this._refresh_select();
          this.recipe__hideAll();
          });
      }

      replace_ingredient(event){
        // for non-IE, this could be used instead. TODO - find out how many use IE.
        // Also, then `replace_ingredient` and `replace_ingredient_from_form` may be possibly merged
        // var old_ingredient_id = event.target.closest("[data-id]").dataset.id
        var old_ingredient_id = event.target.parentNode.parentNode.dataset.id
        var new_ingredient_id = event.target.dataset.id

        this.replace_ingredient_by_ids(old_ingredient_id, new_ingredient_id)
      }


      replace_ingredient_from_form(event){
        event.preventDefault();

        // for non-IE, this could be used. TODO - find out how many use IE
        // var old_ingredient_id = event.target.closest("[data-id]").dataset.id
        var old_ingredient_id = event.target.parentNode.parentNode.parentNode.parentNode.dataset.id
        var new_ingredient_id = event.target.getElementsByTagName('select')[0].value

        this.replace_ingredient_by_ids(old_ingredient_id, new_ingredient_id)
      }

      replace_ingredient_by_ids(old_ingredient_id, new_ingredient_id){
        this.remove_ingredient_by_id(old_ingredient_id)
        this.add_ingredient_by_id(new_ingredient_id)
      }

      _set_main_ingredient_if_missing(){
        if (this._get_main_ingredient_from_table(this.ingredientTableTarget) != null){
          return true;
        }

        if (this._get_currently_selected().length < 1){
          return false;
        }
        else if (this._get_currently_selected().length == 1){
          this._set_main_ingredient(this._get_currently_selected()[0].id);
        }
        else {
          for (let i = 0, row; row = this.ingredientTableTarget.rows[i]; i++) {
            if (row.dataset.fixed != "true"){
              this._set_main_ingredient(row.dataset.id);
              return true;
            }
          }
          this._set_main_ingredient(this._get_currently_selected()[0].id);
          return true;
        }
      }

      set_main_ingredient(event){
        var id = event.target.dataset.id;
        this._set_main_ingredient(id);
      }
      
      _set_main_ingredient(id){
        for (let i = 0, row; row = this.ingredientTableTarget.rows[i]; i++) {
          row.removeAttribute("data-main");
        }

        var row = this._get_ingredient_row_by_id(id, this.ingredientTableTarget);
        row.dataset.main = "true";
        row.removeAttribute("data-fixed");
      }

      remove_ingredient(event){
        this.remove_ingredient_by_id(event.target.dataset.id)
      }

      remove_ingredient_by_id(ingredient_id){
        var rows = this._get_ingredient_rows_by_id(ingredient_id, this.ingredientTableTarget);
        for (let i = 0, row; row = rows[i]; i++) {
          row.remove();
        }

        this._refresh_select();
        this._set_main_ingredient_if_missing();
        this._hide_right();
        // $(".recipe__right").hide();
      }

      remove_duplicate_ingredient_by_id(ingredient_id){
        this.remove_ingredient_by_id(ingredient_id)
        this.add_ingredient_by_id(ingredient_id)
      }

      toggle_fixed_ingredient(event){
        var id = event.target.dataset.id;
        var row = this._get_ingredient_row_by_id(id, this.ingredientTableTarget);

        if (row.dataset.fixed != "true"){
            row.dataset.fixed = "true";
            row.removeAttribute("data-main");
        } else {
            row.removeAttribute("data-fixed");
        }

        this._set_main_ingredient_if_missing();
      }

      _get_ingredient_row_by_id(id, table){
        for (let i = 0, row; row = table.rows[i]; i++) {
          if (row.dataset.id == id){
            return row;
          }
        }
        // else
        return null;
      }

      _get_ingredient_rows_by_id(id, table){
        var rows = []
        for (let i = 0, row; row = table.rows[i]; i++) {
          if (row.dataset.id == id){
            rows.push(row);
          }
        }
        return rows;
      }

      _row_to_ingredient(row){
        var ingredient = {}
        ingredient['id'] = row.dataset.id
        ingredient['name'] = row.dataset.name

        // optional
        ingredient['main'] = row.dataset.main
        ingredient['fixed'] = row.dataset.fixed
        ingredient['unusable'] = row.dataset.unusable
        
        ingredient['amount'] = row.dataset.amount

        return ingredient
      }

      _get_currently_selected(){
        return this._get_ingredients_from_table(this.ingredientTableTarget)
      }

      _get_currently_calculated(){
        return this._get_ingredients_from_table(this.recipeIngredientTableTarget)
      }

      _get_ingredients_from_table(table){
        var ingredients = [];

        for (let i = 0, row; row = table.rows[i]; i++) {
          if ("id" in row.dataset && !("info" in row.dataset)){
            let ingredient = this._row_to_ingredient(row)
            ingredients.push(ingredient);
          }

        }
        return ingredients;
      }

      _get_main_ingredient(ingredients){
        for (let i = 0, ingredient; ingredient = ingredients[i]; i++) {
          if (ingredient.main){
            return ingredient;
          }
        }
        return null;  
      }

      _get_main_ingredient_from_table(table){
        if (table.rows.length == 0){
          return null;
        }
        for (let i = 0, row; row = table.rows[i]; i++) {
          if (row.dataset.main == "true"){
            return this._row_to_ingredient(row);
          }
        }
        return null;
      }

      calculate_recipe(e){
        e.preventDefault();

        this.recipe__loader__show()

        var selected_ingredients = this._get_currently_selected();

        var selected_ingredient_ids = []
        for (let i = 0, ingredient; ingredient = selected_ingredients[i]; i++) {
          selected_ingredient_ids.push(ingredient.id)
        }

        var unique_ingredient_ids = [...new Set(selected_ingredient_ids)];

        // Remove duplicate ingredients
        if (unique_ingredient_ids.length != selected_ingredient_ids.length){
          for (let i = 0, ingredient_id; ingredient_id = unique_ingredient_ids[i]; i++) {
            this.remove_duplicate_ingredient_by_id(ingredient_id)
          }

          bootbox.alert("Nějakou surovinu jste měli ve výběru vícekrát. Odebrali jsme ji. Zkontrolujte prosím správnost surovin")
          this._hide_loader()
          return false;
        }

        var unusable_count = selected_ingredients.filter((x) => x.unusable).length
        if (unusable_count > 0){
          bootbox.alert("Pokoušíte se o výpočet receptu s cizími surovinami.<br> Nejdříve je vyměňte za vlastní, nebo vytvořte jejich kopie.")
          this._hide_loader()
          return false;
        }
        var main_count = selected_ingredients.filter((x) => x.main).length
        var fixed_count = selected_ingredients.filter((x) => x.fixed).length
        var variable_count = selected_ingredients.length - (main_count + fixed_count)

        // main to variable if necessary
        if (variable_count == 2 && main_count == 1){
          var main_ingredient = this._get_main_ingredient(selected_ingredients)
          if (!(main_ingredient === null)){
            this._get_ingredient_row_by_id(main_ingredient.id, this.ingredientTableTarget).removeAttribute("data-main");
            main_count--;
            variable_count++;
          }
        }

        //nefixních (počítaná + hlavní) > 4
        if (variable_count + main_count > 4){
            bootbox.alert("Příliš mnoho počítaných surovin - počítané suroviny musí být právě 3");
            this._hide_loader();
            return false;
        }
        //málo počítaných surovin
        if (variable_count + main_count < 3){
            bootbox.alert("Příliš málo počítaných surovin - počítané suroviny musí být právě 3");
            this._hide_loader();
            return false;
        }

        // values for fixed
        selected_ingredients.forEach(function(ingredient, i){
          if (ingredient.fixed){
            ingredient.amount = parseFloat(prompt("Množství suroviny " + ingredient.name + " v gramech :","").replace(",","."));
          }
        })

        var dietID = this.selectDietTarget.value

        this._calculate_core(selected_ingredients, dietID)
      }

      recalculate_recipe(e){
        e.preventDefault();
        this.recipe__loader__show()

        var calculated_ingredients = this._get_currently_calculated()
        var main_ingredient = this._get_main_ingredient(calculated_ingredients)

        main_ingredient.amount = $("#slider").val();
        main_ingredient.fixed = true
        main_ingredient.min = $('#slider')[0].dataset.sliderMin;
        main_ingredient.max = $('#slider')[0].dataset.sliderMax;

        var dietID = this.recipeDietTarget.dataset.newRecipeDietId

        this._calculate_core(calculated_ingredients, dietID)
      }

      _calculate_core(ingredients, dietID){
        fetch("{{ url_for('RecipeCreatorView:calcRecipeAJAX') }}", {
          method: 'POST',
          body: JSON.stringify({
              'ingredients' : ingredients,
              'dietID' : dietID,
              'trial' : '{{ is_trialrecipe|safe }}'
          }),
          headers: {'Content-Type': 'application/json,charset=UTF-8'},
        })
        .then((response) => {
          if (response.status == 403) {
            return 403;
          } else if (response.status == 204){
            return 204
          }
          else if (!response.ok) {
            return null;
          }
          return response.json();
        })
        .then((response) => {
          if (response == 403) {
            this.recipe__wrong__show("Tuto surovinu nemůžete použít.");
            return;
          } else if(response == 204){
            this.recipe__wrong__show("Recept nelze vytvořit.");
            return;
          } else if (response == null){
            this.recipe__wrong__show("Někde se stala chyba!");
            return;
          }

          this.recipeTarget.innerHTML = response.template_data
          var mySlider = $("#slider").slider();

          this.recipe__right__show();
        })
      }

      save_recipe(e){
        e.preventDefault();

        fetch("{{ url_for('RecipeView:saveRecipeAJAX') }}", {
          method: 'POST',
          body: JSON.stringify({
            'ingredients' : this._get_currently_calculated(),
            'dietID' : this.recipeDietTarget.dataset.newRecipeDietId,
            'name' : this.recipeNameTarget.value,
          }),
          headers: {'Content-Type': 'application/json,charset=UTF-8'},
        })
        .then((response) => {
          return response.text(); })
        .then((response) => {
          var pathname = window.location.pathname.split("/")[0];
          window.location.replace(pathname + response);
        })
      }

      _hide_loader(){
        $(this.loaderTarget).hide();
      }

      _hide_right(){
        $(this.recipeTarget).hide();
      }

      recipe__loader__show(){
        $(this.loaderTarget).show();
        $(this.recipeTarget).hide();
        $(this.wrongRecipeTarget).hide();
      }

      recipe__wrong__show(message){
        $(this.recipeTarget).hide();
        this.wrongRecipeTarget.getElementsByTagName('span')[0].innerHTML = message;
        $(this.wrongRecipeTarget).show();
        $(this.loaderTarget).hide();
      }

      recipe__right__show(){
        $(this.recipeTarget).show();
        $(this.wrongRecipeTarget).hide();
        $(this.loaderTarget).hide();
      }

      recipe__hideAll(){
        $(this.recipeTarget).hide();
        $(this.wrongRecipeTarget).hide();
        $(this.loaderTarget).hide();
      }

      _string_to_list(string){
        return string.replace("[","").replace("]","").replace(/\s+/g, '').split(",")
      }
    });