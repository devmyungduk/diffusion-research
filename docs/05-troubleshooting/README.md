[홈](../README.md) · [문서 지도](../README.md)

# 문제 해결 가이드

> ComfyUI를 쓰다 만나는 대표적인 문제와 해결 방법을 모았습니다. 증상으로 목차를 찾아 해당 항목만 보세요.

## 이 장에서 배우는 것

- 증상에서 출발합니다. 목차에서 지금 겪는 증상을 찾아 해당 항목만 보세요.
- 원인을 좁히는 순서가 정해져 있습니다. 값을 바로 바꾸기 전에 [디버깅 순서](#6-디버깅-순서)를 먼저 보면 헛수고를 줄입니다.

<div class="guide-meta" markdown>
**대상** 오류·비정상 결과를 만난 모든 사용자 · **사전 이해** 필요 없음 · **시간** 필요한 항목만 5분

**이럴 때 읽으세요** 오류가 났거나, 실행은 되는데 결과가 이상할 때.
</div>

## 목차

1. [이미지 생성 문제](#1-이미지-생성-문제)
2. [메모리 관련 문제](#2-메모리-관련-문제)
3. [속도 최적화](#3-속도-최적화)
4. [품질 문제](#4-품질-문제)
6. [디버깅 순서](#6-디버깅-순서)

## 1. 이미지 생성 문제

### 이미지가 아예 안 나온다

대부분 VAE Decode 누락이나 연결 오류입니다. 아래를 순서대로 확인하세요.

```
□ VAE Decode 노드가 있는가
□ KSampler → VAE Decode → Save Image 순서인가
□ 모든 선이 연결되었는가
□ Queue Prompt 버튼을 눌렀는가
□ 콘솔에 에러 메시지가 있는가
```

해결 절차:

1. **연결 확인** — `KSampler [LATENT]` → `VAE Decode [samples]`, `Load Checkpoint [VAE]` → `VAE Decode [vae]`
2. **순서 점검** — 모든 노드가 올바른 순서로 이어졌는지 확인
3. **단순화 테스트** — 기본 워크플로우만 남기고 재실행

### KSampler를 Save Image에 바로 연결하려는데 선이 붙지 않는다

정상입니다. KSampler의 출력은 `LATENT`, Save Image의 입력은 `IMAGE`라 타입이 달라 애초에 연결되지 않습니다.

```
연결 불가: KSampler → Preview/Save Image
올바름:    KSampler → VAE Decode → Preview/Save Image
```

`VAE Decode`를 사이에 넣고, 그 `vae` 입력에는 Load Checkpoint의 VAE를 연결합니다.

!!! warning "선은 붙는데 단색 화면만 나오는 경우"
    `Empty Latent Image`를 KSampler를 건너뛰고 `VAE Decode`에 바로 연결하면 **둘 다 `LATENT` 타입이라 선이 붙습니다.** 이때 KSampler는 출력이 어디에도 쓰이지 않아 실행 자체를 건너뛰고, 0으로 채워진 빈 Latent가 그대로 디코딩되어 **아무 형태도 없는 단색 화면**이 나옵니다. `VAE Decode`의 `samples`가 **KSampler의 출력에서 오는지** 확인하세요.

??? note "이미지가 흐릿할 때 — 원인별 조치"
    | 원인 | 해결 |
    |------|------|
    | Steps 부족 | Steps를 30~40으로 증가 |
    | Denoise 낮음 | Denoise를 1.0으로 설정 |
    | 잘못된 해상도 | 모델 권장 해상도 사용 |
    | VAE 문제 | 다른 VAE로 교체 |

    권장 설정:

    ```
    SD 1.5:
    - 해상도: 512×512
    - Steps: 25~30
    - Sampler: euler, dpmpp_2m

    SDXL:
    - 해상도: 1024×1024
    - Steps: 30~40
    - Sampler: dpmpp_2m
    - Scheduler: karras
    ```

## 2. 메모리 관련 문제

### Out of Memory (OOM)

콘솔에 다음과 같은 메시지가 나타납니다.

```
RuntimeError: CUDA out of memory
```

다음 순서로 조치합니다.

1. **이미지 크기 줄이기** — 1024×1024 또는 768×768 → 512×512
2. **Batch 크기 줄이기** — `batch_size` 4 → 1
3. **그 밖에** — LoRA 제거 또는 개수 축소, ControlNet 비활성화, ComfyUI 재시작

??? note "VRAM 용량별 권장 설정 펼치기"
    ```
    4GB (최소)
       모델: SD 1.5만
       크기: 512×512
       Batch: 1

    6GB
       모델: SD 1.5, SDXL(제한적)
       크기: 512×512(SD 1.5), 768×768(SDXL, 주의)
       Batch: 1~2

    8GB
       모델: SD 1.5, SDXL
       크기: 1024×1024(SDXL)
       Batch: 1~2, LoRA 2~3개

    12GB 이상
       모델: 전체(Flux 포함)
       크기: 제한 없음
       Batch: 4~8, LoRA/ControlNet 자유
    ```

### 메모리 최적화

VAE Tiling은 VRAM 사용량을 크게 줄이는 대신 약간 느려집니다. `VAE Encode (Tiled)` / `VAE Decode (Tiled)` 노드를 사용합니다.

실행 플래그:

```
(플래그 없음)  기본값. ComfyUI가 VRAM에 맞춰 자동으로 조절합니다
--lowvram     텍스트 인코더를 CPU로 내림
--novram      --lowvram으로도 부족할 때
--highvram    모델을 GPU 메모리에 유지(메모리 여유가 클 때)
--gpu-only    텍스트 인코더까지 전부 GPU에 올림
--cpu         GPU를 쓰지 않음(매우 느림)
```

!!! note "먼저 해상도와 batch부터"
    최근 ComfyUI는 VRAM을 동적으로 관리하므로 플래그 없이 실행하는 것이 기본이고, 이 상태에서 `--lowvram`은 아무 동작도 하지 않을 수 있습니다. 위 1~3단계 조치를 먼저 하고, 플래그는 그다음에 시도하세요. (예전 안내에 나오는 `--normalvram`은 현재 존재하지 않는 플래그입니다.)

## 3. 속도 최적화

생성이 느릴 때는 영향이 큰 요인부터 조정합니다.

| 원인 | 영향 | 해결 |
|------|------|------|
| 높은 해상도 | 큼 | 512×512로 시작 |
| 많은 Steps | 중간 | 20~30으로 축소 |
| 느린 Sampler | 중간 | euler로 변경 |
| 여러 LoRA | 작음 | 2~3개로 제한 |
| ControlNet | 큼 | 필요할 때만 사용 |

작업 단계별 권장값:

```
테스트(빠른 반복): 512×512  / Steps 15~20 / euler
개선:              768×768  / Steps 30    / 세밀 조정
최종:              1024×1024 / Steps 40    / sampler dpmpp_2m + scheduler karras
```

## 4. 품질 문제

### 프롬프트를 반영하지 않는다

CFG가 낮거나 프롬프트가 모호한 경우가 많습니다. CFG가 5 미만이면 7~10으로 올리고, 프롬프트를 구체적으로 씁니다.

```
모호함: "cat"
구체적: "a cute orange tabby cat sitting on a windowsill,
         blue sky background, natural lighting,
         high quality, detailed, photorealistic"
```

특정 요소를 강조하려면 가중치 문법을 씁니다.

```
(keyword:1.2)  약하게 강조
(keyword:1.5)  뚜렷하게 강조
(keyword:0.8)  약화
```

값과 반영 강도는 비례하지 않습니다. 값의 의미와 실용 상한은 [프롬프트 가중치](../03-advanced-techniques/prompt-weighting.md)에서 다룹니다.

### 결과가 과장된다

CFG가 너무 높을 때 나타납니다. 10 이상이면 낮춥니다.

```
KSampler cfg 적정 범위
- SD 1.5: 7~8
- SDXL:   7~9
```

!!! warning "FLUX.1 dev는 cfg를 올리지 않습니다"
    Flux에서 프롬프트 반영을 조절하는 값은 KSampler의 `cfg`가 아니라 **`FluxGuidance`의 guidance**입니다.

    | 항목 | FLUX.1 dev 값 |
    |---|---|
    | KSampler `cfg` | **1.0** (공식 기본 구성. 올리지 않습니다) |
    | FluxGuidance `guidance` | **3.5**에서 시작해 비교 |

    KSampler `cfg`에 3.5를 넣는 것은 잘못된 설정입니다. 자세한 내용은 [FluxGuidance 이해와 사용](../02-models/flux/fluxguidance-pipeline.md)을 참고하세요.

??? note "색감이 이상할 때 — 원인별 조치"
    | 원인 | 해결 |
    |------|------|
    | 잘못된 VAE | 다른 VAE로 교체 |
    | 과도한 LoRA | Strength 낮추기 |
    | 프롬프트 충돌 | 표현을 명확히 정리 |

    모델별 권장 VAE:

    ```
    SD 1.5: vae-ft-mse-840000-ema-pruned
    SDXL:   sdxl_vae
    Flux:   ae.safetensors
    ```

??? warning "5. 자주 나오는 오류 메시지 세 가지"
    ### Model file not found

    파일이 올바른 위치에 없을 때 발생합니다.

    ```
    Checkpoint: ComfyUI/models/checkpoints/
    LoRA:       ComfyUI/models/loras/
    VAE:        ComfyUI/models/vae/
    ControlNet: ComfyUI/models/controlnet/

    Flux 전용
    Diffusion:  ComfyUI/models/diffusion_models/
    CLIP:       ComfyUI/models/text_encoders/
    ```

    ### Invalid node type

    커스텀 노드가 없거나 업데이트가 필요할 때 발생합니다. ComfyUI Manager에서 누락된 노드를 설치하고 재시작합니다.

    ### Connection failed

    노드 타입이 맞지 않을 때 발생합니다. 같은 타입끼리만 연결됩니다.

    ```
    올바름: MODEL→MODEL, CLIP→CLIP, LATENT→LATENT, IMAGE→IMAGE, VAE→VAE
    잘못됨: IMAGE→LATENT, MODEL→CLIP
    ```

## 6. 디버깅 순서

문제가 생기면 아래 순서로 원인을 좁힙니다.

1. 콘솔 에러 메시지를 확인합니다.
2. 모든 노드 연결을 검토합니다.
3. 기본 워크플로우만 남기고 테스트합니다.
4. 뺐던 노드를 한 번에 하나씩 다시 추가합니다.
5. 문제를 일으키는 노드나 설정을 특정합니다.
6. 해결하거나 대안을 적용합니다.

문제를 줄이는 습관도 도움이 됩니다. 작동하는 워크플로우는 자주 저장하고 버전별로 파일명을 구분하며, 변경은 한 번에 하나씩만 적용합니다.

## 도움받을 곳

- [ComfyUI GitHub Issues](https://github.com/comfyanonymous/ComfyUI/issues)
- [ComfyUI 공식 문서](https://docs.comfy.org)
- Reddit r/StableDiffusion

## 다음 단계

- [워크플로우 이해하기](../00-getting-started/workflow-basics.md) — 설정값의 의미
- [핵심 개념](../01-core-concepts/README.md) — 오류의 근본 원인
- [첫 워크플로우 직접 만들기](../00-getting-started/first-workflow.md) — 재현 가능한 형태로 저장

---

[홈](../README.md) · [문서 지도](../README.md)
