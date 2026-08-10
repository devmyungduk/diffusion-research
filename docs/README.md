[GitHub 저장소](https://github.com/devmyungduk/diffusion-research)

# Diffusion Research & ComfyUI 온라인 학습서

![프롬프트에서 노이즈와 디노이징 단계를 거쳐 이미지가 만들어지는 학습서 표지](assets/images/diffusion-learning-hero.png)

> 완성 워크플로우를 복사하는 데서 멈추지 않고, **왜 연결하고 무엇을 바꿀지** 스스로 판단하는 힘을 기릅니다.

[5분 빠른 시작](./00-getting-started/quick-start.md){ .md-button .md-button--primary }
[내 목표로 찾아가기](#무엇을-하려고-하시나요){ .md-button }

<div class="learning-color-key" aria-label="문서 강조 색상 안내">
  <span class="learning-color-key__item">핵심 개념</span>
  <span class="learning-color-key__item learning-color-key__item--action">실행·설정</span>
  <span class="learning-color-key__item learning-color-key__item--success">결과·완료</span>
  <span class="learning-color-key__item learning-color-key__item--caution">주의</span>
  <span class="learning-color-key__item learning-color-key__item--danger">오류·문제</span>
</div>

<div class="grid cards learning-path-cards" markdown>

-   **처음 시작합니다**

    ---

    설치부터 기본 7노드 워크플로우와 첫 비교 실험까지 진행합니다.

    [5분 빠른 시작 →](./00-getting-started/quick-start.md)

-   **원리가 궁금합니다**

    ---

    Latent·VAE·CLIP·디노이징을 실제 노드와 연결해 이해합니다.

    [핵심 개념 →](./01-core-concepts/README.md)

-   **결과를 제어하고 싶습니다**

    ---

    LoRA·ControlNet·Sampler로 스타일, 구도, 생성 과정을 조절합니다.

    [심화 제어 →](./03-advanced-techniques/lora/README.md)

-   **지금 오류가 났습니다**

    ---

    OOM·검은 이미지·연결 오류를 증상에서 출발해 진단합니다.

    [문제 해결 →](./05-troubleshooting/README.md)

</div>

각 장은 `학습 목표 → 최소 실습 → 한 변수 실험 → 관찰 질문 → 다음 단계` 순서로 구성됩니다.

## 무엇을 하려고 하시나요?

지금 상황에 맞는 문서로 바로 이동하세요. 처음이라면 위에서부터 순서대로 진행하세요.

| 상황 | 여기서 시작 |
|------|-------------|
| ComfyUI가 처음이다. 일단 이미지부터 만들고 싶다 | [설치](./00-getting-started/installation.md) → [5분 빠른 시작](./00-getting-started/quick-start.md) |
| 노드가 각각 무슨 일을 하는지 이해하고 싶다 | [워크플로우 이해하기](./00-getting-started/workflow-basics.md) |
| 프롬프트를 의도대로 쓰고 싶다 | [프롬프트와 CLIP 이해하기](./00-getting-started/prompt-basics.md) |
| 이미지가 만들어지는 원리가 궁금하다 | [핵심 개념](./01-core-concepts/README.md) |
| Flux 모델을 쓰고 싶다 | [Flux 가이드](./02-models/flux/README.md) |
| 특정 화풍·캐릭터를 적용하고 싶다 | [LoRA](./03-advanced-techniques/lora/README.md) |
| 구도·포즈를 정확히 제어하고 싶다 | [ControlNet](./03-advanced-techniques/controlnet/controlnet-architecture.md) |
| 에러가 나거나 결과가 이상하다 | [문제 해결](./05-troubleshooting/README.md) |
| 모르는 용어가 나왔다 | [용어 사전](./GLOSSARY.md) |

## 학습 경로

전체를 체계적으로 익히려면 수준에 맞는 단계부터 순서대로 진행하세요.

### 입문 — 첫 이미지까지
ComfyUI 설치부터 첫 이미지 생성까지 다룹니다.
- [00. 시작하기](./00-getting-started/README.md)
  - [ComfyUI 설치](./00-getting-started/installation.md) — 약 15분
  - [5분 빠른 시작](./00-getting-started/quick-start.md) — 약 5분
  - [워크플로우 이해하기](./00-getting-started/workflow-basics.md) — 약 30분
  - [프롬프트와 CLIP 이해하기](./00-getting-started/prompt-basics.md) — 약 20분
  - [첫 워크플로우 직접 만들기](./00-getting-started/first-workflow.md) — 약 30분
  - [워크플로우 저장과 재현](./00-getting-started/save-and-reproduce.md) — 약 20분

### 기초 이론 — 원리 이해
이미지가 만들어지는 과정과 모델 구조를 이해합니다.
- [01. 핵심 개념](./01-core-concepts/README.md) — Latent와 VAE, UNet vs Transformer
  - [CLIP과 Contrastive Learning](./01-core-concepts/clip-contrastive-learning.md)
  - [디노이징 프로세스](./01-core-concepts/denoising-process.md)

### 모델 활용 — Flux, SDXL
모델별 특성과 설정을 익힙니다.
- [02. 모델 가이드](./02-models/README.md) — 두 계열의 차이와 선택 기준
- **Flux**
  - [Flux 개요](./02-models/flux/README.md)
  - [텍스트 인코더와 데이터 공간](./02-models/flux/text-encoders.md)
  - [Flux Quick Reference](./02-models/flux/quick-reference.md)
  - [FLUX.1 작업 선택과 Redux 실습](./02-models/flux/flux-practical.md)
  - [FluxGuidance 이해와 사용](./02-models/flux/fluxguidance-pipeline.md)
- **SD·SDXL**
  - [SD / SDXL 개요](./02-models/sd-sdxl/README.md)
  - [SDXL 해상도 최적화](./02-models/sd-sdxl/resolution-optimization.md)

### 심화 제어 — LoRA, 제어 기법, Sampler
정밀한 제어와 커스텀 워크플로우를 구축합니다.
- [03. 심화 제어](./03-advanced-techniques/README.md) — 무엇을 고정할지 고르는 기준
- [프롬프트 가중치](./03-advanced-techniques/prompt-weighting.md)
- [LoRA 기본](./03-advanced-techniques/lora/README.md)
- [LoRA 조합과 선택](./03-advanced-techniques/lora/combining.md)
- **제어 기법**
  - [ControlNet 아키텍처](./03-advanced-techniques/controlnet/controlnet-architecture.md)
  - [ControlNet 연결과 조절](./03-advanced-techniques/controlnet/controlnet-pipeline.md)
  - [IPAdapter](./03-advanced-techniques/controlnet/ipadapter.md)
  - [Flux Redux](./03-advanced-techniques/controlnet/flux-redux.md)
  - [Differential Diffusion](./03-advanced-techniques/controlnet/differential-diffusion.md)
  - [Flux 모델 변형 비교](./03-advanced-techniques/controlnet/flux-model-variants.md)
  - [제어 기법 실전 워크플로우](./03-advanced-techniques/controlnet/example-workflows.md)
- **Sampler**
  - [Sampler 비교](./03-advanced-techniques/samplers/sampler-comparison.md)
  - [KSampler와 SamplerCustomAdvanced](./03-advanced-techniques/samplers/ksampler-vs-advanced.md)

### 실전·문제 해결
- [04. 워크플로우 예제](./04-workflows/README.md)
- [업스케일과 배치 생성](./04-workflows/upscale-and-batch.md)
- [05. 문제 해결](./05-troubleshooting/README.md)

## 참고 자료

- [용어 사전 (Glossary)](./GLOSSARY.md)
- [문서 작성 규약](./maintainers/writing-guide.md)

### 외부 리소스

- [Stability AI](https://stability.ai) — Stable Diffusion 공식
- [ComfyWorkflows](https://comfyworkflows.com) — 커뮤니티 워크플로우 공유
