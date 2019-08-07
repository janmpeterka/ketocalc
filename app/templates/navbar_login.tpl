<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <div class="container">
    <a class="navbar-brand" href="/">Ketogenní kalkulačka</a>

    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div id="navbarNav" class="collapse navbar-collapse">

      <ul class="navbar-nav">
          <li class="nav-item">
            <a class="nav-link" href="/login">Přihlásit se</a>
          </li>

          <li class="nav-item">
            <a class="nav-link" href="/register">Zaregistrovat se</a>
          </li>

          <li class="nav-item">
            <a class="nav-link" href="/trialnewrecipe">Ukázka</a>
          </li>

      </ul>
    </div>
  </div>
</nav>
{% include('_flashing.html.j2') %}
