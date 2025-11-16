[🏠 홈](../../README.md) | [📚 시작 가이드](README.md) | [➡️ PART II](part-02-workflow-practice.md)

---

# PART I - 핵심 개념

> AI 이미지 생성의 기초를 이해합니다

**학습 목표:**
- Latent Image가 무엇이고 왜 사용하는지 이해
- VAE의 압축/복원 원리 파악
- UNet과 Transformer 아키텍처 차이 이해
- 모델 구성 요소 구분하기

**예상 시간:** 20분

---

## 📑 목차

1. [Latent Image - 압축된 설계도](#1-latent-image---압축된-설계도)
2. [VAE - 압축과 복원 엔진](#2-vae---압축과-복원-엔진)
3. [아키텍처 비교: UNet vs Transformer](#3-아키텍처-비교-unet-vs-transformer)
4. [모델 구성 요소 이해하기](#4-모델-구성-요소-이해하기)

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

[⬆️ 목차로](#-목차)

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

[⬆️ 목차로](#-목차)

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

[⬆️ 목차로](#-목차)

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

[⬆️ 목차로](#-목차)

---

## 🎯 PART I 정리

**학습한 핵심 개념:**

1. **Latent Image** - 압축 공간에서 작업, 50배 빠른 처리
2. **VAE** - 압축(Encode)과 복원(Decode), 반드시 Decode 필요
3. **아키텍처** - UNet(지역적/빠름) vs Transformer(전역적/정확)
4. **모델 구성** - 아키텍처 ≠ Checkpoint ≠ Load 노드

**다음 단계:**

PART I의 개념을 이해했다면, 이제 실제 워크플로우를 만들 준비가 되었습니다!

[➡️ PART II - 워크플로우 실전](part-02-workflow-practice.md)

---

[🏠 홈](../../README.md) | [📚 시작 가이드](README.md) | [➡️ PART II](part-02-workflow-practice.md)
