[홈](../../README.md) · [문서 지도](../../README.md)

# FLUX.1 작업 선택과 Redux 실습

FLUX.1에서 참조 이미지를 사용하는 방법은 작업 목적에 따라 달라집니다. 이 문서는 목적에 맞는 기법을 고른 뒤, ComfyUI 공식 Redux 예제를 그대로 불러와 첫 이미지 변형을 실행하는 데 집중합니다.

## 이 장에서 배우는 것

- 참조 이미지를 쓰는 기법이 여럿이라, 먼저 "무엇을 바꾸려 하는가"로 골라야 합니다.
- Redux는 공식 예제를 그대로 불러와 실행하는 것이 가장 빠릅니다. 직접 조립하지 않습니다.

<div class="guide-meta" markdown>
**대상** FLUX.1을 처음 사용하는 입문자·디자이너·작가 · **사전 이해** ComfyUI에서 기본 Text-to-Image 워크플로우를 한 번 실행한 경험 · **시간** 20분

**이럴 때 읽으세요** 참조 이미지로 변형을 만들고 싶은데 Redux·ControlNet·Kontext 중 무엇을 쓸지 모를 때.
</div>

## 학습 목표

- Redux, ControlNet, Kontext의 목적을 구분할 수 있다.
- 공식 Redux 예제에서 텍스트 조건과 참조 이미지 조건이 합쳐지는 지점을 찾을 수 있다.
- `StyleModelApply`의 `strength`와 `strength_type`이 무엇을 조절하는지 설명할 수 있다.
- 같은 Seed와 설정을 유지해 참조 이미지 또는 프롬프트만 비교할 수 있다.

<a id="style-transfer-methods"></a>

## 1. 작업 목적부터 구분하기

참조 이미지를 사용한다는 공통점만으로 기법의 품질 순위를 매길 수는 없습니다. 먼저 바꾸려는 대상을 기준으로 선택합니다.

| 만들려는 결과 | 먼저 확인할 기법 | 제어하는 정보 | 다음 문서 |
|---|---|---|---|
| 텍스트만으로 새 이미지 생성 | FLUX.1 dev Text-to-Image | 프롬프트 조건 | [FluxGuidance 이해와 사용](fluxguidance-pipeline.md) |
| 한 장 이상의 이미지를 참고한 변형 | FLUX.1 Redux | 참조 이미지에서 얻은 조건 | 이 문서의 Redux 실습 |
| 윤곽·깊이·포즈 같은 구조 유지 | FLUX 호환 ControlNet | 전처리한 구조 이미지 | [ControlNet 아키텍처](../../03-advanced-techniques/controlnet/controlnet-architecture.md) |
| 기존 이미지의 내용을 지시문으로 편집 | FLUX.1 Kontext | 입력 이미지와 편집 지시 | 모델별 공식 워크플로우 |

Redux 결과에 참조 이미지의 색감이나 구성이 반영될 수 있지만, Redux의 공식 용도는 특정 화풍만 복제하는 좁은 의미의 스타일 전송이 아니라 **이미지 변형 생성**입니다.

## 2. Redux가 하는 일

Redux는 FLUX.1 dev 또는 FLUX.1 schnell을 이미지로 조건화하는 어댑터입니다. ComfyUI 공식 예제에서는 다음 데이터가 `StyleModelApply`에서 합쳐집니다.

| 입력 | 만들어지는 과정 | 의미 |
|---|---|---|
| `conditioning` | 프롬프트 인코딩 후 FluxGuidance 적용 | 텍스트 조건과 FLUX guidance 값 |
| `style_model` | Style Model Loader로 Redux 모델 로드 | 이미지 조건을 만드는 Redux 모델 |
| `clip_vision_output` | 참조 이미지를 SigCLIP Vision으로 인코딩 | 참조 이미지의 시각 정보 |

`StyleModelApply`는 세 입력을 받아 새로운 `CONDITIONING`을 출력합니다. 여기에 더해 노드 안에 위젯 두 개가 있습니다.

| 위젯 | 기본값 | 역할 |
|---|---|---|
| `strength` | `1.0` | 참조 이미지 조건의 반영 강도 (범위 0.0~10.0) |
| `strength_type` | `multiply` | 강도를 적용하는 방식. `multiply`와 `attn_bias` 중 선택 |

기본값 `1.0` · `multiply`가 공식 예제의 출발점입니다. 다른 값이 항상 더 낫다는 뜻이 아니므로, 먼저 기본값으로 한 장을 만든 뒤 [7절](#7-첫-비교-실험)의 방식으로 하나씩 비교합니다.

!!! warning "오래된 설명에 주의하세요"
    `strength`와 `strength_type`은 Redux 지원과 함께 코어 `StyleModelApply`에 추가된 입력입니다. "코어 Redux에는 강도 조절이 없다"고 설명하는 자료(일부 문서 페이지 포함)는 추가 이전에 쓰인 것입니다. 화면의 노드에 위젯이 보이는지를 보고 판단하세요.

## 3. 필요한 파일

공식 예제를 실행하려면 기본 FLUX.1 모델 구성 외에 Redux용 파일 두 개가 필요합니다.

| 파일 | 저장 위치 | 역할 |
|---|---|---|
| `flux1-redux-dev.safetensors` | `ComfyUI/models/style_models/` | Redux style model |
| `sigclip_vision_patch14_384.safetensors` | `ComfyUI/models/clip_vision/` | 참조 이미지 인코더 |

FLUX.1 dev 전체 모델 구성을 사용할 때는 `flux1-dev.safetensors`, FLUX용 CLIP-L·T5 텍스트 인코더, `ae.safetensors`도 필요합니다. 이미 기본 FLUX.1 dev 워크플로우가 실행된다면 기존 파일을 그대로 사용합니다.

!!! note "파일명은 끝까지 확인하세요"
    실제 선택 목록에 `sigclip_vision_patch14_384.safetensors`가 표시되는지 확인합니다. 문서에서도 파일명을 줄여 쓰지 않습니다.

## 4. 공식 워크플로우 불러오기

1. [ComfyUI 공식 FLUX 예제](https://comfyanonymous.github.io/ComfyUI_examples/flux/)에서 **Redux** 항목으로 이동합니다.
2. 예제 이미지를 내려받습니다.
3. 이미지를 ComfyUI 화면에 끌어다 놓습니다.
4. `Load Image` 노드에서 직접 사용할 참조 이미지를 업로드해 선택합니다. 공식 워크플로우에 기록된 예전 입력 파일이 로컬에 없으면 이 단계를 생략할 수 없습니다.
5. 누락된 모델이 표시되면 3절의 파일명과 저장 위치를 다시 확인합니다.

이 방법으로 불러온 예제는 `SamplerCustomAdvanced` 구성을 사용합니다. `KSampler`로 다시 조립한 변형 워크플로우와 섞지 말고, 먼저 공식 구성을 그대로 한 번 실행합니다.

!!! info "검증 기준"
    이 문서의 노드와 시작값은 2026-08-10에 공식 Redux 예제 PNG의 내장 워크플로우를 확인한 결과입니다. 핵심 구성은 `ModelSamplingFlux`, `FluxGuidance`, `StyleModelApply`, `BasicGuider`, `SamplerCustomAdvanced`입니다. 공식 예제가 바뀌면 새 예제의 내장 워크플로우를 우선합니다.

## 5. 노드와 포트 확인

화면에서 노드 위치를 외우기보다 출력 타입이 어느 입력으로 들어가는지 확인합니다.

### 참조 이미지 조건

| 보내는 출력 | 받는 입력 | 확인할 값 |
|---|---|---|
| CLIP Vision Loader `CLIP_VISION` | CLIP Vision Encode `clip_vision` | `sigclip_vision_patch14_384.safetensors` |
| Load Image `IMAGE` | CLIP Vision Encode `image` | 사용할 참조 이미지 |
| CLIP Vision Encode `CLIP_VISION_OUTPUT` | Style Model Apply `clip_vision_output` | 포트 타입 일치 |
| Style Model Loader `STYLE_MODEL` | Style Model Apply `style_model` | `flux1-redux-dev.safetensors` |

### 텍스트 조건

| 보내는 출력 | 받는 입력 | 역할 |
|---|---|---|
| Dual CLIP Loader `CLIP` | CLIP Text Encode `clip` | 프롬프트 인코딩 |
| CLIP Text Encode `CONDITIONING` | FluxGuidance `conditioning` | 텍스트 조건 전달 |
| FluxGuidance `CONDITIONING` | Style Model Apply `conditioning` | guidance가 포함된 텍스트 조건 전달 |
| Style Model Apply `CONDITIONING` | BasicGuider `conditioning` | 텍스트와 참조 이미지 조건을 sampler에 전달 |

### 샘플링과 이미지 출력

| 보내는 출력 | 받는 입력 | 역할 |
|---|---|---|
| Load Diffusion Model `MODEL` | ModelSamplingFlux `model` | FLUX.1 모델 전달 |
| ModelSamplingFlux `MODEL` | BasicGuider `model` | FLUX 샘플링 설정이 적용된 모델 전달 |
| ModelSamplingFlux `MODEL` | BasicScheduler `model` | 모델에 맞는 sigma schedule 계산 |
| RandomNoise `NOISE` | SamplerCustomAdvanced `noise` | Seed로 만든 시작 노이즈 |
| BasicGuider `GUIDER` | SamplerCustomAdvanced `guider` | 최종 conditioning과 모델 전달 |
| KSamplerSelect `SAMPLER` | SamplerCustomAdvanced `sampler` | sampler 알고리즘 전달 |
| BasicScheduler `SIGMAS` | SamplerCustomAdvanced `sigmas` | 스텝별 노이즈 수준 전달 |
| EmptySD3LatentImage `LATENT` | SamplerCustomAdvanced `latent_image` | 생성 크기와 batch 전달 |
| SamplerCustomAdvanced `output` | VAE Decode `samples` | 생성된 latent 전달 |
| Load VAE `VAE` | VAE Decode `vae` | latent 디코딩 |
| VAE Decode `IMAGE` | Save Image `images` | 이미지 저장 |

## 6. 공식 예제의 시작값

다음 값은 공식 Redux 예제 이미지에 저장된 워크플로우의 설정입니다. 모든 이미지에서 가장 좋은 값이라는 뜻이 아니라, 예제를 재현하기 위한 시작점입니다.

| 노드 | 설정 | 예제 값 |
|---|---|---:|
| FluxGuidance | `guidance` | `3.5` |
| ModelSamplingFlux | `max_shift` | `1.15` |
| ModelSamplingFlux | `base_shift` | `0.5` |
| ModelSamplingFlux | `width`, `height` | `1024`, `1024` |
| KSamplerSelect | `sampler_name` | `euler` |
| BasicScheduler | `scheduler` | `simple` |
| BasicScheduler | `steps` | `20` |
| BasicScheduler | `denoise` | `1.0` |
| EmptySD3LatentImage | `width`, `height`, `batch_size` | `1024`, `1024`, `1` |
| RandomNoise | `noise_seed` | `958831004022715` |

`StyleModelApply`의 `strength`·`strength_type`은 노드 기본값인 `1.0`·`multiply`를 그대로 씁니다. 불러온 워크플로우에서 다른 값으로 되어 있다면 그 값이 우선이며, 비교 실험 전에 무엇으로 설정돼 있는지 먼저 확인하세요.

`SamplerCustomAdvanced`에는 `cfg` 위젯이 없습니다. 공식 예제에서는 `BasicGuider`가 최종 conditioning을 전달합니다. `KSampler`의 `cfg=1.0` 설명을 이 구성에 그대로 옮겨 적지 않습니다.

`ModelSamplingFlux`와 `EmptySD3LatentImage`의 너비·높이는 같은 생성 크기를 사용합니다. 해상도를 바꿀 때 한쪽만 바꾸지 않습니다.

## 7. 첫 비교 실험

먼저 공식 예제를 한 번 실행해 모델과 연결이 정상인지 확인합니다. 공식 PNG의 `RandomNoise`는 생성 후 Seed 동작이 `randomize`로 저장되어 있으므로, 비교 실험 전에 다음 절차로 기준을 다시 만듭니다.

1. `RandomNoise`의 Seed를 기록합니다.
2. 생성 후 Seed 동작을 `fixed`로 바꿉니다.
3. 한 번 더 실행해 비교용 기준 이미지를 저장합니다.
4. 아래 표에 따라 한 번에 하나만 바꿉니다.

| 비교 | 고정할 항목 | 바꿀 항목 | 관찰할 내용 |
|---|---|---|---|
| A | 모델·Seed·프롬프트·샘플링 설정 | 참조 이미지 | 색, 형태, 구도 중 무엇이 달라지는가 |
| B | 모델·Seed·참조 이미지·샘플링 설정 | 프롬프트 | 텍스트 지시가 어떤 요소를 바꾸는가 |
| C | 모델·Seed·참조 이미지·프롬프트 | guidance | 지시 반영과 화면의 자연스러움이 어떻게 달라지는가 |
| D | 나머지 전부 | `StyleModelApply`의 `strength` | 참조 이미지의 영향이 얼마나 강해지거나 약해지는가 |

D를 진행할 때는 기본값 `1.0`에서 출발해 작은 폭으로 올리거나 내립니다. `strength_type`까지 동시에 바꾸면 어느 쪽이 결과를 바꿨는지 구분할 수 없습니다.

### 기록 양식

| 항목 | 기록 |
|---|---|
| 기본 모델·정밀도 |  |
| 참조 이미지 |  |
| 프롬프트 |  |
| Seed |  |
| guidance |  |
| sampler·scheduler·steps |  |
| 참조 이미지에서 유지된 요소 |  |
| 프롬프트로 바뀐 요소 |  |
| 다음에 바꿀 한 가지 |  |

## 8. 문제 해결

| 증상 | 확인 순서 |
|---|---|
| CLIP Vision 모델을 찾지 못함 | 1. 파일명 확인<br>2. `models/clip_vision/` 위치 확인<br>3. ComfyUI 재시작 |
| Style Model을 찾지 못함 | 1. `flux1-redux-dev.safetensors` 확인<br>2. `models/style_models/` 위치 확인 |
| `StyleModelApply`에서 strength를 찾을 수 없음 | ComfyUI가 오래된 버전일 수 있습니다. 업데이트한 뒤 노드를 다시 추가해 `strength`·`strength_type` 위젯이 보이는지 확인 |
| 참조 이미지의 영향이 보이지 않음 | 1. Load Image 연결<br>2. CLIP Vision Encode 출력<br>3. Style Model Apply 출력<br>4. BasicGuider 입력 확인 |
| 프롬프트를 바꿔도 차이가 없음 | CLIP Text Encode 출력이 FluxGuidance와 Style Model Apply를 거쳐 BasicGuider로 들어가는지 확인 |
| `cfg` 입력을 찾을 수 없음 | 공식 예제의 SamplerCustomAdvanced 구성인지 확인. `cfg`는 이 노드의 입력이 아닙니다. |
| 결과가 비교할 때마다 크게 바뀜 | RandomNoise의 Seed와 생성 후 Seed 동작을 고정 |

## 9. 복습 Q&A

**Q. Redux는 스타일 전송 전용인가요?**  
A. 아닙니다. 공식 용도는 참조 이미지로 FLUX.1 dev 또는 schnell을 조건화해 이미지 변형을 만드는 것입니다.

**Q. Style Model Apply의 권장 strength는 얼마인가요?**  
A. 노드 기본값은 `1.0`이며 이것이 공식 예제의 출발점입니다. 모든 이미지에 맞는 권장값은 없으므로, 나머지를 고정하고 이 값만 바꿔 비교해 정합니다.

**Q. FluxGuidance는 참조 이미지를 인코딩하나요?**  
A. 아닙니다. 텍스트 conditioning에 FLUX guidance 값을 설정합니다. 참조 이미지는 CLIP Vision Encode와 Redux style model 경로에서 처리됩니다.

**Q. 공식 예제는 KSampler를 사용하나요?**  
A. 현재 공식 Redux 예제 이미지는 `SamplerCustomAdvanced`, `BasicGuider`, `KSamplerSelect`, `BasicScheduler`를 조립해 사용합니다.

**Q. guidance 3.5가 항상 최적인가요?**  
A. 아닙니다. 공식 예제를 재현하는 시작값입니다. 같은 Seed와 나머지 설정을 고정하고 비교합니다.

## 완료 기준

- 공식 Redux 예제를 ComfyUI에 불러와 실행했다.
- `StyleModelApply`의 세 입력과 출력, 그리고 `strength`·`strength_type` 위젯을 설명할 수 있다.
- Redux 구성과 KSampler 구성을 섞지 않고 sampler 입력을 확인할 수 있다.
- 한 번에 변수 하나만 바꾼 비교 결과를 기록했다.

## 다음 단계와 공식 자료

- [FluxGuidance 이해와 사용](fluxguidance-pipeline.md) — 텍스트 guidance 비교
- [KSampler·KSamplerAdvanced·SamplerCustomAdvanced](../../03-advanced-techniques/samplers/ksampler-vs-advanced.md) — sampler 노드 구분
- [ControlNet 아키텍처](../../03-advanced-techniques/controlnet/controlnet-architecture.md) — 구조 조건이 필요할 때
- [ComfyUI 공식 FLUX 예제](https://comfyanonymous.github.io/ComfyUI_examples/flux/) — Redux 워크플로우와 모델 위치
- [FLUX.1 Redux 공식 설명](https://github.com/black-forest-labs/flux/blob/main/docs/image-variation.md) — 이미지 변형 용도
- [ComfyUI StyleModelApply 노드 페이지](https://docs.comfy.org/built-in-nodes/StyleModelApply) — 문서 페이지가 현재 노드보다 늦게 갱신될 수 있습니다. 위젯 목록은 화면의 노드를 기준으로 확인하세요

---

[홈](../../README.md) · [문서 지도](../../README.md) · [Flux 모델 가이드](README.md)
