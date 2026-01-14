[🏠 홈](../../README.md) | [📚 시작 가이드](README.md) | [⬅️ PART III](part-03-advanced-features.md)

---

# PART III - 실전 실습

> 문제 해결과 첫 워크플로우 만들기

**학습 목표:**
- 일반적인 문제 해결 방법 이해
- 처음부터 끝까지 워크플로우 직접 구축
- 결과 개선 방법 학습

**예상 시간:** 40분

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
