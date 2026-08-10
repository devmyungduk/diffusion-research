[홈](../README.md) · [문서 지도](../README.md)

# 03. 심화 제어

> 프롬프트만으로는 화풍과 구도를 원하는 만큼 고정하기 어렵습니다. 이 장은 무엇을 어떤 수단으로 붙잡을지 고르는 기준을 다룹니다.

## 무엇을 고정하고 싶은가

목적에 따라 쓰는 수단이 다릅니다. 아래에서 먼저 고르세요.

| 고정하고 싶은 것 | 쓰는 수단 |
|---|---|
| 프롬프트 안 특정 단어의 강도 | [프롬프트 가중치](prompt-weighting.md) |
| 화풍, 특정 캐릭터 | [LoRA](lora/README.md) |
| 구도, 포즈, 윤곽선 | [ControlNet](controlnet/controlnet-architecture.md) |
| 참조 이미지의 분위기·구성 | [IPAdapter](controlnet/ipadapter.md) · [Flux Redux](controlnet/flux-redux.md) |
| 마스크 경계 | [Differential Diffusion](controlnet/differential-diffusion.md) |
| 생성 과정의 성향 | [Sampler 비교](samplers/sampler-comparison.md) |

이 수단들은 서로 배타적이지 않습니다. 한 워크플로우에 LoRA와 ControlNet을 함께 쓸 수 있습니다. 연결 순서 자체가 우선순위를 정하지는 않으며, 결과는 strength·guidance·적용 구간과 모델 호환성에 따라 달라집니다. 조합 규칙은 [ControlNet 아키텍처](controlnet/controlnet-architecture.md)의 Pipeline 연결과 조절 규칙에서 다룹니다.

## 프롬프트 가중치

### [프롬프트 가중치](prompt-weighting.md)
`(개념:1.5)` 문법으로 프롬프트 안 특정 단어의 비중만 조절합니다. 노드를 추가하지 않는 가장 가벼운 제어 수단입니다.
예상 시간 10분 · 난이도 기초

## LoRA

### [LoRA 기본 — 스타일 얹기](lora/README.md)
모델 전체를 재학습하지 않고 화풍·캐릭터만 얹는 경량 가중치입니다. 연결, 트리거 워드, 강도 조절을 다룹니다.
예상 시간 20분 · 난이도 기초~중급

### [LoRA 조합과 선택](lora/combining.md)
여러 LoRA를 겹칠 때의 체인 연결과 충돌, 고를 때 확인할 기준입니다.
예상 시간 15분 · 난이도 중급

## 제어 기법

하나의 연속 시리즈입니다. ControlNet 아키텍처부터 순서대로 읽고, 마지막 실전 워크플로우에서 조합합니다.

### [ControlNet 아키텍처](controlnet/controlnet-architecture.md)
구조를 제어하는 ControlNet의 작동 원리, 주요 파라미터, 전처리기 종류, 그리고 여러 제어 수단을 함께 쓸 때의 Pipeline 연결과 조절 규칙을 다룹니다.
예상 시간 20분 · 난이도 중급

### [ControlNet 연결과 조절](controlnet/controlnet-pipeline.md)
전처리 결과를 워크플로우에 연결하고 guidance와 strength의 균형을 잡습니다.
예상 시간 20분 · 난이도 중급

### [IPAdapter](controlnet/ipadapter.md)
참조 이미지 한 장으로 스타일과 구성을 옮깁니다. LoRA와의 차이, 파이프라인 위치, 모델 호환성을 정리합니다.

### [Flux Redux](controlnet/flux-redux.md)
참조 이미지를 조건으로 변형을 만듭니다. IPAdapter와 달리 CONDITIONING 라인에서 동작합니다.

### [Differential Diffusion](controlnet/differential-diffusion.md)
마스크의 회색조를 보간에 활용해 경계가 부드러운 Inpainting을 만듭니다.

### [Flux 모델 변형 비교](controlnet/flux-model-variants.md)
제어 워크플로우에서 쓰는 Flux 모델(Dev/Fill), 정밀도(FP16/FP8), 양자화(GGUF) 선택 기준입니다.

### [제어 기법 실전 워크플로우](controlnet/example-workflows.md)
앞의 기법들을 조합한 실제 구성 예시입니다. 순서대로 읽었다면 마지막에 봅니다.

## Sampler

### [Sampler 비교](samplers/sampler-comparison.md)
샘플러별 성향과 필요한 스텝 수의 차이를 비교합니다.
예상 시간 15분 · 난이도 중급

### [KSampler·KSamplerAdvanced·SamplerCustomAdvanced](samplers/ksampler-vs-advanced.md)
기본 노드, 구간 제어 노드, 구성 요소 조립 노드의 차이를 다룹니다.
예상 시간 10분 · 난이도 중급~고급

## 다음 단계

- [04. 워크플로우 예제](../04-workflows/README.md) — 조합된 완성 예제
- [05. 문제 해결](../05-troubleshooting/README.md) — 적용 후 결과가 어긋날 때
- [02. 모델 가이드](../02-models/README.md) — 모델 계열별 전제
