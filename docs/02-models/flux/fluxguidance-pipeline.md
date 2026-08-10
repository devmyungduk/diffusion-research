[홈](../../README.md) · [문서 지도](../../README.md)

# FluxGuidance 이해와 사용

`FluxGuidance`는 FLUX.1 dev가 프롬프트 조건을 얼마나 강하게 참고할지 나타내는 숫자를 `CONDITIONING`에 넣는 노드입니다. 먼저 기본 생성을 완성하고, 같은 프롬프트와 Seed에서 값을 비교하며 익힙니다.

## 이 장에서 배우는 것

<div class="guide-meta" markdown>
**대상** FLUX.1 dev를 처음 사용하는 입문자·디자이너·작가 · **사전 이해** 프롬프트를 입력하고 워크플로우를 한 번 실행해 본 경험 · **시간** 15분
</div>

## 1. FluxGuidance가 맡는 역할

ComfyUI는 프롬프트를 텍스트 인코더로 처리해 `CONDITIONING`이라는 데이터 묶음을 만듭니다. 이 묶음에는 모델이 생성 과정에서 참고할 텍스트 정보와 추가 설정이 담깁니다.

| 단계 | 처리 | 결과 |
|---:|---|---|
| 1 | 프롬프트를 Text Encode에 입력 | 텍스트 조건이 담긴 `CONDITIONING` |
| 2 | conditioning과 guidance 값을 FluxGuidance에 입력 | guidance 값이 포함된 `CONDITIONING` |
| 3 | 출력 conditioning을 Sampler에 전달 | FLUX.1 dev가 생성 과정에서 조건을 사용 |

작업 지시서에 비유하면 프롬프트는 “무엇을 만들지” 적은 본문이고, guidance는 모델이 그 지시를 참고하는 방식을 조절하는 별도 칸입니다. guidance는 특정 단어 하나의 가중치가 아니며, 값을 두 배로 올린다고 프롬프트 반영이 정확히 두 배가 되지는 않습니다.

### 노드 입력과 출력

| 이름 | 타입 | 역할 |
|---|---|---|
| `conditioning` | `CONDITIONING` | Text Encode 등에서 만든 프롬프트 조건 |
| `guidance` | `FLOAT` | 모델에 전달할 guidance 값 |
| 출력 | `CONDITIONING` | 기존 조건에 guidance 값이 포함된 결과 |

### 구현을 확인할 때

현재 ComfyUI 구현은 기존 conditioning을 받아 `guidance` 항목을 설정합니다. 프롬프트를 다시 토큰화하거나 텍스트 인코더를 다시 실행하는 구조가 아닙니다. 이 세부 내용은 노드 사용법을 익힌 뒤 동작 원리를 확인할 때 참고하면 됩니다.

## 2. 어떤 노드를 연결할까

현재 ComfyUI에서는 두 가지 형태를 볼 수 있습니다. 워크플로우 안에서 한 가지 경로를 선택합니다.

### 경로 A — Text Encode와 FluxGuidance를 분리

FLUX.1 dev 공식 예제에서 볼 수 있는 구성입니다.

| 순서 | 노드 | 입력 또는 설정 | 출력 |
|---:|---|---|---|
| 1 | Dual CLIP Loader | FLUX.1용 CLIP-L·T5 | `CLIP` |
| 2 | CLIP Text Encode | CLIP과 프롬프트 | `CONDITIONING` |
| 3 | FluxGuidance | conditioning과 guidance 값 | guidance가 포함된 `CONDITIONING` |

프롬프트 입력과 guidance 조절 위치가 나뉘어 있어 처음 구조를 이해하기 쉽습니다.

### 경로 B — CLIPTextEncodeFlux에서 함께 입력

현재 내장 `CLIPTextEncodeFlux`는 CLIP-L 프롬프트, T5 프롬프트, guidance 값을 한 노드에서 입력받습니다.

| 순서 | 노드 | 입력 또는 설정 | 출력 |
|---:|---|---|---|
| 1 | Dual CLIP Loader | FLUX.1용 CLIP-L·T5 | `CLIP` |
| 2 | CLIPTextEncodeFlux | CLIP-L 프롬프트, T5 프롬프트, guidance 값 | guidance가 포함된 `CONDITIONING` |

이 경로에서는 출력 conditioning에 guidance 값이 이미 포함됩니다. 같은 값을 넣기 위해 별도 `FluxGuidance`를 다시 연결할 필요가 없습니다. 뒤에서 값을 의도적으로 덮어쓰는 고급 구성이 아니라면 한 경로만 사용하세요.

### 모델별 확인

| 모델 | guidance 구성 |
|---|---|
| FLUX.1 dev | guidance 값을 받는 모델. 공식 예제 출발점은 `3.5` |
| FLUX.1 schnell | dev와 같은 guidance 입력을 사용하지 않는 timestep-distilled 모델 |
| FLUX.1의 편집·제어 변형 | 모델별 공식 예제에서 guidance 입력 여부 확인 |
| 이후 FLUX 세대 | 해당 세대의 로더·텍스트 인코더·샘플링 예제를 따름 |

## 3. KSampler cfg와 무엇이 다른가

FluxGuidance와 KSampler의 `cfg`는 이름이 비슷하지만 같은 조절값이 아닙니다.

| 구분 | FluxGuidance `guidance` | KSampler `cfg` |
|---|---|---|
| 사용 위치 | FLUX.1 dev 모델에 전달되는 조건 | 샘플러의 고전 CFG 결합 |
| 기본 출발점 | `3.5` | FLUX.1 dev 공식 기본 구성은 `1.0` |
| 조절 목적 | guidance-distilled 모델의 프롬프트 조건 조절 | positive·negative 예측 차이 조절 |
| 기본 워크플로우 | 사용 | 고전 CFG 결합은 사용하지 않음 |

KSampler의 `cfg=1.0`은 positive와 negative 예측을 고전 CFG 방식으로 벌리지 않는 설정입니다. FluxGuidance에 넣은 값은 별도 모델 조건으로 유지됩니다.

### negative 입력은 어떻게 하나

KSampler 노드는 `negative` 연결을 요구합니다. ComfyUI의 FLUX.1 dev FP8 체크포인트 공식 예제는 빈 텍스트를 인코딩한 conditioning을 negative에 연결합니다.

| KSampler 입력 | 연결할 출력 | 텍스트와 설정 |
|---|---|---|
| `positive` | FluxGuidance의 `CONDITIONING` | positive 프롬프트, guidance `3.5`에서 시작 |
| `negative` | 별도 CLIP Text Encode의 `CONDITIONING` | 텍스트를 비워 둠 |

이 구성은 negative 프롬프트의 단어를 적극적으로 사용하는 고전 CFG 작업과 다릅니다. 커스텀 체크포인트가 별도 negative 또는 CFG 구성을 요구하면 그 모델의 안내를 우선합니다.

SamplerCustomAdvanced와 `BasicGuider`를 사용하는 공식 전체 모델 예제는 KSampler와 입력 구조가 다르므로 negative 포트가 없습니다. 어느 샘플러 구성을 사용하는지 먼저 확인하세요.

## 4. guidance 값 비교하기

`3.5`는 정답이나 품질 등급이 아니라 공식 예제와 내장 노드의 **출발점**입니다. 값의 효과는 프롬프트, 모델 변형, LoRA와 이미지 조건에 따라 달라집니다.

### 한 변수 실험

다음 항목을 고정합니다.

- 모델과 정밀도
- 프롬프트
- Seed와 `control_after_generate=fixed`
- 해상도
- Sampler·Scheduler·Steps

guidance만 바꿔 세 장을 만듭니다.

| 실행 | guidance | 관찰할 질문 |
|---|---:|---|
| A | 2.5 | 모델의 해석이 넓어졌는가? 핵심 대상이 빠졌는가? |
| B | 3.5 | 프롬프트 내용과 화면의 자연스러움이 균형을 이루는가? |
| C | 4.5 | 지시 반영이 달라졌는가? 대비·질감·형태가 거칠어졌는가? |

값이 높을수록 항상 좋아지거나 모든 문장이 더 정확해지는 것은 아닙니다. 결과를 나란히 보고 작업 목적에 맞는 값을 선택합니다.

### 기록 양식

| 기록 항목 | 작성 내용 |
|---|---|
| 모델·정밀도 |  |
| 프롬프트 |  |
| Seed |  |
| Sampler·Scheduler·Steps |  |
| guidance |  |
| 잘 유지된 요소 |  |
| 빠지거나 과장된 요소 |  |
| 다음 비교값 |  |

## 5. 기본 워크플로우 연결

다음은 `Load Checkpoint`와 KSampler를 쓰는 FLUX.1 dev 체크포인트 구성입니다.

| 연결 대상 | 연결할 출력 | 역할 또는 설정 |
|---|---|---|
| KSampler `model` | Load Checkpoint의 `MODEL` | 생성 모델 |
| positive CLIP Text Encode `clip` | Load Checkpoint의 `CLIP` | positive 프롬프트 인코딩 |
| FluxGuidance `conditioning` | positive CLIP Text Encode의 `CONDITIONING` | guidance `3.5`에서 비교 시작 |
| KSampler `positive` | FluxGuidance의 `CONDITIONING` | guidance가 포함된 positive 조건 |
| negative CLIP Text Encode `clip` | Load Checkpoint의 `CLIP` | 빈 텍스트 인코딩 |
| KSampler `negative` | negative CLIP Text Encode의 `CONDITIONING` | 공식 예제의 빈 negative 조건 |
| KSampler `latent_image` | Empty SD3 Latent Image의 `LATENT` | 생성 크기와 batch 설정 |
| VAE Decode `samples` | KSampler의 `LATENT` | 샘플링 결과 |
| VAE Decode `vae` | Load Checkpoint의 `VAE` | latent를 이미지로 디코딩 |
| Save Image `images` | VAE Decode의 `IMAGE` | 결과 저장 |

!!! tip "분리 로더를 사용하는 경우"
    `Load Diffusion Model`, `Dual CLIP Loader`, `Load VAE`를 따로 쓰더라도 conditioning의 핵심 흐름은 같습니다. 공식 전체 모델 예제처럼 SamplerCustomAdvanced를 사용한다면 해당 예제의 `BasicGuider`, sampler, sigmas 연결을 그대로 따르세요.

??? note "6. ControlNet과 함께 사용하기 — 기본 비교를 끝낸 뒤에"
    기본 Text-to-Image 결과와 guidance 비교를 먼저 끝낸 뒤 ControlNet을 추가합니다. 현재 `Apply ControlNet`은 positive와 negative conditioning을 모두 입력받고 두 conditioning을 다시 출력합니다.

    | 연결 대상 | 연결할 출력 | 확인할 내용 |
    |---|---|---|
    | Apply ControlNet `positive` | FluxGuidance의 `CONDITIONING` | positive 프롬프트와 guidance 포함 |
    | Apply ControlNet `negative` | 빈 텍스트를 사용한 CLIP Text Encode의 `CONDITIONING` | KSampler 구성과 동일한 negative 조건 |
    | Apply ControlNet `control_net` | Load ControlNet의 `CONTROL_NET` | FLUX 호환 모델인지 확인 |
    | Apply ControlNet `image` | 선택한 Preprocessor의 `IMAGE` | ControlNet 종류와 전처리 방식 일치 |
    | Apply ControlNet `vae` | 사용 중인 VAE | 해당 ControlNet이 요구할 때 연결 |
    | KSampler `positive` | Apply ControlNet의 positive `CONDITIONING` | ControlNet이 적용된 positive 조건 |
    | KSampler `negative` | Apply ControlNet의 negative `CONDITIONING` | ControlNet이 적용된 negative 조건 |

    일부 FLUX ControlNet은 `vae` 입력이나 전용 적용 노드를 요구합니다. 사용 중인 ControlNet 배포 페이지와 공식 예제에서 필요한 입력을 확인하세요.

    ### 무엇을 조절할까

    | 바꾸려는 것 | 조절값 | 비교 방법 |
    |---|---|---|
    | 프롬프트 조건의 영향 | Flux guidance | strength를 고정하고 guidance만 변경 |
    | 구조 조건의 영향 | ControlNet `strength` | guidance를 고정하고 strength만 변경 |
    | ControlNet 적용 구간 | `start_percent`, `end_percent` | strength를 고정하고 한 값씩 변경 |

    ControlNet strength에는 모든 모델에 통하는 표준값이 없습니다. 모델 제공자의 권장값이 있으면 그 값에서 시작하고, 없으면 낮은 값부터 작은 간격으로 비교합니다. 노드 배치 순서를 텍스트·구조 우선순위 조절값으로 사용하지 않습니다.

## 7. 문제 해결

| 증상 | 확인 순서 |
|---|---|
| `FluxGuidance` 노드가 보이지 않음 | 1. ComfyUI 업데이트 확인<br>2. `CLIPTextEncodeFlux`에 guidance 입력이 있는지 확인 |
| guidance를 바꿔도 차이가 거의 없음 | 1. FLUX.1 dev 계열인지 확인<br>2. 최종 positive conditioning이 sampler까지 연결됐는지 확인<br>3. Seed 고정 확인 |
| KSampler 실행 구성이 헷갈림 | 1. `cfg=1.0` 확인<br>2. positive에는 guidance가 포함된 조건 연결<br>3. negative에는 공식 예제의 빈 조건 연결 |
| schnell 결과가 이상함 | dev용 FluxGuidance 구성을 제거하고 schnell 공식 워크플로우로 복원 |
| ControlNet이 반영되지 않음 | 1. FLUX 호환 모델 확인<br>2. 전처리 결과 확인<br>3. VAE 필요 여부 확인<br>4. strength와 적용 구간 확인 |
| 비교할 때 구도가 계속 바뀜 | Seed와 `control_after_generate=fixed` 확인 |

??? question "Q&A 점검"
    **Q. guidance 3.5가 가장 좋은 값인가요?**  
    A. 아닙니다. 공식 예제와 내장 노드의 출발점입니다. 고정 조건에서 다른 값을 비교해 선택합니다.

    **Q. `CLIPTextEncodeFlux` 뒤에 `FluxGuidance`를 반드시 연결해야 하나요?**  
    A. 아닙니다. `CLIPTextEncodeFlux`의 guidance 입력을 사용했다면 출력 conditioning에 값이 포함됩니다. 별도 노드는 값을 나중에 의도적으로 바꿀 때만 필요합니다.

    **Q. FluxGuidance는 프롬프트 가중치와 같은가요?**  
    A. 아닙니다. 프롬프트 가중치는 특정 토큰이나 구문의 비중을 바꾸고, Flux guidance는 모델에 전달되는 별도 조건값입니다.

    **Q. KSampler cfg도 함께 올리면 프롬프트가 더 잘 반영되나요?**  
    A. FLUX.1 dev 공식 기본 구성에서는 cfg를 1.0으로 둡니다. cfg와 Flux guidance를 동시에 올리는 구성은 기본 학습 범위를 벗어나므로 커스텀 모델의 안내와 고정 조건 실험 없이 사용하지 않습니다.

    **Q. ControlNet과 충돌하면 어느 노드를 앞으로 옮겨야 하나요?**  
    A. 노드 순서를 우선순위 조절값으로 사용하지 않습니다. 먼저 모델 호환성과 연결을 확인하고 guidance, strength, start/end를 한 번에 하나씩 비교합니다.

## 완료 기준

- FluxGuidance의 입력과 출력을 설명할 수 있다.
- `CLIP Text Encode + FluxGuidance`와 `CLIPTextEncodeFlux` 경로를 구분할 수 있다.
- KSampler cfg와 Flux guidance의 역할을 구분할 수 있다.
- Seed를 고정하고 guidance 하나만 바꾼 비교 결과를 기록했다.
- ControlNet을 추가했을 때 positive·negative conditioning을 모두 sampler까지 연결했다.

## 공식 자료

- [ComfyUI FluxGuidance 노드 설명](https://docs.comfy.org/built-in-nodes/FluxGuidance)
- [ComfyUI FluxGuidance·CLIPTextEncodeFlux 구현](https://github.com/Comfy-Org/ComfyUI/blob/master/comfy_extras/nodes_flux.py)
- [ComfyUI FLUX.1 공식 예제](https://comfyanonymous.github.io/ComfyUI_examples/flux/)
- [FLUX.1 dev 모델 카드](https://github.com/black-forest-labs/flux/blob/main/model_cards/FLUX.1-dev.md)

## 다음 단계

- [FLUX 모델 가이드](./README.md) — 모델 구조와 파일 배치
- [ControlNet 아키텍처](../../03-advanced-techniques/controlnet/controlnet-architecture.md) — 구조 조건과 적용 파라미터
- [Sampler 노드 구분](../../03-advanced-techniques/samplers/ksampler-vs-advanced.md) — KSampler와 SamplerCustomAdvanced 입력 차이

---

[홈](../../README.md) · [문서 지도](../../README.md)
