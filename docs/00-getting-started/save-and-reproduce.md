[홈](../README.md) · [시작하기](README.md) · [이전: 첫 워크플로우 만들기](first-workflow.md)

---

# 워크플로우 저장과 재현

> 만든 워크플로우를 저장하고, 같은 결과를 언제든 다시 만들 수 있는 상태로 남깁니다.

## 이 장에서 배우는 것

- `Save`와 `Save (API Format)`의 차이와 각각의 용도
- PNG 메타데이터로 워크플로우를 복원하는 방법과 그 한계
- 저장한 파일이 실제로 재현되는지 확인하는 절차
- `.json`만으로 부족한 정보를 따로 기록하는 법

<div class="guide-meta" markdown>
**대상** 워크플로우를 완성했고 다시 쓸 수 있게 남기려는 사용자 · **사전 이해** [첫 워크플로우 직접 만들기](first-workflow.md) · **시간** 20분

**이럴 때 읽으세요** 어제 만든 워크플로우를 다시 못 만들거나, 같은 설정인데 결과가 달라질 때.
</div>

## 워크플로우 저장과 재현

이미지 한 장을 만드는 것과, 그 이미지를 다시 만들 수 있는 것은 다릅니다. 여기서 재현 가능한 상태로 남기는 방법을 정리합니다.

### 저장하고 다시 열기

- **저장:** 메뉴의 `Workflows → Save` (또는 `Ctrl+S`). 이름을 지정하면 `.json`으로 저장됩니다.
- **다시 열기:** `Workflows → Open`, 또는 `.json` 파일을 캔버스에 끌어다 놓습니다.

최신 ComfyUI는 저장한 워크플로우를 `ComfyUI/user/default/workflows/` 아래에 보관하고 Workflows 메뉴에서 바로 열 수 있게 합니다. ComfyUI는 자주 업데이트되므로, 메뉴 이름이 다르면 [공식 문서](https://docs.comfy.org)를 확인하세요.

### Save와 Save (API Format)은 다릅니다

|  | `Workflows → Save` | `Workflows → Save (API Format)` |
|---|---|---|
| 담기는 것 | 노드 위치·연결·설정값 | 실행에 필요한 노드 정의와 값 |
| 다시 열기 | 캔버스에 그대로 복원됩니다 | 캔버스로 복원되지 않습니다 |
| 용도 | 작업 저장과 공유 | 서버 API 호출, 자동화 |

!!! warning "Save (API Format) 파일은 작업 백업이 아닙니다"
    노드 배치 정보가 없어 캔버스로 되돌릴 수 없습니다. 작업을 남길 목적이라면 반드시 일반 `Save`를 씁니다.

### 이미지에서 워크플로우 복원하기

**Save Image**로 저장한 PNG에는 워크플로우 정보가 메타데이터로 함께 기록됩니다. 그 PNG를 ComfyUI 캔버스에 끌어다 놓으면 노드 구성이 그대로 복원됩니다.

다만 이 방법은 보조 수단입니다.

- **Preview Image**의 결과는 임시 파일로만 남아 보관용이 아닙니다. 나중에 복원할 결과는 **Save Image**로 저장합니다.
- 이미지를 다른 편집 프로그램에서 다시 저장하거나 메타데이터를 제거하는 서비스에 올리면 정보가 사라집니다.
- 따라서 원본 보관 기준은 `.json` 저장이고, PNG 복원은 편의 기능으로 씁니다.

!!! warning "PNG를 공개하기 전에 메타데이터를 확인하세요"
    Save Image PNG에는 프롬프트, 모델 파일명, 노드 구성과 설정값이 포함될 수 있습니다. 공개용 이미지에 작업 정보가 따라가면 안 되는 경우에는 워크플로우 원본과 `.json`을 비공개로 보관하고, 메타데이터를 제거한 별도 사본을 공유하세요. 제거한 사본은 ComfyUI로 복원할 수 없으므로 원본을 덮어쓰지 않습니다.

### 재현되는지 실제로 확인하기

저장했다는 사실만으로는 재현을 보장하지 못합니다. 다음 순서로 직접 확인합니다.

1. `control_after_generate`를 `fixed`로 두고 한 장 생성합니다.
2. 워크플로우를 저장합니다.
3. 캔버스를 비우거나 브라우저를 새로 고친 뒤, 저장한 파일을 다시 엽니다.
4. 같은 seed로 다시 생성해 1번의 결과와 비교합니다.

결과가 다르면 먼저 모델·VAE·LoRA·Seed·노드 설정이 같은지 확인합니다. 동일 환경에서는 같은 결과가 재현되는 것이 일반적이지만, GPU·정밀도·ComfyUI/PyTorch 버전과 일부 비결정적 연산이 다르면 차이가 생길 수 있습니다.

## 재현 기록 남기기

`.json` 파일만으로 부족한 경우가 있습니다. 모델 파일 이름이 같아도 내용이 다른 버전이 유통되고, 시간이 지나면 어떤 파일을 썼는지 기억나지 않습니다.

| 기록 항목 | 왜 필요한가 |
|---|---|
| 체크포인트 파일명 | 같은 이름의 다른 버전이 존재합니다 |
| 해상도 (width × height) | 모델 기본 해상도와의 차이가 결과를 크게 바꿉니다 |
| `seed`와 `control_after_generate` | 재현의 시작점입니다 |
| `steps`, `cfg`, `sampler_name`, `scheduler`, `denoise` | 샘플링 결과를 결정합니다 |
| LoRA 파일명과 `strength` | 값이 조금 달라도 화풍이 바뀝니다 |
| ComfyUI 버전 | 노드 동작이 버전에 따라 달라질 수 있습니다 |

아래 형식을 복사해 워크플로우 파일과 같은 폴더에 남겨 두면 나중에 확인이 쉽습니다.

```text
목표:
체크포인트:
해상도:
seed / control_after_generate:
steps / cfg:
sampler_name / scheduler / denoise:
LoRA (있으면) 이름 / strength:
ComfyUI 버전:
이 설정을 고른 이유:
다음에 바꿔 볼 값:
```

## 완료 기준

네 가지를 모두 만족했다면 이 장을 끝냈습니다.

- 워크플로우를 `.json`으로 저장했다.
- 저장한 파일을 다시 열어 같은 결과를 재현했다.
- `Save`와 `Save (API Format)`의 차이를 설명할 수 있다.
- 재현 기록을 남겼다.

## 다음 단계

- [핵심 개념](../01-core-concepts/README.md) — Latent·VAE와 디노이징 원리
- [Flux 가이드](../02-models/flux/README.md) · [SD/SDXL 가이드](../02-models/sd-sdxl/README.md) — 모델별 사용법
- [LoRA](../03-advanced-techniques/lora/README.md) · [ControlNet](../03-advanced-techniques/controlnet/controlnet-architecture.md) — 스타일·구도 제어

---

[홈](../README.md) · [시작하기](README.md) · [이전: 첫 워크플로우 만들기](first-workflow.md)
