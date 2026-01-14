# Diffusion Research & ComfyUI Complete Guide

> Stable Diffusion과 ComfyUI의 모든 것 - 기초부터 실전까지

[![License](https://img.shields.io/badge/License-Educational-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()
[![Language](https://img.shields.io/badge/Language-Korean-blue.svg)]()

---

## 🎯 이 리포지토리는?

AI 이미지 생성(Stable Diffusion, Flux)과 ComfyUI 워크플로우에 대한 **포괄적이고 체계적인 한국어 가이드**입니다.

- ✅ 초보자도 따라할 수 있는 단계별 가이드
- ✅ 핵심 개념부터 고급 기술까지
- ✅ 실전 워크플로우와 문제 해결
- ✅ 최신 Flux 모델 완벽 가이드

---

## 📚 학습 경로 (Learning Path)

자신의 수준에 맞는 코스를 선택하세요.

### 🌱 초보자 (Beginner)
**목표:** ComfyUI 설치부터 첫 이미지 생성까지
- [00. 시작하기 (Getting Started)](docs/00-getting-started/README.md)
  - [5분 빠른 시작](docs/00-getting-started/quick-start.md)
  - [기본 개념 요약](docs/00-getting-started/part-01-core-concepts.md)
  - [첫 워크플로우 실습](docs/00-getting-started/part-02-workflow-practice.md)

### 🌿 중급자 (Intermediate)
**목표:** 원리를 이해하고 다양한 모델(Flux)과 기법(LoRA) 활용하기
- [01. 핵심 개념 (Core Concepts)](docs/01-core-concepts/README.md)
  - Latent와 VAE, UNet vs Transformer
- [02. 모델 가이드 (Models)](docs/02-models/flux/README.md)
  - [Flux 완전 정복](docs/02-models/flux/README.md)
  - SDXL 해상도 최적화

### 🌳 고급자 (Advanced)
**목표:** 복잡한 제어(ControlNet)와 커스텀 워크플로우 구축
- [03. 고급 기술 (Advanced Techniques)](docs/03-advanced-techniques/lora/README.md)
  - [LoRA 심화](docs/03-advanced-techniques/lora/README.md)
  - [ControlNet 아키텍처](docs/03-advanced-techniques/controlnet/controlnet-architecture.md)
  - [Sampler 비교 분석](docs/03-advanced-techniques/samplers/sampler-comparison.md)

---

## 🗺️ 문서 구조 (Sitemap)

더 자세한 문서는 [📚 문서 지도 (Documentation Map)](docs/README.md)에서 확인할 수 있습니다.

```
📁 diffusion-research/
│
├── 📄 README.md                        ← 지금 여기!
│
├── 📁 docs/
│   ├── 📄 README.md                    (전체 문서 지도)
│   ├── 📄 GLOSSARY.md                  (용어 사전)
│   │
│   ├── 📁 00-getting-started/          ← 🌱 초보자는 여기서 시작
│   │   ├── part-01-core-concepts.md    (개념 요약 → 정본 01로 연결)
│   │   ├── part-02-workflow-practice.md (실습 튜토리얼)
│   │   └── part-03-advanced-features.md (고급 요약 → 정본 02, 03으로 연결)
│   │
│   ├── 📁 01-core-concepts/            ← 🧠 이론과 원리 (정본)
│   │
│   ├── 📁 02-models/                   ← 🤖 모델별 가이드 (Flux, SDXL)
│   │
│   ├── 📁 03-advanced-techniques/      ← ⚡ LoRA, ControlNet
│   │
│   ├── 📁 04-workflows/                ← 🎨 실전 워크플로우 예제
│   │
│   └── 📁 05-troubleshooting/          ← 🔧 문제 해결
```

---

## 🚀 빠른 시작

### 처음 시작하는 분

```bash
1. ComfyUI 설치 완료했나요? ✅
   └─→ 없다면 ComfyUI 공식 GitHub에서 다운로드

2. 첫 가이드 읽기 (필수!)
   └─→ docs/00-getting-started/README.md

3. 5분 안에 이미지 생성
   └─→ docs/00-getting-started/quick-start.md
```

### 특정 주제를 찾는다면

| 찾고 있는 것 | 바로가기 |
|-------------|---------|
| Flux 모델 사용법 | [Flux 가이드](docs/02-models/flux/README.md) |
| LoRA 사용법 | [LoRA 가이드](docs/03-advanced-techniques/lora/README.md) |
| ControlNet | [ControlNet](docs/03-advanced-techniques/controlnet/controlnet-architecture.md) |
| 용어 뜻이 궁금할 때 | [용어 사전](docs/GLOSSARY.md) |

---

## 💡 이 리포를 최대한 활용하는 법

### 1. 순서대로 학습
```
00-getting-started → 01-core-concepts → 02-models → 03-advanced-techniques
```

### 2. 실습 위주로
- 각 가이드의 예제를 직접 따라하기
- 설정값을 바꿔가며 실험하기

### 3. 문제 발생 시
- [05-troubleshooting](docs/05-troubleshooting/README.md) 먼저 확인
- Issues 탭에서 질문하기

---

## 🔄 최신 업데이트

| 날짜 | 내용 |
|------|------|
| 2026-01-14 | 문서 구조 개편 (초급/중급/고급 경로 명확화), 중복 문서 정리 |
| 2026-01-14 | 리포지토리 구조 리팩토링, ComfyUI 완전 가이드 추가 |
| 2026-01-14 | Flux 관련 문서 추가 |

**📋 문서 확장 계획**: [EXPANSION_ROADMAP.md](EXPANSION_ROADMAP.md) 참고

---

## 📝 라이선스

이 저장소의 코드와 문서는 교육 목적에 한해 자유롭게 수정 및 배포하여 사용할 수 있습니다.

> **주의:** 이 가이드에서 다루는 AI 모델(Flux, SDXL 등) 및 생성된 이미지의 라이선스는 각 모델 제작사의 정책을 따릅니다. 상업적 이용 시 해당 모델의 라이선스를 반드시 확인하세요.

---

## 📧 문의 및 피드백

- **Issues**: 질문이나 버그 리포트
- **Discussions**: 일반적인 토론

---

## 🔗 관련 링크

- [ComfyUI GitHub](https://github.com/comfyanonymous/ComfyUI)
- [Flux Models](https://blackforestlabs.ai)
- [Civitai - 모델 공유](https://civitai.com)

---

**🎨 즐거운 이미지 생성 되세요!**

---

[⬆️ 맨 위로](#diffusion-research--comfyui-complete-guide)
---
<small>**Author:** [@devmyungduk](https://github.com/devmyungduk) | **Created:** 2026-01-14 | **Last Updated:** 2026-01-14</small>
