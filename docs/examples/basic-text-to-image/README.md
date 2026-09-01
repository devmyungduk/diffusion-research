[홈](../../README.md) · [빠른 시작](../../00-getting-started/quick-start.md) · [다음: 워크플로우 이해](../../00-getting-started/workflow-basics.md)

# 기본 Text-to-Image 시작 템플릿

> 빠른 시작의 7노드 구성을 직접 불러오고, 설치된 체크포인트를 골라 첫 결과를 만듭니다.

## 워크플로우 가져오기

복사해서 붙여넣거나, 파일로 받아 캔버스에 끌어다 놓습니다.

**① 복사해서 붙여넣기**

??? note "JSON 펼치기"

    코드 블록 오른쪽 위 복사 버튼을 누른 다음, ComfyUI 캔버스를 클릭하고 `Ctrl + V`로 붙여넣습니다. 파일을 받지 않아도 같은 워크플로우가 만들어집니다.

    ```json
    --8<-- "docs/examples/basic-text-to-image/workflow.json"
    ```

**② 파일로 받기**

[workflow.json](workflow.json)을 우클릭해 `다른 이름으로 저장`을 고른 뒤 캔버스에 끌어다 놓습니다. 링크를 그냥 누르면 브라우저에 글자만 표시됩니다.

## 함께 있는 파일

- [params.yml](params.yml) — `workflow.json`에 담기지 않는 체크포인트 파일명, ComfyUI 버전, 결과 관찰을 적는 빈 서식입니다. 복사해서 채웁니다
- [기본 연결도](../../assets/images/basic-workflow.svg) — 노드 7개가 어떤 포트로 이어지는지 그린 도식입니다

## 실행 순서

1. 위 두 방법 중 하나로 워크플로우를 캔버스에 올립니다. 받은 파일은 `Workflows → Open`으로 열어도 됩니다.
2. `Load Checkpoint`의 `ckpt_name`에서 설치한 SDXL 체크포인트를 선택합니다.
3. 모델이 SD 1.5라면 `Empty Latent Image`를 512×512로 바꾸고, SDXL이면 1024×1024로 둡니다.
4. Positive·Negative 프롬프트를 확인합니다.
5. KSampler의 `control_after_generate`가 `fixed`인지 확인한 뒤 `Run` 버튼을 누릅니다.
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
| seed | 123456 |
| control_after_generate | fixed |

모델 제작자가 권장값을 제공했다면 그 값을 우선합니다. 이 파일은 모델 가중치를 포함하지 않으며, `Load Checkpoint`에서 사용자가 설치한 모델을 직접 선택해야 합니다.

## 완료 기준

네 가지를 모두 만족했다면 이 장을 끝냈습니다.

- JSON을 열었을 때 7개 노드와 연결이 복원된다.
- 체크포인트를 선택하고 이미지 한 장을 생성했다.
- Seed를 고정한 상태에서 프롬프트 또는 CFG 하나만 바꿔 비교했다.
- 실제 사용한 모델과 설정을 params 파일에 기록했다.

## 다음 단계

- [5분 빠른 시작](../../00-getting-started/quick-start.md) — 연결과 첫 비교 실험
- [워크플로우 이해하기](../../00-getting-started/workflow-basics.md) — 각 노드와 설정값의 의미

---

[홈](../../README.md) · [빠른 시작](../../00-getting-started/quick-start.md) · [다음: 워크플로우 이해](../../00-getting-started/workflow-basics.md)
