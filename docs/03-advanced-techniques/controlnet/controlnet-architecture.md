[문서 지도](../../README.md)

# ControlNet 아키텍처

> 이미지의 구조를 제어하는 ControlNet의 작동 원리

## 이 장에서 배우는 것

- ControlNet은 원본 모델을 복제한 사본으로 포즈·깊이·윤곽 같은 구조를 읽고, 그 출력을 Zero Convolution으로 원본에 더합니다.
- 전처리기(Canny/Depth/OpenPose)로 조건 이미지를 만들고 strength와 적용 구간으로 구조 반영 정도를 조절합니다.

<div class="guide-meta" markdown>
**대상** ControlNet이 어떻게 작동하는지 궁금한 중급 사용자 · **사전 이해** Diffusion Model 기본 원리 · **시간** 20분

**이럴 때 읽으세요** 구도·포즈를 정확히 통제하고 싶을 때.
</div>

## 이 폴더의 문서

ControlNet 본체의 원리는 이 문서에서 다루고, 연결과 조합 규칙, 함께 사용되는 제어 기법은 개별 문서로 분리했습니다.

이 문서: [1. 핵심 개념](#1-핵심-개념) · [2. ControlNet 구조](#2-controlnet-구조)

관련 문서:
- [IPAdapter](ipadapter.md) — 참조 이미지로 스타일 옮기기
- [Flux Redux](flux-redux.md) — 참조 기반 변형
- [Differential Diffusion](differential-diffusion.md) — 부드러운 Inpainting
- [Flux 모델 변형 비교](flux-model-variants.md) — Dev/Fill, FP8, GGUF 선택
- [ControlNet 연결과 조절](controlnet-pipeline.md) — 실제 워크플로우 연결
- [제어 기법 실전 워크플로우](example-workflows.md) — 조합 예시

---

## 1. 핵심 개념

### MODEL·CONDITIONING 수정 지점

| Component | 수정 대상 | 라인 | 목적 |
|:----------|:--------|:-----|:-----|
| **LoRA** | MODEL | Model 라인 | 사전 학습된 스타일/캐릭터 |
| **IPAdapter** | MODEL | Model 라인 | 실시간 이미지 참조 |
| **Flux Redux** | CONDITIONING | Conditioning 라인 | 이미지 변형 생성 |
| **ControlNet** | CONDITIONING | Conditioning 라인 | 구조 제어 (포즈/깊이/윤곽선) |
| **InpaintModelConditioning** | CONDITIONING + LATENT | 양쪽 라인 | 마스크 영역 편집 |
| **FluxGuidance** | CONDITIONING | Conditioning 라인 | FLUX.1 dev의 guidance 값 설정 |
| **Differential Diffusion** | MODEL | Model 라인 | 픽셀별 denoise 강도 |

### ControlNet과 Inpainting은 무엇을 받는가

1. **ControlNet** — 전처리한 구조 이미지를 받아 포즈·윤곽·깊이를 conditioning에 얹습니다.
2. **Inpainting** — 마스크를 받아 다시 그릴 영역을 지정합니다.

스타일이나 분위기를 옮기는 것은 ControlNet이 아니라 [IPAdapter](ipadapter.md)·[Flux Redux](flux-redux.md)의 역할입니다.

텍스트 조건은 guidance, 구조 조건은 ControlNet strength와 적용 구간으로 각각 조절합니다. 두 값을 따로 기록해야 어느 쪽을 바꿔서 결과가 달라졌는지 구분됩니다.

---

## 2. ControlNet 구조

### 2.1 구조 개요

1. **Input Conditioning Image** (Depth/Pose/Edge/Canny)
2. **Conv Encoder** — 3→320 channels
3. **ControlNet Copy of U-Net** — 여러 Block으로 구성
4. **Zero Convolution** — 각 Block 출력을 원본 U-Net에 연결
5. **Original SD U-Net** — Encoder→Decoder, ControlNet 출력을 addition으로 합산
6. **Denoised Latent** 출력

### 2.2 주요 파라미터

| 파라미터 | 입력 가능 범위 | 설명 | 시작값 |
|:---------|:-----|:-----|:-------|
| **strength** | 0.0 ~ 10.0 | 제어 강도 | 1.0(노드 기본값) |
| **start_percent** | 0.0 ~ 1.0 | 제어 시작 시점 | 0.0 |
| **end_percent** | 0.0 ~ 1.0 | 제어 종료 시점 | 1.0 |

**strength 값별 경향:**
| Strength | 효과 |
|:---:|---|
| 0.0 | 제어 없음 |
| 0.5 | 약한 힌트 |
| 1.0 | 노드 기본값 |
| 1.5 이상 | 강한 제어. 구도가 경직되고 아티팩트가 늘어나기 쉬움 |

입력 자체는 10.0까지 가능하지만 실사용 범위는 위 표의 0.5~1.5 구간입니다. 실제로 사용할 값은 아래 [ControlNet 연결과 조절](controlnet-pipeline.md#텍스트와-구조-균형-조절)의 방식으로 정합니다.

### 2.3 전처리기 종류

!!! warning "전처리기는 대부분 커스텀 노드입니다"
    아래 전처리기 대부분은 ComfyUI에 기본 포함되어 있지 않습니다. 노드 검색 목록에 `OpenPose Pose`, `Depth Anything`, `Scribble Lines` 같은 이름이 보이지 않는다면 설치되지 않은 것입니다.

    - ComfyUI-Manager에서 전처리기 노드 팩(대표적으로 [comfyui_controlnet_aux](https://github.com/Fannovel16/comfyui_controlnet_aux))을 설치한 뒤 ComfyUI를 재시작합니다.
    - 설치 전 확인할 사항과 안전 원칙은 [설치 가이드의 커스텀 노드 관리자](../../00-getting-started/installation.md#커스텀-노드-관리자와-안전한-확장-설치)를 따르세요.
    - 전처리기를 설치하지 않아도, 이미 만들어 둔 윤곽선·깊이 이미지를 `Load Image`로 불러와 `Apply ControlNet`의 `image`에 바로 연결할 수 있습니다.
    - **예외:** Canny는 코어에 포함되어 있습니다. 노드 검색에서 `Detect Edges (Canny)`로 찾을 수 있고 `low_threshold`·`high_threshold` 두 값을 조절합니다. 설치 없이 시작하려면 Canny부터 사용해 보세요.

| 전처리기 | 입력 | 출력 | 용도 |
|:---------|:-----|:-----|:-----|
| **Canny** | 일반 이미지 | Edge map | 윤곽선 제어 |
| **Depth (Midas)** | 일반 이미지 | Depth map | 깊이/원근 제어 |
| **OpenPose** | 인물 사진 | Skeleton | 포즈 제어 |
| **Scribble** | 낙서 | Line art | 간단 스케치 |
| **LineArt** | 일반 이미지 | Line art | 정밀 선화 |

#### Canny, Depth, Pose 상세 비교

| 구분 | Canny | Depth | Pose |
|:-----|:------|:------|:-----|
| **용도** | 이미지의 외곽선(에지) 추출 후 구조 유지 | 이미지의 깊이(거리) 정보 활용 | 인체의 포즈(뼈대 구조) 추적 |
| **활용 사례** | 선화, 스케치 복원 | 3D 같은 입체감/레이어링 생성 | 캐릭터/인물의 동작 일관성 유지 |
| **유지되는 것** | 원본의 윤곽선 위치 | 앞뒤 거리 관계 | 관절 위치로 표현한 자세 |
| **전처리기** | Canny Edge Detector | MiDaS Depth Estimator | OpenPose Detector |
| **자주 보이는 시작 범위** | 0.3~0.6 (낮게 시작) | 0.5~0.8 | 0.6~0.9 |
| **주의사항** | strength를 올리면 구도가 원본에 묶임 | 평면적인 이미지에서는 깊이 차이가 거의 안 잡힘 | 인물이 없는 이미지에서는 뼈대가 검출되지 않음 |

**용도별 선택:**

```
Canny:  강한 선이 필요한 작업 (만화 스타일, 건축 도면)
Depth:  배경과 오브젝트의 층위를 조절
Pose:   원본 인물의 자세를 그대로 두고 나머지를 바꿀 때
```

위 범위는 시작점을 잡기 위한 경향값입니다. ControlNet 모델마다 학습 방식이 달라 모든 모델에 통하는 표준 strength는 없습니다. 제공자가 권장값을 제시했다면 그 값이 우선입니다([ControlNet 연결과 조절](controlnet-pipeline.md#텍스트와-구조-균형-조절)).

---

## 완료 기준

세 가지를 모두 만족했다면 이 장을 끝냈습니다.

- ControlNet이 CONDITIONING 라인을 수정한다는 점을 설명할 수 있다.
- 목적에 맞는 전처리기(Canny·Depth·Pose)를 고를 수 있다.
- `strength`와 적용 구간이 각각 무엇을 바꾸는지 구분할 수 있다.

## 다음 단계

제어 기법 시리즈의 첫 문서입니다. 아래 순서로 이어집니다.

- [ControlNet 연결과 조절](controlnet-pipeline.md) — 실제 워크플로우에 연결하기
- [IPAdapter](ipadapter.md) — 참조 이미지로 스타일 옮기기
- [Flux Redux](flux-redux.md) — 참조 기반 변형
- [Differential Diffusion](differential-diffusion.md) — 경계가 부드러운 Inpainting
- [Flux 모델 변형 비교](flux-model-variants.md) — Dev/Fill, 정밀도, 양자화 선택
- [제어 기법 실전 워크플로우](example-workflows.md) — 앞의 기법들을 조합한 예시

---

[문서 지도](../../README.md)
