[🏠 홈](../../README.md) | [📚 전체 목차](../../README.md#-전체-문서-목차)

---
# ComfyUI 완전 가이드 - 초보자부터 실전까지

> Stable Diffusion & Flux 이미지 생성 워크플로우 마스터하기  
> 핵심 개념부터 실전 활용까지 체계적으로 정리한 기술노트

---

## 📑 학습 경로

### 🎯 빠른 시작
처음 시작하시나요? 5분 만에 첫 이미지를 생성해보세요.

**➡️ [5분 빠른 시작 가이드](quick-start.md)**

---

### 📚 완전 학습 과정

ComfyUI의 모든 것을 단계별로 배웁니다.

#### [PART I - 핵심 개념](part-01-core-concepts.md)
> AI 이미지 생성의 기초를 이해합니다

**학습 내용:**
1. Latent Image - 압축된 설계도
2. VAE - 압축과 복원 엔진
3. 아키텍처 비교: UNet vs Transformer
4. 모델 구성 요소 이해하기

**예상 시간:** 20분  
**난이도:** 🌱 초급

➡️ **[PART I 시작하기](part-01-core-concepts.md)**

---

#### [PART II - 워크플로우 실전](part-02-workflow-practice.md)
> 실제 이미지를 생성하는 노드 연결 방법을 배웁니다

**학습 내용:**
5. 전체 워크플로우 흐름도
6. KSampler - 이미지 생성 엔진
7. CLIP - 텍스트 이해 시스템
8. 기본 워크플로우 구축하기

**예상 시간:** 30분  
**난이도:** 🌿 중급

➡️ **[PART II 시작하기](part-02-workflow-practice.md)**

---

#### [PART III - 고급 기능과 실전](part-03-advanced-features.md)
> LoRA, ControlNet, Flux 등 고급 기능을 마스터합니다

**학습 내용:**
9. Flux 모델 특수 설정
10. LoRA - 스타일 미세조정
11. ControlNet - 구조 제어
12. 문제 해결 가이드
13. 첫 워크플로우 실습

**예상 시간:** 40분  
**난이도:** 🌳 고급

➡️ **[PART III 시작하기](part-03-advanced-features.md)**

---

### 📖 부록

추가 학습 자료와 참고 정보

➡️ **[용어 정리 및 참고 자료](appendix.md)**

---

## 🎓 추천 학습 순서

### 초보자
```
1. 빠른 시작 (5분)
   └─→ quick-start.md

2. PART I: 핵심 개념 (20분)
   └─→ part-01-core-concepts.md

3. PART II: 워크플로우 실전 (30분)
   └─→ part-02-workflow-practice.md
```

### 중급자
```
PART II 복습 후 → PART III 학습
└─→ part-03-advanced-features.md
```

### 고급자
```
PART III + 심화 문서
├─→ 핵심 개념 심화: ../01-core-concepts/
├─→ 모델별 가이드: ../02-models/
└─→ 고급 기술: ../03-advanced-techniques/
```

---

## 💡 학습 팁

### ✅ 효과적인 학습 방법
- 순서대로 학습 (PART I → II → III)
- 예제를 직접 실행해보기
- 모르는 용어는 부록의 용어집 참조
- 각 PART 완료 후 복습 퀴즈 풀기

### ⚠️ 주의사항
- PART I을 건너뛰지 마세요 (기초 개념 필수)
- 실습 없이 읽기만 하지 마세요
- 에러 발생 시 PART III의 문제 해결 섹션 참조

---

## 📊 전체 목차

| PART | 제목 | 난이도 | 시간 | 링크 |
|:----:|:-----|:------:|:----:|:----:|
| 🚀 | 빠른 시작 | 🌱 | 5분 | [바로가기](quick-start.md) |
| I | 핵심 개념 | 🌱 | 20분 | [바로가기](part-01-core-concepts.md) |
| II | 워크플로우 실전 | 🌿 | 30분 | [바로가기](part-02-workflow-practice.md) |
| III | 고급 기능과 실전 | 🌳 | 40분 | [바로가기](part-03-advanced-features.md) |
| 📖 | 부록 | - | 10분 | [바로가기](appendix.md) |

**총 학습 시간:** 약 2시간

---

## 🔗 관련 문서

### 심화 학습
- [핵심 개념 심화](../01-core-concepts/README.md) - CLIP, 디노이징 프로세스
- [Flux 모델 완전 가이드](../02-models/flux/README.md) - Flux 전문 가이드
- [LoRA 심화](../03-advanced-techniques/lora/README.md) - LoRA 활용법
- [ControlNet 아키텍처](../03-advanced-techniques/controlnet/controlnet-architecture.md) - 구조 제어

### 실전 활용
- [워크플로우 모음](../04-workflows/README.md) - 다양한 예제
- [문제 해결](../05-troubleshooting/README.md) - 일반 오류 해결

---

## 📝 문서 정보

**작성일:** 2025년 11월  
**버전:** 1.0  
**대상:** ComfyUI 초보자 ~ 중급자  
**최종 업데이트:** 2025-11-16

---

[🏠 홈으로](../../README.md)
