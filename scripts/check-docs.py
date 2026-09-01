#!/usr/bin/env python3
"""문서 정합성 검사기.

검사 항목:
  1. 상대 경로 파일 링크가 실제 존재하는가
  2. 같은 문서 내 앵커(#...) 링크가 실제 헤더와 일치하는가
  3. 삭제된 구(舊) 파일명을 아직 참조하는가
  4. 이미지 대체 설명과 SVG 접근성 정보가 있는가
  5. SVG 연결선의 시작·끝과 데이터 타입 색상이 포트와 일치하는가

푸시 전에 실행한다:  python3 scripts/check-docs.py
문제가 있으면 종료 코드 1을 반환한다.
"""
from __future__ import annotations
import re, os, sys, glob
import xml.etree.ElementTree as ET

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 리팩토링으로 사라진 파일명. 다시 등장하면 잔재이므로 차단한다.
RETIRED = [
    "part-01-core-concepts.md",
    "part-02-workflow-practice.md",
    "part-03-advanced-features.md",
    "part-03-hands-on-practice.md",
    "00-getting-started/appendix.md",
    "EXPANSION_ROADMAP.md",
    "전체-문서-목차",  # 존재하지 않던 앵커
]

BASIC_WORKFLOW_CONNECTIONS = {
    ("checkpoint-model", "ksampler-model"),
    ("checkpoint-clip", "positive-clip"),
    ("checkpoint-clip", "negative-clip"),
    ("positive-conditioning", "ksampler-positive"),
    ("negative-conditioning", "ksampler-negative"),
    ("empty-latent", "ksampler-latent"),
    ("ksampler-latent-output", "vae-samples"),
    ("checkpoint-vae", "vae-vae"),
    ("vae-image", "save-images"),
}

COMFYUI_DARK_SLOT_COLORS = {
    "MODEL": "#B39DDB",
    "CLIP": "#FFD500",
    "CONDITIONING": "#FFA931",
    "LATENT": "#FF9CF9",
    "VAE": "#FF6E6E",
    "IMAGE": "#64B5F6",
}


def gh_anchor(heading: str) -> str:
    """GitHub 방식으로 헤더 텍스트를 앵커 slug로 변환.
    소문자화 → 문자/숫자/공백/하이픈/밑줄만 남김(이모지·기호 제거) → 공백을 하이픈으로.
    앞뒤 공백을 trim 하지 않는다(이모지 접두 헤더가 '-목차'가 되는 동작을 재현)."""
    h = heading.strip().lower().replace("*", "").replace("`", "")
    kept = []
    for ch in h:
        if ch.isalnum() or ch in "-_ ":
            kept.append(ch)
    return re.sub(r"\s", "-", "".join(kept))


r_heading = '^#{1,6}\\s+(.*)$'
r_custom = '\\{#([^}]+)\\}\\s*$'
r_idattr = 'id="([^"]+)"'


_ANCHOR_CACHE = {}


def anchors_of(path: str) -> set:
    # 문서 하나가 제공하는 앵커 집합.
    # 헤더에서 만들어지는 앵커, id 속성, 헤더 끝의 {#custom-id} 세 가지를 모은다.
    key = os.path.normpath(path)
    if key in _ANCHOR_CACHE:
        return _ANCHOR_CACHE[key]
    try:
        txt = open(key, encoding='utf-8').read()
    except OSError:
        _ANCHOR_CACHE[key] = set()
        return _ANCHOR_CACHE[key]
    found = set()
    for m in re.finditer(r_heading, txt, re.M):
        heading = m.group(1)
        custom = re.search(r_custom, heading)
        if custom:
            found.add(custom.group(1))
            heading = heading[:custom.start()]
        found.add(gh_anchor(heading))
    for m in re.finditer(r_idattr, txt):
        found.add(m.group(1))
    _ANCHOR_CACHE[key] = found
    return found


def md_files():
    files = glob.glob(os.path.join(ROOT, "docs", "**", "*.md"), recursive=True)
    root_readme = os.path.join(ROOT, "README.md")
    if os.path.exists(root_readme):
        files.append(root_readme)
    return files


def main() -> int:
    problems = []
    for f in md_files():
        rel = os.path.relpath(f, ROOT)
        txt = open(f, encoding="utf-8").read()
        anchors = anchors_of(f)
        d = os.path.dirname(f)
        for m in re.finditer(r"\]\(([^)]+)\)", txt):
            link = m.group(1).split()[0]
            if link.startswith(("http://", "https://", "mailto:")):
                continue
            path, _, anchor = link.partition("#")
            if path:
                target = os.path.normpath(os.path.join(d, path))
                if not os.path.exists(target):
                    problems.append(f"[깨진 링크] {rel} -> {link}")
                elif anchor and target.endswith('.md'):
                    tgt = anchors_of(target)
                    if gh_anchor(anchor) not in tgt and anchor not in tgt:
                        problems.append(f"[앵커 없음] {rel} -> {link}")
            elif anchor:
                # 자기 문서 앵커: 링크 앵커를 정규화해 헤더 앵커 집합과 대조
                if gh_anchor(anchor) not in anchors and anchor not in anchors:
                    problems.append(f"[앵커 없음] {rel} -> #{anchor}")
        for m in re.finditer(r'<img\s+[^>]*src=["\']([^"\']+)["\'][^>]*>', txt, re.I):
            src = m.group(1)
            if not src.startswith(("http://", "https://", "data:")):
                target = os.path.normpath(os.path.join(d, src))
                if not os.path.exists(target):
                    problems.append(f"[깨진 이미지] {rel} -> {src}")
            tag = m.group(0)
            if not re.search(r'alt=["\'][^"\']+["\']', tag, re.I):
                problems.append(f"[이미지 설명 없음] {rel} -> {src}")
        for m in re.finditer(r"!\[([^]]*)\]\(([^)]+)\)", txt):
            if not m.group(1).strip():
                problems.append(f"[이미지 설명 없음] {rel} -> {m.group(2)}")
        for retired in RETIRED:
            if retired in txt:
                problems.append(f"[삭제된 참조] {rel} -> {retired}")

    svg_files = glob.glob(os.path.join(ROOT, "docs", "assets", "images", "*.svg"))
    for svg_file in svg_files:
        rel = os.path.relpath(svg_file, ROOT)
        try:
            root = ET.parse(svg_file).getroot()
        except ET.ParseError as exc:
            problems.append(f"[SVG 문법 오류] {rel} -> {exc}")
            continue
        ns = {"svg": "http://www.w3.org/2000/svg"}
        if root.get("role") != "img":
            problems.append(f"[SVG 접근성 역할 없음] {rel}")
        for tag in ("title", "desc"):
            node = root.find(f"svg:{tag}", ns)
            if node is None or not "".join(node.itertext()).strip():
                problems.append(f"[SVG {tag} 없음] {rel}")

        circle_nodes = root.findall(".//svg:circle", ns)
        port_nodes = {
            node.get("id"): node
            for node in circle_nodes
            if node.get("id") and node.get("cx") and node.get("cy")
        }
        ports = {
            port_id: (float(node.get("cx")), float(node.get("cy")))
            for port_id, node in port_nodes.items()
        }

        for circle in circle_nodes:
            data_type = circle.get("data-type")
            if not data_type:
                continue
            expected_color = COMFYUI_DARK_SLOT_COLORS.get(data_type)
            if expected_color is None:
                problems.append(f"[SVG 알 수 없는 데이터 타입] {rel} -> {data_type}")
                continue
            if circle.get("fill", "").upper() != expected_color:
                label = circle.get("id") or "legend"
                problems.append(
                    f"[SVG 포트 색상 불일치] {rel} -> {label}: "
                    f"{circle.get('fill')} != {expected_color}"
                )

        connections = set()
        for path in root.findall(".//svg:path", ns):
            source, target = path.get("data-from"), path.get("data-to")
            if not source and not target:
                continue
            connections.add((source, target))
            if source not in ports or target not in ports:
                problems.append(f"[SVG 연결 포트 없음] {rel} -> {source} → {target}")
                continue
            coords = [float(n) for n in re.findall(r"-?\d+(?:\.\d+)?", path.get("d", ""))]
            if len(coords) < 4:
                problems.append(f"[SVG 연결 좌표 없음] {rel} -> {source} → {target}")
                continue
            if tuple(coords[:2]) != ports[source]:
                problems.append(f"[SVG 출발점 불일치] {rel} -> {source}")
            if tuple(coords[-2:]) != ports[target]:
                problems.append(f"[SVG 도착점 불일치] {rel} -> {target}")
            data_type = path.get("data-type")
            expected_color = COMFYUI_DARK_SLOT_COLORS.get(data_type)
            if expected_color is None:
                problems.append(
                    f"[SVG 연결 데이터 타입 오류] {rel} -> "
                    f"{source} → {target}: {data_type}"
                )
                continue
            if path.get("stroke", "").upper() != expected_color:
                problems.append(
                    f"[SVG 연결 색상 불일치] {rel} -> {source} → {target}: "
                    f"{path.get('stroke')} != {expected_color}"
                )
            for port_id in (source, target):
                port = port_nodes[port_id]
                if port.get("data-type") != data_type:
                    problems.append(
                        f"[SVG 포트 타입 불일치] {rel} -> {port_id}: "
                        f"{port.get('data-type')} != {data_type}"
                    )
                if port.get("fill", "").upper() != expected_color:
                    problems.append(
                        f"[SVG 연결-포트 색상 불일치] {rel} -> {port_id}: "
                        f"{port.get('fill')} != {expected_color}"
                    )

        if os.path.basename(svg_file) == "basic-workflow.svg":
            for element in root.findall(".//*[@data-to]", ns):
                if element.tag != f"{{{ns['svg']}}}path":
                    problems.append(
                        f"[ComfyUI 기본 도식 화살표 사용] {rel} -> "
                        f"{element.get('data-to')}"
                    )
            missing = BASIC_WORKFLOW_CONNECTIONS - connections
            extra = connections - BASIC_WORKFLOW_CONNECTIONS
            for source, target in sorted(missing):
                problems.append(f"[SVG 필수 연결 없음] {rel} -> {source} → {target}")
            for source, target in sorted(extra):
                problems.append(f"[SVG 정의 외 연결] {rel} -> {source} → {target}")

    if problems:
        print("문서 검사 실패:")
        for p in sorted(set(problems)):
            print("  " + p)
        return 1
    print("문서 검사 통과: 링크·앵커·이미지 설명·SVG 연결·공식 타입 색상 이상 없음")
    return 0


if __name__ == "__main__":
    sys.exit(main())
