#!/usr/bin/env python3
"""헤더의 선두 이모지·기호를 제거하고, 그로 인해 바뀌는 자기문서 앵커 링크를
자동으로 갱신한다. 앵커가 깨지지 않도록 old->new 매핑을 만들어 본문 링크를 치환한다.

사용:
  python3 scripts/tidy_headers.py --dry-run <file...>   # 미리보기
  python3 scripts/tidy_headers.py --write   <file...>   # 실제 수정
"""
from __future__ import annotations
import re, sys, unicodedata


def is_symbol_or_emoji(ch: str) -> bool:
    if ch in "🏠📚📑🎯📊💡🔍🔄✋✅🚨🎨🍕⚡🔒😰😱🎉🧙🎩✨🤖🏗️🐌💥🛠️📈🎭🔌📁🔥⚠️➡️⬅️⬆️🌱🌿🌳📝📖🔗ℹ️🎓🎬🔤💬📥🍎❤️":
        return True
    cat = unicodedata.category(ch)
    return cat.startswith("So") or cat.startswith("Sk")


def strip_leading_symbols(text: str) -> str:
    i = 0
    while i < len(text) and (is_symbol_or_emoji(text[i]) or text[i] in " \t\ufe0f"):
        i += 1
    return text[i:].strip()


def gh_anchor(heading: str) -> str:
    h = heading.strip().lower().replace("*", "").replace("`", "")
    kept = [ch for ch in h if ch.isalnum() or ch in "-_ "]
    return re.sub(r"\s", "-", "".join(kept))


def process(path: str, write: bool) -> bool:
    src = open(path, encoding="utf-8").read()
    lines = src.split("\n")
    rename = {}  # old_anchor -> new_anchor
    seen_old, seen_new = {}, {}

    def dedupe(anchor, seen):
        n = seen.get(anchor, 0)
        seen[anchor] = n + 1
        return anchor if n == 0 else f"{anchor}-{n}"

    out = []
    changed_headers = 0
    for ln in lines:
        m = re.match(r"^(#{1,6})\s+(.*)$", ln)
        if not m:
            out.append(ln)
            continue
        hashes, text = m.group(1), m.group(2)
        old_anchor = dedupe(gh_anchor(text), seen_old)
        new_text = strip_leading_symbols(text)
        if new_text != text:
            changed_headers += 1
        new_anchor = dedupe(gh_anchor(new_text), seen_new)
        if old_anchor != new_anchor:
            rename[old_anchor] = new_anchor
        out.append(f"{hashes} {new_text}")

    body = "\n".join(out)

    def repl(m):
        pre, anc = m.group(1), m.group(2)
        return f"{pre}#{rename.get(anc, anc)})"

    # only self-file anchors (link starts with #)
    body2 = re.sub(r"(\]\()#([^)]+)\)", repl, body)

    if body2 == src:
        print(f"  변경 없음: {path}")
        return False
    print(f"  {path}: 헤더 {changed_headers}개 정리, 앵커 링크 {len(rename)}종 갱신")
    if write:
        open(path, "w", encoding="utf-8").write(body2)
    else:
        # show a couple of sample renames
        for i, (o, n) in enumerate(list(rename.items())[:4]):
            print(f"      #{o}  ->  #{n}")
    return True


def main():
    args = sys.argv[1:]
    write = "--write" in args
    files = [a for a in args if not a.startswith("--")]
    if not files:
        print("파일을 지정하세요")
        return 1
    for f in files:
        process(f, write)
    return 0


if __name__ == "__main__":
    sys.exit(main())
