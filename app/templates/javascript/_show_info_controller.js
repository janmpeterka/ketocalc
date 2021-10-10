Stimulus.register("show-info", class extends Controller {
  static get targets() {
    return ["info", "icon"]
  }

  connect() {
    this.set_icon()
    this.hide_info()
  }

  show_info() {
    $(this.infoTarget).show()
  }

  hide_info() {
    $(this.infoTarget).hide()
  }

  set_icon() {
    this.iconTarget.dataset.action = "mouseover->show-info#show_info mouseout->show-info#hide_info"
    this.iconTarget.className = "help fa fa-info-circle"
  }

})