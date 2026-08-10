[홈](../../README.md) · [문서 지도](../../README.md)

# Flux Redux의 위치와 역할

Flux Redux는 참조 이미지로 FLUX.1 dev 또는 FLUX.1 schnell을 조건화해 이미지 변형을 만드는 어댑터입니다. 설치와 실행은 [FLUX.1 작업 선택과 Redux 실습](../../02-models/flux/flux-practical.md)에서 다루며, 이 문서는 Redux가 파이프라인의 어느 데이터를 바꾸는지 설명합니다.

## 이 장에서 배우는 것

- Redux는 MODEL이 아니라 CONDITIONING을 바꿉니다. `StyleModelApply`가 텍스트 조건과 참조 이미지 조건을 합칩니다.
- IPAdapter와 달리 ComfyUI 코어 기능이라 커스텀 노드 설치가 필요 없습니다.

<div class="guide-meta" markdown>
**대상** 공식 Redux 예제를 실행한 뒤 연결 원리를 이해하려는 사용자 · **사전 이해** `MODEL`, `CONDITIONING`, `LATENT` 데이터 타입 · **시간** 8분

**이럴 때 읽으세요** Redux 예제는 돌렸고 각 노드가 왜 그렇게 연결되는지 알고 싶을 때.
</div>

## 1. Redux가 수정하는 데이터

ComfyUI 코어 Redux 구성은 참조 이미지에서 얻은 정보를 `CONDITIONING`에 반영합니다. 기본 모델 자체를 패치하는 기법으로 설명하면 안 됩니다.

| 기법 | 주된 목적 | sampler로 전달되는 경로 |
|---|---|---|
| Flux Redux | 참조 이미지 기반 이미지 변형 | `StyleModelApply`가 만든 `CONDITIONING` |
| ControlNet | 윤곽·깊이·포즈 같은 구조 조건 | Apply ControlNet이 만든 positive·negative `CONDITIONING` |
| Kontext | 입력 이미지의 내용 편집 | 모델별 공식 편집 워크플로우 |

세 기법은 목적과 조건 입력이 다르므로 단일 품질 순위로 비교하지 않습니다.

## 2. StyleModelApply에서 합쳐지는 정보

| 입력 | 타입 | 공식 예제의 공급 노드 |
|---|---|---|
| `conditioning` | `CONDITIONING` | FluxGuidance |
| `style_model` | `STYLE_MODEL` | Style Model Loader |
| `clip_vision_output` | `CLIP_VISION_OUTPUT` | CLIP Vision Encode |

`StyleModelApply`는 세 입력을 받아 새 `CONDITIONING`을 출력합니다. 이 출력이 `BasicGuider`로 전달되면서 텍스트 조건과 참조 이미지 조건이 생성 과정에 사용됩니다.

여기에 더해 노드 안에 `strength`(기본 `1.0`, 범위 0.0~10.0)와 `strength_type`(`multiply` 또는 `attn_bias`) 위젯이 있습니다. 참조 이미지 조건의 반영 강도를 이 값으로 조절합니다.

화면에서 노드가 놓인 위치는 조건의 우선순위를 뜻하지 않습니다. 실제로 어떤 출력 포트가 다음 입력 포트에 연결됐는지를 확인해야 합니다.

## 3. 코어 Redux에 있는 값과 없는 값

무엇이 코어 노드의 입력인지 먼저 구분합니다.

| 자주 보는 설명 | 확인할 사실 |
|---|---|
| “Redux 강도는 strength로 조절한다” | 맞습니다. 코어 StyleModelApply의 위젯이며 기본값은 `1.0` |
| “Redux strength는 0.8부터 시작해야 한다” | 근거 없는 고정값입니다. 기본값 `1.0`에서 출발해 직접 비교합니다 |
| “downsampling_factor로 Redux 강도를 바꾼다” | 공식 코어 Redux 연결의 입력이 아님 |
| “Conditioning Combine이 반드시 필요하다” | 공식 예제는 FluxGuidance 출력을 StyleModelApply에 직접 연결 |
| “프롬프트 가중치를 높이면 이미지 조건과 일정 비율로 경쟁한다” | 그런 비례 관계는 보장되지 않음 |

커스텀 노드에서 별도 입력을 제공하면 노드 이름과 배포 문서를 확인하고 코어 Redux와 구분합니다.

## 4. ControlNet과 구분하는 기준

| 질문 | Redux | ControlNet |
|---|---|---|
| 입력 이미지에서 사용하는 정보 | SigCLIP Vision으로 얻은 시각 조건 | Canny·Depth·Pose 등 구조 조건 |
| 코어 조절 위치 | StyleModelApply의 `strength`·`strength_type` | 적용 노드의 strength와 시작·종료 구간 |
| 먼저 확인할 실패 지점 | CLIP Vision과 Style Model 연결 | 전처리기와 ControlNet 모델의 종류 일치 |

참조 이미지의 전반적인 변형이 목적이면 Redux부터 확인합니다. 윤곽이나 깊이처럼 명시적인 구조를 따라야 한다면 FLUX 호환 ControlNet을 확인합니다. 두 기법의 결합은 각각을 단독으로 실행한 뒤 진행합니다.

## 복습 Q&A

**Q. Redux는 MODEL을 바꾸나요?**  
A. 코어 구성에서 Redux 정보는 `StyleModelApply`가 출력하는 `CONDITIONING` 경로로 전달됩니다.

**Q. Redux conditioning을 만들기 위해 Conditioning Combine이 필수인가요?**  
A. 아닙니다. 공식 예제는 FluxGuidance의 conditioning을 `StyleModelApply`에 직접 넣습니다.

**Q. 참조 이미지의 영향은 어디에서 확인하나요?**  
A. Load Image, CLIP Vision Encode, StyleModelApply, BasicGuider의 포트 연결을 차례로 확인합니다. 실행과 비교 절차는 [Redux 실습](../../02-models/flux/flux-practical.md#7-첫-비교-실험)을 따릅니다.

## 완료 기준

세 가지를 모두 만족했다면 이 장을 끝냈습니다.

- Redux가 CONDITIONING 라인에서 동작한다는 점을 설명할 수 있다.
- `StyleModelApply`의 세 입력이 각각 어느 노드에서 오는지 짚을 수 있다.
- Redux와 ControlNet 중 어느 쪽을 쓸지 목적으로 판단할 수 있다.

## 다음 단계

- [FLUX.1 작업 선택과 Redux 실습](../../02-models/flux/flux-practical.md) — 실제 실행과 비교 실험
- [ControlNet 아키텍처](controlnet-architecture.md) — 구조 조건이 필요할 때
- [제어 기법 실전 워크플로우](example-workflows.md) — 조합 예시

## 공식 자료

- [ComfyUI 공식 FLUX Redux 예제](https://comfyanonymous.github.io/ComfyUI_examples/flux/)
- [FLUX.1 Redux 공식 설명](https://github.com/black-forest-labs/flux/blob/main/docs/image-variation.md)
- [ComfyUI StyleModelApply 노드 페이지](https://docs.comfy.org/built-in-nodes/StyleModelApply) — 문서 페이지가 현재 노드보다 늦게 갱신될 수 있으므로 위젯 목록은 화면의 노드를 기준으로 확인

---

[홈](../../README.md) · [문서 지도](../../README.md) · [ControlNet 아키텍처](controlnet-architecture.md)
