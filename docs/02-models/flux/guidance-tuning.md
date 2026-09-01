[문서 지도](../../README.md)

# guidance 값 비교와 연결

> guidance 값을 실제로 바꿔 보고, 워크플로우에 연결해 ControlNet까지 확장합니다.

## 이 장에서 배우는 것

- Seed를 고정하고 guidance만 바꿔 세 장을 비교하는 절차
- KSampler 구성에서 각 포트에 무엇을 연결하는지
- ControlNet을 더할 때 guidance와 strength를 따로 비교하는 방법

<div class="guide-meta" markdown>
**대상** FluxGuidance의 역할을 이해했고 값을 직접 정하려는 사용자 · **사전 이해** [FluxGuidance 이해와 사용](fluxguidance-pipeline.md) · **시간** 20분

**이럴 때 읽으세요** `3.5`를 그대로 사용하고 있는데 이 값이 내 작업에 맞는지 확인하고 싶을 때.
</div>

## 1. guidance 값 비교하기

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

## 2. 기본 워크플로우 연결

다음은 `Load Checkpoint`와 KSampler를 사용하는 FLUX.1 dev 체크포인트 구성입니다.

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
    `Load Diffusion Model`, `Dual CLIP Loader`, `Load VAE`를 따로 사용하더라도 conditioning의 핵심 흐름은 같습니다. 공식 전체 모델 예제처럼 SamplerCustomAdvanced를 사용한다면 해당 예제의 `BasicGuider`, sampler, sigmas 연결을 그대로 따르세요.

## 3. ControlNet과 함께 사용하기

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

## 4. 문제 해결

??? warning "증상별 확인 순서"
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

세 가지를 모두 만족했다면 이 장을 끝냈습니다.

- Seed를 고정하고 guidance 하나만 바꾼 비교 결과를 기록했다.
- KSampler 구성에서 positive·negative에 무엇을 연결하는지 설명할 수 있다.
- ControlNet을 추가했을 때 guidance와 strength를 따로 비교했다.

## 다음 단계

- [FLUX.1 작업 선택과 Redux 실습](flux-practical.md) — 참조 이미지로 변형 만들기
- [ControlNet 아키텍처](../../03-advanced-techniques/controlnet/controlnet-architecture.md) — 구조 조건의 원리
- [ControlNet 연결과 조절](../../03-advanced-techniques/controlnet/controlnet-pipeline.md) — 구조 조건 연결

---

[문서 지도](../../README.md) · [Flux 모델 가이드](README.md)
