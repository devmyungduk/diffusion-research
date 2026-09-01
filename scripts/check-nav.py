#!/usr/bin/env python3
"""네비게이션 감사기.

1. 루트 README에서 링크를 따라가 모든 문서에 도달 가능한지(고아 문서 탐지)
2. 각 문서 최상단에 브레드크럼 네비게이션 줄이 있는지
3. 학습 순서 문서와 섹션·nav 그룹 대표 문서에 '다음 단계' 전진 링크가 있는지

푸시 전에 실행한다:  python3 scripts/check-nav.py
문제가 있으면 종료 코드 1을 반환한다.
"""
from __future__ import annotations
import re, os, sys, glob, collections

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def rel(p):
    return os.path.relpath(p, ROOT)


def links_in(path):
    d = os.path.dirname(path)
    out = []
    for m in re.finditer(r"\]\(([^)]+)\)", open(path, encoding="utf-8").read()):
        link = m.group(1).split()[0]
        if link.startswith(("http", "mailto", "#")):
            continue
        p = link.split("#")[0]
        if not p:
            continue
        out.append(os.path.normpath(os.path.join(d, p)))
    return out


def main() -> int:
    all_md = {os.path.normpath(p) for p in
              glob.glob(os.path.join(ROOT, "docs", "**", "*.md"), recursive=True)}
    all_md.add(os.path.normpath(os.path.join(ROOT, "README.md")))

    start = os.path.normpath(os.path.join(ROOT, "README.md"))
    docs_home = os.path.normpath(os.path.join(ROOT, "docs", "README.md"))
    seen = {start}
    q = collections.deque([start])
    while q:
        cur = q.popleft()
        for t in links_in(cur):
            if t in all_md and t not in seen:
                seen.add(t)
                q.append(t)

    orphans = sorted(all_md - seen)
    print("== 도달성 ==")
    print(f"전체 {len(all_md)}개 중 도달 가능 {len(seen)}개")
    if orphans:
        print("고아 문서(루트에서 링크로 못 감):")
        for o in orphans:
            print("   " + rel(o))
    else:
        print("고아 문서 없음")

    print("\n== 브레드크럼(최상단 홈/지도 링크) ==")
    missing_nav = []
    for p in sorted(all_md):
        head = "\n".join(open(p, encoding="utf-8").read().splitlines()[:6])
        if "](../" not in head and "](./" not in head and p not in (start, docs_home):
            missing_nav.append(rel(p))
    if missing_nav:
        print("상단 네비 없음:")
        for m in missing_nav:
            print("   " + m)
    else:
        print("모든 문서 상단 네비 존재")

    print("\n== 전진 링크(다음 단계) ==")
    # 학습 순서 문서와 각 섹션·nav 그룹의 대표 문서.
    # 대표 문서에서 다음 단계가 끊기면 학습자가 그 지점에서 막힌다.
    seq = [
        "docs/00-getting-started/README.md",
        "docs/00-getting-started/installation.md",
        "docs/00-getting-started/quick-start.md",
        "docs/00-getting-started/workflow-basics.md",
        "docs/00-getting-started/first-workflow.md",
        "docs/01-core-concepts/README.md",
        "docs/02-models/README.md",
        "docs/02-models/flux/README.md",
        "docs/02-models/sd-sdxl/README.md",
        "docs/03-advanced-techniques/README.md",
        "docs/03-advanced-techniques/lora/README.md",
        "docs/03-advanced-techniques/controlnet/controlnet-architecture.md",
        "docs/03-advanced-techniques/samplers/sampler-comparison.md",
        "docs/04-workflows/README.md",
        "docs/05-troubleshooting/README.md",
    ]
    # 본문에 '다음'이 우연히 들어간 문서를 통과시키지 않도록 제목이나 굵은 라벨만 인정한다.
    next_re = re.compile(r"^\s*(#{2,4}\s*다음 단계|\*\*다음 단계)", re.M)
    missing = []
    for s in seq:
        p = os.path.join(ROOT, s)
        if not os.path.exists(p):
            missing.append(f"{s} (파일 없음)")
            print(f"   없음 {s} (파일 없음)")
            continue
        ok = bool(next_re.search(open(p, encoding="utf-8").read()))
        if not ok:
            missing.append(s)
        print(f"   {'OK ' if ok else '없음'} {s}")
    if missing:
        print("   전진 링크 없는 문서:")
        for m in missing:
            print("      " + m)

    problems = len(orphans) + len(missing_nav) + len(missing)
    if problems:
        print(f"\n네비게이션 검사 실패: 문제 {problems}건")
        return 1
    print("\n네비게이션 검사 통과: 고아 문서·브레드크럼·전진 링크 이상 없음")
    return 0


if __name__ == "__main__":
    sys.exit(main())
