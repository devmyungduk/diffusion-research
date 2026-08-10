[홈](../../README.md) · [문서 지도](../../README.md)

# Flux 모델 가이드

> Flux 모델의 기초 개념부터 실전 구현까지. 아래 상세 가이드는 로컬에서 가장 널리 쓰이는 FLUX.1(dev/schnell) 파이프라인을 기준으로 합니다. 최신 라인업은 바로 아래 표를 참고하세요.

---

## 이 장에서 배우는 것

- 이 문서의 기준인 FLUX.1은 Transformer 계열 모델이며 CLIP-L과 T5를 함께 사용합니다. FLUX.1 dev는 guidance 조건을 사용하고, KSampler 기반 공식 기본 구성에서는 `cfg=1.0`으로 둡니다.
- 로컬 표준은 FLUX.1 dev/schnell이며, 최신 세대(FLUX.2/FLUX 3)는 아래 [Flux 모델 라인업](#flux-모델-라인업)을 참고하세요.
- Flux와 기존 SD 모델의 근본적 차이 (Transformer 아키텍처)
- FLUX.1 전용 파이프라인 구축법 (CLIP-L + T5, Load Diffusion Model)
- Flux Redux, ControlNet 등 제어 기법 활용

<div class="guide-meta" markdown>
**대상** Flux 모델을 본격적으로 활용하고 싶은 중급자 ~ 고급자 · **사전 이해** SD 기본 사용법 (Load Checkpoint, KSampler, VAE 개념) · **시간** 40분

**이럴 때 읽으세요** SD에서 Flux로 넘어가 파이프라인 차이를 이해할 때.
</div>

## Flux 모델 라인업

> 확인 시점 2026년 8월. Flux는 빠르게 갱신되므로, 현재 상태와 라이선스는 공식 [bfl.ai/models](https://bfl.ai/models)에서 재확인하세요.

Flux는 Black Forest Labs(BFL)가 만든 이미지 생성 모델 계열입니다. 세대별로 다음과 같이 나뉩니다.

| 세대 | 출시 | 상태(2026-08) | 로컬 사용 | 특징 |
|------|------|---------------|-----------|------|
| FLUX.1 | 2024-08 | 유지 | dev/schnell 공개 가중치 | 로컬 생성의 사실상 표준. 이 문서의 기준 |
| FLUX.2 | 2025-11 | 현행 주력 | dev/klein 공개 가중치 | 다중 참조(최대 ~10장), 4MP 출력, 향상된 텍스트 렌더링 |
| FLUX 3 | 2026-07 | 초기 접근(게이트) | 미정(dev 공개 예정) | 이미지·영상·오디오·로보틱스 통합 멀티모달 |

**FLUX.1 (2024)** — 최초 계열. `schnell`(빠름, Apache 2.0), `dev`(12B, 비상업 라이선스, 품질 중심), `pro`(독점 API)로 나뉩니다. 공개 가중치와 품질 대비 속도 덕분에 로컬 커뮤니티의 표준으로 자리 잡았습니다. 이 문서의 실습은 이 계열을 기준으로 합니다.

**FLUX.2 (2025-11)** — 현재 주력 세대. `pro`·`max`·`flex`·`dev`·`klein` 등으로 세분화됩니다(`klein`은 2026-01 추가). 하나의 캐릭터·제품을 여러 장에 걸쳐 일관되게 유지하는 다중 참조 조건화, 4메가픽셀 생성·편집, 개선된 텍스트 렌더링이 핵심 변화입니다. 로컬에는 공개 가중치인 `dev`와 온디바이스용 경량 `klein`이 적합합니다. `klein`의 4B 변형은 Apache 2.0으로 공개되어 상업적 이용에 제약이 적습니다.

**FLUX 3 (2026-07)** — 이미지·영상·오디오·로보틱스를 하나의 가중치로 다루는 멀티모달 모델입니다. 발표 시점 기준 초기 접근(게이트) 단계이며, 공개 가중치(dev)와 가격은 아직 확정 발표되지 않았습니다. 로컬 워크플로우에 바로 쓰기에는 이릅니다.

**이 문서를 읽는 법:** 아래 상세 내용은 FLUX.1 기준입니다. FLUX.2 dev는 Mistral 계열 텍스트 인코더와 전용 VAE·latent·scheduler 구성을 사용하므로 DualCLIPLoader 기반 FLUX.1 워크플로우와 호환되지 않습니다. FLUX.2와 FLUX 3의 정확한 노드 구성은 해당 세대의 공식 문서와 ComfyUI 예제를 확인하세요.

---

## 함께 볼 문서

- [FLUX.1 작업 선택과 Redux 실습](flux-practical.md) — 참조 이미지 작업의 목적을 구분하고 공식 Redux 예제를 재현합니다.
- [FluxGuidance 이해와 사용](fluxguidance-pipeline.md) — guidance 값을 직접 비교합니다.
- [FLUX.1 텍스트 인코더와 데이터 공간](text-encoders.md) — T5XXL·CLIP의 역할과 정밀도 선택
- [빠른 참조](quick-reference.md) — 파일 위치와 시작값만 모은 표입니다.

---

## 1부: 핵심 개념

> FLUX.1의 핵심 개념과 아키텍처 이해. 이후 세대에는 그대로 적용하지 않습니다.

### SDXL과 SD 1.5 비교

#### 핵심 차이점 비교

| 항목 | SD 1.5 | SDXL | Flux |
|:---:|:---:|:---:|:---:|
| **출시년도** | 2022 | 2023 | 2024 |
| **개발사** | Stability AI | Stability AI | Black Forest Labs |
| **Native Resolution** | 512×512 | 1024×1024 | 1024×1024 |
| **Parameters** | ~1B | ~3.5B | ~12B |
| **Architecture** | Latent Diffusion | Latent Diffusion | Rectified Flow |

#### 해상도 이해

| 모델 | 기본 해상도 | 특징 |
|------|-----------|------|
| SD 1.5 | 512×512 | 2022년 표준 (768px 이상 품질 저하) |
| SDXL | 1024×1024 | 2023년 업그레이드 (파라미터 3배) |
| Flux | 1024×1024 | 2024년 차세대, 새 아키텍처 |

!!! warning "SDXL은 SD 1.5의 업그레이드가 아닙니다"
    별개 모델이라 LoRA도, 권장 해상도도 서로 통하지 않습니다.

---

### Flux 모델 호환성

#### LoRA 호환성 매트릭스

| LoRA 종류 | SD 1.5 | SDXL | Flux | 상호 호환 |
|:---:|:---:|:---:|:---:|:---:|
| **SD 1.5 LoRA** | ✅ | ❌ | ❌ | ❌ |
| **SDXL LoRA** | ❌ | ✅ | ❌ | ❌ |
| **Flux LoRA** | ❌ | ❌ | ✅ | ❌ |

> **결론**: 각 모델 전용 LoRA 필요. Flux LoRA는 CivitAI/HuggingFace에서 수천 개 이용 가능

#### IPAdapter 상태

| IPAdapter 타입 | SD 1.5/SDXL | Flux | 성숙도 |
|:---:|:---:|:---:|:---:|
| **Standard IPAdapter** | ✅ 완벽 지원 | ❌ 불가능 | - |
| **Flux-specific** | ❌ | 실험적 | 초기 단계 |

**실전 팁:**

- Flux LoRA는 바로 쓸 수 있는 수준입니다.
- Flux IPAdapter는 아직 실험 단계라, 참조 이미지 작업에는 코어 기능인 Redux가 안전합니다.

---

### Flux Guidance 시스템

#### FluxGuidance의 역할

FLUX.1 dev는 프롬프트 조건과 함께 별도의 guidance 숫자를 받습니다. ComfyUI에서는 다음 두 경로 중 하나를 사용합니다.

| 경로 | 구성 | 사용할 때 |
|---|---|---|
| 분리형 | `CLIP Text Encode → FluxGuidance` | 프롬프트 입력과 guidance 값을 별도 노드에서 조절 |
| 통합형 | `CLIPTextEncodeFlux`의 guidance 입력 사용 | CLIP-L·T5 프롬프트와 guidance를 한 노드에서 입력 |

통합형 출력에는 guidance 값이 이미 포함됩니다. 같은 값을 넣기 위해 `FluxGuidance`를 다시 연결할 필요가 없습니다.

FLUX.1 dev 공식 예제와 내장 노드의 출발값은 `3.5`입니다. 이 값은 최적값이 아니므로 모델·프롬프트·Seed·Sampler를 고정하고 guidance만 바꿔 비교합니다. KSampler를 사용하는 공식 기본 구성에서는 `cfg=1.0`으로 고전 CFG 결합을 사용하지 않습니다.

FLUX.1 schnell은 dev와 같은 guidance 입력을 사용하지 않습니다. 편집·제어 변형과 이후 세대 모델은 해당 모델의 공식 워크플로우를 따릅니다.

[FluxGuidance 이해와 사용](fluxguidance-pipeline.md)에서 노드 입력, KSampler negative 연결, 값 비교, ControlNet 결합을 단계별로 확인할 수 있습니다.

---

## 참고 자료

### 공식 링크
- [Black Forest Labs](https://blackforestlabs.ai/)
- [Flux Models (HuggingFace)](https://huggingface.co/black-forest-labs)
- [ComfyUI Examples](https://comfyanonymous.github.io/ComfyUI_examples/flux/)

### 커뮤니티 자료
- [XLabs AI ControlNets](https://github.com/XLabs-AI/x-flux-comfyui)
- [CivitAI Flux Models](https://civitai.com/models?query=flux)
- [ComfyUI Manager](https://github.com/ltdrdata/ComfyUI-Manager)

---

## 라이선스

이 문서는 학습용입니다. 모델과 소프트웨어에는 각각 별도의 라이선스가 적용됩니다.

- Flux 모델: 세대·변형마다 라이선스가 다릅니다. 상업적 이용 전 각 모델 카드를 확인하세요.
- ComfyUI: GPL-3.0

질문과 오류 제보는 저장소 Issues를 이용해 주세요.

---

## 완료 기준

네 가지를 모두 만족했다면 이 장을 끝냈습니다.

- FLUX.1이 SD 계열과 무엇이 다른지(구조, 로더 구성, 텍스트 인코더) 설명할 수 있다.
- FLUX.1 dev의 guidance와 KSampler의 cfg를 구분할 수 있다.
- 쓰려는 Flux 세대에 맞는 로더 구성을 확인하고 파일을 배치했다.

## 문서 정보

- **다루는 모델 범위:** FLUX.1(dev/schnell) 실습 + FLUX.2/FLUX 3 라인업 개요
- **최신 확인:** 2026-08 (모델 상태는 [bfl.ai](https://bfl.ai/models)에서 재확인 권장)
- **세대 구분:** CLIP-L+T5·FluxGuidance 설명은 FLUX.1 범위이며 이후 세대에는 해당 공식 구성을 사용

## 다음 단계

- [FluxGuidance 이해와 사용](fluxguidance-pipeline.md) — 역할, 연결, 값 비교
- [Flux Quick Reference](quick-reference.md) — 바로 쓸 설정표
- [Flux 실전 구현](flux-practical.md) — 실제 파이프라인 구성
- [LoRA](../../03-advanced-techniques/lora/README.md) · [제어 기법](../../03-advanced-techniques/controlnet/controlnet-architecture.md) — 스타일·구도 제어

[홈](../../README.md)
