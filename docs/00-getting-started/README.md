[홈](../README.md) · [문서 지도](../README.md)

# 00. 시작하기

> ComfyUI로 Stable Diffusion과 Flux 이미지를 생성하는 입문 과정입니다. 코딩 경험이 없어도 됩니다. 디자이너·아티스트처럼 처음 접하는 분을 기준으로, 설치부터 첫 이미지 생성까지 순서대로 안내합니다.

## 이 폴더의 문서

설치 → 첫 이미지 → 노드 이해 → 프롬프트 이해 → 직접 제작 → 저장·재현 순서이며, 전체 약 120분입니다.

### 0. [ComfyUI 설치](installation.md)
ComfyUI를 컴퓨터에 설치합니다. 터미널을 쓰지 않는 데스크톱 앱을 기준으로, 방법 선택과 모델 파일 배치까지 다룹니다.
예상 시간 15분 · 난이도 입문

### 1. [5분 빠른 시작](quick-start.md)
노드 7개를 연결해 첫 이미지를 만듭니다. 원리 설명은 최소화하고 "일단 되게 하는 것"에 집중합니다.
예상 시간 5분 · 난이도 입문

### 2. [워크플로우 이해하기](workflow-basics.md)
빠른 시작에서 연결한 각 노드가 무슨 일을 하는지 이해합니다. 전체 흐름도와 노드별 역할, KSampler 설정값의 의미를 다룹니다.
예상 시간 30분 · 난이도 기초

### 3. [프롬프트와 CLIP 이해하기](prompt-basics.md)
사람이 쓴 문장이 조건으로 바뀌어 KSampler에 전달되는 과정을 이해합니다. Positive·Negative 구분과 프롬프트 작성 구조를 다룹니다.
예상 시간 20분 · 난이도 기초

### 4. [첫 워크플로우 직접 만들기](first-workflow.md)
연결도를 덮어두고 스스로 구성합니다. 막힌 지점을 진단하는 순서와 목표에 맞는 변수를 고르는 기준을 다룹니다.
예상 시간 30분 · 난이도 기초~중급

### 5. [워크플로우 저장과 재현](save-and-reproduce.md)
만든 워크플로우를 저장하고 같은 결과를 다시 만드는 방법을 다룹니다.
예상 시간 20분 · 난이도 기초

## 핵심 개념 미리보기

빠른 시작에 바로 등장하는 세 가지 용어입니다. 자세한 원리는 [핵심 개념](../01-core-concepts/README.md)에서 다룹니다.

- **Latent** — AI는 원본 이미지를 직접 다루지 않고, 압축된 상태(Latent)에서 작업합니다. 그래서 빠릅니다.
- **VAE** — Latent와 이미지를 서로 변환합니다. 결과를 보려면 반드시 `VAE Decode`를 거쳐야 합니다. 노이즈나 검은 화면이 나온다면 대부분 VAE 문제입니다. 특별한 이유가 없다면 체크포인트가 내보낸 VAE를 그대로 씁니다.
- **Checkpoint** — 학습이 끝난 모델 파일(.safetensors)입니다. 내부에 UNet(생성), CLIP(텍스트 이해), VAE(압축)가 함께 들어 있습니다.

## 다음 단계

입문 과정을 마쳤다면 심화 문서로 이동하세요.

- [핵심 개념](../01-core-concepts/README.md) — Latent·VAE와 디노이징 원리
- [Flux 가이드](../02-models/flux/README.md) · [SD/SDXL 가이드](../02-models/sd-sdxl/README.md) — 모델별 사용법
- [LoRA](../03-advanced-techniques/lora/README.md) · [ControlNet](../03-advanced-techniques/controlnet/controlnet-architecture.md) — 스타일·구도 제어
- [문제 해결](../05-troubleshooting/README.md) — 오류와 비정상 결과 진단
- [용어 사전](../GLOSSARY.md) — 모르는 용어 확인
