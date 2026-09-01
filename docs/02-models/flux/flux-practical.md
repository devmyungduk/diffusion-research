[문서 지도](../../README.md)

# FLUX.1 작업 선택과 Redux 실습

> FLUX.1에서 참조 이미지를 사용하는 방법은 작업 목적에 따라 달라집니다. 이 문서는 목적에 맞는 기법을 고른 뒤, ComfyUI 공식 Redux 예제를 그대로 불러와 첫 이미지 변형을 실행하는 데 집중합니다.

## 이 장에서 배우는 것

- 참조 이미지를 사용하는 기법이 여럿이라, 먼저 "무엇을 바꾸려 하는가"로 골라야 합니다.
- Redux는 공식 예제 PNG를 캔버스에 끌어다 놓아 실행합니다. 노드를 직접 조립하지 않습니다.

<div class="guide-meta" markdown>
**대상** FLUX.1을 처음 사용하는 입문자·디자이너·작가 · **사전 이해** ComfyUI에서 기본 Text-to-Image 워크플로우를 한 번 실행한 경험 · **시간** 20분

**이럴 때 읽으세요** 참조 이미지로 변형을 만들고 싶은데 Redux·ControlNet·Kontext 중 무엇을 사용할지 모를 때.
</div>

<a id="style-transfer-methods"></a>

## 1. 작업 목적부터 구분하기

참조 이미지를 사용한다는 공통점만으로 기법의 품질 순위를 매길 수는 없습니다. 무엇을 바꾸려는지에 따라 사용할 기법이 갈립니다.

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

기본값 `1.0` · `multiply`가 공식 예제의 출발점입니다. 다른 값이 항상 더 낫다는 뜻이 아니므로, 먼저 기본값으로 한 장을 만든 뒤 [Redux 확인과 비교 실험](redux-tuning.md)의 방식으로 하나씩 비교합니다.

!!! warning "오래된 설명에 주의하세요"
    `strength`와 `strength_type`은 Redux 지원과 함께 코어 `StyleModelApply`에 추가된 입력입니다. "코어 Redux에는 강도 조절이 없다"고 설명하는 자료(일부 문서 페이지 포함)는 추가 이전에 작성된 것입니다. 화면의 노드에 위젯이 보이는지를 보고 판단하세요.

## 3. 필요한 파일

공식 예제를 실행하려면 기본 FLUX.1 모델 구성 외에 Redux용 파일 두 개가 필요합니다.

| 파일 | 저장 위치 | 역할 |
|---|---|---|
| `flux1-redux-dev.safetensors` | `ComfyUI/models/style_models/` | Redux style model |
| `sigclip_vision_patch14_384.safetensors` | `ComfyUI/models/clip_vision/` | 참조 이미지 인코더 |

FLUX.1 dev 전체 모델 구성을 사용할 때는 `flux1-dev.safetensors`, FLUX용 CLIP-L·T5 텍스트 인코더, `ae.safetensors`도 필요합니다. 이미 기본 FLUX.1 dev 워크플로우가 실행된다면 기존 파일을 그대로 사용합니다.

!!! note "파일명은 끝까지 확인하세요"
    실제 선택 목록에 `sigclip_vision_patch14_384.safetensors`가 표시되는지 확인합니다. 문서에서도 파일명을 줄여 표기하지 않습니다.

## 4. 공식 워크플로우 불러오기

1. [ComfyUI 공식 FLUX 예제](https://comfyanonymous.github.io/ComfyUI_examples/flux/)에서 **Redux** 항목으로 이동합니다.
2. 예제 이미지를 내려받습니다.
3. 이미지를 ComfyUI 화면에 끌어다 놓습니다.
4. `Load Image` 노드에서 직접 사용할 참조 이미지를 업로드해 선택합니다. 공식 워크플로우에 기록된 예전 입력 파일이 로컬에 없으면 이 단계를 생략할 수 없습니다.
5. 누락된 모델이 표시되면 3절의 파일명과 저장 위치를 다시 확인합니다.

이 방법으로 불러온 예제는 `SamplerCustomAdvanced` 구성을 사용합니다. `KSampler`로 다시 조립한 변형 워크플로우와 섞지 말고, 먼저 공식 구성을 그대로 한 번 실행합니다.

!!! info "검증 기준"
    이 문서의 노드와 시작값은 2026-08-10에 공식 Redux 예제 PNG의 내장 워크플로우를 확인한 결과입니다. 핵심 구성은 `ModelSamplingFlux`, `FluxGuidance`, `StyleModelApply`, `BasicGuider`, `SamplerCustomAdvanced`입니다. 공식 예제가 바뀌면 새 예제의 내장 워크플로우를 우선합니다.

## 완료 기준

세 가지를 모두 만족했다면 이 장을 끝냈습니다.

- Redux, ControlNet, Kontext의 목적을 구분할 수 있다.
- Redux용 파일 두 개를 알맞은 폴더에 배치했다.
- 공식 Redux 예제를 불러와 이미지 한 장을 만들었다.

## 다음 단계

- [Redux 확인과 비교 실험](redux-tuning.md) — 연결을 확인하고 값을 바꿔 비교하기
- [FluxGuidance 이해와 사용](fluxguidance-pipeline.md) — 텍스트 guidance 비교
- [ControlNet 아키텍처](../../03-advanced-techniques/controlnet/controlnet-architecture.md) — 구조 조건이 필요할 때

---

[문서 지도](../../README.md) · [Flux 모델 가이드](README.md)
