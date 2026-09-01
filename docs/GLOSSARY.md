[문서 지도](./README.md)

# 용어 사전 (Glossary)

ComfyUI와 Stable Diffusion 생태계에서 자주 사용하는 용어를 모았습니다.

## A - E

### Auto Queue
`Run` 버튼의 `Run options`에 있는 자동 반복 설정입니다. `Disabled`는 자동 실행을 하지 않고, `Instant`는 생성이 끝나면 다시 큐에 넣고, `On Change`는 값이 바뀔 때 큐에 넣습니다.

### BasicGuider
`SamplerCustomAdvanced` 구성에서 모델과 conditioning을 묶어 샘플러에 넘기는 노드입니다. KSampler와 달리 negative 입력 포트가 없습니다. ComfyUI 공식 FLUX.1 예제가 이 구성을 사용합니다.

### Batch Count
`Run` 버튼 옆의 숫자입니다. 한 번 누를 때 같은 워크플로우를 큐에 몇 개 넣을지 정합니다. 한 장을 여러 번 생성하는 설정이며, 한 번의 생성에서 이미지를 몇 장 만들지 정하는 Batch Size와 다릅니다.

### Batch Size (배치 크기)
한 번 실행할 때 만들 이미지 장수입니다. `Empty Latent Image`에서 지정하며, 늘리면 VRAM 사용량도 함께 늘어납니다.

### 버킷 (Bucket)
모델이 학습한 해상도 목록의 각 항목입니다. SDXL은 총 픽셀이 약 1메가픽셀인 여러 비율의 크기로 학습했고, 목록을 벗어난 크기에서는 구도가 왜곡되거나 같은 대상이 화면 안에서 반복됩니다. 전체 목록은 [SDXL 해상도 최적화](./02-models/sd-sdxl/resolution-optimization.md#3-권장-해상도-목록)에 있습니다.

### Bypass (바이패스)
선택한 노드의 계산을 건너뛰고 **입력을 그대로 출력으로 넘기는** 상태입니다. 단축키는 `Ctrl + B`(macOS `⌘ + B`). 연결이 유지되므로 뒤쪽 노드는 계속 실행되고, 같은 키로 되돌립니다. 노드 하나를 뺀 결과를 비교할 때 사용합니다.

### 캔버스 (Canvas)
노드를 놓고 연결하는 ComfyUI의 작업 화면입니다. 빈 공간을 왼쪽 버튼으로 끌면 화면이 움직이고, 노드 위에서 끌면 그 노드가 움직입니다. 조작은 [캔버스 다루기](./00-getting-started/canvas-basics.md)에 있습니다.

### Cancel current run
실행 중인 작업을 멈추는 버튼입니다. 실행이 시작되면 실행 영역의 버튼이 이것으로 바뀌며 단축키는 `Ctrl + Alt + Enter`입니다. 멈춘 작업의 중간 결과는 저장되지 않습니다.

### CFG (Classifier-Free Guidance)
프롬프트 조건을 얼마나 강하게 밀어붙일지 정하는 KSampler의 값입니다. 품질 점수가 아니라 **조건을 강제하는 정도**이며, 너무 높이면 대비가 과해지고 형태가 깨집니다. SD 1.5·SDXL은 7 전후에서 시작합니다. FLUX.1 dev는 예외로 `cfg=1.0`을 사용하고 대신 Guidance를 조절합니다.

### Checkpoint (체크포인트)
학습이 끝난 AI 모델 파일 전체입니다. 확장자는 `.safetensors` 또는 `.ckpt`입니다. 안에 UNet(또는 DiT), VAE, CLIP이 함께 들어 있습니다.

### Conditioning (조건)
프롬프트를 텍스트 인코더가 변환한 결과로, 모델이 생성 과정에서 참고하는 조건 데이터입니다. ComfyUI에서 `CONDITIONING` 타입으로 흐르며 KSampler의 `positive`·`negative`에 연결됩니다.

### CLIP (Contrastive Language-Image Pre-training)
OpenAI가 만든 모델입니다. 텍스트와 이미지를 같은 의미 공간에 놓도록 학습해, 프롬프트를 모델이 다루는 숫자(Embedding)로 바꿉니다.

### CLIP Vision
CLIP의 이미지 인코더 부분입니다. 참조 이미지를 임베딩으로 바꿔 IPAdapter나 Redux가 조건으로 사용할 수 있게 합니다. 텍스트를 처리하는 `CLIP Text Encode`와는 다른 경로입니다.

### ComfyUI-Manager
커스텀 노드를 설치·갱신·제거·비활성화하는 확장입니다. Desktop 앱에는 기본으로 들어 있고 켜져 있으며, Portable과 수동 설치본에서는 ComfyUI 코어에 들어 있지만 따로 켜야 합니다. 워크플로우에 없는 노드가 있으면 찾아서 설치합니다.

### ControlNet
이미지의 구조(윤곽선, 포즈, 깊이 등)를 제어하기 위한 보조 모델입니다. 텍스트 프롬프트만으로는 설명하기 힘든 구체적인 형태를 지정할 때 사용합니다.

### control_after_generate
KSampler의 `seed` 아래에 있는 위젯입니다. 한 장을 생성한 뒤 seed를 어떻게 바꿀지 정합니다. `fixed`로 두면 seed가 유지되므로 다른 값 하나만 바꿔 결과를 비교할 수 있습니다.

### Denoising (노이즈 제거)
확산(Diffusion) 모델의 핵심 작동 원리입니다. 무작위 노이즈에서 시작하여 점차 의미 있는 이미지로 다듬어가는 과정을 말합니다.

### Denoise (디노이즈 강도)
KSampler의 설정값으로, 전체 샘플링 구간 중 어느 정도를 사용할지 정합니다. 텍스트로 새 이미지를 만들 때는 `1.0`, 기존 이미지를 부분 수정할 때는 1.0보다 낮춥니다. `0.5`가 "픽셀의 절반이 바뀐다"는 뜻은 아닙니다.

### Differential Diffusion
마스크의 밝기에 따라 픽셀마다 denoise 강도를 다르게 적용하는 기법입니다. 검정은 유지, 흰색은 교체, 회색은 그 중간입니다. 마스크 안팎을 이분해 처리하는 일반 인페인팅과 이 점이 다릅니다.

### EmptySD3LatentImage
Flux·SD3 계열에서 빈 Latent를 만드는 노드입니다. SD 1.5·SDXL이 사용하는 `Empty Latent Image`와 채널 구성이 달라 서로 바꿔 사용하지 않습니다. `width`, `height`, `batch_size`를 지정합니다.

### Embedding (임베딩)
텍스트나 이미지를 AI가 처리할 수 있도록 숫자의 나열(벡터)로 변환한 데이터입니다.

---

## F - J

### Fit View
선택한 노드가 없으면 워크플로우 전체가, 선택한 노드가 있으면 그 노드가 화면에 들어오도록 시야를 조정하는 기능입니다. 단축키는 `.`이고 화면 오른쪽 아래에 같은 기능의 버튼이 있습니다.

### Flux
Black Forest Labs가 만든 이미지 생성 모델 계열입니다. Stable Diffusion의 UNet 대신 Transformer(DiT) 구조를 사용하고, 텍스트 인코더로 CLIP-L과 T5를 함께 사용합니다.

### FluxGuidance
프롬프트를 인코딩한 `CONDITIONING`에 guidance 값을 얹어 FLUX.1 dev에 넘기는 노드입니다. KSampler를 사용하는 공식 기본 구성은 `cfg=1.0`을 두고 이 노드로 조건 강도를 정합니다. `SamplerCustomAdvanced` 구성에는 `cfg` 위젯 자체가 없습니다. 넣는 값의 의미는 `Guidance (FLUX.1 dev)` 항목에 있습니다.

### FP8 / FP16
모델 가중치를 저장하는 숫자 정밀도입니다. FP16은 16비트, FP8은 8비트를 사용합니다. 비트 수가 작으면 파일 크기와 VRAM 사용량이 줄어듭니다. 이 학습서는 FLUX.1 dev 기준으로 FP8 최소 12GB, FP16 권장 24GB를 적습니다.

### GGUF
양자화한 모델을 담는 파일 형식입니다. Q6, Q5처럼 단계가 나뉘고 단계를 낮출수록 VRAM 사용량이 줄어듭니다. ComfyUI에서 GGUF 파일은 `diffusion_models/`가 아니라 `unet/` 폴더에 둡니다.

### Group (그룹)
노드 여러 개를 테두리로 묶는 기능입니다. 캔버스 우클릭 `Add Group`으로 빈 그룹을 만들거나, 노드를 선택하고 `Add Group For Selected Nodes`로 만듭니다. 그룹 제목을 끌면 안의 노드가 함께 움직입니다.

### Guidance (FLUX.1 dev)
FLUX.1 dev가 프롬프트 조건을 얼마나 참고할지 나타내는 값으로, `FluxGuidance` 노드에서 지정합니다. 공식 예제의 출발점은 `3.5`입니다. KSampler의 CFG와는 다른 값이므로 혼동하지 않습니다.

### Inference (추론)
학습된 AI 모델을 사용하여 실제로 결과물(이미지)을 만들어내는 과정입니다.

### Inpainting (인페인팅)
이미지의 일부 영역을 마스크로 지정해 그 부분만 다시 생성하는 작업입니다.

### Outpainting (아웃페인팅)
원본 이미지 바깥으로 화면을 넓혀 없던 영역을 새로 생성하는 작업입니다. Inpainting과 같은 노드 구성을 사용하되 마스크가 원본 바깥쪽에 놓입니다.

### IPAdapter
참조 이미지를 CLIP Vision으로 인코딩해 MODEL을 수정하는 제어 기법입니다. conditioning이 아니라 MODEL 라인에서 동작합니다. 미리 학습해 두는 LoRA와 달리 참조 이미지를 그 자리에서 분석합니다.

---

## K - O

### KSampler
ComfyUI에서 노이즈 제거 과정(Denoising)을 실행하는 핵심 노드입니다. Steps, CFG, Sampler Name 등을 정해 이미지를 만듭니다.

### KSamplerAdvanced
KSampler와 같은 샘플링을 사용하면서 `add_noise`, `start_at_step`, `end_at_step`, `return_with_leftover_noise`를 직접 지정하는 노드입니다. 샘플링을 두 단계로 나눠 중간에 모델이나 conditioning을 바꿀 때 사용합니다.

### Latent Image (잠재 이미지)
이미지 정보를 고도로 압축한 데이터 형태입니다. AI는 픽셀 단위의 큰 이미지를 직접 다루는 대신, 이 Latent 공간에서 연산을 수행하여 속도와 효율을 높입니다.

### LoRA (Low-Rank Adaptation)
거대 모델을 효율적으로 미세조정(Fine-tuning)하는 기술, 또는 그 결과물 파일입니다. 용량이 작으며(수십~수백 MB), 특정 화풍, 캐릭터, 개념을 기존 모델에 추가할 때 사용합니다.

### 미니맵 (Minimap)
워크플로우 전체를 축소해 표시하는 작은 지도입니다. 화면 오른쪽 아래 아이콘으로 켜고 끕니다. 노드가 많아 전체 보기로는 글자가 안 보일 때 위치를 잡는 데 사용합니다.

### Mask Editor (마스크 편집기)
ComfyUI 안에서 이미지 위에 마스크를 그리는 편집기입니다. `Load Image` 노드를 선택한 뒤 선택 툴박스의 마스크 아이콘, 이미지 미리보기의 `Edit or mask image`, 노드 우클릭 메뉴의 `Open in Mask Editor` 세 가지로 엽니다. `Save`를 누르면 그 노드에 마스크가 적용됩니다.

### ModelSamplingFlux
FLUX.1 워크플로우에서 MODEL 라인에 넣는 노드입니다. 해상도에 따라 sigma 스케줄을 조정하며 `max_shift`, `base_shift`, `width`, `height` 위젯을 가집니다. 공식 Redux 예제의 시작값은 `max_shift 1.15`, `base_shift 0.5`이고, `width`·`height`는 `EmptySD3LatentImage`와 같은 값을 사용합니다.

### Mute (뮤트)
선택한 노드가 출력을 내보내지 않는 상태입니다. 단축키는 `Ctrl + M`(macOS `⌘ + M`). 뒤쪽 노드는 입력을 받지 못해 실행되지 않습니다. 입력을 넘기는 Bypass와 다릅니다.

### 노드 (Node)
ComfyUI에서 하나의 작업을 맡는 상자입니다. 왼쪽에 입력 포트, 오른쪽에 출력 포트가 있고, 상자 안에서 직접 값을 넣는 칸을 위젯이라고 부릅니다. 캔버스를 더블클릭하거나 우클릭해 추가합니다.

### Note
캔버스에 글을 적어 두는 노드입니다. 입력·출력 포트가 없고 실행에 참여하지 않으므로 결과를 바꾸지 않으며, 적은 내용은 워크플로우 `.json`에 함께 저장됩니다. 마크다운 표기를 사용하는 `MarkdownNote`도 같은 자리에서 추가합니다.

### OOM (Out of Memory)
그래픽카드 메모리(VRAM)가 부족해 생성이 중단되는 오류입니다. 해상도와 배치 크기를 줄이는 것이 첫 조치입니다.

---

## P - T

### 전처리기 (Preprocessor)
입력 이미지를 ControlNet이 받는 형식으로 바꾸는 노드입니다. `OpenPose Pose`, `Depth Anything`, `Scribble Lines` 등이 있습니다. 대부분 ComfyUI 기본 노드가 아니라 따로 설치해야 노드 검색 목록에 나옵니다.

### Prompt (프롬프트)
AI에게 어떤 이미지를 만들지 지시하는 텍스트 명령어입니다.
- **Positive Prompt:** 생성하고 싶은 요소
- **Negative Prompt:** 생성하지 말아야 할 요소

### patch (패치)
Transformer 계열 모델이 이미지를 다룰 때 나누는 정사각형 조각입니다. 픽셀 하나씩이 아니라 패치 단위로 계산하고, 모든 패치가 서로를 참조합니다. UNet이 주변 픽셀 위주로 계산하는 것과 이 지점이 다릅니다.

### 양자화 (Quantization)
모델 가중치를 더 적은 비트로 바꿔 저장하는 것입니다. 파일 크기와 VRAM 요구가 줄고 품질이 조금씩 떨어집니다. Flux에서는 GGUF 형식의 Q8·Q6·Q5·Q4 단계로 유통되며, 단계를 낮출수록 형태가 무너지고 이미지 안의 글자가 깨집니다.

### 큐 (Queue)
실행을 기다리는 작업 목록입니다. `Run`을 누르면 작업이 이 목록 끝에 들어가고, 앞에서부터 하나씩 실행됩니다. `Q`로 사이드바를 열어 대기 목록과 실행 기록을 봅니다.

### Queue Prompt
`Run` 버튼의 예전 이름입니다. 바깥 자료에서 이 이름을 보면 `Run (실행)` 항목을 보세요.

### Run (실행)
현재 워크플로우를 큐에 넣는 버튼입니다. 화면 우측 상단에 있으며 단축키는 `Ctrl + Enter`입니다. 누르면 ComfyUI가 출력 노드에서 거꾸로 필요한 노드만 골라 실행하고, 출력이 어디에도 사용되지 않는 노드는 건너뜁니다. 예전 이름은 `Queue Prompt`입니다.

### 포트 (Port)
노드끼리 선으로 잇는 자리입니다. 왼쪽이 입력, 오른쪽이 출력이며 같은 데이터 타입끼리만 연결됩니다. 노드 안에서 값을 직접 넣는 위젯과 다릅니다.

### Redux
FLUX.1 dev와 FLUX.1 schnell을 이미지로 조건화하는 어댑터입니다. 참조 이미지를 CLIP Vision으로 인코딩한 뒤 `StyleModelApply`에서 텍스트 conditioning과 합칩니다.

### Refiner (리파이너)
1단계 샘플링을 중간에 끊고, 남은 구간을 다른 모델이나 다른 conditioning으로 이어 마무리하는 구성입니다. SDXL이 Base와 Refiner 두 체크포인트를 짝으로 배포하면서 널리 사용됐습니다. ComfyUI에서는 `KSamplerAdvanced`의 `start_at_step`·`end_at_step`으로 구간을 나눕니다.

### Sampler (샘플러)
각 단계에서 Latent를 다음 상태로 갱신하는 계산 방법입니다. ComfyUI에서는 `sampler_name`으로 지정하며 `euler`, `dpmpp_2m` 등이 있습니다. Scheduler와는 별개 항목입니다.

### SamplerCustomAdvanced
`noise`, `guider`, `sampler`, `sigmas`, `latent_image` 다섯 입력을 각각 다른 노드에서 받는 샘플러 노드입니다. Seed·CFG·sampler 이름을 직접 넣는 위젯이 없습니다. 하나라도 연결이 비면 실행되지 않습니다.

### Reroute (리라우트)
연결선의 경유점 역할만 하는 노드입니다. 데이터를 바꾸지 않고 선이 다른 노드 위를 지나가지 않도록 우회시킬 때 사용합니다.

### safetensors
모델 파일 형식입니다. 체크포인트·LoRA·VAE·텍스트 인코더가 모두 이 확장자를 사용하기 때문에, 확장자만으로는 종류를 구분할 수 없습니다. 내려받은 페이지에 적힌 종류를 확인하고 알맞은 폴더에 넣어야 합니다.

### Scheduler (스케줄러)
전체 Steps에 노이즈 수준(sigma)을 어떻게 배분할지 정하는 시간표입니다. `normal`, `karras`, `simple` 등이 있습니다. 다른 도구의 `DPM++ 2M Karras` 같은 표기는 ComfyUI에서 Sampler(`dpmpp_2m`)와 Scheduler(`karras`)로 나뉩니다.

### Seed (시드)
난수 생성의 기준이 되는 숫자입니다. 같은 모델·설정·Seed와 동일한 실행 환경에서는 대체로 같은 결과를 재현할 수 있습니다. GPU, 연산 정밀도, 라이브러리·ComfyUI 버전이 달라지면 차이가 생길 수 있습니다.

### seq_len
텍스트 인코더가 프롬프트를 토큰으로 나눴을 때의 토큰 개수입니다. T5XXL의 출력 크기 `[seq_len × 4096]`에서 앞자리에 해당하며, 프롬프트가 길어지면 이 값이 커집니다.

### sigma
각 denoising 단계에서 남아 있는 노이즈의 크기를 나타내는 값입니다. Scheduler가 이 값을 단계별로 배치하고 Sampler가 그 순서대로 latent를 갱신합니다.

### Stable Diffusion (SD)
Stability AI에서 공개한 오픈소스 이미지 생성 모델 시리즈입니다. (SD 1.5, SDXL 등)

### Steps (스텝)
디노이징을 반복하는 횟수입니다. 20~30에서 시작하며, 무작정 늘려도 어느 지점부터는 눈에 띄는 개선 없이 시간만 늘어납니다.

### Subgraph (서브그래프)
노드 여러 개를 노드 하나로 접는 기능입니다. 노드를 선택하고 `Convert to Subgraph`로 만들고, 더블클릭해 안으로 들어가며 `Exit Subgraph`로 나옵니다. `Unpack Subgraph`로 원래 노드들로 되돌립니다. 프론트엔드 1.24.3 이상에서 동작합니다.

### strength_type
`StyleModelApply`의 위젯입니다. `multiply`는 참조 이미지 조건 전체에 `strength`를 곱하고, `attn_bias`는 attention 단계에서 편향으로 더합니다. 기본값은 `multiply`이며, 비교 실험에서는 `strength`와 이 값을 동시에 바꾸지 않습니다.

### StyleModelApply
`conditioning`, `style_model`, `clip_vision_output` 세 입력을 받아 새 `CONDITIONING`을 만드는 노드입니다. `style_model`에는 Redux 같은 스타일 모델을 로더로 불러 연결합니다. `strength`와 `strength_type` 위젯으로 참조 이미지를 얼마나 반영할지 정합니다.

### T5XXL
FLUX.1이 사용하는 텍스트 인코더입니다. 프롬프트 문장을 `[seq_len × 4096]` 크기의 임베딩으로 바꿉니다. ComfyUI에서는 `text_encoders/` 폴더에 두고 `Dual CLIP Loader`로 CLIP과 함께 불러옵니다.

### timestep
모델을 학습할 때 노이즈 수준을 가리키는 시간 좌표입니다. 연속으로 정의될 수도 있고 이산 단계로 정의될 수도 있습니다. 이미지를 만들 때 지정하는 ComfyUI의 Steps와는 다른 값입니다.

### Trigger Word (트리거 워드)
일부 LoRA가 학습 때 함께 사용한 단어입니다. 이 단어를 프롬프트에 적어야 해당 화풍이나 캐릭터가 제대로 나타납니다. 내려받은 페이지의 설명란에 적혀 있습니다.

### Transformer / DiT
Flux 모델의 기반 아키텍처입니다. SD의 UNet이 주변 픽셀 위주로 계산하는 것과 달리, 이미지를 패치로 나눠 모든 패치가 서로 참조합니다.

---

## U - Z

### Upscale (업스케일)
생성된 이미지를 더 큰 해상도로 확대하는 작업입니다. 확대만 하는 방법과, 확대한 뒤 낮은 Denoise로 다시 샘플링해 디테일을 채우는 방법이 있습니다.

### UNet
Stable Diffusion(v1.5, XL) 모델의 핵심 아키텍처입니다. 이미지의 노이즈를 예측하고 없애는 역할을 합니다.

### VAE (Variational AutoEncoder)
이미지(Pixel 공간)와 Latent(압축 공간) 사이를 변환하는 도구입니다.
- **Encode:** 이미지 → Latent (압축)
- **Decode:** Latent → 이미지 (복원)

### Vector Space와 Latent Space
텍스트 인코더가 만드는 공간(Vector Space)과 VAE가 만드는 이미지 압축 공간(Latent Space)은 서로 다릅니다. 텍스트 벡터는 Latent로 변환되지 않고, Latent가 만들어지는 방향을 안내할 뿐입니다.

### 워크플로우 (Workflow)
노드와 연결, 각 노드의 설정값을 합친 하나의 구성입니다. `.json`으로 저장하고 다시 열 수 있으며, `Save Image`로 저장한 PNG에도 메타데이터로 함께 기록됩니다. 저장과 재현은 [워크플로우 저장과 재현](./00-getting-started/save-and-reproduce.md)에 있습니다.

### 위젯 (Widget)
노드 상자 안에서 값을 직접 넣거나 고르는 칸입니다. 선으로 연결하는 포트와 다릅니다. KSampler의 `seed`·`steps`·`cfg`가 위젯이고, `model`·`positive`는 포트입니다. 일부 위젯은 우클릭해 포트로 바꿀 수 있습니다.

### VRAM
그래픽카드에 달린 메모리입니다. 모델 크기, 해상도, 배치 크기가 여기에 들어갈 수 있어야 생성이 진행됩니다. 부족하면 OOM 오류가 납니다.

---

## 더 볼 곳

- [워크플로우 이해하기](./00-getting-started/workflow-basics.md) — KSampler와 CLIP 설정값의 의미
- [문제 해결](./05-troubleshooting/README.md) — 오류 메시지에서 출발하는 진단
- [문서 지도](./README.md) — 목적별 문서 찾기
