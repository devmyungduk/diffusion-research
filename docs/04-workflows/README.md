# 실전 워크플로우 모음

> 다양한 상황별 ComfyUI 워크플로우 예제

[🏠 홈](../../README.md) | [📚 전체 목차](../../docs/README.md)

---

## 🎯 가이드 개요

**대상 독자:** 이론보다는 실제 "돌아가는 예제"가 필요한 사용자
**사전 이해:** ComfyUI 노드 추가/연결 방법
**예상 소요 시간:** 5분 (탐색 시간)

**핵심 내용:**
- 바로 복사해서 쓸 수 있는 검증된 워크플로우 모음 (JSON)
- Inpainting, Upscaling 등 목적별 템플릿 제공
- 복잡한 노드 구성을 한눈에 파악하는 예제

---

## 📖 이 문서는?

실전에서 자주 사용하는 ComfyUI 워크플로우들을 모아놓았습니다.

**대상:**
- 기본 워크플로우를 이해한 분
- 다양한 생성 방법을 배우고 싶은 분
- 실전 예제가 필요한 분

---

## 📑 목차

1. [기본 Text-to-Image](#1-기본-text-to-image)
2. [Image-to-Image](#2-image-to-image)
3. [LoRA 스타일 적용](#3-lora-스타일-적용)
4. [고해상도 업스케일](#4-고해상도-업스케일)
5. [배치 생성](#5-배치-생성)

---

## 1. 기본 Text-to-Image

### 🎯 목적
프롬프트만으로 새 이미지 생성

### 🏗️ 워크플로우

```
[Load Checkpoint]
    ├─→ MODEL → [KSampler]
    ├─→ CLIP → [Text Encode +/-]
    └─→ VAE → [VAE Decode]

[Empty Latent Image] → [KSampler]
[KSampler] → [VAE Decode] → [Save Image]
```

### 📝 설정 예시

**프롬프트:**
```
Positive: 
a beautiful sunset over mountains,
vibrant colors, dramatic lighting,
high quality, detailed, 8k

Negative:
blurry, low quality, distorted,
watermark, text
```

**설정:**
```
Size: 512×512 (SD 1.5) or 1024×1024 (SDXL)
Steps: 30
CFG: 7
Sampler: euler or dpmpp_2m
```

### 💡 활용
- 컨셉 아트
- 아이디어 스케치
- 빠른 프로토타입

[⬆️ 목차로](#-목차)

---

## 2. Image-to-Image

### 🎯 목적
기존 이미지를 수정하거나 스타일 변경

### 🏗️ 워크플로우

```
[Load Image]
    ↓
[VAE Encode]
    ↓
[KSampler] (denoise < 1.0)
    ↓
[VAE Decode]
    ↓
[Save Image]
```

### 📝 설정 예시

**Denoise 강도:**
```
0.3-0.4: 약간만 수정 (색감, 조명)
0.5-0.7: 중간 수정 (스타일 변경) ✅
0.8-0.9: 많이 수정 (거의 새로 생성)
```

**프롬프트:**
```
Positive:
[원하는 스타일], based on reference,
maintain composition, high quality

Negative:
deformed, distorted, low quality
```

### 💡 활용
- 스타일 변환 (사진 → 그림)
- 색감 조정
- 디테일 개선

[⬆️ 목차로](#-목차)

---

## 3. LoRA 스타일 적용

### 🎯 목적
특정 스타일이나 화풍 추가

### 🏗️ 워크플로우

```
[Load Checkpoint]
    ↓
[Load LoRA 1] (Watercolor 0.8)
    ↓
[Load LoRA 2] (Lighting 0.5)
    ↓
[KSampler]
    ↓
[VAE Decode]
    ↓
[Save Image]
```

### 📝 설정 예시

**LoRA 조합:**
```
1. 스타일 LoRA (0.7-0.9)
   └─ 수채화, 유화, 애니메이션 등

2. 보조 LoRA (0.4-0.6)
   └─ 조명, 디테일, 분위기 등
```

**프롬프트 팁:**
```
LoRA 스타일과 일치하는 키워드 사용
예: 수채화 LoRA + "watercolor painting"
```

### 💡 활용
- 일관된 스타일 유지
- 브랜드 아이덴티티
- 시리즈 작업

[⬆️ 목차로](#-목차)

---

## 4. 고해상도 업스케일

### 🎯 목적
작은 이미지를 고해상도로 확대

### 🏗️ 워크플로우 (2단계)

**1단계: 기본 생성**
```
[KSampler] (512×512)
    ↓
[VAE Decode]
    ↓
[Upscale Image] (2x or 4x)
```

**2단계: 디테일 추가**
```
[Upscaled Image]
    ↓
[VAE Encode]
    ↓
[KSampler] (denoise 0.3-0.5)
    ↓
[VAE Decode]
    ↓
[Save Image] (1024×1024 or 2048×2048)
```

### 📝 설정 예시

**Upscale 방법:**
```
- Lanczos: 선명함
- Bilinear: 부드러움
- Nearest: 픽셀아트 유지
```

**Denoise (2단계):**
```
0.3: 최소 수정
0.4-0.5: 디테일 추가 ✅
0.6+: 너무 많이 변경
```

### 💡 활용
- 최종 결과물 고해상도화
- 인쇄용 이미지
- 포스터, 배너

[⬆️ 목차로](#-목차)

---

## 5. 배치 생성

### 🎯 목적
한 번에 여러 이미지 생성

### 🏗️ 워크플로우

```
[Empty Latent Image]
├─ batch_size: 4
    ↓
[KSampler]
├─ seed: -1 (랜덤)
    ↓
[VAE Decode]
    ↓
[Save Image]
└─ 4개 이미지 동시 생성
```

### 📝 설정 예시

**Batch Size:**
```
1: 일반 (기본)
4: 4개 동시 ✅ (메모리 충분 시)
8: 8개 동시 (12GB+ VRAM)
```

**Seed 설정:**
```
-1: 매번 다른 결과 (추천)
고정 숫자: 비슷한 결과들
```

### 💡 활용
- 다양한 옵션 비교
- 최적 결과 선택
- 시간 절약

### ⚠️ 주의사항
```
- VRAM 사용량 증가
- 배치 크기 = 메모리 × 배치
- 4개 권장 (8GB VRAM 기준)
```

[⬆️ 목차로](#-목차)

---

## 💡 워크플로우 조합 팁

### 실전 프로젝트 흐름

**1. 컨셉 단계**
```
기본 Text-to-Image
+ Batch 생성 (여러 옵션)
→ 최적 결과 선택
```

**2. 스타일 적용**
```
선택된 이미지
+ Image-to-Image
+ LoRA 스타일
→ 원하는 느낌 완성
```

**3. 최종 마무리**
```
완성된 이미지
+ 고해상도 업스케일
+ 디테일 보강
→ 최종 결과물
```

---

## 📚 고급 워크플로우 (추가 예정)

**준비 중인 내용:**
- ControlNet 활용 워크플로우
- Inpainting (부분 수정)
- Outpainting (이미지 확장)
- 애니메이션 생성
- 멀티 캐릭터 합성

---

## 🎓 학습 제안

### 단계별 실습

**1주차: 기본 마스터**
- Text-to-Image 100회
- 다양한 프롬프트 실험
- 설정값 변경 테스트

**2주차: 스타일 탐구**
- LoRA 10개 이상 시도
- 스타일 조합 실험
- 최적 Strength 찾기

**3주차: 고급 기법**
- Image-to-Image 활용
- 업스케일 실습
- 배치 생성 최적화

---

## 🔗 관련 문서

- [LoRA 가이드](../03-advanced-techniques/lora/README.md)
- [ControlNet](../03-advanced-techniques/controlnet/controlnet-architecture.md)
- [문제 해결](../05-troubleshooting/README.md)

---

**🎨 창의적인 워크플로우를 만들어보세요!**

---

[🏠 홈으로](../../README.md) | [📖 문제 해결로](../05-troubleshooting/README.md)
