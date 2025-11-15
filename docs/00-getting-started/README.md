[🏠 홈](../../README.md) | [📚 전체 목차](../../README.md#-전체-문서-목차)

---
# ComfyUI 완전 가이드 - 초보자부터 실전까지

> Stable Diffusion & Flux 이미지 생성 워크플로우 마스터하기  
> 핵심 개념부터 실전 활용까지 체계적으로 정리한 기술노트

---

## 📑 목차

### [PART I - 핵심 개념](#part-i---핵심-개념)
1. [Latent Image - 압축된 설계도](#1-latent-image---압축된-설계도)
2. [VAE - 압축과 복원 엔진](#2-vae---압축과-복원-엔진)
3. [아키텍처 비교: UNet vs Transformer](#3-아키텍처-비교-unet-vs-transformer)
4. [모델 구성 요소 이해하기](#4-모델-구성-요소-이해하기)

### [PART II - 워크플로우 실전](#part-ii---워크플로우-실전)
5. [전체 워크플로우 흐름도](#5-전체-워크플로우-흐름도)
6. [KSampler - 이미지 생성 엔진](#6-ksampler---이미지-생성-엔진)
7. [CLIP - 텍스트 이해 시스템](#7-clip---텍스트-이해-시스템)
8. [기본 워크플로우 구축하기](#8-기본-워크플로우-구축하기)

### [PART III - 고급 기능과 실전](#part-iii---고급-기능과-실전)
9. [Flux 모델 특수 설정](#9-flux-모델-특수-설정)
10. [LoRA - 스타일 미세조정](#10-lora---스타일-미세조정)
11. [ControlNet - 구조 제어](#11-controlnet---구조-제어)
12. [문제 해결 가이드](#12-문제-해결-가이드)
13. [첫 워크플로우 실습](#13-첫-워크플로우-실습)

### [부록](#부록)
- [용어 정리](#용어-정리)
- [참고 자료](#참고-자료)

---

# PART I - 핵심 개념

> AI 이미지 생성의 기초를 이해합니다

---

## 1. Latent Image - 압축된 설계도

### 🎯 핵심 개념

**Latent Image = 압축된 "설계도"**

일반 이미지를 그대로 처리하면 너무 무겁습니다. AI는 이것을 작은 "암호화된 설계도"로 줄여서 작업합니다.

### 📊 구체적 비유

```
일반 이미지     →  완성된 레고 작품 (용량 큼, 처리 느림)
Latent Image   →  레고 조립 설명서 (용량 작음, 처리 빠름)
```

AI는 "설명서"만 보고 작업하다가, 마지막에 "완성된 작품"으로 복원합니다.

### 💡 왜 Latent를 사용하나?

| 비교 항목 | 일반 이미지 (512×512 RGB) | Latent (64×64) |
|----------|------------------------|----------------|
| 처리할 숫자 | 786,432개 | 16,384개 |
| 처리 속도 | 기준 | **약 50배 빠름** |
| 사람이 볼 수 있나? | ✅ 가능 | ❌ 불가능 (압축 상태) |

### 🔄 Latent 작업 흐름

```
빈 Latent Image (노이즈)
        ↓
    [KSampler] - AI가 노이즈 제거하며 이미지 생성
        ↓
  Latent Image (완성, 여전히 압축 상태)
        ↓
   [VAE Decode] - 압축 해제
        ↓
   실제 이미지 (사람이 볼 수 있음)
```

### ✅ 초보자 체크포인트

- [x] Latent는 "보이지 않는 압축 공간"에서 작업하는 것
- [x] 사람이 볼 수 없지만, AI가 효율적으로 작업 가능
- [x] 반드시 **VAE Decode**를 거쳐야 실제 이미지로 변환됨
- [x] **Empty Latent Image** = 깨끗한 빈 캔버스 (시작점)

### 🎨 빈 Latent Image의 역할

**왜 "빈" 것에서 시작하나?**

```
1. 깨끗한 시작점 제공
   └─→ 빈 종이에 그림 그리듯 방해 없이 시작

2. 공정한 비교 가능
   └─→ 여러 이미지를 만들 때 같은 출발점

3. 더 좋은 품질
   └─→ 기존 잡음 없이 깔끔하게 발전
```

[⬆️ 목차로 돌아가기](#-목차)

---

## 2. VAE - 압축과 복원 엔진

### 🎯 핵심 개념

**VAE (Variational AutoEncoder) = 압축/압축 해제 도구**

이미지를 압축된 Latent로 바꾸고, 다시 원래 이미지로 복원하는 역할을 합니다.

### 📊 VAE의 두 가지 역할

| 역할 | 이름 | 입력 | 출력 | 언제 사용? |
|-----|------|------|------|-----------|
| **압축** | VAE Encode | 일반 이미지 | Latent Image | 기존 이미지 수정 시 |
| **복원** | VAE Decode | Latent Image | 일반 이미지 | **결과 확인 시 (필수!)** |

### 🔄 작동 원리

```
[일반 이미지 512×512]
        ↓ VAE Encode (압축)
    [Latent 64×64]
        ↓ AI 작업 (KSampler)
    [Latent 64×64] (생성 완료)
        ↓ VAE Decode (복원)
[일반 이미지 512×512]
```

### 💡 실제 사용 예시

**신규 이미지 생성:**
```
Empty Latent Image → KSampler → VAE Decode → Save Image
(압축 상태 유지)
```

**기존 이미지 수정:**
```
Load Image → VAE Encode → KSampler → VAE Decode → Save Image
```

### ⚠️ 초보자 주의사항

**VAE Decode 없으면 이미지가 안 보입니다!**

```
❌ 잘못된 연결:
KSampler → Save Image (Latent는 이미지가 아님!)

✅ 올바른 연결:
KSampler → VAE Decode → Save Image
```

### ✅ 체크리스트

- [x] KSampler 뒤에 **VAE Decode** 연결했나?
- [x] VAE Decode 뒤에 **Save/Preview Image** 연결했나?
- [x] Load Checkpoint에서 VAE 출력을 VAE Decode에 연결했나?

[⬆️ 목차로 돌아가기](#-목차)

---

## 3. 아키텍처 비교: UNet vs Transformer

### 🎯 핵심 차이

AI 이미지 생성 모델의 두 가지 근본적인 구조 방식입니다.

### 📊 비교표

| 항목 | UNet (SD 1.5/SDXL) | Transformer/DiT (Flux) |
|------|-------------------|----------------------|
| **기반 기술** | CNN (합성곱 신경망) | Self-Attention |
| **처리 방식** | 지역적 (주변만 봄) | 전역적 (전체 동시 참조) |
| **구조** | U자 파이프라인 | 패치 간 상호작용 |
| **텍스트 이해** | 보통 | 우수 ⭐ |
| **구도 파악** | 약함 | 강함 ⭐ |
| **처리 속도** | 빠름 | 상대적으로 느림 |
| **메모리 사용** | 적음 | 많음 |
| **적합한 용도** | 빠른 생성, 디테일 | 정확한 프롬프트 반영 |

### 🏗️ UNet 구조 (SD 1.5/SDXL)

```
입력 이미지
    ↓ [압축 - CNN 레이어]
    ↓ [더 압축]
    ↓ [최대 압축] ← 핵심 정보만 남음
    ↑ [복원]
    ↑ [더 복원]
출력 이미지
```

**특징:**
- **CNN 기반** - 3×3, 5×5 같은 작은 필터로 주변 픽셀만 봄
- **지역적 패턴 인식** - 눈, 코, 입 같은 부분적 특징에 강함
- **빠르지만** - 전체 맥락 파악은 약함

**비유:** 근시안적 화가 - 세밀하지만 전체 구도 파악 어려움

### 🤖 Transformer 구조 (Flux)

```
이미지를 16×16 패치로 분할

[패치1] ←→ [패치2] ←→ [패치3]
   ↕         ↕         ↕
[패치4] ←→ [패치5] ←→ [패치6]
   ↕         ↕         ↕
[패치7] ←→ [패치8] ←→ [패치9]

모든 패치가 Self-Attention으로 서로 정보 교환
```

**특징:**
- **Self-Attention 기반** - 모든 영역을 동시에 참조
- **전역적 이해** - "왼쪽 위 꽃"과 "오른쪽 아래 나비"의 관계 파악
- **텍스트 정합성 우수** - 프롬프트 이해력 ↑

**비유:** 조감도를 보는 건축가 - 전체 맥락 파악 강함

### 💡 실전 차이 예시

**프롬프트:** "왼쪽에 빨간 사과, 오른쪽에 초록 사과"

| 모델 | 결과 |
|------|------|
| **UNet (SD)** | 때때로 위치 혼동 (전체 맥락 약함) |
| **Transformer (Flux)** | 위치 관계 정확히 파악 (attention으로 전체 보기) |

### 🎯 한 문장 요약

- **UNet**: 부분을 잘 그리는 세밀한 화가
- **Transformer**: 전체 구도를 이해하는 감독

Flux가 프롬프트 이해력과 구도가 더 좋은 이유가 바로 이 Transformer 구조 때문입니다!

[⬆️ 목차로 돌아가기](#-목차)

---

## 4. 모델 구성 요소 이해하기

### 🎯 핵심 개념 정리

ComfyUI에서 자주 혼동되는 세 가지 개념을 명확히 구분합니다.

### 📊 비교표

| 개념 | 본질 | 비유 | 파일/위치 |
|------|------|------|-----------|
| **UNet/DiT** | AI 엔진 구조 (아키텍처) | 자동차 엔진 설계 방식 | - (개념) |
| **Checkpoint** | 학습 완료된 모델 파일 | 완성된 자동차 | `.safetensors`, `.ckpt` |
| **Load Diffusion Model** | 파일을 메모리에 올리는 노드 | 자동차 시동 걸기 | ComfyUI 노드 |

### 🔍 상세 설명

#### 1️⃣ UNet / DiT (아키텍처)

**"뇌의 구조 설계도"**

- Stable Diffusion의 핵심 신경망 구조
- 노이즈 제거 역할을 하는 AI 엔진
- 모든 SD/Flux 모델이 사용하는 기본 구조
- 사용자는 직접 다루지 않음 (자동으로 작동)

#### 2️⃣ Checkpoint (저장 파일)

**"학습된 완제품"**

- 학습이 완료된 모델 전체를 담은 파일
- **포함 내용:**
  - UNet/DiT (노이즈 제거)
  - VAE (압축/복원)
  - Text Encoder (프롬프트 이해)
- **예시:** `realisticVision_v60.safetensors`

#### 3️⃣ Load Diffusion Model (노드)

**"파일을 메모리에 올리는 행위"**

- ComfyUI에서 checkpoint 파일을 불러오는 노드
- 하드디스크 → RAM/VRAM으로 로드

### 🏗️ 관계도

```
하드디스크: [Checkpoint 파일 .safetensors]
                    ↓
          [Load Checkpoint 노드 실행]
                    ↓
           메모리에 로드된 모델
                    ├─ UNet/DiT (노이즈 제거)
                    ├─ VAE (압축/복원)
                    └─ Text Encoder (프롬프트 이해)
                    ↓
              워크플로우에서 사용
```

### ⚡ SD vs Flux 차이점

| 구분 | SD 1.5 / SDXL | Flux Dev / Schnell |
|------|--------------|-------------------|
| **노드** | `Load Checkpoint` | `Load Diffusion Model` |
| **폴더** | `models/checkpoints/` | `models/unet/` 또는 `models/diffusion_models/` |
| **구조** | UNet 기반 | DiT (Transformer) 기반 |
| **파일 구성** | 통합 checkpoint | UNet + VAE + CLIP 분리 |

### 📁 Flux 폴더 구조

```
ComfyUI/models/
├── checkpoints/        # SD 1.5, SDXL 체크포인트
├── unet/              # ✅ Flux 모델 파일
├── diffusion_models/  # ✅ Flux 모델 파일 (대체 위치)
├── vae/               # VAE 파일
└── clip/              # CLIP 인코더 파일
```

### 💡 실제 워크플로우 예시

**SD 1.5/SDXL:**
```
[Load Checkpoint] → MODEL/CLIP/VAE 모두 출력
        ↓
   한 번에 사용 준비 완료
```

**Flux:**
```
[Load Diffusion Model] → MODEL 출력 (UNet만)
[Load VAE] → VAE 출력
[Dual CLIP Loader] → CLIP 출력
        ↓
   각각 따로 로드 필요
```

### ✅ 초보자 체크포인트

- [x] UNet/DiT는 아키텍처 (설계 방식)
- [x] Checkpoint는 학습된 데이터 파일
- [x] Load 노드는 파일을 불러오는 액션
- [x] Flux는 일반 SD와 로딩 방식이 다름!

[⬆️ 목차로 돌아가기](#-목차)

---

# PART II - 워크플로우 실전

> 실제 이미지를 생성하는 노드 연결 방법을 배웁니다

---

## 5. 전체 워크플로우 흐름도

### 🎯 전체 프로세스 이해하기

ComfyUI의 이미지 생성 과정을 한눈에 파악합니다.

### 🏗️ 기본 워크플로우 (SD 1.5/SDXL)

```
┌─────────────────────────────────────────────────────────┐
│              ComfyUI 이미지 생성 전체 흐름              │
└─────────────────────────────────────────────────────────┘

1. 모델 준비
┌──────────────────┐
│ Load Checkpoint  │
└──┬───┬─────┬─────┘
   │   │     │
   │   │     └──→ [VAE] ────────────────┐
   │   │                                  ↓
   │   └──→ [CLIP] ──→ [Text Encode +]   │
   │                ↘                     │
   │                  [Text Encode -]     │
   │                         ↓            ↓
   └──→ [MODEL] ───→ [KSampler] ←────────┘
                           ↓
2. 이미지 생성            ↓
┌──────────────────┐     ↓
│ Empty Latent     │ ────┘
│ Image            │
└──────────────────┘
        ↓
[Latent 생성]
        ↓
3. 결과 복원
[VAE Decode]
        ↓
[Save/Preview Image]
```

### 📊 단계별 세부 설명

| 단계 | 노드 | 역할 | 출력 |
|-----|------|------|------|
| **1단계** | Load Checkpoint | 모델 파일 로드 | MODEL, CLIP, VAE |
| **2단계** | CLIP Text Encode | 프롬프트 변환 | Conditioning (긍정/부정) |
| **3단계** | Empty Latent Image | 빈 캔버스 생성 | Latent (노이즈) |
| **4단계** | KSampler | AI 이미지 생성 | Latent (완성) |
| **5단계** | VAE Decode | 압축 해제 | 일반 이미지 |
| **6단계** | Save Image | 저장 | 파일 출력 |

### 🔄 데이터 흐름 상세

```
사용자 입력
    ↓
[Positive Prompt] → [CLIP Encode] → Conditioning+
[Negative Prompt] → [CLIP Encode] → Conditioning-
                                         ↓
                                    [KSampler]
                                         ↑
[Empty Latent] ──────────────────────→  │
[MODEL] ─────────────────────────────→  │
                                         ↓
                                   [Latent Output]
                                         ↓
[VAE] ───────────────────────────→ [VAE Decode]
                                         ↓
                                    [이미지]
                                         ↓
                                   [Save Image]
```

### 🎨 각 노드의 입출력

```
┌─────────────────────┐
│  Load Checkpoint    │
├─────────────────────┤
출력:
├─→ MODEL (노이즈 제거 엔진)
├─→ CLIP (텍스트 인코더)
└─→ VAE (압축/복원 도구)
```

```
┌─────────────────────┐
│  CLIP Text Encode   │
├─────────────────────┤
입력: CLIP, 텍스트
출력: Conditioning
```

```
┌─────────────────────┐
│     KSampler        │
├─────────────────────┤
입력:
├─ MODEL
├─ Positive Conditioning
├─ Negative Conditioning
├─ Latent Image (빈 캔버스)
└─ 설정값 (steps, cfg 등)
출력: Latent (생성 완료)
```

```
┌─────────────────────┐
│    VAE Decode       │
├─────────────────────┤
입력: VAE, Latent
출력: IMAGE
```

### ⚡ Flux 워크플로우 차이점

```
SD 방식:
[Load Checkpoint] → 한 번에 MODEL+CLIP+VAE

Flux 방식:
[Load Diffusion Model] → MODEL만
[Load VAE] → VAE만
[Dual CLIP Loader] → CLIP만 (T5xxl + CLIP-L)
```

### ✅ 초보자 체크리스트

- [x] 모든 노드가 올바르게 연결되었나?
- [x] CLIP Text Encode가 2개 (긍정/부정)인가?
- [x] KSampler에 5가지 입력이 모두 연결되었나?
- [x] VAE Decode를 거쳤나?
- [x] 최종적으로 Save Image가 연결되었나?

[⬆️ 목차로 돌아가기](#-목차)

---

## 6. KSampler - 이미지 생성 엔진

### 🎯 핵심 개념

**KSampler = 노이즈를 이미지로 변환하는 감독**

AI가 지저분한 노이즈에서 실제 이미지를 만드는 과정을 조정하는 핵심 노드입니다.

### 🔄 작동 원리

```
시작: [완전한 노이즈 100%]
        ↓ Step 1
     [노이즈 95%]
        ↓ Step 2
     [노이즈 90%]
        ↓ ...
     [노이즈 10%]
        ↓ Step 30
완료: [완성된 이미지 0%]
```

KSampler는 이 "노이즈 제거 과정"을 몇 번 반복할지, 얼마나 강하게 할지를 결정합니다.

### 📊 주요 설정 항목

| 항목 | 의미 | 범위 | 초보자 추천값 | 설명 |
|------|------|------|-------------|------|
| **Steps** | 이미지를 다듬는 횟수 | 10-150 | **30** | 많을수록 정밀, 느림 |
| **CFG Scale** | 프롬프트 준수 강도 | 1-20 | **7** | 높을수록 프롬프트 강제, 과도하면 부자연 |
| **Sampler** | 노이즈 제거 알고리즘 | 여러 종류 | **euler** 또는 **dpmpp_2m** | 품질과 속도 균형 |
| **Scheduler** | 노이즈 제거 속도 조절 | normal, karras 등 | **normal** | 제거 일정 결정 |
| **Denoise** | 노이즈 제거 강도 | 0.0-1.0 | **1.0** | 1.0=완전 생성, <1.0=부분 수정 |

### 🔍 CFG (Classifier-Free Guidance) 상세

**CFG = "프롬프트 안내 강도"**

```
CFG 1-3:  AI가 창의적으로 해석 (프롬프트 느슨하게)
CFG 5-8:  균형잡힌 해석 ✅ 추천
CFG 10+:  프롬프트 강제 적용 (과도하면 부자연)
```

**비유:** CFG는 화가에게 주는 지시의 강도
- 낮음: "자유롭게 그려주세요"
- 중간: "이렇게 그려주세요"
- 높음: "정확히 이렇게만 그려주세요!"

### 🛠️ Sampler 종류 비교

| Sampler | 속도 | 품질 | 특징 | 추천 용도 |
|---------|------|------|------|-----------|
| **euler** | 빠름 | 중 | 안정적, 빠름 | 테스트, 빠른 생성 |
| **euler_a** | 빠름 | 중 | 약간 랜덤함 | 다양성 원할 때 |
| **dpmpp_2m** | 중간 | 높음 | 고품질 | **최종 결과물** |
| **dpmpp_2m_karras** | 중간 | 높음 | 후반 디테일 강화 | 정밀한 이미지 |
| **ddim** | 느림 | 높음 | 안정적 | 일관성 필요 시 |

### 📈 Steps에 따른 결과 차이

```
Steps 10-15:  빠르지만 흐릿, 테스트용
Steps 20-30:  일반적 품질 ✅ 추천
Steps 40-50:  고품질, 느림
Steps 50+:    미세 개선만, 시간 낭비 가능
```

### ⚙️ K-Sample 개념 보충

**K-Sample = "k개의 샘플(후보) 생성"**

같은 설정으로 여러 버전의 이미지를 만들 수 있습니다.
- K=5이면 5개의 다른 이미지 생성
- Seed 값을 바꿔서 다양성 확보

### 💡 실전 설정 예시

**빠른 테스트용:**
```
Steps: 20
CFG: 7
Sampler: euler
Scheduler: normal
```

**최종 결과물용:**
```
Steps: 30-40
CFG: 7
Sampler: dpmpp_2m_karras
Scheduler: karras
```

**창의적 실험용:**
```
Steps: 25
CFG: 4-5
Sampler: euler_a
Scheduler: normal
```

### ✅ 초보자 체크포인트

- [x] Steps는 30 정도가 적당 (너무 높이면 시간 낭비)
- [x] CFG는 7-8이 가장 무난
- [x] Sampler는 euler로 시작, 나중에 dpmpp_2m 시도
- [x] Denoise는 1.0으로 시작 (완전 생성)

### 🚨 주의사항

**이런 증상이 나타나면:**

| 문제 | 원인 | 해결 |
|------|------|------|
| 이미지가 과장됨 | CFG 너무 높음 | CFG 낮추기 (7 정도) |
| 이미지가 흐릿함 | Steps 너무 적음 | Steps 늘리기 (30+) |
| 너무 느림 | Steps 너무 많음 | Steps 줄이기 (20-30) |
| 프롬프트 무시 | CFG 너무 낮음 | CFG 높이기 (7-10) |

[⬆️ 목차로 돌아가기](#-목차)

---

## 7. CLIP - 텍스트 이해 시스템

### 🎯 핵심 개념

**CLIP = 텍스트를 AI가 이해하는 언어로 변환하는 번역기**

사람이 입력한 프롬프트를 AI가 이해할 수 있는 숫자(벡터)로 변환합니다.

### 🔄 작동 원리

```
사용자 입력: "빨간 사과, 사실적, 고품질"
        ↓
    [CLIP Text Encode]
        ↓
   숫자 벡터: [0.8, -0.3, 0.5, 1.2, ...]
        ↓
   AI가 이해 가능한 형태 (Conditioning)
        ↓
    [KSampler]로 전달
```

### 📊 Positive vs Negative Prompt

| 구분 | 역할 | 예시 | 효과 |
|------|------|------|------|
| **Positive** | 원하는 것 | `a cat, blue sky, high quality` | 이런 요소를 이미지에 포함 |
| **Negative** | 원하지 않는 것 | `blurry, low quality, distorted` | 이런 요소를 이미지에서 제거 |

### 🏗️ ComfyUI 연결 구조

```
[Load Checkpoint]
        │
    [CLIP 출력]
        ├─→ [CLIP Text Encode (Positive)]
        │       ↓
        │   [Conditioning+] → [KSampler]
        │
        └─→ [CLIP Text Encode (Negative)]
                ↓
            [Conditioning-] → [KSampler]
```

### 💡 프롬프트 작성 팁

**좋은 프롬프트 구조:**
```
[주제] + [스타일] + [품질] + [디테일]

예시:
"a cute cat sitting on a window, 
watercolor painting style, 
high quality, detailed fur, 
soft lighting, cozy atmosphere"
```

**나쁜 프롬프트:**
```
❌ "cat"  → 너무 간단
❌ "a very very very beautiful cat" → 반복 무의미
❌ "고양이, 예쁜" → 한국어 (영어 추천)
```

### 🌐 언어별 효과

| 언어 | 효과 | 추천도 |
|------|------|--------|
| **영어** | 가장 정확한 이해 | ⭐⭐⭐⭐⭐ |
| 한국어 | 제한적 이해 | ⭐⭐ |
| 일본어 | 제한적 이해 | ⭐⭐ |
| 기타 | 매우 제한적 | ⭐ |

**이유:** CLIP은 주로 영어 데이터로 학습됨

### 🎨 Negative Prompt 활용

**기본 Negative Prompt 세트:**
```
"blurry, low quality, distorted, 
ugly, bad anatomy, extra limbs, 
watermark, text, signature"
```

**사진 스타일용:**
```
"cartoon, 3d render, illustration, 
painting, drawing"
```

**일러스트용:**
```
"photograph, realistic, photo"
```

### ⚡ Dual CLIP Loader (Flux용)

Flux 모델은 **2개의 CLIP**을 사용하여 더 정확한 이해를 합니다.

```
[Dual CLIP Loader]
    ├─ CLIP-L: 시각적 연상
    └─ T5xxl: 문맥·뉘앙스 이해
          ↓
    두 번역가가 협업
          ↓
    더 정확한 이미지 생성
```

**필요 파일:**
- `clip_l.safetensors` (약 1GB)
- `t5xxl_fp8_e4m3fn.safetensors` (약 5GB)
- 위치: `ComfyUI/models/clip/`

### 📁 설정 방법

```
[Dual CLIP Loader]
├─ clip_name1: "t5xxl_fp8_e4m3fn.safetensors"
├─ clip_name2: "clip_l.safetensors"
└─ type: "flux" (Flux 모델 사용 시)
```

### ✅ 초보자 체크포인트

- [x] Positive와 Negative 2개 모두 필요
- [x] 프롬프트는 영어로 작성하는 것이 가장 좋음
- [x] 구체적으로 작성할수록 정확한 결과
- [x] Flux 사용 시 Dual CLIP Loader 사용
- [x] CLIP 출력은 반드시 KSampler에 연결

[⬆️ 목차로 돌아가기](#-목차)

---

## 8. 기본 워크플로우 구축하기

### 🎯 목표

"파란 하늘 배경의 고양이" 이미지를 처음부터 만들어봅니다.

### 📋 필요한 노드 목록

```
1. Load Checkpoint
2. CLIP Text Encode (Positive)
3. CLIP Text Encode (Negative)
4. Empty Latent Image
5. KSampler
6. VAE Decode
7. Save Image
```

### 🏗️ 단계별 구축 가이드

#### 1단계: 모델 로드

```
[Load Checkpoint]
├─ ckpt_name: "realisticVision_v60.safetensors" (예시)
│
출력:
├─→ MODEL
├─→ CLIP
└─→ VAE
```

#### 2단계: 프롬프트 설정

```
[CLIP Text Encode (Positive)]
├─ clip: Load Checkpoint의 CLIP 연결
└─ text: "a cute cat with blue sky background, 
          high quality, detailed, 8k"

[CLIP Text Encode (Negative)]
├─ clip: Load Checkpoint의 CLIP 연결
└─ text: "blurry, low quality, distorted, 
          ugly, watermark"
```

#### 3단계: 캔버스 생성

```
[Empty Latent Image]
├─ width: 512
├─ height: 512
└─ batch_size: 1
```

#### 4단계: 이미지 생성 설정

```
[KSampler]
├─ model: Load Checkpoint의 MODEL 연결
├─ positive: Positive CLIP의 Conditioning 연결
├─ negative: Negative CLIP의 Conditioning 연결
├─ latent_image: Empty Latent Image 연결
├─ seed: 12345 (원하는 숫자)
├─ steps: 30
├─ cfg: 7
├─ sampler_name: euler
├─ scheduler: normal
└─ denoise: 1.0
```

#### 5단계: 결과 복원 및 저장

```
[VAE Decode]
├─ samples: KSampler의 LATENT 연결
└─ vae: Load Checkpoint의 VAE 연결

[Save Image]
├─ images: VAE Decode의 IMAGE 연결
└─ filename_prefix: "cat_blue_sky"
```

### 🔗 완전한 연결 다이어그램

```
┌─────────────────┐
│ Load Checkpoint │
└─┬───┬─────┬─────┘
  │   │     │
  │   │     └─→ [VAE] ──────────────────────┐
  │   │                                       ↓
  │   └─→ [CLIP] ─┬─→ [Text Encode +] ──┐   │
  │                └─→ [Text Encode -] ──┼─→ │
  │                                       ↓   ↓
  └─→ [MODEL] ────────────────────────→ [KSampler]
                                             ↑
  ┌──────────────────┐                      │
  │ Empty Latent     │ ─────────────────────┘
  │ Image            │
  └──────────────────┘
                                             ↓
                                        [LATENT]
                                             ↓
                                     [VAE Decode] ← [VAE]
                                             ↓
                                         [IMAGE]
                                             ↓
                                      [Save Image]
```

### 📊 설정값 요약표

| 노드 | 파라미터 | 값 |
|------|---------|-----|
| Empty Latent Image | width | 512 |
| | height | 512 |
| | batch_size | 1 |
| KSampler | seed | 12345 |
| | steps | 30 |
| | cfg | 7 |
| | sampler_name | euler |
| | scheduler | normal |
| | denoise | 1.0 |

### ✅ 체크리스트 (실행 전)

- [ ] Load Checkpoint에서 모델 선택됨
- [ ] Positive Prompt 작성 완료
- [ ] Negative Prompt 작성 완료
- [ ] 이미지 크기 설정 (512×512 권장)
- [ ] KSampler 설정 완료
- [ ] 모든 선이 올바르게 연결됨
- [ ] VAE Decode가 연결됨
- [ ] Save Image가 마지막에 연결됨

### 🚀 실행하기

1. **Queue Prompt** 버튼 클릭
2. 진행 상황 모니터링
3. 생성 완료 후 결과 확인
4. 만족스럽지 않으면 설정 조정 후 재실행

### 🔧 결과가 마음에 안 들 때

| 문제 | 조정할 설정 |
|------|------------|
| 흐릿함 | Steps 늘리기 (30 → 40) |
| 프롬프트 무시 | CFG 높이기 (7 → 10) |
| 너무 과장됨 | CFG 낮추기 (7 → 5) |
| 다른 느낌 원함 | Seed 값 변경 |
| 속도 느림 | 이미지 크기 줄이기 (512×512) |

### 💡 다음 단계

기본 워크플로우가 익숙해지면:
1. 다양한 프롬프트 실험
2. 다른 Sampler 시도 (dpmpp_2m)
3. 이미지 크기 변경 (768×768, 1024×1024)
4. LoRA 추가로 스타일 변경 (PART III)

[⬆️ 목차로 돌아가기](#-목차)

---

# PART III - 고급 기능과 실전

> LoRA, ControlNet, Flux 등 고급 기능을 마스터합니다

---

## 9. Flux 모델 특수 설정

### 🎯 핵심 개념

**Flux = Transformer 기반의 차세대 이미지 생성 모델**

일반 SD 모델과는 구조와 로딩 방식이 다릅니다.

### 📊 SD vs Flux 비교

| 항목 | SD 1.5 / SDXL | Flux Dev / Schnell |
|------|--------------|-------------------|
| **아키텍처** | UNet (CNN) | DiT (Transformer) |
| **텍스트 이해** | 보통 | 우수 ⭐ |
| **구도 파악** | 약함 | 강함 ⭐ |
| **로딩 노드** | Load Checkpoint | Load Diffusion Model |
| **파일 구성** | 통합 | 분리 (UNet+VAE+CLIP) |
| **메모리 사용** | 낮음 | 높음 |
| **속도** | 빠름 | 상대적 느림 |

### 📁 Flux 폴더 구조

```
ComfyUI/models/
├── checkpoints/           # ❌ Flux는 여기 아님!
├── unet/                 # ✅ Flux 모델 파일
│   └── flux1-dev.safetensors
├── diffusion_models/     # ✅ Flux 대체 위치
├── vae/                  # VAE 파일
│   └── ae.safetensors
└── clip/                 # CLIP 인코더 파일
    ├── t5xxl_fp8_e4m3fn.safetensors
    └── clip_l.safetensors
```

### 🏗️ Flux 워크플로우 구조

```
[Load Diffusion Model]
├─ unet_name: "flux1-dev.safetensors"
└─ weight_dtype: "default"
    │
    └─→ [MODEL 출력]

[Load VAE]
├─ vae_name: "ae.safetensors"
    │
    └─→ [VAE 출력]

[Dual CLIP Loader]
├─ clip_name1: "t5xxl_fp8_e4m3fn.safetensors"
├─ clip_name2: "clip_l.safetensors"
└─ type: "flux"
    │
    └─→ [CLIP 출력]
          │
          ├─→ [CLIP Text Encode +]
          └─→ [CLIP Text Encode -]
                    ↓
              [KSampler]
```

### 🔧 Flux 설정 가이드

#### 필수 파일 다운로드

| 파일 | 용도 | 크기 | 위치 |
|------|------|------|------|
| `flux1-dev.safetensors` | 메인 모델 | ~12GB | `models/unet/` |
| `ae.safetensors` | VAE | ~320MB | `models/vae/` |
| `t5xxl_fp8_e4m3fn.safetensors` | Text Encoder | ~5GB | `models/clip/` |
| `clip_l.safetensors` | Text Encoder | ~1GB | `models/clip/` |

#### 노드 설정

**Load Diffusion Model:**
```
unet_name: flux1-dev.safetensors
weight_dtype: default
```

**Dual CLIP Loader:**
```
clip_name1: t5xxl_fp8_e4m3fn.safetensors
clip_name2: clip_l.safetensors
type: flux
```

**Load VAE:**
```
vae_name: ae.safetensors
```

### ⚙️ KSampler 권장 설정

**Flux는 SD와 다른 설정이 필요합니다:**

| 설정 | SD 권장값 | Flux 권장값 |
|------|----------|-----------|
| Steps | 30 | 20-25 |
| CFG | 7 | 3.5-5 |
| Sampler | euler | euler |
| Scheduler | normal | simple |

### 💡 Flux 장단점

**장점:**
- ✅ 프롬프트 이해력 우수
- ✅ 복잡한 구도 정확히 표현
- ✅ 위치 관계 정확
- ✅ 자연스러운 결과

**단점:**
- ❌ 메모리 사용량 높음 (12GB+ VRAM 권장)
- ❌ 생성 속도 느림
- ❌ 파일 크기 큼
- ❌ 노드 연결 복잡

### 🚨 주의사항

**Flux는 일반 SD 체크포인트가 아닙니다!**

```
❌ 잘못된 방법:
[Load Checkpoint] → flux1-dev.safetensors

✅ 올바른 방법:
[Load Diffusion Model] → flux1-dev.safetensors
[Load VAE] → ae.safetensors
[Dual CLIP Loader] → t5xxl + clip_l
```

### 🎨 Flux 프롬프트 작성 팁

Flux는 자연어를 더 잘 이해합니다:

```
SD 스타일:
"a cat, blue sky, high quality, 8k, detailed"

Flux 스타일:
"A cute orange cat sitting on a windowsill, 
looking out at a bright blue sky with fluffy clouds. 
The sunlight creates soft shadows on the cat's fur."
```

- 더 자연스러운 문장 사용
- 관계와 위치를 명확히 서술
- 세부 묘사 추가

### ✅ Flux 체크리스트

- [ ] 모든 필수 파일 다운로드 완료
- [ ] 파일을 올바른 폴더에 배치
- [ ] Load Diffusion Model 사용 (Load Checkpoint 아님)
- [ ] Dual CLIP Loader 설정
- [ ] KSampler 설정 조정 (CFG 낮게)
- [ ] 충분한 VRAM 확보 (12GB+)

[⬆️ 목차로 돌아가기](#-목차)

---

## 10. LoRA - 스타일 미세조정

### 🎯 핵심 개념

**LoRA (Low-Rank Adaptation) = 기존 모델에 특정 스타일을 추가하는 플러그인**

전체 모델을 새로 학습하지 않고, 일부만 조정하여 원하는 스타일을 적용합니다.

### 🔍 LoRA의 작동 원리

```
기존 모델 (100%)
    ↓
LoRA 적용 (5%만 수정)
    ↓
새로운 스타일 모델 (기존 능력 유지 + 새 스타일)
```

**비유:**
- **기존 모델** = 다양한 그림을 그릴 수 있는 화가
- **LoRA** = 특정 화풍을 배우는 단기 수업
- **결과** = 기본 실력 + 새로운 화풍

### 📊 LoRA vs 완전 미세조정

| 항목 | 완전 미세조정 | LoRA |
|------|-------------|------|
| **학습 데이터** | 수천 장 필요 | 수십 장으로 가능 |
| **학습 시간** | 수일 ~ 수주 | 수시간 |
| **파일 크기** | 2-7GB | 10-200MB |
| **기존 능력** | 손실 가능 | 유지됨 |
| **적용** | 모델 교체 | 플러그인 형태 |

### 🎨 LoRA 활용 예시

**1. 화풍 LoRA:**
```
Base Model: realisticVision
+ Watercolor LoRA
= 수채화 스타일 이미지 생성
```

**2. 캐릭터 LoRA:**
```
Base Model: anyDreamer
+ Specific Character LoRA
= 특정 캐릭터 일관성 있게 생성
```

**3. 컨셉 LoRA:**
```
Base Model: SDXL
+ Cyberpunk LoRA
= 사이버펑크 스타일 강화
```

### 🏗️ ComfyUI에서 LoRA 사용

```
[Load Checkpoint]
    ↓
[MODEL]
    ↓
[Load LoRA]
├─ model: Load Checkpoint의 MODEL
├─ clip: Load Checkpoint의 CLIP
├─ lora_name: "watercolor_style.safetensors"
└─ strength_model: 0.8
└─ strength_clip: 0.8
    ↓
[수정된 MODEL] → [KSampler]
[수정된 CLIP] → [CLIP Text Encode]
```

### ⚙️ LoRA 강도 설정

| Strength | 효과 | 사용 상황 |
|----------|------|----------|
| **0.3-0.5** | 은은한 효과 | 스타일 힌트만 |
| **0.6-0.8** | 중간 효과 | 일반적 사용 ✅ |
| **0.9-1.0** | 강한 효과 | 스타일 강조 |
| **1.0+** | 매우 강함 | 특수한 경우 |

**주의:** 너무 높으면 이미지 품질 저하 가능

### 📁 LoRA 파일 위치

```
ComfyUI/models/
└── loras/
    ├── watercolor_style.safetensors
    ├── cyberpunk_aesthetic.safetensors
    └── character_lora.safetensors
```

### 🔗 여러 LoRA 동시 사용

```
[Load Checkpoint]
    ↓
[Load LoRA 1] - Watercolor Style (0.8)
    ↓
[Load LoRA 2] - Soft Lighting (0.6)
    ↓
[Load LoRA 3] - Detail Enhancer (0.5)
    ↓
[KSampler]
```

**주의점:**
- 너무 많이 사용하면 충돌 가능
- 2-3개가 적당
- 각 LoRA의 강도를 조절하여 균형 맞추기

### 💡 LoRA 선택 가이드

**좋은 LoRA 특징:**
- 명확한 목적 (화풍, 캐릭터, 개념)
- 적절한 학습 데이터
- 활발한 커뮤니티 피드백
- 다양한 예시 이미지

**LoRA 다운로드 사이트:**
- Civitai (civitai.com)
- Hugging Face (huggingface.co)

### 🎯 LoRA vs ControlNet

| 기능 | LoRA | ControlNet |
|------|------|------------|
| **목적** | 스타일 변경 | 구조 제어 |
| **적용 방식** | 모델 가중치 수정 | 추가 입력 제공 |
| **파일 크기** | 작음 (10-200MB) | 큼 (1-2GB) |
| **사용 난이도** | 쉬움 | 중간 |
| **효과** | 전체 스타일 | 구조적 제어 |

### ✅ LoRA 체크리스트

- [ ] LoRA 파일을 `models/loras/` 폴더에 배치
- [ ] Load LoRA 노드 추가
- [ ] MODEL과 CLIP 모두 연결
- [ ] 강도를 0.6-0.8로 시작
- [ ] 결과 확인 후 강도 조정
- [ ] 여러 LoRA 사용 시 충돌 주의

[⬆️ 목차로 돌아가기](#-목차)

---

## 11. ControlNet - 구조 제어

### 🎯 핵심 개념

**ControlNet = 이미지 구조를 제어하는 가이드 시스템**

LoRA가 "스타일"을 바꾼다면, ControlNet은 "구조"를 지정합니다.

### 🔍 LoRA vs ControlNet 핵심 차이

```
LoRA:
[Base Model] + [Style Adjustment] = [Styled Image]
"이런 스타일로 그려줘"

ControlNet:
[Base Model] + [Structure Guide] = [Structured Image]
"이 구도대로 그려줘"
```

### 📊 비교표

| 항목 | LoRA | ControlNet |
|------|------|------------|
| **조정 대상** | 모델 내부 가중치 | 생성 과정 입력 |
| **목적** | 스타일/화풍 변경 | 구조/포즈 유지 |
| **입력** | 없음 (자동 적용) | 참조 이미지 필요 |
| **예시** | "수채화 스타일로" | "이 스케치 구도로" |
| **파일 크기** | 10-200MB | 1-2GB |
| **동시 사용** | 가능 ✅ | 가능 ✅ |

### 🎨 ControlNet 종류

| 타입 | 추출 정보 | 활용 |
|------|----------|------|
| **Canny** | 윤곽선 | 스케치 → 이미지 |
| **Depth** | 깊이 정보 | 3D 구조 유지 |
| **OpenPose** | 인체 포즈 | 자세 일관성 |
| **Scribble** | 간단한 그림 | 러프 스케치 → 완성작 |
| **Normal** | 표면 방향 | 정밀한 3D 형태 |
| **Lineart** | 선화 | 라인아트 → 채색 |

### 🏗️ ControlNet 작동 흐름

```
1. 입력 이미지 준비
   [참조 이미지] (예: 사진)
        ↓
2. 전처리
   [Preprocessor] (예: Canny Edge Detection)
        ↓
   [구조 정보 추출] (윤곽선만)
        ↓
3. ControlNet 적용
   [ControlNet Model]
        ↓
   [KSampler] + [구조 가이드]
        ↓
4. 생성
   [새 이미지] (구조는 유지, 스타일은 새로)
```

### 🔧 ComfyUI 연결 예시

```
[Load Image] (참조 이미지)
    ↓
[ControlNet Preprocessor: Canny]
    ↓
[ControlNet Model Loader]
├─ control_net_name: "control_canny.pth"
    ↓
[Apply ControlNet]
├─ conditioning: CLIP Text Encode 출력
├─ control_net: ControlNet Model
├─ image: Preprocessor 출력
└─ strength: 0.8
    ↓
[KSampler]
```

### 💡 실전 활용 예시

**1. 스케치 → 완성 이미지**
```
손그림 스케치 (Canny)
    ↓
Prompt: "a beautiful landscape, oil painting"
    ↓
스케치 구도 유지 + 유화 스타일 적용
```

**2. 포즈 복사**
```
참조 사진 (OpenPose)
    ↓
Prompt: "anime character, cute girl, colorful"
    ↓
같은 포즈의 애니메이션 캐릭터 생성
```

**3. 3D 구조 유지**
```
3D 렌더링 (Depth)
    ↓
Prompt: "cyberpunk city, neon lights"
    ↓
3D 구조 유지 + 사이버펑크 스타일
```

### ⚙️ ControlNet 강도 설정

| Strength | 효과 | 사용 상황 |
|----------|------|----------|
| **0.3-0.5** | 약한 가이드 | 참고만 |
| **0.6-0.8** | 중간 제어 | 일반적 ✅ |
| **0.9-1.0** | 강한 제어 | 정확한 복제 |

### 🔗 LoRA + ControlNet 동시 사용

```
[Load Checkpoint]
    ↓
[Load LoRA] (스타일 조정)
    ↓
[Apply ControlNet] (구조 제어)
    ↓
[KSampler]
    ↓
스타일 + 구조 모두 적용된 이미지
```

**예시:**
```
Base Model: SDXL
+ Watercolor LoRA (스타일)
+ Canny ControlNet (구조)
= 수채화 스타일 + 특정 구도
```

### 📁 파일 위치

```
ComfyUI/models/
└── controlnet/
    ├── control_canny.pth
    ├── control_depth.pth
    ├── control_openpose.pth
    └── control_lineart.pth
```

### 🚨 주의사항

**ControlNet은 무겁습니다:**
- VRAM 사용량 증가
- 생성 속도 느려짐
- 여러 개 동시 사용 시 메모리 부족 가능

**권장 사양:**
- 12GB+ VRAM (안정적 사용)
- 8GB VRAM (1개 사용 가능)

### ✅ ControlNet 체크리스트

- [ ] 참조 이미지 준비
- [ ] 적절한 Preprocessor 선택
- [ ] ControlNet 모델 다운로드 및 배치
- [ ] Strength 0.7-0.8로 시작
- [ ] 메모리 사용량 모니터링
- [ ] LoRA와 조합하여 스타일+구조 제어

### 🎯 결론

| 목적 | 사용 도구 |
|------|----------|
| 스타일만 변경 | **LoRA** |
| 구조만 제어 | **ControlNet** |
| 스타일 + 구조 | **LoRA + ControlNet** |

[⬆️ 목차로 돌아가기](#-목차)

---

## 12. 문제 해결 가이드

### 🚨 이미지가 안 나와요!

#### 증상 1: 아무 것도 생성되지 않음

```
체크리스트:
□ VAE Decode 노드가 있나요?
□ KSampler → VAE Decode → Save Image 순서로 연결?
□ Load Checkpoint에서 VAE가 VAE Decode에 연결?
□ Queue Prompt 버튼을 눌렀나요?
□ 콘솔에 에러 메시지가 있나요?
```

**해결:**
```
[KSampler] → [VAE Decode] → [Save Image]
           ↑
        [VAE]
```

#### 증상 2: Latent 이미지만 보임

```
문제: VAE Decode를 거치지 않음

❌ 잘못:
KSampler → Save Image

✅ 정답:
KSampler → VAE Decode → Save Image
```

### 🎨 이미지가 이상해요!

| 증상 | 원인 | 해결 |
|------|------|------|
| **과장되고 부자연스러움** | CFG 너무 높음 | CFG 7-8로 낮추기 |
| **흐릿하고 디테일 부족** | Steps 부족 | Steps 30-40으로 증가 |
| **프롬프트 무시** | CFG 너무 낮음 | CFG 7-10으로 높이기 |
| **색이 이상함** | VAE 문제 | 다른 VAE 시도 |
| **노이즈 많음** | Steps 부족 | Steps 증가 |

### 💥 메모리 부족 에러

#### Out of Memory (OOM)

**증상:**
```
RuntimeError: CUDA out of memory
```

**해결 방법:**

| 방법 | 효과 | 설정 |
|------|------|------|
| **이미지 크기 줄이기** | 높음 | 1024→512, 768→512 |
| **Batch 크기 줄이기** | 중간 | batch_size: 4→1 |
| **LoRA 개수 줄이기** | 낮음 | 2-3개 이하 |
| **ControlNet 비활성화** | 높음 | 임시로 제거 |
| **VAE 메모리 최적화** | 중간 | tiled VAE 사용 |

**추가 팁:**
```
1. ComfyUI 재시작
2. 다른 프로그램 종료
3. --lowvram 플래그로 실행
```

### 🐌 속도가 너무 느려요!

| 원인 | 해결 |
|------|------|
| **이미지 크기 큼** | 512×512로 시작 |
| **Steps 많음** | 30으로 줄이기 |
| **Sampler 느림** | euler로 변경 |
| **LoRA 많음** | 2개 이하로 줄이기 |
| **ControlNet 사용** | 필요시에만 사용 |

### 🔧 Flux 특수 문제

#### 문제: Flux 모델이 안 불러와짐

```
체크:
□ Load Diffusion Model 노드 사용? (Load Checkpoint 아님)
□ 파일이 models/unet/ 폴더에?
□ Dual CLIP Loader 설정?
□ 모든 파일 다운로드 완료?
```

#### 문제: Flux 결과가 이상함

```
설정 확인:
□ CFG가 3.5-5인가? (7 아님)
□ Scheduler가 simple인가?
□ Steps가 20-25인가?
```

### 🎭 프롬프트 관련 문제

#### 증상: 원하는 결과가 안 나옴

**체크리스트:**
```
□ 프롬프트를 영어로 작성?
□ 구체적으로 서술?
□ Negative Prompt 작성?
□ CFG가 적절한가?
```

**개선 예시:**

```
❌ 나쁜 프롬프트:
"cat"

✅ 좋은 프롬프트:
"a cute orange tabby cat sitting on a windowsill, 
looking at blue sky, high quality, detailed fur, 
soft natural lighting, 8k"

Negative:
"blurry, low quality, distorted, ugly, 
bad anatomy, watermark"
```

### 🔌 노드 연결 문제

#### 증상: 노드가 연결이 안 됨

**타입 불일치:**
```
MODEL 출력 → MODEL 입력 ✅
MODEL 출력 → LATENT 입력 ❌
IMAGE 출력 → LATENT 입력 ❌
```

**해결:**
- 같은 타입끼리 연결
- 변환 필요 시 VAE Encode/Decode 사용

### 📁 파일 경로 문제

#### Flux 파일이 인식 안 됨

```
올바른 경로:
ComfyUI/
└── models/
    ├── unet/
    │   └── flux1-dev.safetensors ✅
    ├── vae/
    │   └── ae.safetensors ✅
    └── clip/
        ├── t5xxl_fp8_e4m3fn.safetensors ✅
        └── clip_l.safetensors ✅

잘못된 경로:
ComfyUI/
└── models/
    └── checkpoints/
        └── flux1-dev.safetensors ❌
```

### 🔍 디버깅 체크리스트

문제 발생 시 순서대로 확인:

```
1. □ 콘솔 에러 메시지 확인
2. □ 모든 노드 연결 확인
3. □ VAE Decode 연결 확인
4. □ 파일 경로 확인
5. □ VRAM 사용량 확인
6. □ 설정값 기본값으로 초기화
7. □ ComfyUI 재시작
8. □ 간단한 워크플로우로 테스트
```

### 💡 자주 묻는 질문 (FAQ)

**Q: 이미지가 계속 같게 나와요**
A: Seed 값을 고정했나요? Seed를 -1로 설정하면 매번 랜덤 생성

**Q: Negative Prompt가 작동 안 하는 것 같아요**
A: CFG가 너무 낮거나 높을 수 있음. CFG 7-8 시도

**Q: LoRA 적용이 안 되는 것 같아요**
A: Strength를 0.8-1.0으로 높여보기. MODEL과 CLIP 모두 연결 확인

**Q: ControlNet이 너무 강해요**
A: Strength를 0.5-0.7로 낮추기

[⬆️ 목차로 돌아가기](#-목차)

---

## 13. 첫 워크플로우 실습

### 🎯 실습 목표

**완성 이미지:** "파란 하늘 배경의 귀여운 고양이"

초보자가 처음부터 끝까지 직접 만들어봅니다.

### 📋 준비물

```
필수:
□ ComfyUI 설치
□ SD 1.5 또는 SDXL 모델 1개
   예: realisticVision_v60.safetensors

선택:
□ LoRA 파일 (스타일 추가 시)
□ ControlNet (구조 제어 시)
```

### 🏗️ Step-by-Step 가이드

---

#### Step 1: 워크스페이스 준비

1. ComfyUI 실행
2. 빈 캔버스 확인
3. 노드 추가 준비

```
우클릭 → Add Node → [원하는 노드]
```

---

#### Step 2: 모델 로드 (5분)

**추가할 노드:**
```
Add Node → loaders → Load Checkpoint
```

**설정:**
```
ckpt_name: "realisticVision_v60.safetensors"
```

**출력 확인:**
- MODEL (초록색)
- CLIP (노란색)
- VAE (보라색)

---

#### Step 3: 프롬프트 작성 (5분)

**Positive Prompt 노드 추가:**
```
Add Node → conditioning → CLIP Text Encode (Prompt)
```

**연결:**
```
Load Checkpoint [CLIP] → CLIP Text Encode [clip]
```

**입력 텍스트:**
```
a cute orange tabby cat sitting on a windowsill, 
looking at bright blue sky with white clouds, 
natural lighting, high quality, detailed, 
photorealistic, 8k
```

**Negative Prompt 노드 추가:**
```
Add Node → conditioning → CLIP Text Encode (Prompt)
```

**연결:**
```
Load Checkpoint [CLIP] → CLIP Text Encode [clip]
```

**입력 텍스트:**
```
blurry, low quality, distorted, ugly, 
bad anatomy, extra limbs, deformed, 
watermark, text, signature, cartoon
```

---

#### Step 4: 빈 캔버스 생성 (2분)

**노드 추가:**
```
Add Node → latent → Empty Latent Image
```

**설정:**
```
width: 512
height: 512
batch_size: 1
```

---

#### Step 5: KSampler 설정 (5분)

**노드 추가:**
```
Add Node → sampling → KSampler
```

**연결:**
```
Load Checkpoint [MODEL] → KSampler [model]
CLIP Text Encode (Positive) [CONDITIONING] → KSampler [positive]
CLIP Text Encode (Negative) [CONDITIONING] → KSampler [negative]
Empty Latent Image [LATENT] → KSampler [latent_image]
```

**설정:**
```
seed: 12345 (또는 원하는 숫자)
control_after_generate: randomize (매번 다른 결과)
steps: 30
cfg: 7
sampler_name: euler
scheduler: normal
denoise: 1.0
```

---

#### Step 6: 이미지 복원 (3분)

**VAE Decode 노드 추가:**
```
Add Node → latent → VAE Decode
```

**연결:**
```
KSampler [LATENT] → VAE Decode [samples]
Load Checkpoint [VAE] → VAE Decode [vae]
```

---

#### Step 7: 저장 (2분)

**Save Image 노드 추가:**
```
Add Node → image → Save Image
```

**연결:**
```
VAE Decode [IMAGE] → Save Image [images]
```

**설정:**
```
filename_prefix: "cat_blue_sky"
```

---

#### Step 8: 실행! (1분)

1. **Queue Prompt** 버튼 클릭 (오른쪽 상단)
2. 진행 상황 확인
3. 완료 후 이미지 확인

```
진행 표시:
[████████░░] 80% (Step 24/30)
```

---

### 🔄 완성된 워크플로우 구조

```
[Load Checkpoint]
    ├─→ [MODEL] ────────────────→ [KSampler]
    ├─→ [CLIP] ──┬─→ [Text Encode +] ─→ [KSampler]
    │            └─→ [Text Encode -] ─→ [KSampler]
    └─→ [VAE] ──────────────────────→ [VAE Decode]

[Empty Latent Image] ─────────────→ [KSampler]

[KSampler] ─────────────────────→ [VAE Decode]

[VAE Decode] ───────────────────→ [Save Image]
```

---

### 📊 설정값 요약

| 노드 | 설정 | 값 |
|------|------|-----|
| **Empty Latent** | width × height | 512 × 512 |
| | batch_size | 1 |
| **KSampler** | seed | 12345 |
| | steps | 30 |
| | cfg | 7 |
| | sampler_name | euler |
| | scheduler | normal |
| | denoise | 1.0 |

---

### ✅ 결과 확인 체크리스트

생성된 이미지를 보고 확인:

```
□ 고양이가 보이나요?
□ 파란 하늘이 배경인가요?
□ 이미지가 선명한가요?
□ 프롬프트와 일치하나요?
□ 만족스러운가요?
```

---

### 🔧 결과 개선하기

**만족스럽지 않다면:**

#### 1. 프롬프트 수정
```
더 구체적으로:
"a cute ORANGE TABBY cat with GREEN EYES..."
```

#### 2. Seed 변경
```
seed: -1 (랜덤)
또는 다른 숫자 시도
```

#### 3. Steps 증가
```
steps: 30 → 40
```

#### 4. CFG 조정
```
프롬프트 무시: cfg: 7 → 10
너무 과장: cfg: 7 → 5
```

#### 5. Sampler 변경
```
sampler_name: euler → dpmpp_2m
```

---

### 🎨 다음 단계 도전

**기본이 익숙해졌다면:**

#### 레벨 1: 프롬프트 실험
```
- 다양한 주제 시도
- 스타일 키워드 추가 (watercolor, oil painting)
- 조명 효과 (sunset, golden hour)
```

#### 레벨 2: 이미지 크기 변경
```
width: 768
height: 768
```

#### 레벨 3: LoRA 추가
```
Add Node → loaders → Load LoRA
→ 스타일 변경 실험
```

#### 레벨 4: Batch 생성
```
batch_size: 4
→ 한 번에 4개 생성
```

#### 레벨 5: ControlNet
```
스케치나 참조 이미지 기반 생성
```

---

### 💾 워크플로우 저장

**워크플로우 저장하기:**
```
1. 메뉴 → Save → Save Workflow
2. 파일명: "cat_workflow.json"
3. 저장 위치: 원하는 폴더
```

**불러오기:**
```
1. 메뉴 → Load → Load Workflow
2. "cat_workflow.json" 선택
```

---

### 🎉 축하합니다!

첫 ComfyUI 워크플로우를 완성했습니다!

**배운 것:**
- ✅ 노드 연결 방법
- ✅ 프롬프트 작성
- ✅ KSampler 설정
- ✅ 이미지 생성 전체 흐름

**다음 학습:**
- PART III의 고급 기능들
- 다양한 스타일 실험
- LoRA와 ControlNet

[⬆️ 목차로 돌아가기](#-목차)

---

# 부록

---

## 용어 정리

| 용어 | 설명 |
|------|------|
| **Checkpoint** | 학습 완료된 AI 모델 파일 (.safetensors, .ckpt) |
| **Latent** | 압축된 이미지 상태 (사람이 볼 수 없음) |
| **VAE** | 이미지 압축/복원 도구 (Encode/Decode) |
| **CLIP** | 텍스트를 AI가 이해하는 형태로 변환 |
| **UNet** | SD 1.5/SDXL의 이미지 생성 아키텍처 |
| **Transformer/DiT** | Flux의 이미지 생성 아키텍처 |
| **Prompt** | 원하는 이미지를 설명하는 텍스트 |
| **Negative Prompt** | 원하지 않는 요소를 설명하는 텍스트 |
| **Steps** | 이미지를 다듬는 횟수 (높을수록 정밀) |
| **CFG (Scale)** | 프롬프트 준수 강도 (7-8 권장) |
| **Sampler** | 노이즈 제거 알고리즘 (euler, dpmpp_2m 등) |
| **Scheduler** | 노이즈 제거 일정 (normal, karras 등) |
| **Seed** | 랜덤 시작점 (같은 숫자 = 비슷한 결과) |
| **Denoise** | 노이즈 제거 강도 (1.0 = 완전 생성) |
| **LoRA** | 스타일 미세조정 플러그인 (10-200MB) |
| **ControlNet** | 구조 제어 도구 (1-2GB) |
| **Conditioning** | CLIP이 변환한 프롬프트 데이터 |
| **Batch Size** | 한 번에 생성할 이미지 개수 |

---

## 참고 자료

### 공식 문서
- [ComfyUI GitHub](https://github.com/comfyanonymous/ComfyUI)
- [Stable Diffusion 공식 문서](https://stability.ai)
- [Flux 모델 문서](https://blackforestlabs.ai)

### 커뮤니티
- [ComfyUI Discord](https://discord.gg/comfyui)
- [Reddit r/StableDiffusion](https://reddit.com/r/StableDiffusion)
- [Civitai - 모델/LoRA 공유](https://civitai.com)

### 학습 자료
- [ComfyUI YouTube 튜토리얼](https://youtube.com/results?search_query=comfyui+tutorial)
- [Hugging Face 모델 허브](https://huggingface.co)

### 유용한 도구
- [ComfyUI Manager](https://github.com/ltdrdata/ComfyUI-Manager) - 노드 관리
- [ComfyUI Workflows](https://comfyworkflows.com) - 워크플로우 공유
- [OpenPose Editor](https://github.com/fkunn1326/openpose-editor) - 포즈 편집

---

## 마무리

이 가이드는 ComfyUI를 처음 시작하는 분들을 위한 것입니다.

**기억하세요:**
- 실수해도 괜찮습니다
- 다양한 설정을 실험해보세요
- 커뮤니티에서 도움을 구하세요
- 즐기면서 배우세요! 🎨

**피드백:**
이 가이드에 대한 의견이나 추가 요청사항이 있다면
ComfyUI 커뮤니티에서 공유해주세요.

---

**작성일:** 2025년 11월  
**버전:** 1.0  
**대상:** ComfyUI 초보자 ~ 중급자

[⬆️ 목차로 돌아가기](#-목차)

---

**끝**

---

[🏠 홈으로](../../README.md)