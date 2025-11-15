[🏠 홈](../../../README.md) | [📚 전체 목차](../../../README.md#-전체-문서-목차)

---
# FluxGuidance Pipeline

> 🔬 텍스트 인코더와 ControlNet 간 상호작용 제어 구조 심층 분석  
> Flux 모델의 Conditioning 흐름 완벽 가이드

---

## 📚 Table of Contents

- [FluxGuidance 개요](#fluxguidance-개요)
- [Pipeline A: Text Guidance First](#pipeline-a-text-guidance-first)
- [Pipeline B: ControlNet First](#pipeline-b-controlnet-first)
- [파이프라인 비교 분석](#파이프라인-비교-분석)
- [실전 적용 가이드](#실전-적용-가이드)
- [FluxGuidance vs CFG](#fluxguidance-vs-cfg)
- [Best Practices](#best-practices)

---

## FluxGuidance 개요

### 핵심 개념

**FluxGuidance = Flux의 Conditioning 제어 시스템**

| 구성요소 | 역할 | 처리 시점 |
|:---:|:---:|:---:|
| **Text Encoder** | 텍스트 의미 이해 | Pre-conditioning |
| **FluxGuidance** | Conditioning 강도 제어 | Conditioning 단계 |
| **ControlNet** | 구조/형태 제어 | Conditioning 병합 |
| **U-Net/Sampler** | 이미지 생성 | Denoising 과정 |

### SD/SDXL vs Flux 차이

| 특성 | SD/SDXL | Flux |
|:---:|:---:|:---:|
| **Guidance 방식** | CFG (Runtime) | Guidance Distillation (Pre-applied) |
| **처리 위치** | KSampler 내부 | FluxGuidance 노드 (별도) |
| **기본값** | CFG=7.0~8.0 | Guidance=3.5 |
| **연산 횟수** | 2x per step | 1x per step |
| **속도** | 느림 | 빠름 |

> 📖 **관련 문서**: [Flux Complete Guide](./README.md#flux-guidance-system) - FluxGuidance 기초 개념

[🔝 목차로 돌아가기](#-table-of-contents)

---

## Pipeline A: Text Guidance First

> 🎨 텍스트 조건 우선 처리 파이프라인

### Workflow Diagram

```plaintext
Text Prompt
    │
    ▼
┌──────────────────────────┐
│  CLIP/T5 Text Encoder    │  Step 1: 텍스트 임베딩 생성
│  - CLIP: 768-dim         │         (의미/개념 추출)
│  - T5XXL: 4096-dim       │
└──────────────────────────┘
    │ text embedding
    ▼
┌──────────────────────────┐
│  FluxGuidance Module     │  Step 2: 텍스트 기반 조건 처리
│  - Guidance = 3.5        │         (프롬프트 충실도 제어)
│  - Pre-conditioning      │
└──────────────────────────┘
    │ guided text condition
    ▼
┌──────────────────────────┐
│  ControlNet (Optional)   │  Step 3: 구조 정보 추가 병합
│  - Depth/Canny/HED       │         (이미 텍스트 가중치 높음)
│  - Lower weight          │
└──────────────────────────┘
    │ text-dominant condition
    ▼
┌──────────────────────────┐
│  U-Net Sampler           │  Step 4: Denoising 반복
│  - Euler/DPM++           │         (텍스트 중심 생성)
│  - CFG = 1.0 (Flux)      │
└──────────────────────────┘
    │ denoised latent
    ▼
┌──────────────────────────┐
│  VAE Decoder             │  Step 5: Latent → Image
└──────────────────────────┘
    │
    ▼
Final Image

우선순위: Text [████████] > Control [███░░░]
```

### 특징

| 항목 | 설명 |
|:---:|:---:|
| **텍스트 반영** | ⭐⭐⭐⭐⭐ 매우 높음 |
| **구조 정확도** | ⭐⭐⭐ 중간 |
| **감성 표현** | ⭐⭐⭐⭐⭐ 우수 |
| **스타일 일관성** | ⭐⭐⭐⭐⭐ 우수 |
| **구도 제어** | ⭐⭐ 제한적 |

### 최적 사용 사례

✅ **추천:**
- 🎨 스타일/분위기 중심 생성
- 📝 텍스트 프롬프트 정확도 중요
- 🌈 색감/톤 제어
- ✨ 예술적 표현

❌ **비추천:**
- 📐 정확한 구도/레이아웃 필요
- 🤸 특정 포즈/자세 복제
- 🏢 건축물 정확한 구조

### ComfyUI 노드 순서

```plaintext
DualCLIPLoader → CLIPTextEncodeFlux → FluxGuidance
                                           ↓
LoadImage → ControlNetApply ──────────────→ KSampler
```

[🔝 목차로 돌아가기](#-table-of-contents)

---

## Pipeline B: ControlNet First

> 🎮 구조 조건 우선 처리 파이프라인

### Workflow Diagram

```plaintext
Control Image              Text Prompt
(Depth/Pose/Canny)              │
    │                           ▼
    ▼                   ┌──────────────────┐
┌──────────────────┐   │  CLIP/T5 Text    │
│  ControlNet      │   │  Encoder         │
│  Preprocessor    │   └──────────────────┘
│  - Depth Est.    │           │
│  - Canny Edge    │           │ text embedding
│  - Pose Detect   │           │
└──────────────────┘           │
    │                          │
    │ spatial features         │
    ▼                          ▼
┌─────────────────────────────────────────┐
│       Feature Fusion Layer              │
│  Control [███████] + Text [████░░]      │
│  (구조 정보가 강하게 반영됨)            │
└─────────────────────────────────────────┘
    │ merged condition (control-dominant)
    ▼
┌──────────────────────────┐
│  FluxGuidance Module     │  Step 3: 통합 조건 스케일링
│  - Guidance = 3.5        │         (구조 우선 상태 유지)
│  - 이미 병합된 조건 처리 │
└──────────────────────────┘
    │ control-dominant condition
    ▼
┌──────────────────────────┐
│  U-Net Sampler           │  Step 4: Denoising 반복
│  - Euler/DPM++           │         (구조 중심 생성)
│  - CFG = 1.0 (Flux)      │
└──────────────────────────┘
    │ denoised latent
    ▼
┌──────────────────────────┐
│  VAE Decoder             │  Step 5: Latent → Image
└──────────────────────────┘
    │
    ▼
Final Image

우선순위: Control [████████] > Text [████░░░]
```

### 특징

| 항목 | 설명 |
|:---:|:---:|
| **텍스트 반영** | ⭐⭐⭐ 중간 |
| **구조 정확도** | ⭐⭐⭐⭐⭐ 매우 높음 |
| **감성 표현** | ⭐⭐⭐ 중간 |
| **스타일 일관성** | ⭐⭐⭐ 중간 |
| **구도 제어** | ⭐⭐⭐⭐⭐ 우수 |

### 최적 사용 사례

✅ **추천:**
- 📐 정확한 구도/레이아웃 복제
- 🤸 특정 포즈 재현
- 🏢 건축물 구조 유지
- 🎨 기존 이미지 스타일 변경
- 📏 Depth/공간감 제어

❌ **비추천:**
- ✨ 자유로운 창의적 생성
- 🌈 텍스트만으로 표현 가능한 경우
- 📝 프롬프트 정확도가 최우선

### ComfyUI 노드 순서

```plaintext
LoadImage → ControlNetPreprocessor → ControlNetApply
                                           ↓
DualCLIPLoader → CLIPTextEncodeFlux ──────→ FluxGuidance → KSampler
```

[🔝 목차로 돌아가기](#-table-of-contents)

---

## 파이프라인 비교 분석

### 상세 비교표

| 항목 | Pipeline A (Text First) | Pipeline B (Control First) |
|:---:|:---:|:---:|
| **텍스트 반영** | ⭐⭐⭐⭐⭐ 매우 높음 | ⭐⭐⭐ 중간 |
| **구조 정확도** | ⭐⭐⭐ 중간 | ⭐⭐⭐⭐⭐ 매우 높음 |
| **감성 표현** | ⭐⭐⭐⭐⭐ 우수 | ⭐⭐⭐ 중간 |
| **구도 제어** | ⭐⭐ 제한적 | ⭐⭐⭐⭐⭐ 우수 |
| **처리 속도** | 빠름 | 약간 느림 (전처리) |
| **유연성** | 높음 | 낮음 (구조 고정) |
| **적용 분야** | 스타일/분위기 | 구조/형태 |

### 장단점 비교

#### Pipeline A (Text First)

| 장점 ✅ | 단점 ❌ |
|:---:|:---:|
| 감성/스타일 표현 우수 | 구조 제어 불안정 |
| 문체 일관성 유지 | 정확한 포즈 어려움 |
| 빠른 생성 속도 | 레이아웃 제어 제한 |
| 창의적 결과물 | 구도 예측 어려움 |

#### Pipeline B (Control First)

| 장점 ✅ | 단점 ❌ |
|:---:|:---:|
| 구조적 일관성 보장 | 텍스트 표현 감소 |
| 레이아웃 정확 제어 | 창의성 제한 |
| 포즈/깊이 재현 우수 | 전처리 시간 필요 |
| 예측 가능한 결과 | 스타일 변화 제한 |

### 가중치 균형 조정

#### ControlNet Strength 설정

| Strength | Text vs Control 비율 | 사용 상황 |
|:---:|:---:|:---:|
| **0.3~0.5** | Text [██████] Control [███] | 구조 힌트만 제공 |
| **0.6~0.8** | Text [████] Control [█████] | 균형잡힌 제어 ⭐ |
| **0.9~1.0** | Text [██] Control [███████] | 구조 정확 복제 |

#### FluxGuidance 조정

| Guidance | Text 영향력 | 추천 파이프라인 |
|:---:|:---:|:---:|
| **2.0~2.5** | 낮음 (자유로움) | Pipeline B + High Control |
| **3.5** | 중간 (기본) ⭐ | 모두 적합 |
| **4.5~5.0** | 높음 (충실함) | Pipeline A |

[🔝 목차로 돌아가기](#-table-of-contents)

---

## 실전 적용 가이드

### 시나리오별 추천

| 작업 | 추천 Pipeline | FluxGuidance | Control Strength |
|:---:|:---:|:---:|:---:|
| 🎨 컨셉 아트 | A (Text First) | 3.5~4.0 | - |
| 📸 포트레이트 (포즈 제어) | B (Control First) | 3.0~3.5 | 0.7~0.9 |
| 🏢 건축 시각화 | B (Control First) | 3.5 | 0.8~1.0 |
| 🖼️ 스타일 트랜스퍼 | B (Control First) | 3.0~3.5 | 0.5~0.7 |
| ✨ 추상 예술 | A (Text First) | 2.5~3.5 | - |
| 📐 정확한 구도 복제 | B (Control First) | 3.5 | 0.9~1.0 |

### ComfyUI 워크플로우 예시

#### Pipeline A: Text First 기본 워크플로우

```plaintext
[DualCLIPLoader]
    ↓
[CLIPTextEncodeFlux] "a beautiful sunset over mountains"
    ↓
[FluxGuidance] (3.5)
    ↓
[UNETLoader] flux1-dev
    ↓
[EmptyLatentImage] 1024×1024
    ↓
[KSampler] CFG=1.0, Steps=25
    ↓
[VAEDecode]
    ↓
[SaveImage]
```

#### Pipeline B: Control First 기본 워크플로우

```plaintext
[LoadImage] (참조 이미지)
    ↓
[DepthAnythingPreprocessor]
    ↓
[ControlNetLoader] flux-depth-v3
    ↓
[ControlNetApply] strength=0.8
    ↓
[DualCLIPLoader] + [CLIPTextEncodeFlux]
    ↓
[FluxGuidance] (3.5)
    ↓
[UNETLoader] flux1-dev
    ↓
[EmptyLatentImage] 1024×1024
    ↓
[KSampler] CFG=1.0, Steps=25
    ↓
[VAEDecode]
    ↓
[SaveImage]
```

[🔝 목차로 돌아가기](#-table-of-contents)

---

## FluxGuidance vs CFG

### 기술적 차이

| 특성 | SD/SDXL CFG | Flux Guidance |
|:---:|:---:|:---:|
| **알고리즘** | Classifier-Free Guidance | Guidance Distillation |
| **적용 시점** | Sampling 매 스텝 | Pre-conditioning (한 번) |
| **연산량** | 높음 (2x per step) | 낮음 (1x total) |
| **KSampler CFG** | 7.0~8.0 (활성) | 1.0 (비활성) |
| **파라미터 위치** | KSampler 내부 | FluxGuidance 노드 |
| **값 범위** | 1~30 | 1~10 |

### CFG 계산 방식

#### SD/SDXL (Traditional CFG)

```plaintext
매 Sampling Step마다:

1. Unconditional Forward Pass
   noise_pred_uncond = model(latent, t, condition=None)

2. Conditional Forward Pass  
   noise_pred_cond = model(latent, t, condition=text_embed)

3. CFG Interpolation
   noise_pred = noise_pred_uncond + cfg_scale × (noise_pred_cond - noise_pred_uncond)

→ 매 스텝마다 2번 계산 (느림)
```

#### Flux (Guidance Distillation)

```plaintext
Conditioning 단계 (한 번만):

1. Text Embedding 생성
   text_embed = T5XXL(prompt)

2. Guidance 적용
   guided_embed = apply_guidance(text_embed, guidance=3.5)

3. Sampling (매 스텝)
   noise_pred = model(latent, t, condition=guided_embed)

→ 한 번만 계산 후 재사용 (빠름)
```

### 왜 Flux가 더 빠른가?

```plaintext
SD/SDXL (CFG=7.0, Steps=20):
- Forward Pass: 20 steps × 2 = 40회
- 총 연산: 40 passes

Flux (Guidance=3.5, Steps=20):
- Guidance 적용: 1회
- Forward Pass: 20 steps × 1 = 20회  
- 총 연산: 21 passes (절반!)

→ 약 2배 빠른 속도
```

> 📖 **관련 문서**: [Flux Complete Guide - CFG in Flux](./README.md#cfg-in-flux)

[🔝 목차로 돌아가기](#-table-of-contents)

---

## Best Practices

### 1️⃣ 파이프라인 선택 가이드

```plaintext
시작: 무엇이 더 중요한가?

텍스트 내용 > 구조
    ↓
Pipeline A (Text First)
- FluxGuidance: 3.5~4.5
- ControlNet: 사용 안 함 또는 낮게 (0.3~0.5)

구조/형태 > 텍스트 내용
    ↓
Pipeline B (Control First)  
- FluxGuidance: 3.0~3.5
- ControlNet: 높게 (0.7~1.0)
```

### 2️⃣ 파라미터 튜닝 순서

```plaintext
Step 1: 기본값으로 테스트
└─ FluxGuidance: 3.5
└─ ControlNet: 0.7 (사용 시)
└─ Steps: 25

Step 2: 결과 평가
├─ 텍스트 따르지 않음 → FluxGuidance ↑ (4.0~4.5)
├─ 구조 약함 → ControlNet Strength ↑ (0.8~1.0)
└─ 너무 경직됨 → FluxGuidance ↓ (2.5~3.0)

Step 3: 미세 조정
└─ 0.5 단위로 조정하며 최적값 찾기
```

### 3️⃣ 일반적인 실수 방지

| 실수 | 결과 | 해결 |
|:---:|:---:|:---:|
| FluxGuidance=1.0 | 프롬프트 무시 | 3.5로 설정 |
| ControlNet=1.0 + Text First | 텍스트 약함 | Strength 낮추기 |
| CFG > 1.0 (Flux) | 오류/이상한 결과 | CFG=1.0 고정 |
| Guidance=6.0+ | 아티팩트 발생 | 3.5~4.5 범위 유지 |

### 4️⃣ 최적 조합

| 목표 | Pipeline | FluxGuidance | ControlNet | Steps |
|:---:|:---:|:---:|:---:|:---:|
| **최고 품질** | B | 3.5 | 0.8 | 30~40 |
| **빠른 생성** | A | 3.5 | - | 15~20 |
| **균형잡힌 결과** ⭐ | B | 3.5 | 0.7 | 25 |
| **창의적 결과** | A | 2.5~3.0 | - | 20~25 |
| **정확한 복제** | B | 3.5 | 0.9~1.0 | 30 |

[🔝 목차로 돌아가기](#-table-of-contents)

---

## 결론

### 핵심 요약

1. **Pipeline A (Text First)**
   - ✨ 텍스트 중심, 창의적 생성
   - 🎨 스타일/감성 표현 우수
   - 📝 FluxGuidance로 프롬프트 충실도 제어

2. **Pipeline B (Control First)**
   - 📐 구조 중심, 정확한 제어
   - 🎮 레이아웃/포즈/깊이 정확
   - ⚖️ ControlNet Strength로 균형 조절

3. **입력 순서 = 우선순위**
   - 먼저 처리되는 조건이 더 강하게 반영됨
   - FluxGuidance는 이미 병합된 조건을 스케일링
   - 목적에 맞는 파이프라인 선택이 중요

### 추천 워크플로우

```plaintext
일반 사용자:
→ Pipeline A (Text First) + FluxGuidance=3.5

구도 제어 필요:
→ Pipeline B (Control First) + FluxGuidance=3.5 + ControlNet=0.7~0.8

최고 품질:
→ Pipeline B + FluxGuidance=3.5 + ControlNet=0.8 + Steps=30
```

---

## 관련 문서

- 📖 [Flux Complete Guide](./README.md) - Flux 모델 전체 가이드
- 🎮 [ControlNet 구조](../controlnet/controlnet-architecture.md) - ControlNet 아키텍처 분석
- ⚙️ [Sampler 비교](../samplers/sampler-comparison.md) - 샘플러 특성 비교

---

## 참고 자료

- [Black Forest Labs - Flux](https://blackforestlabs.ai/)
- [Flux Examples - ComfyUI](https://comfyanonymous.github.io/ComfyUI_examples/flux/)
- [XLabs AI - Flux ControlNet](https://github.com/XLabs-AI/x-flux-comfyui)

---

<div align="center">

**[⬆️ Back to Top](#fluxguidance-pipeline)**

Last Updated: 2025-11-12

</div>
---

[🏠 홈으로](../../../README.md)