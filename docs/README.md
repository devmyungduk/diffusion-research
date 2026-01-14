# 📚 문서 지도 (Documentation Map)

> Diffusion Research & ComfyUI 학습을 위한 전체 문서 가이드입니다.

[🏠 저장소 홈](../README.md)

---

## 🗺️ 학습 경로 (Learning Path)

자신의 수준에 맞는 단계부터 시작하세요.

### 🌱 초보자 (Beginner)
**목표:** ComfyUI 설치부터 첫 이미지 생성까지
- [00. 시작하기 (Getting Started)](./00-getting-started/README.md)
  - [5분 빠른 시작](./00-getting-started/quick-start.md)
  - [기본 개념 요약](./00-getting-started/part-01-core-concepts.md)
  - [첫 워크플로우 실습](./00-getting-started/part-02-workflow-practice.md)

### 🌿 중급자 (Intermediate)
**목표:** 원리를 이해하고 다양한 모델(Flux)과 기법(LoRA) 활용하기
- [01. 핵심 개념 (Core Concepts)](./01-core-concepts/README.md)
  - [Latent와 VAE](./01-core-concepts/README.md#1-latent-image---ai의-비밀-작업실)
  - [UNet vs Transformer](./01-core-concepts/README.md#3-아키텍처-비교-unet-vs-transformer)
- [02. 모델 가이드 (Models)](./02-models/flux/README.md)
  - [Flux 완전 정복](./02-models/flux/README.md)
  - [SDXL 해상도 최적화](./02-models/sd-sdxl/resolution-optimization.md)

### 🌳 고급자 (Advanced)
**목표:** 복잡한 제어(ControlNet)와 커스텀 워크플로우 구축
- [03. 고급 기술 (Advanced Techniques)](./03-advanced-techniques/lora/README.md)
  - [LoRA 심화](./03-advanced-techniques/lora/README.md)
  - [ControlNet 아키텍처](./03-advanced-techniques/controlnet/controlnet-architecture.md)
  - [Sampler 비교 분석](./03-advanced-techniques/samplers/sampler-comparison.md)

---

## 📂 전체 문서 목록

### 00. Getting Started
- [시작하기 가이드](./00-getting-started/README.md)
- [Part 1: 핵심 개념 요약](./00-getting-started/part-01-core-concepts.md) (→ [상세본](./01-core-concepts/README.md))
- [Part 2: 워크플로우 실전](./00-getting-started/part-02-workflow-practice.md)
- [Part 3: 고급 기능 요약](./00-getting-started/part-03-advanced-features.md) (→ [상세본](./02-models/flux/README.md))

### 01. Core Concepts (이론)
- [핵심 개념 모음](./01-core-concepts/README.md)
- [CLIP과 Contrastive Learning](./01-core-concepts/clip-contrastive-learning.md)
- [Denoising Process](./01-core-concepts/denoising-process.md)

### 02. Models (모델)
- **Flux:**
  - [Flux 가이드](./02-models/flux/README.md)
  - [FluxGuidance Pipeline](./02-models/flux/fluxguidance-pipeline.md)
- **SD / SDXL:**
  - [SD 가이드](./02-models/sd-sdxl/README.md)
  - [해상도 최적화](./02-models/sd-sdxl/resolution-optimization.md)

### 03. Advanced Techniques (심화)
- **LoRA:** [LoRA 가이드](./03-advanced-techniques/lora/README.md)
- **ControlNet:** [ControlNet 아키텍처](./03-advanced-techniques/controlnet/controlnet-architecture.md)
- **Samplers:**
  - [Sampler 비교](./03-advanced-techniques/samplers/sampler-comparison.md)
  - [KSampler vs Advanced](./03-advanced-techniques/samplers/ksampler-vs-advanced.md)

### 04. Workflows (실전 예제)
- [워크플로우 모음](./04-workflows/README.md)

### 05. Troubleshooting
- [문제 해결 가이드](./05-troubleshooting/README.md)

---

## ℹ️ 참고 자료
- [용어 사전 (Glossary)](./GLOSSARY.md)
