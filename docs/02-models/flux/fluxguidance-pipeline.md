[문서 지도](../../README.md)

# FluxGuidance 이해와 사용

> `FluxGuidance`는 FLUX.1 dev가 프롬프트 조건을 얼마나 강하게 참고할지 나타내는 숫자를 `CONDITIONING`에 넣는 노드입니다. 먼저 기본 생성을 완성한 뒤, 같은 프롬프트와 Seed에서 값을 바꿔 비교합니다.

## 이 장에서 배우는 것

- FluxGuidance는 프롬프트를 인코딩한 `CONDITIONING`에 guidance 값을 얹어 FLUX.1 dev에 전달합니다.
- 연결 경로는 `CLIP Text Encode + FluxGuidance`와 `CLIPTextEncodeFlux` 두 가지이며, 겹쳐 사용하면 뒤 노드의 값이 앞의 값을 덮어씁니다.
- KSampler의 `cfg`와는 다른 값입니다. FLUX.1 dev 공식 기본 구성은 `cfg=1.0`이고 negative에는 빈 텍스트를 넣습니다.

<div class="guide-meta" markdown>
**대상** FLUX.1 dev를 처음 사용하는 입문자·디자이너·작가 · **사전 이해** 프롬프트를 입력하고 워크플로우를 한 번 실행해 본 경험 · **시간** 15분

**이럴 때 읽으세요** guidance 값을 어느 노드에 넣는지 모르거나, KSampler의 `cfg`와 무엇이 다른지 확인하고 싶을 때.
</div>

## 1. FluxGuidance가 맡는 역할

ComfyUI는 프롬프트를 텍스트 인코더로 처리해 `CONDITIONING`이라는 데이터 묶음을 만듭니다. 이 묶음에는 모델이 생성 과정에서 참고할 텍스트 정보와 추가 설정이 담깁니다.

| 단계 | 처리 | 결과 |
|---:|---|---|
| 1 | 프롬프트를 Text Encode에 입력 | 텍스트 조건이 담긴 `CONDITIONING` |
| 2 | conditioning과 guidance 값을 FluxGuidance에 입력 | guidance 값이 포함된 `CONDITIONING` |
| 3 | 출력 conditioning을 Sampler에 전달 | FLUX.1 dev가 생성 과정에서 조건을 사용 |

guidance는 프롬프트와 별개로 `CONDITIONING`에 얹히는 하나의 숫자입니다. 특정 단어 하나의 가중치가 아니며, 값을 두 배로 올린다고 프롬프트 반영이 정확히 두 배가 되지는 않습니다.

### 노드 입력과 출력

| 이름 | 타입 | 역할 |
|---|---|---|
| `conditioning` | `CONDITIONING` | Text Encode 등에서 만든 프롬프트 조건 |
| `guidance` | `FLOAT` | 모델에 전달할 guidance 값 |
| 출력 | `CONDITIONING` | 기존 조건에 guidance 값이 포함된 결과 |

### 구현을 확인할 때

현재 ComfyUI 구현은 기존 conditioning을 받아 `guidance` 항목을 설정합니다. 프롬프트를 다시 토큰화하거나 텍스트 인코더를 다시 실행하는 구조가 아닙니다. 이 세부 내용은 노드를 한 번 사용해 본 뒤 동작 원리를 확인할 때 참고합니다.

## 2. 어떤 노드를 연결할까

현재 ComfyUI에서는 두 가지 형태를 볼 수 있습니다. 워크플로우 안에서 한 가지 경로를 선택합니다.

### 경로 A — Text Encode와 FluxGuidance를 분리

FLUX.1 dev 공식 예제에서 볼 수 있는 구성입니다.

| 순서 | 노드 | 입력 또는 설정 | 출력 |
|---:|---|---|---|
| 1 | Dual CLIP Loader | FLUX.1용 CLIP-L·T5 | `CLIP` |
| 2 | CLIP Text Encode | CLIP과 프롬프트 | `CONDITIONING` |
| 3 | FluxGuidance | conditioning과 guidance 값 | guidance가 포함된 `CONDITIONING` |

프롬프트는 `CLIP Text Encode`에, guidance 값은 `FluxGuidance`에 각각 넣습니다. guidance만 바꾸고 싶으면 `FluxGuidance` 노드만 열면 됩니다.

### 경로 B — CLIPTextEncodeFlux에서 함께 입력

현재 내장 `CLIPTextEncodeFlux`는 CLIP-L 프롬프트, T5 프롬프트, guidance 값을 한 노드에서 입력받습니다.

| 순서 | 노드 | 입력 또는 설정 | 출력 |
|---:|---|---|---|
| 1 | Dual CLIP Loader | FLUX.1용 CLIP-L·T5 | `CLIP` |
| 2 | CLIPTextEncodeFlux | CLIP-L 프롬프트, T5 프롬프트, guidance 값 | guidance가 포함된 `CONDITIONING` |

`CLIPTextEncodeFlux`가 프롬프트와 guidance를 한 번에 받아 `CONDITIONING`으로 내보냅니다. 뒤에 `FluxGuidance`를 또 붙일 필요가 없습니다.

두 경로를 겹쳐 사용하면 나중 노드의 값이 앞의 값을 덮어씁니다. 의도한 것이 아니라면 **한 경로만 사용하세요.**

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

KSampler의 `cfg=1.0`은 negative 쪽 예측을 계산에 사용하지 않겠다는 설정입니다. FluxGuidance에 넣은 값은 이와 별개로 모델에 그대로 전달됩니다.

### negative 입력은 어떻게 하나

KSampler 노드는 `negative` 연결을 요구합니다. ComfyUI의 FLUX.1 dev FP8 체크포인트 공식 예제는 빈 텍스트를 인코딩한 conditioning을 negative에 연결합니다.

| KSampler 입력 | 연결할 출력 | 텍스트와 설정 |
|---|---|---|
| `positive` | FluxGuidance의 `CONDITIONING` | positive 프롬프트, guidance `3.5`에서 시작 |
| `negative` | 별도 CLIP Text Encode의 `CONDITIONING` | 텍스트를 비워 둠 |

SD에서는 negative에 `blurry, low quality` 같은 단어를 적어 원치 않는 요소를 걸러냅니다. FLUX.1 dev의 기본 구성에서는 그 방식이 동작하지 않습니다. `cfg`가 `1.0`이면 모델이 negative 쪽을 계산에 사용하지 않기 때문입니다.

그래서 negative는 빈 칸으로 둡니다. 단어를 적어도 그 요소가 빠지지 않습니다. 커스텀 체크포인트가 별도 negative나 CFG 설정을 요구하면 그 모델의 안내를 우선합니다.

SamplerCustomAdvanced와 `BasicGuider`를 사용하는 공식 전체 모델 예제는 KSampler와 입력 구조가 다르므로 negative 포트가 없습니다. 어느 샘플러 구성을 사용하는지 먼저 확인하세요.

## 완료 기준

세 가지를 모두 만족했다면 이 장을 끝냈습니다.

- FluxGuidance의 입력과 출력을 설명할 수 있다.
- `CLIP Text Encode + FluxGuidance`와 `CLIPTextEncodeFlux` 경로를 구분할 수 있다.
- KSampler cfg와 Flux guidance의 역할을 구분할 수 있다.

## 공식 자료

- [ComfyUI FluxGuidance 노드 설명](https://docs.comfy.org/built-in-nodes/FluxGuidance)
- [ComfyUI FluxGuidance·CLIPTextEncodeFlux 구현](https://github.com/Comfy-Org/ComfyUI/blob/master/comfy_extras/nodes_flux.py)
- [ComfyUI FLUX.1 공식 예제](https://comfyanonymous.github.io/ComfyUI_examples/flux/)
- [FLUX.1 dev 모델 카드](https://github.com/black-forest-labs/flux/blob/main/model_cards/FLUX.1-dev.md)

## 다음 단계

- [guidance 값 비교와 연결](guidance-tuning.md) — 값을 직접 바꿔 보고 워크플로우에 연결하기
- [FLUX 모델 가이드](./README.md) — 모델 구조와 파일 배치
- [Sampler 노드 구분](../../03-advanced-techniques/samplers/ksampler-vs-advanced.md) — KSampler와 SamplerCustomAdvanced 입력 차이

---

[문서 지도](../../README.md)
