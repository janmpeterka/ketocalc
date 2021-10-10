Stimulus.register("show-recipe", class extends Controller {
  static targets = [ "ingredientTable", "totals"]
  static values = { dietRatio: Number, percentage: Number }

  connect() {}

  percentageValueChanged(){
    this.calculate_recipe()
  }

    calculate_recipe(){
      var percentage = this.percentageValue
      var coeficient = percentage / 100
      var selected_ingredients = this._get_currently_selected()

      var totals = {
        "sugar": 0,
        "protein": 0,
        "fat": 0,
        "calorie": 0,
        "amount": 0
      }

      for (let i = 0, ingredient; ingredient = selected_ingredients[i]; i++) {
          ingredient["amount"] = this._amount(ingredient["amount"]) * coeficient
          this._ingredient_to_row(ingredient, this.ingredientTableTarget);

          totals["sugar"] += ingredient["sugar"] * ingredient["amount"]
          totals["protein"] += ingredient["protein"] * ingredient["amount"]
          totals["fat"] += ingredient["fat"] * ingredient["amount"]
          totals["calorie"] += ingredient["calorie"] * ingredient["amount"]
          totals["amount"] += ingredient["amount"] * 100
      }

      totals["ratio"] = totals["fat"] / (totals["sugar"] + totals["protein"])

      this._set_totals(totals)
    }

    _float_to_fixed(data){
      return parseFloat(data).toFixed(2)
    }

    _amount(amount){
      return (amount / 100);
    }

    _get_currently_selected(){
      return this._get_ingredients_from_table(this.ingredientTableTarget)
    }

    _get_ingredients_from_table(table){
      var ingredients = [];

      for (let i = 1, row; row = table.rows[i]; i++) {
        if ("id" in row.dataset){
          let ingredient = this._row_to_ingredient(row)
          ingredients.push(ingredient);
        }

      }
      return ingredients;
    }

    _row_to_ingredient(row){
      var ingredient = {}
      ingredient['id'] = row.dataset.id
      ingredient['name'] = row.dataset.name
      ingredient['calorie'] = row.dataset.calorie
      ingredient['fat'] = row.dataset.fat
      ingredient['protein'] = row.dataset.protein
      ingredient['sugar'] = row.dataset.sugar
      ingredient['amount'] = row.dataset.amount

      return ingredient
    }

    _ingredient_to_row(ingredient, table){
      var fields = ["calorie", "protein", "fat", "sugar", "amount"]
      var row = table.querySelectorAll(`[data-id='` + ingredient.id + `']`)[0]

      for (let i = 0, field; field = fields[i]; i++) {
        row.querySelectorAll('[data-type='+ field + ']')[0].innerHTML = this._float_to_fixed(ingredient[field] * ingredient["amount"])
      }

      row.querySelectorAll(`[data-type='amount']`)[0].innerHTML = this._float_to_fixed(ingredient["amount"] * 100)
    }

    _set_totals(totals){
      var fields = ["calorie", "protein", "fat", "sugar", "amount"]

      for (let i = 0, field; field = fields[i]; i++) {
        this.totalsTarget.querySelector('[data-field=' + field + ']').innerHTML = this._float_to_fixed(totals[field])
      }

      if (this.dietRatioValue == this._float_to_fixed(totals["ratio"])){
        this.totalsTarget.querySelector('[data-field="ratio"]').innerHTML = "<em>" + this._float_to_fixed(totals["ratio"]) + " : 1 </em>"
      } else {
        this.totalsTarget.querySelector('[data-field="ratio"]').innerHTML = "<em>" + this._float_to_fixed(totals["ratio"]) + ' : 1 </em> <span data-toggle="tooltip" title="Pozor, recept má jiný poměr než dieta! ('+ this.dietRatioValue +')"><i class="fa fa-exclamation-circle color-red"></i></span>'
      }

    }

});
