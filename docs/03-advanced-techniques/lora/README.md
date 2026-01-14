# LoRA - 스타일 미세조정 가이드

> 기존 모델에 특정 스타일을 추가하는 방법

[🏠 홈](../../../README.md) | [📚 전체 목차](../../../docs/README.md)

---

## 🎯 가이드 개요

**대상 독자:** 모델 전체를 새로 학습하지 않고 특정 화풍만 추가하고 싶은 분
**사전 이해:** 기본 이미지 생성 경험 (Part 2 수료 권장)
**예상 소요 시간:** 20분

**핵심 내용:**
- LoRA의 개념 (모델 전체 학습 vs 부분 학습)
- ComfyUI에서 LoRA 노드 연결 및 사용법
- 적절한 강도(Strength) 조절 팁

---

## 📑 목차

1. [LoRA란 무엇인가?](#lora란-무엇인가)
2. [ComfyUI에서 사용하기](#comfyui에서-사용하기)
3. [강도 조절](#강도-조절)
4. [여러 LoRA 동시 사용](#여러-lora-동시-사용)
5. [LoRA 선택 가이드](#lora-선택-가이드)

---

## LoRA란 무엇인가?

### 🎯 핵심 개념

**LoRA = 기존 모델에 스타일을 추가하는 플러그인**

전체 모델을 다시 학습하지 않고, 일부만 조정하여 새로운 스타일을 적용합니다.

### 🔍 작동 원리

```
기존 모델 (100%)
    ↓
LoRA 적용 (5%만 수정)
    ↓
새로운 스타일 모델
(기존 능력 유지 + 새 스타일)
```

**비유:**
- **기존 모델** = 다양한 그림을 그리는 화가
- **LoRA** = 특정 화풍을 배우는 단기 수업
- **결과** = 기본 실력 + 새로운 화풍

### 📊 LoRA vs 전체 미세조정

| 항목 | 전체 미세조정 | LoRA |
|------|-------------|------|
| 학습 데이터 | 수천 장 | 수십 장 |
| 학습 시간 | 수일~수주 | 수시간 |
| 파일 크기 | 2-7GB | 10-200MB |
| 기존 능력 | 손실 가능 | 유지 ✅ |
| 적용 방식 | 모델 교체 | 플러그인 |

[⬆️ 목차로](#-목차)

---

## ComfyUI에서 사용하기

### 🏗️ 기본 워크플로우

```
[Load Checkpoint]
    ↓
[Load LoRA]
├─ model: Load Checkpoint의 MODEL
├─ clip: Load Checkpoint의 CLIP
├─ lora_name: watercolor_style.safetensors
├─ strength_model: 0.8
└─ strength_clip: 0.8
    ↓
[수정된 MODEL] → [KSampler]
[수정된 CLIP] → [CLIP Text Encode]
```

### 📝 단계별 가이드

**1. LoRA 파일 준비**
```
다운로드: Civitai, Hugging Face
위치: ComfyUI/models/loras/
예: watercolor_style.safetensors
```

**2. Load LoRA 노드 추가**
```
Add Node → loaders → Load LoRA
```

**3. 연결**
```
Load Checkpoint [MODEL] → Load LoRA [model]
Load Checkpoint [CLIP] → Load LoRA [clip]
Load LoRA [MODEL] → KSampler
Load LoRA [CLIP] → CLIP Text Encode
```

**4. 설정**
```
lora_name: 원하는 LoRA 파일 선택
strength_model: 0.8
strength_clip: 0.8
```

**5. 생성!**

[⬆️ 목차로](#-목차)

---

## 강도 조절

### 📊 Strength 가이드

| Strength | 효과 | 사용 상황 |
|----------|------|----------|
| 0.3-0.5 | 은은한 힌트 | 스타일 살짝만 |
| 0.6-0.8 | 중간 효과 | **일반적 사용** ✅ |
| 0.9-1.0 | 강한 효과 | 스타일 강조 |
| 1.0+ | 매우 강함 | 특수 경우만 |

### 💡 조절 팁

**너무 약하면 (0.3 이하):**
- 스타일이 거의 안 보임
- LoRA 효과 미미

**적절한 범위 (0.6-0.8):**
- 스타일과 품질 균형 ✅
- 대부분의 경우 추천

**너무 강하면 (1.0+):**
- 과도한 스타일
- 이미지 품질 저하 가능
- 디테일 손실

### 🎨 실험 예시

**수채화 LoRA:**
```
Strength 0.5: 약간 수채화 느낌
Strength 0.8: 명확한 수채화 ✅
Strength 1.2: 과도한 수채화 효과
```

[⬆️ 목차로](#-목차)

---

## 여러 LoRA 동시 사용

### 🔗 체인 연결

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

### ⚠️ 주의사항

**권장:**
- 2-3개까지 적당
- 각 LoRA의 Strength 합계가 2.5 이하

**문제 발생 가능:**
- 4개 이상: 충돌 가능
- 높은 Strength: 품질 저하
- 비슷한 LoRA: 효과 중복

### 💡 조합 전략

**좋은 조합:**
```
스타일 LoRA (0.8)
+ 조명 LoRA (0.5)
+ 디테일 LoRA (0.4)
= 조화로운 결과 ✅
```

**나쁜 조합:**
```
수채화 LoRA (1.0)
+ 유화 LoRA (1.0)
+ 애니메이션 LoRA (1.0)
= 충돌, 이상한 결과 ❌
```

[⬆️ 목차로](#-목차)

---

## LoRA 선택 가이드

### 🎨 LoRA 종류

**1. 스타일 LoRA**
```
- 수채화, 유화, 애니메이션 등
- 전체 이미지 스타일 변경
- 예: watercolor_style.safetensors
```

**2. 캐릭터 LoRA**
```
- 특정 캐릭터 일관성
- 얼굴, 의상 특징 유지
- 예: character_lora.safetensors
```

**3. 컨셉 LoRA**
```
- 특정 분위기나 테마
- 사이버펑크, 판타지 등
- 예: cyberpunk_aesthetic.safetensors
```

**4. 디테일 LoRA**
```
- 세부 묘사 강화
- 품질 향상
- 예: add_detail.safetensors
```

### ✅ 좋은 LoRA 특징

- 명확한 목적 (화풍, 캐릭터, 개념)
- 충분한 학습 데이터
- 활발한 커뮤니티 피드백
- 다양한 예시 이미지

### 📥 다운로드 사이트

**주요 플랫폼:**
- [Civitai](https://civitai.com) - 가장 큰 커뮤니티
- [Hugging Face](https://huggingface.co) - 공식 모델들

**체크 사항:**
- 라이선스 확인
- 호환 모델 (SD 1.5 / SDXL / Flux)
- 사용자 리뷰
- 예시 이미지 품질

[⬆️ 목차로](#-목차)

---

## 💡 실전 팁

### 효과적인 사용법

**1. 단계적 테스트**
```
Strength 0.5 → 0.7 → 0.9
점진적으로 올리며 최적값 찾기
```

**2. 프롬프트 조합**
```
LoRA: 수채화 스타일
Prompt: "watercolor painting style"
→ 상승 효과 ✅
```

**3. 네거티브 프롬프트**
```
LoRA 스타일이 너무 강하면
Negative에 스타일 키워드 추가
```

### 문제 해결

**LoRA 효과가 안 보여요**
- Strength 0.8-1.0으로 높이기
- MODEL과 CLIP 모두 연결 확인
- 프롬프트에 관련 키워드 추가

**이미지 품질이 저하돼요**
- Strength 낮추기 (0.5-0.7)
- LoRA 개수 줄이기
- 다른 LoRA 시도

**스타일이 너무 강해요**
- Strength 0.3-0.5로 낮추기
- Negative Prompt에 스타일 키워드

---

## 📚 다음 단계

**LoRA 마스터 완료!**

1. [ControlNet](../controlnet/controlnet-architecture.md) - 구조 제어
2. [워크플로우](../../04-workflows/README.md) - LoRA 활용 예제
3. [Flux 모델](../../02-models/flux/README.md) - Flux용 LoRA

---

**🎨 창의적인 스타일 만들기를 즐기세요!**

---

[🏠 홈으로](../../../README.md) | [📖 ControlNet으로](../controlnet/controlnet-architecture.md)
