#!/usr/bin/env python3
"""본문 산문에서 장식성 이모지만 제거한다.

보존 대상:
  - 코드블록(```) 내부 전체 (다이어그램·아스키아트)
  - 박스 그리기 문자와 방향 화살표(→ ← ↑ ↓ ↔ ↕ ▲ ▼ ●)
  - 의미를 담는 ✅ / ❌ 마커
  - 헤더 라인(별도 도구로 이미 처리)

사용:
  python3 scripts/tidy_body.py --dry-run <file...>
  python3 scripts/tidy_body.py --write   <file...>
"""
from __future__ import annotations
import re, sys

DECORATIVE = set("🎯📊💡🔍🔄✋🚨🎨🍕🔒😰😱🎉🧙🎩✨🤖🐌💥🛠📈🎭🔌📁🔥"
                 "🌱🌿🌳📝📖🔗🎓💬📥🍎❤🏠📚📑😅⚡➡⬅⬆🚀🏗⚙🔤📏🎬ℹ🙋🆚🧠🔧🎁🖼️🏆💾🖥️📱🎮💻📐📏✂🧩🗂️🔖")
KEEP = set("✅❌⭐→←↑↓↔↕▲▼●○◆◇■□")


def strip_line(line: str) -> str:
    m = re.match(r"^(\s*)(.*)$", line)
    indent, rest = m.group(1), m.group(2)
    out = []
    for ch in rest:
        if ch == "\ufe0f":  # variation selector
            continue
        if ch in KEEP:
            out.append(ch)
        elif ch in DECORATIVE:
            continue
        else:
            out.append(ch)
    s = "".join(out)
    s = re.sub(r"[ \t]{2,}", " ", s)          # 내부 다중 공백만 축소(들여쓰기 제외)
    s = re.sub(r"\[ +(?=[^\]\n]*\]\()", "[", s)  # 링크 라벨 앞 공백만 제거(체크박스 [ ] 보호)
    return (indent + s).rstrip()


def process(path: str, write: bool) -> None:
    lines = open(path, encoding="utf-8").read().split("\n")
    in_code = False
    changed = 0
    out = []
    for ln in lines:
        if ln.lstrip().startswith("```"):
            in_code = not in_code
            out.append(ln)
            continue
        if in_code or ln.startswith("#"):
            out.append(ln)
            continue
        new = strip_line(ln)
        if new != ln:
            changed += 1
        out.append(new)
    print(f"  {path}: 산문 {changed}줄 정리")
    if write:
        open(path, "w", encoding="utf-8").write("\n".join(out))


def main():
    args = sys.argv[1:]
    write = "--write" in args
    files = [a for a in args if not a.startswith("--")]
    for f in files:
        process(f, write)


if __name__ == "__main__":
    main()
