Stimulus.register("recipe-percentage", class extends Controller {
  static targets = [ "percentage", "percentageInput", "showPercentage"]
  static values = { percentage: Number }

  connect() {
    this.showRecipeControllerElement = document.querySelector('[data-controller="show-recipe"]')

  }

  set_percentage(event){
    event.preventDefault();

    var percentage = this.showRecipeControllerElement.dataset.showRecipePercentageValue;
    var old_percentage = percentage;

    if ("percentage" in event.target.dataset){
      percentage = event.target.dataset.percentage;
    } else {
      percentage = this.percentageInputTarget.value;
    }

    if (! (percentage > 0)){
      percentage = old_percentage;
    }

    this._set_percentage(percentage)
  }

  _set_percentage(percentage){
    this.percentageValue = percentage
    this.showRecipeControllerElement.dataset.showRecipePercentageValue = percentage;
  }

  percentageValueChanged(){
    this._show_percentage()
  }

  _show_percentage(){
    this.showPercentageTarget.innerHTML = this.percentageValue;
  }

  });