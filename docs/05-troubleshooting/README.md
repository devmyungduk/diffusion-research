# 문제 해결 가이드

> ComfyUI 사용 중 발생하는 일반적인 문제와 해결 방법

[🏠 홈](../../README.md) | [📚 전체 목차](../../docs/README.md)

---

## 🎯 가이드 개요

**대상 독자:** 에러 메시지를 보고 당황한 사용자
**사전 이해:** 없음
**예상 소요 시간:** 5분 (해결 시간)

**핵심 내용:**
- "빨간색 노드"가 떴을 때 대처법
- OOM (메모리 부족) 해결을 위한 설정 팁
- 이미지가 검게 나오거나 이상하게 나올 때의 체크리스트

---

## 📖 이 문서는?

ComfyUI 사용 중 발생할 수 있는 문제들과 해결 방법을 정리했습니다.

**대상:**
- 문제가 발생한 모든 사용자
- 최적화가 필요한 분
- 오류 메시지를 이해하고 싶은 분

---

## 📑 목차

1. [이미지 생성 문제](#1-이미지-생성-문제)
2. [메모리 관련 문제](#2-메모리-관련-문제)
3. [속도 최적화](#3-속도-최적화)
4. [품질 문제](#4-품질-문제)
5. [일반적인 오류](#5-일반적인-오류)

---

## 1. 이미지 생성 문제

### 🚨 이미지가 아예 안 나와요

#### 체크리스트
```
□ VAE Decode 노드가 있나요?
□ KSampler → VAE Decode → Save Image 순서?
□ 모든 선이 제대로 연결되었나요?
□ Queue Prompt 버튼을 눌렀나요?
□ 콘솔에 에러가 있나요?
```

#### 해결 방법
```
1. 연결 확인
   KSampler [LATENT] → VAE Decode [samples]
   Load Checkpoint [VAE] → VAE Decode [vae]

2. 노드 재배치
   모든 노드가 올바른 순서로 연결

3. 단순화 테스트
   기본 워크플로우로 테스트
```

---

### 🎨 Latent 이미지만 보여요

#### 원인
VAE Decode를 거치지 않음

#### 해결
```
❌ 잘못:
KSampler → Preview/Save Image

✅ 정답:
KSampler → VAE Decode → Preview/Save Image
```

---

### 🌫️ 이미지가 흐릿해요

#### 원인과 해결

| 원인 | 해결 |
|------|------|
| Steps 부족 | Steps 30-40으로 증가 |
| Denoise 낮음 | Denoise 1.0으로 설정 |
| 잘못된 해상도 | 모델 권장 해상도 사용 |
| VAE 문제 | 다른 VAE 시도 |

#### 권장 설정
```
SD 1.5:
- 해상도: 512×512
- Steps: 25-30
- Sampler: euler, dpmpp_2m

SDXL:
- 해상도: 1024×1024
- Steps: 30-40
- Sampler: dpmpp_2m_karras
```

[⬆️ 목차로](#-목차)

---

## 2. 메모리 관련 문제

### 💥 Out of Memory (OOM)

#### 증상
```
RuntimeError: CUDA out of memory
```

#### 즉시 해결법

**1단계: 이미지 크기 줄이기**
```
1024×1024 → 512×512
768×768 → 512×512
```

**2단계: Batch 크기 줄이기**
```
batch_size: 4 → 1
```

**3단계: 기타**
```
- LoRA 제거 또는 줄이기
- ControlNet 비활성화
- ComfyUI 재시작
```

---

### 📊 VRAM별 권장 설정

**4GB VRAM (최소)**
```
모델: SD 1.5만
크기: 512×512
Batch: 1
옵션: --lowvram 플래그 사용
```

**6GB VRAM**
```
모델: SD 1.5, SDXL (제한적)
크기: 512×512 (SD 1.5)
      768×768 (SDXL, 주의)
Batch: 1-2
```

**8GB VRAM**
```
모델: SD 1.5, SDXL
크기: 1024×1024 (SDXL)
Batch: 1-2
LoRA: 2-3개
```

**12GB+ VRAM**
```
모델: 모든 모델 (Flux 포함)
크기: 제한 없음
Batch: 4-8
LoRA/ControlNet: 자유롭게
```

---

### 🛠️ 최적화 방법

**VAE Tiling**
```
노드: VAE Encode (Tiled) / VAE Decode (Tiled)
효과: VRAM 사용량 50% 감소
단점: 약간 느림
```

**실행 플래그**
```
--lowvram: 메모리 절약 (느림)
--normalvram: 기본 (권장)
--highvram: 속도 우선 (메모리 많을 때)
```

[⬆️ 목차로](#-목차)

---

## 3. 속도 최적화

### 🐌 생성이 너무 느려요

#### 원인 분석

| 원인 | 영향 | 해결 |
|------|------|------|
| 높은 해상도 | 큼 | 512×512로 시작 |
| 많은 Steps | 중간 | 20-30으로 줄이기 |
| 느린 Sampler | 중간 | euler로 변경 |
| 여러 LoRA | 작음 | 2-3개로 제한 |
| ControlNet | 큼 | 필요시만 사용 |

---

### ⚡ 빠른 테스트 설정

**초고속 (품질 희생)**
```
해상도: 512×512
Steps: 15
Sampler: euler
CFG: 7
```

**균형 (권장)**
```
해상도: 512×512
Steps: 25
Sampler: euler
CFG: 7
```

**고품질 (최종)**
```
해상도: 1024×1024
Steps: 40
Sampler: dpmpp_2m_karras
CFG: 7
```

---

### 📈 단계별 최적화

**1. 테스트 단계**
```
- 512×512
- Steps 20
- 빠른 반복
```

**2. 개선 단계**
```
- 768×768
- Steps 30
- 세밀한 조정
```

**3. 최종 단계**
```
- 1024×1024
- Steps 40
- 최고 품질
```

[⬆️ 목차로](#-목차)

---

## 4. 품질 문제

### 😕 프롬프트를 무시해요

#### 원인
- CFG가 너무 낮음
- 프롬프트가 불명확
- 모델이 개념을 모름

#### 해결

**CFG 조정**
```
현재 CFG 5 미만 → 7-10으로 높이기
```

**프롬프트 개선**
```
❌ 나쁜 예:
"cat"

✅ 좋은 예:
"a cute orange tabby cat sitting on windowsill,
blue sky background, natural lighting,
high quality, detailed, photorealistic"
```

**강조 기법**
```
(keyword:1.2) - 20% 강조
(keyword:1.5) - 50% 강조
(keyword:0.8) - 20% 약화
```

---

### 🎭 이미지가 과장되었어요

#### 원인
CFG가 너무 높음

#### 해결
```
현재 CFG 10 이상 → 7-8로 낮추기

적정 범위:
- SD 1.5: CFG 7-8
- SDXL: CFG 7-9
- Flux: CFG 3.5-5
```

---

### 🎨 색감이 이상해요

#### 원인과 해결

| 원인 | 해결 |
|------|------|
| 잘못된 VAE | 다른 VAE 시도 |
| 과도한 LoRA | Strength 낮추기 |
| 프롬프트 충돌 | 명확하게 수정 |

**VAE 선택**
```
SD 1.5: vae-ft-mse-840000-ema-pruned
SDXL: sdxl_vae
Flux: ae.safetensors
```

[⬆️ 목차로](#-목차)

---

## 5. 일반적인 오류

### ❌ Model file not found

#### 원인
파일이 올바른 위치에 없음

#### 해결
```
파일 위치 확인:
- Checkpoint: ComfyUI/models/checkpoints/
- LoRA: ComfyUI/models/loras/
- VAE: ComfyUI/models/vae/
- ControlNet: ComfyUI/models/controlnet/

Flux 특수 위치:
- Diffusion: ComfyUI/models/unet/
- CLIP: ComfyUI/models/clip/
```

---

### ❌ Invalid node type

#### 원인
커스텀 노드 누락 또는 업데이트 필요

#### 해결
```
1. ComfyUI Manager 확인
2. 필요한 커스텀 노드 설치
3. ComfyUI 재시작
```

---

### ❌ Connection failed

#### 원인
노드 타입 불일치

#### 해결
```
올바른 연결:
✅ MODEL → MODEL
✅ CLIP → CLIP
✅ LATENT → LATENT
✅ IMAGE → IMAGE
✅ VAE → VAE

잘못된 연결:
❌ IMAGE → LATENT
❌ MODEL → CLIP
```

[⬆️ 목차로](#-목차)

---

## 🔍 디버깅 프로세스

### 문제 발생 시 순서

```
1. 콘솔 에러 메시지 확인
   ↓
2. 모든 노드 연결 검토
   ↓
3. 기본 워크플로우로 테스트
   ↓
4. 한 번에 하나씩 추가
   ↓
5. 문제 노드/설정 특정
   ↓
6. 해결 또는 대안 찾기
```

---

## 💡 예방 팁

### 안정적인 작업 환경

**1. 정기적 저장**
```
워크플로우를 자주 저장
- Save → Save Workflow
- 버전별로 파일명 구분
```

**2. 점진적 변경**
```
한 번에 하나씩만 수정
- 문제 원인 특정 쉬움
- 롤백 용이
```

**3. 백업 유지**
```
작동하는 워크플로우 백업
- 기본 템플릿 보관
- 프로젝트별 저장
```

---

## 📚 추가 자원

### 도움받을 곳

**공식:**
- [ComfyUI GitHub Issues](https://github.com/comfyanonymous/ComfyUI/issues)
- [ComfyUI Discord](https://discord.gg/comfyui)

**커뮤니티:**
- Reddit r/StableDiffusion
- ComfyUI 관련 포럼

**한국어:**
- 관련 디스코드 서버
- 커뮤니티 포럼

---

## 🆘 긴급 해결법

### 완전히 막혔을 때

```
1. ComfyUI 완전 재시작
2. 기본 예제 워크플로우 로드
3. 한 단계씩 다시 구축
4. 문제 발생 지점 특정
5. 해당 부분만 수정
```

---

**🔧 문제 해결 성공하셨기를 바랍니다!**

---

[🏠 홈으로](../../README.md) | [📖 시작 가이드로](../00-getting-started/README.md)
