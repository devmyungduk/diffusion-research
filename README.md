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

## 📚 학습 경로

### 🌱 초보자 (ComfyUI 처음 시작)

```
1. ComfyUI 시작하기 (필수!)
   └─→ docs/00-getting-started/README.md ⭐

2. 5분 빠른 시작
   └─→ docs/00-getting-started/quick-start.md

3. 첫 이미지 생성해보기
   └─→ docs/04-workflows/README.md
```

**예상 소요 시간:** 1-2시간

---

### 🌿 중급자 (기본 워크플로우 이해함)

```
1. 핵심 개념 이해하기
   └─→ docs/01-core-concepts/README.md

2. Flux 모델 마스터하기
   └─→ docs/02-models/flux/README.md

3. LoRA로 스타일 추가
   └─→ docs/03-advanced-techniques/lora/README.md

4. Sampler 비교 및 선택
   └─→ docs/03-advanced-techniques/samplers/sampler-comparison.md
```

**예상 소요 시간:** 3-5시간

---

### 🌳 고급자 (심화 기술 학습)

```
1. ControlNet 아키텍처
   └─→ docs/03-advanced-techniques/controlnet/controlnet-architecture.md

2. FluxGuidance Pipeline 완전 분석
   └─→ docs/02-models/flux/fluxguidance-pipeline.md

3. 고급 워크플로우 구축
   └─→ docs/04-workflows/README.md

4. 성능 최적화
   └─→ docs/05-troubleshooting/README.md
```

**예상 소요 시간:** 5-10시간

---

## 📖 문서 구조

```
📁 diffusion-research/
│
├── 📄 README.md                        ← 지금 여기!
│
├── 📁 docs/
│   │
│   ├── 📁 00-getting-started/          ← 🌱 초보자는 여기서 시작
│   │   ├── README.md                   (ComfyUI 완전 가이드)
│   │   └── quick-start.md              (5분 빠른 시작)
│   │
│   ├── 📁 01-core-concepts/            ← 🧠 이론과 개념
│   │   └── README.md                   (핵심 개념 모음)
│   │
│   ├── 📁 02-models/                   ← 🤖 모델별 가이드
│   │   ├── sd-sdxl/
│   │   │   └── README.md
│   │   └── flux/
│   │       ├── README.md               (Flux 완전 가이드)
│   │       └── fluxguidance-pipeline.md
│   │
│   ├── 📁 03-advanced-techniques/      ← ⚡ 고급 기능
│   │   ├── lora/
│   │   │   └── README.md
│   │   ├── controlnet/
│   │   │   └── controlnet-architecture.md
│   │   └── samplers/
│   │       └── sampler-comparison.md
│   │
│   ├── 📁 04-workflows/                ← 🎨 실전 워크플로우
│   │   └── README.md
│   │
│   └── 📁 05-troubleshooting/          ← 🔧 문제 해결
│       └── README.md
│
├── 📁 examples/                        ← 예제 워크플로우 JSON
└── 📁 assets/                          ← 이미지, 다이어그램
```

---

## 🗺️ 전체 문서 목차

### 00. Getting Started - 시작하기

| 문서 | 난이도 | 소요시간 | 설명 |
|------|--------|---------|------|
| [**ComfyUI 완전 가이드**](docs/00-getting-started/README.md) | 🌱 초급 | 1시간 | 전체 개념과 워크플로우 |
| [5분 빠른 시작](docs/00-getting-started/quick-start.md) | 🌱 초급 | 5분 | 바로 시작하기 |

---

### 01. Core Concepts - 핵심 개념

| 주제 | 난이도 | 설명 |
|------|--------|------|
| [핵심 개념 모음](docs/01-core-concepts/README.md) | 🌿 중급 | Latent Space, VAE, 아키텍처 비교 |

**포함 내용:**
- Latent Image - 압축된 설계도
- VAE - 압축과 복원 엔진
- UNet vs Transformer 아키텍처
- 모델 구성 요소 이해
- 
**세부 기술 문서:**
- [CLIP과 Contrastive Learning](docs/01-core-concepts/clip-contrastive-learning.md) - 텍스트 이해 원리
- [디노이징 프로세스](docs/01-core-concepts/denoising-process.md) - 이미지 생성 메커니즘
---

### 02. Models - 모델별 가이드

#### SD 1.5 / SDXL

| 문서 | 난이도 | 설명 |
|------|--------|------|
| [SD/SDXL 가이드](docs/02-models/sd-sdxl/README.md) | 🌿 중급 | 일반 SD 모델 사용법 |
| [해상도 최적화](docs/02-models/sd-sdxl/resolution-optimization.md) | 🌿 중급 | SDXL 해상도 설정 |

#### Flux

| 문서 | 난이도 | 소요시간 | 설명 |
|------|--------|---------|------|
| [**Flux 완전 가이드**](docs/02-models/flux/README.md) | 🌿 중급 | 40분 | Flux 모델 A-Z |
| [FluxGuidance Pipeline](docs/02-models/flux/fluxguidance-pipeline.md) | 🌳 고급 | 1시간 | Pipeline 완전 분석 |

**Flux 특징:**
- Transformer 기반 (DiT)
- 뛰어난 프롬프트 이해력
- 정확한 구도 제어

---

### 03. Advanced Techniques - 고급 기술

| 기술 | 난이도 | 문서 | 설명 |
|------|--------|------|------|
| **LoRA** | 🌿 중급 | [가이드](docs/03-advanced-techniques/lora/README.md) | 스타일 미세조정 |
| **ControlNet** | 🌳 고급 | [아키텍처](docs/03-advanced-techniques/controlnet/controlnet-architecture.md) | 구조 제어 |
| **Samplers** | 🌿 중급 | [비교](docs/03-advanced-techniques/samplers/sampler-comparison.md) | Sampler 선택 가이드 |

---

### 04. Workflows - 실전 워크플로우

| 문서 | 난이도 | 설명 |
|------|--------|------|
| [워크플로우 모음](docs/04-workflows/README.md) | 🌱-🌳 | 실전 예제들 |

**포함 예정:**

- Inpainting-Techniques
- Qwen-Image

---

### 05. Troubleshooting - 문제 해결

| 문서 | 난이도 | 설명 |
|------|--------|------|
| [문제 해결 가이드](docs/05-troubleshooting/README.md) | 🌱-🌳 | 일반 오류, 최적화 |

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
| 에러 해결 | [문제 해결](docs/05-troubleshooting/README.md) |
| Sampler 선택 | [Sampler 비교](docs/03-advanced-techniques/samplers/sampler-comparison.md) |

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
- 05-troubleshooting 먼저 확인
- Issues 탭에서 질문하기

### 4. 북마크 추천
- 자주 참조하는 가이드는 북마크
- 각 문서의 목차 활용

---

## 🎓 학습 팁

### 초보자
- ✅ 천천히, 순서대로
- ✅ 예제를 직접 실행해보기
- ✅ 모르는 용어는 부록의 용어집 참조

### 중급자
- ✅ 개념 섹션 깊이 있게 학습
- ✅ 다양한 모델 비교 실험
- ✅ LoRA, ControlNet 활용

### 고급자
- ✅ Pipeline 분석 문서 정독
- ✅ 커스텀 워크플로우 구축
- ✅ 성능 최적화 실험

---

## 🔄 최신 업데이트

| 날짜 | 내용 |
|------|------|
| 2025-11-14 | 리포지토리 구조 리팩토링, ComfyUI 완전 가이드 추가 |
| 2025-11-13 | Flux 관련 문서 추가 |

---

## 📝 라이선스

Educational Use - 교육 목적으로 자유롭게 사용 가능

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
<small>**Author:** [@devmyungduk](https://github.com/devmyungduk) | **Created:** 2025-11-15 | **Last Updated:** 2025-11-15</small>
