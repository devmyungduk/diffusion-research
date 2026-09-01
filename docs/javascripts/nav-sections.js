/* 좌측 최상위 네비게이션에 섹션 이름을 표시한다.
 *
 * 색을 nth-child 순번으로 걸면 mkdocs.yml nav 에 최상위 항목을 하나 넣거나
 * 뺄 때마다 그 뒤 색이 한 칸씩 밀린다. 오류가 나지 않아 눈으로 볼 때까지
 * 모르고, 검사 스크립트도 잡지 못한다.
 *
 * 그래서 순번 대신 문서 폴더 이름을 쓴다. 각 최상위 항목의 첫 링크를 절대
 * 경로로 바꾸고, 항목들의 공통 접두(사이트 루트)를 뺀 첫 구간을
 * data-nav-section 으로 남긴다. CSS 는 순번이 아니라 그 이름으로 색을
 * 고르므로, 섹션을 더하거나 순서를 바꿔도 색이 어긋나지 않는다.
 *
 * href 를 CSS 선택자로 쓰지 못하는 이유는 MkDocs 가 페이지마다 다른 상대
 * 경로를 내보내기 때문이다(홈에서는 00-getting-started/, 그 섹션 안에서는
 * ../). JS 는 절대 경로로 바꿀 수 있어 이 제약을 받지 않는다.
 *
 * 이 스크립트가 돌지 않으면 색 구분만 빠지고 네비게이션은 그대로 동작한다.
 */
(function () {
  var ITEMS = ".md-nav--primary > .md-nav__list > .md-nav__item";

  // 항목 안에서 실제 문서를 가리키는 첫 링크의 절대 경로.
  // navigation.indexes 를 쓰면 현재 페이지의 목차(#...)가 이 목록 안에
  // 섞여 들어오므로 앵커만 있는 링크는 건너뛴다.
  function firstPath(item) {
    var links = item.querySelectorAll("a.md-nav__link[href]");
    for (var i = 0; i < links.length; i++) {
      var href = links[i].getAttribute("href");
      if (!href || href.charAt(0) === "#") continue;
      return new URL(href, location.href).pathname;
    }
    return null;
  }

  // 경로들의 공통 디렉터리. 사이트가 어느 하위 경로에 배포되든 루트를 찾는다.
  function commonDir(paths) {
    var parts = paths[0].split("/");
    var n = parts.length;
    for (var i = 1; i < paths.length; i++) {
      var other = paths[i].split("/");
      var k = 0;
      while (k < n && k < other.length && parts[k] === other[k]) k++;
      n = k;
    }
    return parts.slice(0, n).join("/") + "/";
  }

  function apply() {
    var items = document.querySelectorAll(ITEMS);
    var found = [];
    for (var i = 0; i < items.length; i++) {
      var path = firstPath(items[i]);
      if (path) found.push([items[i], path]);
    }
    // 항목이 하나뿐이면 공통 접두가 그 경로 전체가 되어 구간을 못 얻는다.
    if (found.length < 2) return;

    var base = commonDir(found.map(function (pair) { return pair[1]; }));
    found.forEach(function (pair) {
      var key = pair[1].slice(base.length).split("/")[0];
      // 루트를 가리키는 항목(문서 지도)은 구간이 비어 색을 주지 않는다.
      if (key) pair[0].setAttribute("data-nav-section", key);
      else pair[0].removeAttribute("data-nav-section");
    });
  }

  document.addEventListener("DOMContentLoaded", apply);

  // navigation.instant 로 화면이 교체될 때도 다시 적용한다.
  // 한 프레임에 한 번만 돌려 연속 변경에서 되풀이하지 않는다.
  // 속성만 바꾸므로 childList 관찰자가 다시 깨어나지는 않는다.
  var pending = false;
  new MutationObserver(function () {
    if (pending) return;
    pending = true;
    requestAnimationFrame(function () {
      pending = false;
      apply();
    });
  }).observe(document.body || document.documentElement, {
    childList: true,
    subtree: true
  });
})();
