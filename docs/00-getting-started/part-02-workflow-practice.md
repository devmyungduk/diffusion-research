[🏠 홈](../../README.md) | [📚 시작 가이드](README.md) | [⬅️ PART I](part-01-core-concepts.md) | [➡️ PART III](part-03-advanced-features.md)

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

## 🎯 PART II 정리

**학습한 실전 기술:**

1. **전체 워크플로우** - 7개 노드 연결 구조 이해
2. **KSampler** - Steps, CFG, Sampler 설정의 의미
3. **CLIP** - 텍스트를 AI가 이해하는 형태로 변환
4. **기본 워크플로우** - 실제 이미지 생성 가능

**다음 단계:**

기본 워크플로우가 익숙해졌다면, 이제 고급 기능으로 품질을 한층 높일 차례입니다!

[➡️ PART III - 고급 기능과 실전](part-03-advanced-features.md)

---

[🏠 홈](../../README.md) | [📚 시작 가이드](README.md) | [⬅️ PART I](part-01-core-concepts.md) | [➡️ PART III](part-03-advanced-features.md)
