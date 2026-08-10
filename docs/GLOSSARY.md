# 용어 사전 (Glossary)

ComfyUI와 Stable Diffusion 생태계에서 자주 사용되는 핵심 용어들을 정리했습니다.

[홈](README.md) · [문서 지도](./README.md)

---

## A - E

### Batch Size (배치 크기)
한 번 실행할 때 만들 이미지 장수입니다. `Empty Latent Image`에서 지정하며, 늘리면 VRAM 사용량도 함께 늘어납니다.

### CFG (Classifier-Free Guidance)
프롬프트 조건을 얼마나 강하게 밀어붙일지 정하는 KSampler의 값입니다. 품질 점수가 아니라 **조건을 강제하는 정도**이며, 너무 높이면 대비가 과해지고 형태가 깨집니다. SD 1.5·SDXL은 7 전후에서 시작합니다. FLUX.1 dev는 예외로 `cfg=1.0`을 쓰고 대신 Guidance를 조절합니다.

### Checkpoint (체크포인트)
학습이 완료된 AI 모델 파일 전체를 의미합니다. `.safetensors` 또는 `.ckpt` 확장자를 가집니다. UNet(또는 DiT), VAE, CLIP 등이 포함되어 있습니다.

### Conditioning (조건)
프롬프트를 텍스트 인코더가 변환한 결과로, 모델이 생성 과정에서 참고하는 조건 데이터입니다. ComfyUI에서 `CONDITIONING` 타입으로 흐르며 KSampler의 `positive`·`negative`에 연결됩니다.

### CLIP (Contrastive Language-Image Pre-training)
OpenAI가 개발한 모델로, 텍스트와 이미지 사이의 연관성을 이해하는 역할을 합니다. 사용자가 입력한 프롬프트를 AI가 이해할 수 있는 숫자(Embedding)로 변환해줍니다.

### ControlNet
이미지의 구조(윤곽선, 포즈, 깊이 등)를 제어하기 위한 보조 모델입니다. 텍스트 프롬프트만으로는 설명하기 힘든 구체적인 형태를 지정할 때 사용합니다.

### Denoising (노이즈 제거)
확산(Diffusion) 모델의 핵심 작동 원리입니다. 무작위 노이즈에서 시작하여 점차 의미 있는 이미지로 다듬어가는 과정을 말합니다.

### Denoise (디노이즈 강도)
KSampler의 설정값으로, 전체 샘플링 구간 중 어느 정도를 사용할지 정합니다. 텍스트로 새 이미지를 만들 때는 `1.0`, 기존 이미지를 부분 수정할 때는 1.0보다 낮춥니다. `0.5`가 "픽셀의 절반이 바뀐다"는 뜻은 아닙니다.

### Embedding (임베딩)
텍스트나 이미지를 AI가 처리할 수 있도록 숫자의 나열(벡터)로 변환한 데이터입니다.

---

## F - J

### Flux
Black Forest Labs에서 개발한 고성능 이미지 생성 모델입니다. 기존 Stable Diffusion과 달리 Transformer(DiT) 아키텍처를 사용하여 프롬프트 이해력과 텍스트 생성 능력이 뛰어납니다.

### Guidance (FLUX.1 dev)
FLUX.1 dev가 프롬프트 조건을 얼마나 참고할지 나타내는 값으로, `FluxGuidance` 노드에서 지정합니다. 공식 예제의 출발점은 `3.5`입니다. KSampler의 CFG와는 다른 값이므로 혼동하지 않습니다.

### Inference (추론)
학습된 AI 모델을 사용하여 실제로 결과물(이미지)을 만들어내는 과정입니다.

### Inpainting (인페인팅)
이미지의 일부 영역을 마스크로 지정해 그 부분만 다시 생성하는 작업입니다. 반대로 이미지 바깥으로 화면을 넓히는 것은 Outpainting입니다.

---

## K - O

### KSampler
ComfyUI에서 노이즈 제거 과정(Denoising)을 실행하는 핵심 노드입니다. Steps, CFG, Sampler Name 등을 설정하여 이미지를 생성합니다.

### Latent Image (잠재 이미지)
이미지 정보를 고도로 압축한 데이터 형태입니다. AI는 픽셀 단위의 큰 이미지를 직접 다루는 대신, 이 Latent 공간에서 연산을 수행하여 속도와 효율을 높입니다.

### LoRA (Low-Rank Adaptation)
거대 모델을 효율적으로 미세조정(Fine-tuning)하는 기술, 또는 그 결과물 파일입니다. 용량이 작으며(수십~수백 MB), 특정 화풍, 캐릭터, 개념을 기존 모델에 추가할 때 사용합니다.

### OOM (Out of Memory)
그래픽카드 메모리(VRAM)가 부족해 생성이 중단되는 오류입니다. 해상도와 배치 크기를 줄이는 것이 첫 조치입니다.

---

## P - T

### Prompt (프롬프트)
AI에게 어떤 이미지를 만들지 지시하는 텍스트 명령어입니다.
- **Positive Prompt:** 생성하고 싶은 요소
- **Negative Prompt:** 생성하지 말아야 할 요소

### Sampler (샘플러)
각 단계에서 Latent를 다음 상태로 갱신하는 계산 방법입니다. ComfyUI에서는 `sampler_name`으로 지정하며 `euler`, `dpmpp_2m` 등이 있습니다. Scheduler와는 별개 항목입니다.

### safetensors
모델 파일 형식입니다. 체크포인트·LoRA·VAE·텍스트 인코더가 모두 이 확장자를 쓰기 때문에, 확장자만으로는 종류를 구분할 수 없습니다. 내려받은 페이지에 적힌 종류를 확인하고 알맞은 폴더에 넣어야 합니다.

### Scheduler (스케줄러)
전체 Steps에 노이즈 수준(sigma)을 어떻게 배분할지 정하는 시간표입니다. `normal`, `karras`, `simple` 등이 있습니다. 다른 도구의 `DPM++ 2M Karras` 같은 표기는 ComfyUI에서 Sampler(`dpmpp_2m`)와 Scheduler(`karras`)로 나뉩니다.

### Seed (시드)
난수 생성의 기준이 되는 숫자입니다. 같은 모델·설정·Seed와 동일한 실행 환경에서는 대체로 같은 결과를 재현할 수 있습니다. GPU, 연산 정밀도, 라이브러리·ComfyUI 버전이 달라지면 차이가 생길 수 있습니다.

### Stable Diffusion (SD)
Stability AI에서 공개한 오픈소스 이미지 생성 모델 시리즈입니다. (SD 1.5, SDXL 등)

### Steps (스텝)
디노이징을 반복하는 횟수입니다. 20~30에서 시작하며, 무작정 늘려도 어느 지점부터는 눈에 띄는 개선 없이 시간만 늘어납니다.

### Trigger Word (트리거 워드)
일부 LoRA가 학습 때 함께 쓴 단어입니다. 이 단어를 프롬프트에 적어야 해당 화풍이나 캐릭터가 제대로 나타납니다. 내려받은 페이지의 설명란에 적혀 있습니다.

### Transformer / DiT
Flux 모델의 기반이 되는 아키텍처입니다. 기존 SD의 UNet과 달리 전체 맥락(Global Context)을 한 번에 파악하는 능력이 뛰어나 복잡한 프롬프트 처리에 유리합니다.

---

## U - Z

### Upscale (업스케일)
생성된 이미지를 더 큰 해상도로 확대하는 작업입니다. 확대만 하는 방법과, 확대한 뒤 낮은 Denoise로 다시 샘플링해 디테일을 채우는 방법이 있습니다.

### UNet
Stable Diffusion(v1.5, XL) 모델의 핵심 아키텍처입니다. 이미지의 노이즈를 예측하고 제거하는 역할을 수행합니다.

### VAE (Variational AutoEncoder)
이미지(Pixel 공간)와 Latent(압축 공간) 사이를 변환해주는 도구입니다.
- **Encode:** 이미지 → Latent (압축)
- **Decode:** Latent → 이미지 (복원)

### VRAM
그래픽카드에 달린 메모리입니다. 모델 크기, 해상도, 배치 크기가 여기에 들어갈 수 있어야 생성이 진행됩니다. 부족하면 OOM 오류가 납니다.

---

## 더 볼 곳

- [워크플로우 이해하기](./00-getting-started/workflow-basics.md) — KSampler와 CLIP 설정값의 의미
- [문제 해결](./05-troubleshooting/README.md) — 오류 메시지에서 출발하는 진단
- [문서 지도](./README.md) — 목적별 문서 찾기
