[🏠 홈](../../README.md) | [📚 시작 가이드](README.md) | [⬅️ PART II](part-02-workflow-practice.md) | [➡️ 부록](appendix.md)

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

## 🎯 PART III 정리

**학습한 고급 기능:**

1. **Flux 모델** - Transformer 기반 차세대 모델 설정
2. **LoRA** - 스타일 미세조정으로 다양한 표현
3. **ControlNet** - 구조 제어로 정밀한 결과
4. **문제 해결** - 일반적인 오류 디버깅
5. **첫 워크플로우 실습** - 실전 이미지 생성

**축하합니다!**

ComfyUI의 핵심 기능을 모두 마스터했습니다. 이제 자유롭게 실험하고 창작하세요!

[➡️ 부록 - 용어 정리 및 참고 자료](appendix.md)

---

[🏠 홈](../../README.md) | [📚 시작 가이드](README.md) | [⬅️ PART II](part-02-workflow-practice.md) | [➡️ 부록](appendix.md)
