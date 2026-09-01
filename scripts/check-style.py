#!/usr/bin/env python3
"""문체·용어 검사기.

검사 항목:
  1. 이 학습서에서 쓰지 않기로 한 표현이 본문에 있는가
  2. 화면에 보이는 노드·위젯·기능 이름이 용어 사전에 등재돼 있는가

코드 블록과 인라인 코드는 검사하지 않는다. 노드 이름이나 설정값에는
금지 표현과 같은 글자가 들어갈 수 있기 때문이다.

푸시 전에 실행한다:  python3 scripts/check-style.py
문제가 있으면 종료 코드 1을 반환한다.
"""
from __future__ import annotations
import glob
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 쓰지 않기로 한 표현. 왼쪽은 분류, 가운데는 정규식, 오른쪽은 대신 쓸 방향.
BANNED = [
    ("번역투", r"확장자를 가집니다|변환해줍니다|되어집니다|에 대해|를 통해|을 통해|"
              r"것이 [^.]{0,20}의 장점입니다|해 줍니다|해줍니다",
     "'확장자는 ~입니다', '~로 바꿉니다', '~로'처럼 주어와 서술어를 맞춘다"),
    ("감탄", r"완료!|생성!|성공!|즐거운 |좋은 결과 되세요",
     "느낌표와 인사말을 빼고 사실만 적는다"),
    ("근거 없는 평가", r"뛰어납니다|유리합니다|안전합니다|이해하기 쉽|바로 보입니다|"
                 r"쉽습니다|편이 빠릅니다|편이 낫습니다|편이 안전|훨씬 좋",
     "평가를 빼고 관찰 가능한 사실이나 독자가 할 행동으로 적는다"),
    ("독자 달래기", r"겁먹지|어렵지 않습니다|걱정하지|없는 것이 정상",
     "문장을 삭제한다"),
    ("과장 라벨", r"가장 자주|가장 많이|가장 흔한|가장 큰 |핵심 중|반드시 알아야",
     "'~인 경우가 많습니다'처럼 범위를 좁히거나 근거를 붙인다"),
    ("과장 수량", r"키 하나로|클릭 한 번으로|하나만 알면|한 방에",
     "실제 동작만 적는다"),
    ("구어", r"통하지 않습니다|빽빽|끌려가지 않",
     "'적용되지 않습니다', '호환되지 않습니다'처럼 무엇이 안 되는지 적는다"),
    ("동행·유도", r"눌러 보세요|살펴봅시다|함께 살펴|먼저 이것부터|익힙니다|익히려면|익히세요|익혔습니다|익히기 위해|익힌 뒤",
     "독자가 무엇을 얻을지 선언하지 말고, 문서가 무엇을 다루는지 적는다"),
    ("모호", r"대부분입니다|대부분의 경우|대부분 [가-힣]+ 문제|대부분 여기서|"
            r"대부분 다른|대부분의 [가-힣]+는|보통은 그렇습니다",
     "조건을 밝히거나 문장을 삭제한다"),
    ("정도 강조", r"매우 |아주 |훨씬 |정말 |엄청",
     "정도를 나타내는 부사 대신 수치나 조건을 적는다"),
    ("구어 표현", r"지저분|헷갈립니다|괜찮습니다|어렵게 느껴지면|기억하면 (됩니다|충분)|"
                r"무난하다|무난합니다|잘 맞습니다|이점은 분명",
     "관찰 가능한 사실로 바꾸거나 문장을 삭제한다"),
    ("등호 정의", r"\*\*[^*]{2,40} = [^*]+\*\*",
     "'A는 B입니다'처럼 문장으로 적는다. 약자 풀이는 표를 쓴다"),
    ("근거 없는 우열", r"더 정확하게 반영|가장 빠른 확인|최고 품질|성능이 가장 좋|"
                   r"편이 정확합니다|편이 좋습니다",
     "무엇이 어떻게 다른지 관찰 가능한 형태로 적는다"),
    ("구질한 표현", r"으로 삼습니다|로 삼습니다|기준으로 삼으",
     "'~입니다'로 끝낸다"),
    ("비유어", r"비유하면|비유로 이해|\*\*비유:|GPS 내비게이션|요리 레시피|"
              r"자동차 엔진|종이 클립처럼|화가에게 지시|화가에 비유|가위로 자르|에어브러시",
     "비유를 빼고 실제 데이터 흐름이나 노드 이름으로 설명한다"),
]

# 화면에 보이는 이름. 문서에 등장하면 용어 사전에 표제어가 있어야 한다.
# 새 노드·기능을 문서에 넣을 때 여기에도 추가한다.
UI_TERMS = [
    "노드", "워크플로우", "캔버스", "위젯", "포트", "Queue Prompt", "Fit View", "미니맵",
    "Bypass", "Mute", "Reroute", "Note", "ComfyUI-Manager", "Run", "Cancel current run", "큐", "Batch Count", "Auto Queue", "Mask Editor", "Group", "Subgraph",
    "KSampler", "KSamplerAdvanced", "SamplerCustomAdvanced", "BasicGuider",
    "FluxGuidance", "StyleModelApply", "ModelSamplingFlux", "EmptySD3LatentImage",
    "CLIP Vision", "ControlNet", "IPAdapter", "Redux", "Differential Diffusion",
    "LoRA", "VAE", "Checkpoint", "Conditioning", "Latent", "Seed", "Steps",
    "control_after_generate", "strength_type", "sigma", "timestep", "seq_len",
    "GGUF", "safetensors", "전처리기", "양자화", "Trigger Word", "Refiner",
    "Inpainting", "Outpainting", "Upscale", "Batch Size", "OOM", "VRAM",
]

GLOSSARY = os.path.join(ROOT, "docs", "GLOSSARY.md")


def strip_code(text: str) -> list[tuple[int, str]]:
    """코드 블록과 인라인 코드를 지운 (행 번호, 본문) 목록을 만든다."""
    out = []
    fenced = False
    for i, line in enumerate(text.splitlines(), 1):
        if re.match(r"^\s*(```|~~~)", line):
            fenced = not fenced
            continue
        if fenced:
            continue
        out.append((i, re.sub(r"`[^`]*`", "", line)))
    return out


def md_files() -> list[str]:
    return sorted(glob.glob(os.path.join(ROOT, "docs", "**", "*.md"), recursive=True))


def check_banned() -> list[str]:
    problems = []
    for path in md_files():
        rel = os.path.relpath(path, ROOT)
        text = open(path, encoding="utf-8").read()
        for lineno, line in strip_code(text):
            for label, pattern, hint in BANNED:
                found = re.search(pattern, line)
                if found:
                    problems.append(
                        f"[{label}] {rel}:{lineno} «{found.group(0)}» -> {hint}")
    return problems


def check_terms() -> list[str]:
    if not os.path.exists(GLOSSARY):
        return ["[용어 사전 없음] docs/GLOSSARY.md"]
    heads = re.findall(r"(?m)^### (.+)$", open(GLOSSARY, encoding="utf-8").read())
    heads_lower = [h.strip().lower() for h in heads]

    texts = {}
    for path in md_files():
        if os.path.basename(path) == "GLOSSARY.md":
            continue
        texts[os.path.relpath(path, ROOT)] = open(path, encoding="utf-8").read()

    problems = []
    for term in UI_TERMS:
        used = [rel for rel, body in texts.items() if term in body]
        if not used:
            continue
        if any(term.lower() in head for head in heads_lower):
            continue
        problems.append(
            f"[용어 사전 미등재] {term} — {len(used)}개 문서에서 사용 (예: {used[0]})")
    return problems


def main() -> int:
    banned = check_banned()
    terms = check_terms()

    if banned:
        print("쓰지 않기로 한 표현:")
        for p in sorted(set(banned)):
            print("  " + p)
    if terms:
        print("용어 사전에 없는 이름:")
        for p in sorted(set(terms)):
            print("  " + p)

    if banned or terms:
        print(f"\n문체·용어 검사 실패: 표현 {len(banned)}건, 용어 {len(terms)}건")
        return 1
    print("문체·용어 검사 통과: 금지 표현 없음, 화면 이름 모두 등재됨")
    return 0


if __name__ == "__main__":
    sys.exit(main())
