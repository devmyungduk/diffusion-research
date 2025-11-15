[🏠 홈](../../../README.md) | [📚 전체 목차](../../../README.md#-전체-문서-목차)

---
# Flux Model Complete Guide

![Flux](https://img.shields.io/badge/Flux-v1.0-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-Educational-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Complete-success?style=for-the-badge)

> Flux 모델의 A-Z: 기초 개념부터 실전 구현까지  
> 강의용 기술문서 | ComfyUI 워크플로우 포함  
> 해당 파이프라인 구조와 수치는 공식 표준이 아닌 실험적 가이드로, 환경과 모델에 따라 달라질 수 있습니다.

---

## 📚 Table of Contents

### 📖 [Part 1: Core Concepts](#part-1-core-concepts)
- [SDXL vs SD 1.5 비교](#sdxl-vs-sd-15)
- [Flux Model 호환성](#flux-model-compatibility)
- [Flux Guidance 시스템](#flux-guidance-system)
- [Text Encoder 이해](#text-encoders)
- [Vector Space vs Latent Space](#vector-space-vs-latent-space)

### 🛠️ [Part 2: Practical Implementation](#part-2-practical-implementation)
- [Style Transfer Methods](#style-transfer-methods)
- [Flux Redux 구현](#flux-redux-implementation)
- [ControlNet 가이드](#controlnet-guide)
- [Storage Requirements](#storage-requirements)
- [Latent Space Visualization](#latent-visualization)

### 📌 [Quick Reference](#quick-reference)

---

## Part 1: Core Concepts

> 💡 Flux 모델의 핵심 개념과 아키텍처 이해

### SDXL vs SD 1.5

#### 핵심 차이점 비교

| 항목 | SD 1.5 | SDXL | Flux |
|:---:|:---:|:---:|:---:|
| **출시년도** | 2022 | 2023 | 2024 |
| **개발사** | Stability AI | Stability AI | Black Forest Labs |
| **Native Resolution** | 512×512 | 1024×1024 | 1024×1024 |
| **Parameters** | ~1B | ~3.5B | ~12B |
| **Architecture** | Latent Diffusion | Latent Diffusion | Rectified Flow |

#### 해상도 이해

```plaintext
SD 1.5:  512×512 기본 (768px 이상은 품질 저하)
         └─ 2022년 표준

SDXL:    1024×1024 기본 (3배 많은 파라미터)
         └─ 2023년 업그레이드

Flux:    1024×1024 + 완전히 새로운 아키텍처
         └─ 2024년 차세대 모델
```

> ⚠️ **중요**: SDXL ≠ SD 1.5 업그레이드가 아닌 **완전히 다른 모델**입니다.

[🔝 목차로 돌아가기](#-table-of-contents)

---

### Flux Model Compatibility

#### LoRA 호환성 매트릭스

| LoRA 종류 | SD 1.5 | SDXL | Flux | 상호 호환 |
|:---:|:---:|:---:|:---:|:---:|
| **SD 1.5 LoRA** | ✅ | ❌ | ❌ | ❌ |
| **SDXL LoRA** | ❌ | ✅ | ❌ | ❌ |
| **Flux LoRA** | ❌ | ❌ | ✅ | ❌ |

> 📦 **결론**: 각 모델 전용 LoRA 필요. Flux LoRA는 CivitAI/HuggingFace에서 수천 개 이용 가능

#### IPAdapter 상태

| IPAdapter 타입 | SD 1.5/SDXL | Flux | 성숙도 |
|:---:|:---:|:---:|:---:|
| **Standard IPAdapter** | ✅ 완벽 지원 | ❌ 불가능 | - |
| **Flux-specific** | ❌ | ⚠️ 실험적 | 🟡 Early stage |

**💡 실전 팁:**
- ✅ Flux LoRA: Production-ready
- ⚠️ Flux IPAdapter: Experimental (Redux 권장)

[🔝 목차로 돌아가기](#-table-of-contents)

---

### Flux Guidance System

#### FluxGuidance의 역할

> 🎯 **FluxGuidance** = Flux의 프롬프트 충실도 제어 시스템

#### SD vs Flux 비교

| 모델 | Guidance 방식 | 위치 | 기본값 |
|:---:|:---:|:---:|:---:|
| **SD 1.5/SDXL** | CFG Scale | KSampler 내부 | 7.0~8.0 |
| **Flux** | Guidance (Distilled) | FluxGuidance 노드 | 3.5 |

#### 파이프라인 구조 비교

**SD 1.5/SDXL 파이프라인:**
```plaintext
Text Encoder → KSampler (CFG=7.0) → Output
```

**Flux 파이프라인:**
```plaintext
Text Encoder → FluxGuidance (3.5) → KSampler (CFG=1.0) → Output
                    ↓
            Guidance가 conditioning에 미리 적용됨
```

#### 기술적 차이점

| 특성 | SD CFG | Flux Guidance |
|:---:|:---:|:---:|
| **처리 시점** | Sampling 중 매 스텝 | Conditioning 단계 (사전 적용) |
| **계산 횟수** | 2번 (conditional + unconditional) | 1번 (distilled) |
| **속도** | 느림 (2x 연산) | 빠름 (1x 연산) |
| **값 범위** | 1~30 (보통 7~8) | 1~10 (보통 3~4) |

#### FluxGuidance 값 설정 가이드

| Guidance 값 | 효과 | 추천 용도 |
|:---:|:---:|:---:|
| **1.0~2.0** | 매우 자유로운 해석 | 추상적/예술적 작업 |
| **3.5** ⭐ | **최적 균형** | **대부분의 경우 (기본값)** |
| **4.0~5.0** | 프롬프트에 더 충실 | 정확한 복제 필요시 |
| **6.0+** | 과도하게 강조 | ⚠️ 비권장 (아티팩트) |

> 💡 **왜 3.5가 기본값?** Black Forest Labs의 수천 번 테스트 결과 최적 균형점

#### CFG in Flux

**❌ 잘못된 이해:**
```plaintext
Flux도 KSampler CFG를 사용한다
```

**✅ 올바른 이해:**
```plaintext
Flux는 CFG=1.0 고정 (CFG 비활성화)
대신 FluxGuidance 노드로 제어
```

| CFG 값 | 의미 |
|:---:|:---:|
| **1.0** | CFG 비활성화 (Guidance 없음) |
| **> 1.0** | CFG 활성화 |

**Flux에서 KSampler CFG는 항상 1.0으로 고정!**

[🔝 목차로 돌아가기](#-table-of-contents)

---

### Text Encoders

#### T5XXL 이해

**T5 = Text-to-Text Transfer Transformer**

| 구성 | 의미 | 설명 |
|:---:|:---:|:---:|
| **T5** | Text-to-Text Transfer Transformer | Google AI 2019년 모델 |
| **XXL** | eXtra eXtra Large | 11B parameters |

##### T5의 역할

```plaintext
Text Prompt: "a cat wearing a hat"
      ↓
  T5XXL Encoder  (텍스트 → 4096차원 벡터 변환)
      ↓
Text Embeddings: [sequence_length × 4096]
      ↓
  Flux Model에 전달 (이미지 생성 가이드)
```

##### T5XXL 파일 크기

| 파일명 | 크기 | 정밀도 | 권장 RAM |
|:---:|:---:|:---:|:---:|
| `t5xxl_fp16.safetensors` | 9.79 GB | 16-bit | 32GB+ |
| `t5xxl_fp8_e4m3fn_scaled.safetensors` | ~4.9 GB | 8-bit | <32GB |

**📊 선택 가이드:**
- 💪 RAM 32GB 이상 → **FP16** (최고 품질)
- 💡 RAM 32GB 미만 → **FP8** (메모리 절약)

#### CLIP 이해

**CLIP = Contrastive Language-Image Pre-training**

##### 쉬운 암기법 📎

| 글자 | 쉬운 단어 | 역할 |
|:---:|:---:|:---:|
| **C** | **Connect** | 텍스트와 이미지 연결 |
| **L** | **Language** | 언어 이해 |
| **I** | **Image** | 이미지 이해 |
| **P** | **Pair** | 둘을 페어링 |

> 💡 **기억법**: CLIP = 📎 Paperclip처럼 텍스트와 이미지를 클립으로 연결

##### Flux의 이중 텍스트 인코더

```plaintext
Text → CLIP → Text Embeddings (768-dim)
              ↓
          Flux Model  ← 이중 인코더 사용
              ↓
Text → T5XXL → Text Embeddings (4096-dim)
```

**역할 분담:**
- **CLIP**: 짧고 빠른 이해 (기본 개념)
- **T5XXL**: 깊고 정확한 이해 (세부 사항)

[🔝 목차로 돌아가기](#-table-of-contents)

---

### Vector Space vs Latent Space

#### 핵심 차이점

| 구분 | Vector Space | Latent Space |
|:---:|:---:|:---:|
| **생성자** | Text Encoder (T5/CLIP) | VAE Encoder |
| **표현 대상** | 텍스트 의미/개념 | 이미지 시각 정보 |
| **차원** | (seq_len, 4096) | (128, 128, 16) |
| **역할** | **WHAT** to generate | **HOW** image looks |
| **공간 타입** | Semantic embedding | Compressed visual |

#### Complete Flux Pipeline

```plaintext
┌─────────────────────────────┐
│   Text Prompt               │  User Input
│   "a cat wearing a hat"     │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│  T5XXL + CLIP Encoder       │  Vector Space 생성
│  Text → Embeddings          │  (4096-dim vectors)
└──────────────┬──────────────┘
               ↓ (conditioning/guidance)
┌─────────────────────────────┐
│  Random Noise               │  Starting point
│  (128×128×16)               │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│  Flux Diffusion Model       │  Latent Space 조작
│  (Guided Denoising)         │  (Guided by text vectors)
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│  Denoised Latent            │  Clean latent
│  (128×128×16)               │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│  VAE Decoder                │  Latent → Image
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│  Final Image                │  Output
│  (1024×1024×3 RGB)          │
└─────────────────────────────┘
```

#### 관계 이해

**❓ 질문**: "Latent is constructed from vector?"

**✅ 답변**: "Latent is constructed **ACCORDING TO** vector guidance"

| 개념 | 올바름 | 설명 |
|:---:|:---:|:---:|
| Vector → Latent | ❌ | 벡터가 직접 Latent으로 변환 X |
| Vector **guides** Latent | ✅ | 벡터가 Latent 생성을 **가이드** |
| Separate spaces | ✅ | 서로 다른 공간, 다른 목적 |

#### 비유로 이해하기 🚗

```plaintext
Vector Space (T5/CLIP)  =  GPS 내비게이션
                           (목적지 안내)

Latent Space            =  자동차
                           (실제 이동하는 것)

Flux Model              =  운전자
                           (GPS 따라 운전)

💡 GPS가 길을 알려주지만, GPS가 자동차가 되는 건 아니다!
```

[🔝 목차로 돌아가기](#-table-of-contents)

---

## Part 2: Practical Implementation

> 🛠️ Flux 실전 구현: 스타일 트랜스퍼부터 시스템 요구사항까지

### Style Transfer Methods

#### 방법론 비교

| 방법 | 품질 | 속도 | 난이도 | 상태 |
|:---:|:---:|:---:|:---:|:---:|
| **Flux Redux** | ⭐⭐⭐⭐⭐ | 빠름 | 쉬움 | ✅ Official BFL |
| **Flux IPAdapter** | ⭐⭐⭐⭐ | 빠름 | 중간 | ⚠️ Community |
| **RF-Inversion** | ⭐⭐⭐⭐⭐ | 느림 | 고급 | ⚠️ Research |
| **Flux Kontext** | ⭐⭐⭐⭐⭐ | 빠름 | 중간 | ✅ Official BFL |

#### 용도별 추천

| 사용 목적 | 최적 방법 | 이유 |
|:---:|:---:|:---:|
| 🎨 빠른 스타일 트랜스퍼 | **Flux Redux** | 공식 지원, 간단함 |
| 🎮 스타일 + 구도 제어 | **IPAdapter + ControlNet** | 최고 제어력 |
| 🏆 최고 품질 결과 | **RF-Inversion** | 연구급 품질 |
| ✏️ 기존 이미지 편집 | **Flux Kontext** | 구도 보존 |

[🔝 목차로 돌아가기](#-table-of-contents)

---

### Flux Redux Implementation

> 🎯 Black Forest Labs 공식 스타일 트랜스퍼 어댑터

#### 특징
- ✅ 텍스트 프롬프트 없이 이미지 스타일 변형
- ✅ 단 129 MB 경량 모델
- ✅ Dev/Schnell 모두 호환

#### 필수 모델 다운로드

| 모델 파일 | 크기 | 위치 | 다운로드 |
|:---:|:---:|:---:|:---:|
| `flux1-redux-dev.safetensors` | 129 MB | `models/style_models/` | [HuggingFace](https://huggingface.co/black-forest-labs/FLUX.1-Redux-dev) |
| `sigclip_vision_patch14_384.safetensors` | ~350 MB | `models/clip_vision/` | [HuggingFace](https://huggingface.co/google/siglip-so400m-patch14-384) |
| `flux1-dev.safetensors` | 23.8 GB | `models/diffusion_models/` | Official Flux Dev |
| `t5xxl_fp16.safetensors` | 9.79 GB | `models/text_encoders/` | Standard |
| `clip_l.safetensors` | ~250 MB | `models/text_encoders/` | Standard |
| `ae.safetensors` | ~335 MB | `models/vae/` | Flux VAE |

#### Redux Workflow Diagram

```plaintext
┌──────────────────────────┐
│   Load Image             │  ← 스타일 참조 이미지
│   (Style Reference)      │
└───────────┬──────────────┘
            ↓
┌──────────────────────────┐
│  CLIPVisionLoader        │  ← sigclip_vision_384
└───────────┬──────────────┘
            ↓
┌──────────────────────────┐
│  CLIPVisionEncode        │  ← 이미지 → 벡터
└───────────┬──────────────┘
            ↓
┌──────────────────────────┐
│  StyleModelLoader        │  ← flux1-redux-dev
└───────────┬──────────────┘
            ↓
┌──────────────────────────┐
│  StyleModelApply         │  ← 스타일 conditioning
│  (strength = 0.8~1.0)    │
└───────────┬──────────────┘
            ↓
            ├──────────────────────┐
            ↓                      ↓
┌────────────────────┐   ┌────────────────────┐
│  CLIPTextEncode    │   │  FluxGuidance      │
│  (prompt)          │   │  (3.5)             │
└─────────┬──────────┘   └─────────┬──────────┘
          └──────────┬───────────────┘
                     ↓
          ┌────────────────────┐
          │    KSampler        │
          │    (CFG=1.0)       │
          │    (steps=20-30)   │
          └─────────┬──────────┘
                    ↓
          ┌────────────────────┐
          │    VAEDecode       │
          └─────────┬──────────┘
                    ↓
          ┌────────────────────┐
          │   SaveImage        │
          └────────────────────┘
```

#### Redux 노드 설정

| 노드 | 기능 | 핵심 설정 |
|:---:|:---:|:---:|
| **LoadImage** | 스타일 참조 로드 | - |
| **CLIPVisionLoader** | Vision 모델 | sigclip_vision_384 |
| **CLIPVisionEncode** | 이미지 인코딩 | - |
| **StyleModelLoader** | Redux 로드 | flux1-redux-dev |
| **StyleModelApply** | 스타일 적용 | strength: 0.8~1.0 |
| **DualCLIPLoader** | 텍스트 인코더 | t5xxl + clip_l |
| **CLIPTextEncodeFlux** | 프롬프트 | 텍스트 입력 |
| **UNETLoader** | Flux 모델 | flux1-dev |
| **FluxGuidance** | Guidance | 3.5 |
| **EmptyLatentImage** | Latent 생성 | 1024×1024 |
| **KSampler** | 샘플링 | steps:20-30, cfg:1.0 |
| **VAELoader** | VAE | ae.safetensors |
| **VAEDecode** | 디코딩 | - |
| **SaveImage** | 저장 | - |

#### Redux 파라미터 가이드

| 파라미터 | 권장값 | 효과 |
|:---:|:---:|:---:|
| **Style Strength** | 0.8~1.0 | 스타일 적용 강도 |
| **FluxGuidance** | 3.5 | 프롬프트 충실도 |
| **Steps** | 20~30 | 품질/속도 균형 |
| **Resolution** | 1024×1024 | Native 해상도 |

[🔝 목차로 돌아가기](#-table-of-contents)

---

### ControlNet Guide

> ⚠️ **중요**: Flux 전용 ControlNet 필수! SD 1.5/SDXL ControlNet 사용 불가

#### Flux ControlNet 종류

##### 1️⃣ Black Forest Labs 공식 (Full Models)

| 모델 | 크기 | 타입 | 위치 |
|:---:|:---:|:---:|:---:|
| `flux1-canny-dev.safetensors` | 23.8 GB | Full model | `models/diffusion_models/` |
| `flux1-depth-dev.safetensors` | 23.8 GB | Full model | `models/diffusion_models/` |

**특징:**
- ✅ 최고 품질
- ⚠️ Base 모델 대체 방식
- 💡 "Flux Tools"라고 불림

##### 2️⃣ Black Forest Labs 공식 (LoRA Versions)

| 모델 | 크기 | 타입 | 위치 |
|:---:|:---:|:---:|:---:|
| `flux1-canny-dev-lora.safetensors` | ~1-2 GB | LoRA | `models/loras/` |
| `flux1-depth-dev-lora.safetensors` | ~1-2 GB | LoRA | `models/loras/` |

**특징:**
- 💾 저장공간 절약
- ✅ Flux Dev에 어댑터로 적용
- 📊 Full 대비 약간의 품질 차이

##### 3️⃣ XLabs AI 커뮤니티 (V3) ⭐ 권장

| 모델 | 크기 | 위치 |
|:---:|:---:|:---:|
| `flux-canny-controlnet-v3.safetensors` | ~3.5 GB | `models/controlnet/` |
| `flux-depth-controlnet-v3.safetensors` | ~3.5 GB | `models/controlnet/` |
| `flux-hed-controlnet-v3.safetensors` | ~3.5 GB | `models/controlnet/` |

**다운로드:**
- [Canny V3](https://huggingface.co/XLabs-AI/flux-controlnet-canny-v3)
- [Depth V3](https://huggingface.co/XLabs-AI/flux-controlnet-depth-v3)
- [HED V3](https://huggingface.co/XLabs-AI/flux-controlnet-hed-v3)

**특징:**
- ⚖️ 크기/품질 최적 균형
- ✅ 전통적 ControlNet 방식
- 📐 1024×1024 학습됨

#### ControlNet 타입별 용도

| ControlNet | 추출 방법 | 최적 용도 |
|:---:|:---:|:---:|
| **Canny** | Canny Edge Detection | 선명한 윤곽선 유지 |
| **Depth** | Depth Map Estimation | 3D 공간/깊이 유지 |
| **HED** | HED Edge Detection | 부드러운 경계선 |

#### ControlNet 권장 설정

| ControlNet | Strength | 추천 상황 |
|:---:|:---:|:---:|
| **Depth** | 0.5~0.8 | 인물, 공간감 중요 |
| **HED** | 0.6~0.9 | 스타일 트랜스퍼, 유연한 구도 |
| **Canny** | 0.3~0.6 ⚠️ | 선명한 구조 (낮게!) |

> ⚠️ **Canny 주의**: 너무 강하면 구도 경직됨. **HED/Depth 우선 권장**

[🔝 목차로 돌아가기](#-table-of-contents)

---

### Storage Requirements

#### 📊 시나리오별 저장공간

##### Scenario A: Full Setup (최고 품질)

```plaintext
📦 Core Models
├─ flux1-dev.safetensors              : 23.8 GB
├─ t5xxl_fp16.safetensors             :  9.8 GB
├─ clip_l.safetensors                 :  0.3 GB
└─ ae.safetensors                     :  0.3 GB

🎨 Style Transfer
├─ flux1-redux-dev.safetensors        :  0.1 GB
└─ sigclip_vision_patch14_384         :  0.4 GB

🎮 ControlNet (Full Models)
├─ flux1-canny-dev.safetensors        : 23.0 GB
└─ flux1-depth-dev.safetensors        : 23.0 GB

────────────────────────────────────────
✨ Total                              : ~80 GB
```

##### Scenario B: LoRA Version (공간 절약) ⭐

```plaintext
📦 Core Models
├─ flux1-dev.safetensors              : 23.8 GB
├─ t5xxl_fp8_e4m3fn_scaled            :  4.9 GB
├─ clip_l.safetensors                 :  0.3 GB
└─ ae.safetensors                     :  0.3 GB

🎨 Style Transfer
├─ flux1-redux-dev.safetensors        :  0.1 GB
└─ sigclip_vision_patch14_384         :  0.4 GB

🎮 ControlNet (LoRA)
├─ flux1-canny-dev-lora               :  1.5 GB
└─ flux1-depth-dev-lora               :  1.5 GB

────────────────────────────────────────
💡 Total                              : ~33 GB
```

##### Scenario C: XLabs Community (균형) 🎯

```plaintext
📦 Core Models
├─ flux1-dev.safetensors              : 23.8 GB
├─ t5xxl_fp16.safetensors             :  9.8 GB
├─ clip_l.safetensors                 :  0.3 GB
└─ ae.safetensors                     :  0.3 GB

🎨 Style Transfer
├─ flux1-redux-dev.safetensors        :  0.1 GB
└─ sigclip_vision_patch14_384         :  0.4 GB

🎮 ControlNet (XLabs V3)
├─ flux-canny-controlnet-v3           :  3.5 GB
├─ flux-depth-controlnet-v3           :  3.5 GB
└─ flux-hed-controlnet-v3             :  3.5 GB

────────────────────────────────────────
⚖️ Total                              : ~45 GB
```

#### 사용자별 권장 구성

| 사용자 타입 | 권장 시나리오 | 이유 |
|:---:|:---:|:---:|
| 🌱 **입문자** | Scenario B | 저장공간 부담 최소 |
| 👤 **일반 사용자** | Scenario C ⭐ | 크기/품질 최적 균형 |
| 💼 **프로/연구자** | Scenario A | 최고 품질 필요 |

[🔝 목차로 돌아가기](#-table-of-contents)

---

### Latent Visualization

#### Latent vs Vector Space 시각화

| 공간 | 생성자 | 차원 | 시각화 가능성 |
|:---:|:---:|:---:|:---:|
| **Vector Space** | T5/CLIP | (seq_len, 4096) | ❌ 추상적 |
| **Latent Space** | VAE | (128, 128, 16) | ✅ 가능 (복원 필요) |

#### Latent 시각화 방법

##### Method 1: VAE Decode (가장 일반적)

```plaintext
Latent (128×128×16 channels)
        ↓
   VAE Decoder
        ↓
Image (1024×1024×3 RGB)  ← 우리가 보는 것!
```

##### Method 2: Per-Channel Heatmap

```plaintext
16 Channels → 16개의 Grayscale 히트맵

Channel 0:  ████████░░  ← Edge info
Channel 1:  ░░░██████░  ← Color info
Channel 2:  ░░░░░░████  ← Texture info
Channel 3:  ██░░░░░░██  ← Pattern info
...
Channel 15: ░█░█░█░█░█  ← High-freq noise
```

##### Method 3: RGB Mapping

```python
# 16채널 중 처음 3개를 RGB로 매핑
latent_visual = latent[:, :, 0:3]  # R, G, B
latent_visual = normalize(latent_visual)  # 0-255로 스케일
# → 추상적인 컬러 패턴으로 보임
```

#### Denoising 과정 시각화

| Step | Progress | Latent 상태 | 디코드 시 이미지 |
|:---:|:---:|:---:|:---:|
| **0** | 0% | Pure noise | 완전한 노이즈 |
| **5** | 25% | 초기 구조 | 흐릿한 형태 |
| **10** | 50% | 중간 형태 | 대략적인 구조 |
| **15** | 75% | 세부 디테일 | 거의 완성 |
| **20** | 100% | Clean latent | 완성된 이미지 |

#### ComfyUI 시각화 도구

| 노드/확장 | 기능 | 난이도 |
|:---:|:---:|:---:|
| **LatentPreview** | 실시간 미리보기 | 🟢 Easy |
| **TAESD** | 빠른 근사 디코딩 | 🟢 Easy |
| **Latent to RGB** | 채널 → RGB 변환 | 🟡 Medium |
| **Save Latent** | Raw latent 저장 | 🟡 Medium |

[🔝 목차로 돌아가기](#-table-of-contents)

---

## Quick Reference

### 📁 필수 파일 위치

| 파일 타입 | 위치 | 예시 |
|:---:|:---:|:---:|
| **Diffusion Models** | `ComfyUI/models/diffusion_models/` | flux1-dev.safetensors |
| **Text Encoders** | `ComfyUI/models/text_encoders/` | t5xxl_fp16.safetensors |
| **VAE** | `ComfyUI/models/vae/` | ae.safetensors |
| **LoRA** | `ComfyUI/models/loras/` | flux-lora-*.safetensors |
| **Style Models** | `ComfyUI/models/style_models/` | flux1-redux-dev.safetensors |
| **ControlNet** | `ComfyUI/models/controlnet/` | flux-depth-v3.safetensors |
| **CLIP Vision** | `ComfyUI/models/clip_vision/` | sigclip_vision_384.safetensors |

### ⚙️ 기본 Flux 파라미터

| 파라미터 | 권장값 | 설명 |
|:---:|:---:|:---:|
| **Resolution** | 1024×1024 | Native 해상도 |
| **FluxGuidance** | 3.5 | 기본 최적값 |
| **KSampler CFG** | 1.0 | 항상 고정! |
| **Steps** | 20~30 | 품질/속도 균형 |
| **Sampler** | Euler | 안정적 |
| **Scheduler** | Simple | 기본값 |

### 🔧 Troubleshooting

| 문제 | 원인 | 해결책 |
|:---:|:---:|:---:|
| **Out of Memory** | VRAM 부족 | FP8 모델, 해상도 낮춤 |
| **Redux 결과 이상** | CLIP Vision 오류 | sigclip_vision_384 확인 |
| **ControlNet 안 됨** | SD ControlNet 사용 | Flux 전용 사용 |
| **CFG 작동 안 됨** | CFG > 1.0 설정 | CFG=1.0, FluxGuidance 사용 |
| **생성 속도 느림** | FP16 + 고해상도 | FP8, 작은 해상도 테스트 |

### 💻 최소 시스템 요구사항

| 구성요소 | 최소 | 권장 |
|:---:|:---:|:---:|
| **VRAM** | 12 GB (FP8) | 24 GB (FP16) |
| **RAM** | 16 GB | 32 GB+ |
| **Storage** | 40 GB | 100 GB |
| **GPU** | RTX 3060 12GB | RTX 4090 |

### 📚 모델 약어 정리

| 약어 | 전체 이름 | 설명 |
|:---:|:---:|:---:|
| **T5** | Text-to-Text Transfer Transformer | 텍스트 인코더 |
| **CLIP** | Contrastive Language-Image Pre-training | 이미지-텍스트 매칭 |
| **VAE** | Variational AutoEncoder | 이미지 압축/복원 |
| **CFG** | Classifier-Free Guidance | 프롬프트 충실도 |
| **LoRA** | Low-Rank Adaptation | 경량 파인튜닝 |
| **FP8/FP16** | Float Point 8/16 | 모델 정밀도 |

[🔝 목차로 돌아가기](#-table-of-contents)

---

## 🔗 Resources

### Official Links
- [Black Forest Labs](https://blackforestlabs.ai/)
- [Flux Models (HuggingFace)](https://huggingface.co/black-forest-labs)
- [ComfyUI Examples](https://comfyanonymous.github.io/ComfyUI_examples/flux/)

### Community Resources
- [XLabs AI ControlNets](https://github.com/XLabs-AI/x-flux-comfyui)
- [CivitAI Flux Models](https://civitai.com/models?query=flux)
- [ComfyUI Manager](https://github.com/ltdrdata/ComfyUI-Manager)

---

## 📝 License

This document is provided for educational purposes.
- Flux models: Check individual model licenses
- ComfyUI: GPL-3.0 License

## 🤝 Contributing

Issues and improvements welcome!

---

## 📌 Version

- **Document Version**: 1.0
- **Last Updated**: 2025-11-12
- **Author**: Educational Purpose
- **Language**: Korean + English (Technical Terms)

---

<div align="center">

**[⬆️ Back to Top](#flux-model-complete-guide)**

Made with ❤️ for Flux learners

</div>
---

[🏠 홈으로](../../../README.md)