// Tema claro / oscuro de IASD Las Lomas.
// Se carga en el <head> (sin defer) para poner data-theme antes de pintar y evitar el destello.
// Si la persona no ha elegido, sigue el modo del teléfono/computadora; si elige con el botón, se recuerda.
(function () {
  var raiz = document.documentElement, CLAVE = 'tema';
  var mq = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;

  function guardado() {
    try { var t = localStorage.getItem(CLAVE); return t === 'dark' || t === 'light' ? t : null; } catch (e) { return null; }
  }
  function actual() { return guardado() || (mq && mq.matches ? 'dark' : 'light'); }
  function aplicar(t) {
    raiz.setAttribute('data-theme', t);
    var m = document.querySelector('meta[name="theme-color"]');
    if (m) m.setAttribute('content', t === 'dark' ? '#0F1213' : '#EDEAE3');
    var b = document.querySelector('.tema-btn');
    if (b) {
      var txt = t === 'dark' ? 'Cambiar a tema claro' : 'Cambiar a tema oscuro';
      b.setAttribute('aria-label', txt);
      b.title = txt;
    }
  }

  aplicar(actual());
  if (mq) {
    var alCambiar = function () { if (!guardado()) aplicar(actual()); };
    if (mq.addEventListener) mq.addEventListener('change', alCambiar); else if (mq.addListener) mq.addListener(alCambiar);
  }

  document.addEventListener('DOMContentLoaded', function () {
    var nav = document.querySelector('header .nav');
    if (!nav || nav.querySelector('.tema-btn')) return;
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'tema-btn';
    b.innerHTML =
      '<svg class="luna" viewBox="0 0 24 24" aria-hidden="true"><path d="M20.5 14.5A8.5 8.5 0 0 1 9.5 3.5a8.5 8.5 0 1 0 11 11z"/></svg>' +
      '<svg class="sol" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>';
    if (!nav.querySelector('nav')) b.style.marginLeft = 'auto';   // cabeceras sin menú (privacidad, solicitar)
    b.addEventListener('click', function () {
      var t = raiz.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      try { localStorage.setItem(CLAVE, t); } catch (e) {}
      aplicar(t);
    });
    nav.appendChild(b);
    aplicar(raiz.getAttribute('data-theme') || actual());

    // Marca la cabecera cuando el menú ☰ está visible, sin importar el corte de cada página.
    var toggle = nav.querySelector('.nav-toggle');
    if (toggle) {
      var marcar = function () { nav.classList.toggle('con-hamburguesa', getComputedStyle(toggle).display !== 'none'); };
      marcar();
      window.addEventListener('resize', marcar);
    }
  });
})();
