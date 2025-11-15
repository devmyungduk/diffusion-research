# 5분 빠른 시작 가이드

> ComfyUI로 첫 이미지를 5분 안에 생성해봅니다

[🏠 홈](../../README.md) | [📚 전체 목차](../../README.md#-전체-문서-목차) | [📖 완전 가이드](README.md)

---

## 🎯 목표

5분 내에 "고양이" 이미지 하나 생성하기!

---

## ✅ 사전 준비

- [x] ComfyUI 설치 완료
- [x] SD 1.5 또는 SDXL 모델 1개 다운로드
- [x] 모델을 `ComfyUI/models/checkpoints/` 폴더에 배치

---

## 🚀 3단계로 완성

### Step 1: 기본 노드 배치 (2분)

**1. ComfyUI 실행**

**2. 기본 노드 추가 (우클릭 → Add Node)**
```
필요한 노드 7개:
1. Load Checkpoint
2. CLIP Text Encode (2개 - Positive/Negative)
3. Empty Latent Image
4. KSampler
5. VAE Decode
6. Save Image
```

---

### Step 2: 노드 연결 (2분)

**연결 순서:**

```
[Load Checkpoint]
├─→ MODEL → [KSampler]
├─→ CLIP → [CLIP Text Encode +] → [KSampler]
├─→ CLIP → [CLIP Text Encode -] → [KSampler]
└─→ VAE → [VAE Decode]

[Empty Latent Image] → [KSampler]
[KSampler] → [VAE Decode]
[VAE Decode] → [Save Image]
```

**시각적 구조:**
```
┌────────────────┐
│Load Checkpoint │
└─┬──┬────┬──────┘
  │  │    └─→ VAE ────────┐
  │  └─→ CLIP ─┬─→ Text+ ─┤
  │            └─→ Text- ─┼─→ [KSampler]
  └─→ MODEL ──────────────┘       ↓
                            [VAE Decode]
[Empty Latent] ──────────→       ↓
                            [Save Image]
```

---

### Step 3: 설정 및 실행 (1분)

**1. 프롬프트 입력**

**Positive (원하는 것):**
```
a cute cat, high quality
```

**Negative (원하지 않는 것):**
```
blurry, low quality
```

**2. 기본 설정 (그대로 두면 됨)**
- KSampler:
  - steps: 20
  - cfg: 8
  - sampler: euler

- Empty Latent:
  - width: 512
  - height: 512

**3. 실행!**
```
Queue Prompt 버튼 클릭!
```

**대기:** 30초 ~ 1분 (GPU 성능에 따라)

---

## 🎉 완성!

이미지가 나타났나요? 축하합니다! 🎨

---

## 🔄 다음 시도해보기

### 프롬프트 변경
```
a dog playing in the park, sunny day, high quality
```

### 스타일 추가
```
a cat, watercolor painting style, high quality
```

### Negative 강화
```
blurry, low quality, distorted, ugly, bad anatomy
```

---

## 😕 문제가 생겼나요?

### 이미지가 안 나와요
→ VAE Decode가 연결되었는지 확인

### 이미지가 이상해요
→ steps를 30으로 늘려보세요

### 너무 느려요
→ 이미지 크기를 512×512로 줄이세요

---

## 📚 더 배우기

**다음 단계:**
1. [완전 가이드](README.md) - 모든 기능 상세 설명
2. [핵심 개념](../01-core-concepts/README.md) - 이론 이해
3. [워크플로우](../04-workflows/README.md) - 다양한 예제

---

## 💡 추가 팁

### 빠른 반복 테스트
- Steps: 15-20
- Size: 512×512

### 고품질 최종 결과
- Steps: 30-40
- Size: 768×768 or 1024×1024

### 다양한 결과 시도
- Seed: -1 (매번 랜덤)
- Batch size: 4 (한번에 4개)

---

**🎨 즐거운 생성 되세요!**

---

[🏠 홈으로](../../README.md) | [📖 완전 가이드로](README.md)
