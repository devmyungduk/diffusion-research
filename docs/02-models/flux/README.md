[문서 지도](../../README.md)

# Flux 모델 가이드

> SD 계열에서 Flux로 넘어갈 때 달라지는 것과, 세대별 모델을 고르는 기준을 정리합니다. 실습은 로컬 표준인 FLUX.1(dev/schnell)을 기준으로 합니다.

## 이 장에서 배우는 것

- SD 계열과 Flux가 구조·로더·조절값에서 무엇이 다른지
- FLUX.1 전용 파이프라인을 어떻게 구성하는지
- 세대(FLUX.1 / FLUX.2 / FLUX 3)를 어떻게 구분하고 무엇을 골라야 하는지

<div class="guide-meta" markdown>
**대상** SD를 사용해 봤고 Flux로 넘어가려는 사용자 · **사전 이해** Load Checkpoint, KSampler, VAE의 역할 · **시간** 30분

**이럴 때 읽으세요** SD에서 Flux로 넘어가 파이프라인 차이를 이해할 때.
</div>

## SD 계열과 무엇이 다른가

SD를 사용하던 방식이 그대로 통하지 않는 지점입니다.

| 항목 | SD 1.5 · SDXL | FLUX.1 |
|---|---|---|
| **모델 구조** | UNet | ==Transformer 계열== |
| **텍스트 인코더** | CLIP (SDXL은 CLIP-L + CLIP-G) | ==CLIP-L과 T5를 함께 사용== |
| **모델 로딩** | `Load Checkpoint` 하나 | ==`Load Diffusion Model` + `Dual CLIP Loader` + `Load VAE`로 분리== |
| **프롬프트 조건 조절** | KSampler의 `cfg` | ==`FluxGuidance`의 guidance. KSampler `cfg`는 `1.0`== |
| **기본 해상도** | 512 / 1024 | 1024 |

!!! warning "혼동하기 쉬운 지점"
    Flux에서 프롬프트 반영을 올리려고 KSampler의 `cfg`를 올리면 안 됩니다. FLUX.1 dev의 공식 기본 구성은 `cfg=1.0`이고, 조절하는 값은 `FluxGuidance`의 guidance(출발값 `3.5`)입니다. 자세한 내용은 [FluxGuidance 이해와 사용](fluxguidance-pipeline.md)에 있습니다.

로컬에서 사용하는 표준은 FLUX.1 dev/schnell입니다. 최신 세대는 아래 [Flux 모델 라인업](#flux-모델-라인업)을 참고하세요.

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

**FLUX 3 (2026-07)** — 이미지·영상·오디오·로보틱스를 하나의 가중치로 다루는 멀티모달 모델입니다. 발표 시점 기준 초기 접근(게이트) 단계이며, 공개 가중치(dev)와 가격은 아직 확정 발표되지 않았습니다. 로컬 워크플로우에 바로 사용하기에는 이릅니다.

**이 문서를 읽는 법:** 아래 상세 내용은 FLUX.1 기준입니다. FLUX.2 dev는 Mistral 계열 텍스트 인코더와 전용 VAE·latent·scheduler 구성을 사용하므로 DualCLIPLoader 기반 FLUX.1 워크플로우와 호환되지 않습니다. FLUX.2와 FLUX 3의 정확한 노드 구성은 해당 세대의 공식 문서와 ComfyUI 예제를 확인하세요.

## 모델 계열별 호환성

LoRA와 IPAdapter는 학습된 아키텍처에서만 동작합니다. 다른 계열의 파일을 가져와 사용할 수 없습니다.

| 종류 | SD 1.5 | SDXL | Flux |
|:---|:---:|:---:|:---:|
| **SD 1.5 LoRA** | 사용 가능 | 불가 | 불가 |
| **SDXL LoRA** | 불가 | 사용 가능 | 불가 |
| **Flux LoRA** | 불가 | 불가 | 사용 가능 |
| **표준 IPAdapter** | 사용 가능 | 사용 가능 | 불가 |

Flux LoRA는 CivitAI와 Hugging Face에서 받습니다. `Load LoRA`에 넣으면 바로 사용하고, 커스텀 노드는 필요 없습니다.

Flux용 IPAdapter는 준비할 것이 많습니다. 제공자마다 짝이 되는 이미지 인코더가 다르고, 전용 sampler를 요구하기도 합니다. 하나만 어긋나도 동작하지 않습니다. 참조 이미지를 사용할 일이 있다면 ComfyUI에 기본 포함된 [Flux Redux](../../03-advanced-techniques/controlnet/flux-redux.md)를 먼저 보세요.

!!! warning "SDXL은 SD 1.5의 업그레이드가 아닙니다"
    별개 모델이라 LoRA도, 권장 해상도도 서로 호환되지 않습니다.

---

## 함께 볼 문서

읽는 순서대로 정리했습니다.

1. [텍스트 인코더와 데이터 공간](text-encoders.md) — T5XXL·CLIP의 역할과 정밀도 선택
2. [FluxGuidance 이해와 사용](fluxguidance-pipeline.md) — guidance가 무엇을 조절하는가
3. [guidance 값 비교와 연결](guidance-tuning.md) — 값을 바꿔 비교하고 워크플로우에 연결
4. [작업 선택과 Redux 실습](flux-practical.md) — 참조 이미지로 변형 만들기
5. [Redux 확인과 비교 실험](redux-tuning.md) — 연결 확인과 값 비교
6. [빠른 참조](quick-reference.md) — 파일 위치와 시작값만 모은 표

---

## 참고 자료

### 공식 링크
- [Black Forest Labs](https://blackforestlabs.ai/)
- [Flux Models (HuggingFace)](https://huggingface.co/black-forest-labs)
- [ComfyUI Examples](https://comfyanonymous.github.io/ComfyUI_examples/flux/)

### 커뮤니티 자료
- [XLabs AI ControlNets](https://github.com/XLabs-AI/x-flux-comfyui)
- [CivitAI Flux Models](https://civitai.com/models?query=flux)
- [ComfyUI-Manager](https://github.com/ltdrdata/ComfyUI-Manager)

---

## 라이선스

이 문서는 학습용입니다. 모델과 소프트웨어에는 각각 별도의 라이선스가 적용됩니다.

- Flux 모델: 세대·변형마다 라이선스가 다릅니다. 상업적 이용 전 각 모델 카드를 확인하세요.
- ComfyUI: GPL-3.0

질문과 오류 제보는 저장소 Issues를 이용해 주세요.

---

## 완료 기준

세 가지를 모두 만족했다면 이 장을 끝냈습니다.

- FLUX.1이 SD 계열과 무엇이 다른지(구조, 로더 구성, 텍스트 인코더) 설명할 수 있다.
- FLUX.1 dev의 guidance와 KSampler의 cfg를 구분할 수 있다.
- 사용하려는 Flux 세대에 맞는 로더 구성을 확인하고, [필수 파일 위치](quick-reference.md#필수-파일-위치)에 따라 파일을 배치했다.

## 문서 정보

- **다루는 모델 범위:** FLUX.1(dev/schnell) 실습 + FLUX.2/FLUX 3 라인업 개요
- **최신 확인:** 2026-08 (모델 상태는 [bfl.ai](https://bfl.ai/models)에서 재확인 권장)
- **세대 구분:** CLIP-L+T5·FluxGuidance 설명은 FLUX.1 범위이며 이후 세대에는 해당 공식 구성을 사용

## 다음 단계

- [텍스트 인코더와 데이터 공간](text-encoders.md) — 인코더 구성과 정밀도 선택
- [FluxGuidance 이해와 사용](fluxguidance-pipeline.md) — guidance의 역할과 연결
- [LoRA 기본](../../03-advanced-techniques/lora/README.md) · [제어 기법](../../03-advanced-techniques/controlnet/controlnet-architecture.md) — 스타일·구도 제어
