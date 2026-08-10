[홈](../README.md) · [문서 지도](../README.md)

# 02. 모델 가이드

> 모델 계열마다 파이프라인 구성과 권장 설정이 다릅니다. Flux와 SD·SDXL의 차이를 먼저 정리하고, 각 계열의 실전 설정으로 이어집니다.

## 어느 계열부터 볼까

| 지금 쓰는 모델 | 볼 문서 |
|---|---|
| SD 1.5 · SDXL | [SD·SDXL 가이드](#sdsdxl) |
| Flux | [Flux 가이드](#flux) |

아직 정하지 않았다면 아래 비교표부터 보세요.

## 두 계열의 차이

| 항목 | SD 1.5 · SDXL | Flux |
|---|---|---|
| 구조 | UNet 기반 | Transformer(DiT) 기반 |
| 모델 로딩 | `Load Checkpoint` 하나로 MODEL·CLIP·VAE | `Load Diffusion Model` + `Load VAE` + `Dual CLIP Loader`로 분리 |
| 텍스트 인코더 | CLIP (SDXL은 CLIP-L + CLIP-G) | CLIP-L + T5 |
| 프롬프트 조건 조절 | KSampler의 `cfg` | FLUX.1 dev는 guidance 조건 사용, KSampler 공식 기본 구성은 `cfg=1.0` |
| 기본 해상도 | 512 (SD 1.5) / 1024 (SDXL) | 1024 |
| 요구 사양 | 낮음 | 높음 (파일이 여러 개, 용량 큼) |

처음이라면 SD 1.5나 SDXL로 흐름을 익힌 뒤 Flux로 넘어가는 편이 안전합니다. Flux는 로더 구성이 달라 [빠른 시작](../00-getting-started/quick-start.md)의 7노드 구조를 그대로 쓸 수 없습니다.

## Flux

### [Flux 모델 가이드](flux/README.md)
FLUX.1의 Transformer 구조, CLIP-L+T5, FluxGuidance와 세대별 모델 라인업을 다룹니다.
예상 시간 40분 · 난이도 중급

### [FLUX.1 텍스트 인코더와 데이터 공간](flux/text-encoders.md)
T5XXL과 CLIP의 역할, 정밀도 선택, 텍스트 조건과 Latent 공간의 차이를 다룹니다.
예상 시간 15분 · 난이도 중급

### [Flux Quick Reference](flux/quick-reference.md)
자주 찾는 설정값과 파일 배치를 한곳에 모은 참조표입니다.

### [FLUX.1 작업 선택과 Redux 실습](flux/flux-practical.md)
Redux·ControlNet·Kontext의 목적을 구분하고 공식 Redux 예제를 재현합니다.

### [FluxGuidance 이해와 사용](flux/fluxguidance-pipeline.md)
노드의 역할, 두 가지 입력 경로, KSampler cfg와의 차이부터 고정 Seed 비교와 ControlNet 확장까지 순서대로 다룹니다.
예상 시간 15분 · 난이도 기초~중급

## SD·SDXL

### [SD 1.5 / SDXL 모델 가이드](sd-sdxl/README.md)
두 세대의 차이와 모델 선택 기준을 정리합니다.
예상 시간 10분 · 난이도 기초

### [SDXL 해상도 최적화](sd-sdxl/resolution-optimization.md)
SDXL이 학습한 해상도와 권장 조합, 벗어났을 때 생기는 문제를 다룹니다.
예상 시간 10분 · 난이도 기초~중급

## 다음 단계

- [03. 심화 제어](../03-advanced-techniques/README.md) — 스타일·구도 제어
- [04. 워크플로우 예제](../04-workflows/README.md) — 바로 쓸 예제
- [05. 문제 해결](../05-troubleshooting/README.md) — 모델 로딩 실패 진단
