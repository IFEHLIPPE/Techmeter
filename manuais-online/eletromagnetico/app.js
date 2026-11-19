// Busca no manual: mostra só as seções que contêm o termo e destaca as ocorrências.
(function () {
  var campo = document.getElementById('busca');
  if (!campo) return;
  var secoes = Array.prototype.slice.call(document.querySelectorAll('section.cap'));
  var indice = document.querySelector('.indice');
  var vazio = document.getElementById('busca-vazio');
  var originais = secoes.map(function (s) { return s.innerHTML; });
  var normal = function (t) { return t.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase(); };

  function destacar(no, termo) {
    var andar = document.createTreeWalker(no, NodeFilter.SHOW_TEXT, null);
    var textos = [], n;
    while ((n = andar.nextNode())) textos.push(n);
    textos.forEach(function (t) {
      var s = t.nodeValue, ns = normal(s), i = ns.indexOf(termo);
      if (i < 0 || !t.parentNode || t.parentNode.closest('script,style')) return;
      var frag = document.createDocumentFragment(), pos = 0;
      while (i >= 0) {
        frag.appendChild(document.createTextNode(s.slice(pos, i)));
        var m = document.createElement('mark'); m.textContent = s.slice(i, i + termo.length); frag.appendChild(m);
        pos = i + termo.length; i = ns.indexOf(termo, pos);
      }
      frag.appendChild(document.createTextNode(s.slice(pos)));
      t.parentNode.replaceChild(frag, t);
    });
  }

  var timer;
  campo.addEventListener('input', function () {
    clearTimeout(timer);
    timer = setTimeout(function () {
      var termo = normal(campo.value.trim());
      var achou = 0;
      secoes.forEach(function (s, k) {
        s.innerHTML = originais[k];
        if (!termo) { s.hidden = false; return; }
        var tem = normal(s.textContent).indexOf(termo) >= 0;
        s.hidden = !tem;
        if (tem) {
          achou++;
          s.querySelectorAll('details').forEach(function (d) { if (normal(d.textContent).indexOf(termo) >= 0) d.open = true; });
          destacar(s, termo);
        }
      });
      if (indice) indice.hidden = !!termo;
      if (vazio) vazio.hidden = !termo || achou > 0;
    }, 180);
  });

  var btn = document.getElementById('ir-indice');
  if (btn) btn.addEventListener('click', function () {
    campo.value = ''; campo.dispatchEvent(new Event('input'));
    (indice || document.body).scrollIntoView();
  });
})();
