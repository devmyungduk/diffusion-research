# 용어 사전 (Glossary)

ComfyUI와 Stable Diffusion 생태계에서 자주 사용되는 핵심 용어들을 정리했습니다.

[🏠 홈](../../README.md) | [📚 문서 가이드](./README.md)

---

## A - E

### Checkpoint (체크포인트)
학습이 완료된 AI 모델 파일 전체를 의미합니다. `.safetensors` 또는 `.ckpt` 확장자를 가집니다. UNet(또는 DiT), VAE, CLIP 등이 포함되어 있습니다.

### CLIP (Contrastive Language-Image Pre-training)
OpenAI가 개발한 모델로, 텍스트와 이미지 사이의 연관성을 이해하는 역할을 합니다. 사용자가 입력한 프롬프트를 AI가 이해할 수 있는 숫자(Embedding)로 변환해줍니다.

### ControlNet
이미지의 구조(윤곽선, 포즈, 깊이 등)를 제어하기 위한 보조 모델입니다. 텍스트 프롬프트만으로는 설명하기 힘든 구체적인 형태를 지정할 때 사용합니다.

### Denoising (노이즈 제거)
확산(Diffusion) 모델의 핵심 작동 원리입니다. 무작위 노이즈에서 시작하여 점차 의미 있는 이미지로 다듬어가는 과정을 말합니다.

### Embedding (임베딩)
텍스트나 이미지를 AI가 처리할 수 있도록 숫자의 나열(벡터)로 변환한 데이터입니다.

---

## F - J

### Flux
Black Forest Labs에서 개발한 고성능 이미지 생성 모델입니다. 기존 Stable Diffusion과 달리 Transformer(DiT) 아키텍처를 사용하여 프롬프트 이해력과 텍스트 생성 능력이 뛰어납니다.

### Inference (추론)
학습된 AI 모델을 사용하여 실제로 결과물(이미지)을 만들어내는 과정입니다.

---

## K - O

### KSampler
ComfyUI에서 노이즈 제거 과정(Denoising)을 실행하는 핵심 노드입니다. Steps, CFG, Sampler Name 등을 설정하여 이미지를 생성합니다.

### Latent Image (잠재 이미지)
이미지 정보를 고도로 압축한 데이터 형태입니다. AI는 픽셀 단위의 큰 이미지를 직접 다루는 대신, 이 Latent 공간에서 연산을 수행하여 속도와 효율을 높입니다.

### LoRA (Low-Rank Adaptation)
거대 모델을 효율적으로 미세조정(Fine-tuning)하는 기술, 또는 그 결과물 파일입니다. 용량이 작으며(수십~수백 MB), 특정 화풍, 캐릭터, 개념을 기존 모델에 추가할 때 사용합니다.

---

## P - T

### Prompt (프롬프트)
AI에게 어떤 이미지를 만들지 지시하는 텍스트 명령어입니다.
- **Positive Prompt:** 생성하고 싶은 요소
- **Negative Prompt:** 생성하지 말아야 할 요소

### Seed (시드)
난수 생성의 기준이 되는 고유 숫자입니다. 같은 설정과 같은 Seed를 사용하면 항상 동일한 이미지가 생성됩니다.

### Stable Diffusion (SD)
Stability AI에서 공개한 오픈소스 이미지 생성 모델 시리즈입니다. (SD 1.5, SDXL 등)

### Transformer / DiT
Flux 모델의 기반이 되는 아키텍처입니다. 기존 SD의 UNet과 달리 전체 맥락(Global Context)을 한 번에 파악하는 능력이 뛰어나 복잡한 프롬프트 처리에 유리합니다.

---

## U - Z

### UNet
Stable Diffusion(v1.5, XL) 모델의 핵심 아키텍처입니다. 이미지의 노이즈를 예측하고 제거하는 역할을 수행합니다.

### VAE (Variational AutoEncoder)
이미지(Pixel 공간)와 Latent(압축 공간) 사이를 변환해주는 도구입니다.
- **Encode:** 이미지 → Latent (압축)
- **Decode:** Latent → 이미지 (복원)

---
