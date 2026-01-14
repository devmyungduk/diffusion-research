# PART III - 고급 기능과 실전 (요약)

> LoRA, ControlNet, Flux 등 심화 기능을 소개합니다.

[🏠 홈](../../README.md) | [📚 시작 가이드](README.md) | [⬅️ PART II](part-02-workflow-practice.md)

---

## ⚠️ 문서 이동 알림

이 문서는 **빠른 요약본**입니다. 각 기술에 대한 상세 가이드는 **전문 섹션**으로 분리되었습니다.

---

## 🚀 무엇을 배우고 싶으신가요?

### 1. Flux 모델 마스터하기
최신 고성능 모델인 Flux의 사용법과 전용 워크플로우를 배웁니다.
- **[Flux 완전 가이드 보러가기](../02-models/flux/README.md)**
  - Flux 전용 노드 설정법
  - Dual CLIP Loader 사용법
  - SDXL과의 차이점

### 2. LoRA로 스타일 입히기
기존 모델에 수채화, 애니메이션 등 특정 화풍을 추가하는 방법을 배웁니다.
- **[LoRA 활용 가이드 보러가기](../03-advanced-techniques/lora/README.md)**
  - LoRA 다운로드 및 적용법
  - 적절한 강도(Strength) 조절
  - 여러 LoRA 섞어 쓰기

### 3. ControlNet으로 구도 제어하기
스케치, 포즈, 깊이 정보를 이용해 원하는 구도로 이미지를 생성합니다.
- **[ControlNet 가이드 보러가기](../03-advanced-techniques/controlnet/controlnet-architecture.md)**
  - Canny, OpenPose, Depth 활용
  - 구조를 유지하며 스타일 바꾸기

---

## 📝 핵심 요약

### Flux 모델
- **Transformer 기반**이라 프롬프트 이해력이 매우 좋습니다.
- **Load Diffusion Model** 노드를 사용해야 합니다 (Load Checkpoint 아님!).
- **Dual CLIP** (T5 + CLIP-L)을 사용하여 뉘앙스를 정확히 파악합니다.

### LoRA (Low-Rank Adaptation)
- 모델 전체를 재학습하지 않고 **스타일만 가볍게 추가**하는 플러그인입니다.
- **Strength 0.6~0.8** 정도가 가장 자연스럽습니다.

### ControlNet
- 텍스트만으로는 힘든 **"구도"와 "포즈"를 제어**합니다.
- Canny(윤곽선), OpenPose(자세), Depth(깊이)가 가장 많이 쓰입니다.

---

## 🎓 다음 단계

이제 모든 기초 학습이 끝났습니다!
더 깊은 내용은 **[문서 지도(Documentation Map)](../README.md)**에서 원하는 주제를 찾아보세요.

[🏠 문서 지도 보러가기](../README.md) | [📚 용어 사전(Glossary)](../GLOSSARY.md)
