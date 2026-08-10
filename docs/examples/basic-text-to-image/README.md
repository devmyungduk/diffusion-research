[홈](../../README.md) · [빠른 시작](../../00-getting-started/quick-start.md) · [다음: 워크플로우 이해](../../00-getting-started/workflow-basics.md)

# 기본 Text-to-Image 시작 템플릿

> 빠른 시작의 7노드 구성을 직접 불러오고, 설치된 체크포인트를 선택해 첫 결과를 생성합니다.

## 파일

- [workflow.json](workflow.json) — ComfyUI에서 여는 기본 워크플로우
- [params.yml](params.yml) — 모델과 실행 결과를 기록하는 설정표
- [기본 연결도](../../assets/images/basic-workflow.svg) — 포트와 데이터 타입을 확인하는 구조도

연결도는 실제 생성 결과 이미지가 아니라 노드 구조 설명용입니다.

## 실행 순서

1. `workflow.json`을 내려받아 ComfyUI 캔버스에 끌어다 놓거나 `Workflows → Open`으로 엽니다.
2. `Load Checkpoint`의 `ckpt_name`에서 설치한 SDXL 체크포인트를 선택합니다.
3. 모델이 SD 1.5라면 `Empty Latent Image`를 512×512로 바꾸고, SDXL이면 1024×1024로 둡니다.
4. Positive·Negative 프롬프트를 확인합니다.
5. KSampler의 Seed가 `fixed`인지 확인한 뒤 Queue를 실행합니다.
6. 사용한 모델 파일명과 결과 관찰을 `params.yml` 사본에 기록합니다.

## 템플릿 시작값

| 항목 | 값 |
|---|---|
| 해상도 | 1024×1024(SDXL 기준) |
| steps | 25 |
| cfg | 6.0 |
| sampler_name | euler |
| scheduler | normal |
| denoise | 1.0 |
| seed | 123456, fixed |

모델 제작자가 권장값을 제공했다면 그 값을 우선합니다. 이 파일은 모델 가중치를 포함하지 않으며, `Load Checkpoint`에서 사용자가 설치한 모델을 직접 선택해야 합니다.

## 완료 기준

- JSON을 열었을 때 7개 노드와 연결이 복원된다.
- 체크포인트를 선택하고 이미지 한 장을 생성했다.
- Seed를 고정한 상태에서 프롬프트 또는 CFG 하나만 바꿔 비교했다.
- 실제 사용한 모델과 설정을 params 파일에 기록했다.

## 다음 단계

- [5분 빠른 시작](../../00-getting-started/quick-start.md) — 연결과 첫 비교 실험
- [워크플로우 이해하기](../../00-getting-started/workflow-basics.md) — 각 노드와 설정값의 의미

