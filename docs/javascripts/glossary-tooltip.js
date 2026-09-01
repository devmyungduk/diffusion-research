/* 용어 사전 툴팁.
 *
 * 말풍선을 body 에 붙은 고정 위치 요소 하나로 그린다.
 * 용어에 ::after 로 붙이면 표의 가로 스크롤 컨테이너
 * (.md-typeset__scrollwrap, overflow-x:auto)에 갇혀 잘린다.
 *
 * - title 을 data-tip 으로 옮긴다. 남겨 두면 브라우저 기본 툴팁까지 떠서
 *   설명 상자가 두 개로 보인다.
 * - 데스크톱은 마우스, 터치 기기는 탭으로 연다.
 * - 화면 밖으로 나가지 않게 좌우를 가두고, 위가 좁으면 아래로 뒤집는다.
 */
(function () {
  var GAP = 8;      // 용어와 말풍선 사이 간격(px)
  var EDGE = 8;     // 화면 가장자리 여백(px)
  var tip = null;
  var current = null;

  var TIP_ID = "glossary-tip";

  function ensureTip() {
    if (!tip) {
      tip = document.createElement("div");
      tip.className = "glossary-tip";
      tip.id = TIP_ID;
      tip.setAttribute("role", "tooltip");
      document.body.appendChild(tip);
    }
    return tip;
  }

  function prepare() {
    // 용어 사전 페이지에서는 표제어 바로 아래에 같은 정의가 이미 있다.
    // 말풍선까지 띄우면 같은 문장이 두 번 나오므로 title 만 지운다.
    var glossary = /\/GLOSSARY(\/|\.html)?$/i.test(location.pathname);
    document.querySelectorAll(".md-typeset abbr[title]").forEach(function (el) {
      if (glossary) {
        el.removeAttribute("title");
        return;
      }
      el.setAttribute("data-tip", el.getAttribute("title"));
      el.removeAttribute("title");
      el.setAttribute("tabindex", "0");
    });
  }

  function place(el) {
    if (current && current !== el) current.removeAttribute("aria-describedby");
    var t = ensureTip();
    t.textContent = el.getAttribute("data-tip");
    t.classList.add("glossary-tip--visible");

    var r = el.getBoundingClientRect();
    var w = t.offsetWidth;
    var h = t.offsetHeight;

    var left = r.left + r.width / 2 - w / 2;
    left = Math.max(EDGE, Math.min(left, window.innerWidth - w - EDGE));

    var top = r.top - h - GAP;
    if (top < EDGE) top = r.bottom + GAP;          // 위가 좁으면 아래로
    t.classList.toggle("glossary-tip--below", top > r.top);

    t.style.left = left + "px";
    t.style.top = top + "px";
    // title 을 지웠으므로 열린 동안 말풍선을 설명으로 연결한다.
    // 이것이 없으면 보조기술이 정의를 얻을 수단이 사라진다.
    el.setAttribute("aria-describedby", TIP_ID);
    current = el;
  }

  function hide() {
    if (tip) tip.classList.remove("glossary-tip--visible");
    if (current) {
      current.removeAttribute("data-tip-open");
      current.removeAttribute("aria-describedby");
    }
    current = null;
  }

  function target(e) {
    return e.target && e.target.closest
      ? e.target.closest(".md-typeset abbr[data-tip]")
      : null;
  }

  document.addEventListener("mouseover", function (e) {
    var el = target(e);
    if (el) place(el);
  });

  document.addEventListener("mouseout", function (e) {
    if (target(e) && !matchMedia("(hover: none)").matches) hide();
  });

  document.addEventListener("focusin", function (e) {
    var el = target(e);
    if (el) place(el);
  });

  document.addEventListener("focusout", hide);

  document.addEventListener("click", function (e) {
    var el = target(e);
    if (!el) { hide(); return; }
    e.preventDefault();
    if (current === el) { hide(); return; }
    el.setAttribute("data-tip-open", "");
    place(el);
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") hide();
  });

  // 스크롤·회전하면 위치가 어긋나므로 닫는다.
  window.addEventListener("scroll", hide, true);
  window.addEventListener("resize", hide);

  document.addEventListener("DOMContentLoaded", prepare);

  // navigation.instant 로 본문만 교체될 때도 다시 적용한다.
  // 말풍선을 body 에 붙이는 것도 DOM 변경이라 관찰자를 다시 부른다.
  // 한 프레임에 한 번만 돌려 연속 변경에서 문서 전체를 되풀이해
  // 훑지 않게 한다.
  var pending = false;
  function schedulePrepare() {
    if (pending) return;
    pending = true;
    requestAnimationFrame(function () {
      pending = false;
      prepare();
    });
  }

  new MutationObserver(schedulePrepare).observe(
    document.body || document.documentElement,
    { childList: true, subtree: true }
  );
})();
