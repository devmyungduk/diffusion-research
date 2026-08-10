[홈](../README.md) · [문서 지도](../README.md) · [시작하기](README.md)

# 5분 빠른 시작

> 목표: 노드 7개를 연결해 첫 이미지를 만들고, Seed를 고정한 첫 비교 실험까지 끝냅니다.

## 이 장에서 배우는 것

- 기본 Text-to-Image 워크플로우의 입력과 출력 방향을 읽는 법
- 프롬프트와 해상도를 바꿔 다시 생성하는 법
- 결과가 달라진 이유를 확인하기 위해 Seed를 고정하는 법

<div class="guide-meta" markdown>
**대상** ComfyUI를 설치했고 첫 이미지를 만들려는 사용자 · **사전 이해** 필요 없음. 체크포인트 모델 1개만 있으면 됩니다 · **시간** 5분 + 비교 실험 3분
</div>

## 0. 준비 확인

- ComfyUI가 실행되고 브라우저에 캔버스가 보입니다.
- SD 1.5 또는 SDXL 체크포인트 1개가 `ComfyUI/models/checkpoints/`에 있습니다.
- 모델을 아직 설치하지 않았다면 [설치 가이드](installation.md)를 먼저 진행하세요.

!!! tip "더 빠른 시작"
    최근 ComfyUI에서는 **Workflows → Browse Workflow Templates**에서 기본 이미지 생성 템플릿을 열 수 있습니다. 이 장은 노드 흐름을 익히기 위해 빈 캔버스에서 직접 연결합니다.

직접 연결하기 전에 [기본 7노드 예제 설명](../examples/basic-text-to-image/README.md)과 [workflow.json](../examples/basic-text-to-image/workflow.json)을 열어 구조를 확인할 수 있습니다. 템플릿에는 모델 파일이 포함되지 않으므로 `Load Checkpoint`에서 설치한 모델을 선택해야 합니다.

## 1. 완성 모습을 먼저 보기

<div class="workflow-figure" markdown>

[![ComfyUI 기본 Text-to-Image 워크플로우. 체크포인트, 두 개의 프롬프트, 빈 Latent가 KSampler와 VAE Decode를 거쳐 이미지가 됩니다.](../assets/images/basic-workflow.svg)](../assets/images/basic-workflow.svg)

<p class="workflow-figure__caption">이미지를 선택하면 원본 크기로 볼 수 있습니다. 작은 화면에서는 좌우로 이동해 연결을 확인하세요.</p>

</div>

포트 위치와 이름을 함께 읽으세요. ComfyUI 기본 화면은 연결선에 화살표를 표시하지 않습니다. 선은 **노드 오른쪽 출력 포트에서 시작**해 **다음 노드의 왼쪽 입력 포트에 도착**하며, 같은 데이터 타입의 선과 포트는 같은 색을 사용합니다.

- `CLIP` 선이 중간 점에서 두 갈래로 나뉘어 Positive와 Negative의 `clip` 입력으로 들어갑니다.
- `CONDITIONING` 두 선은 KSampler의 `positive`와 `negative` 입력에 각각 대응합니다.
- 주황색 `VAE` 선은 아래쪽으로 우회하지만, 출발점과 도착점은 모두 `VAE` 타입입니다.

1. **Load Checkpoint**가 MODEL·CLIP·VAE를 꺼냅니다.
2. **CLIP Text Encode** 두 개가 원하는 것과 피할 것을 조건으로 바꿉니다.
3. **Empty Latent Image**가 이미지의 작업 공간과 크기를 만듭니다.
4. **KSampler**가 노이즈를 조건에 맞춰 정리합니다.
5. **VAE Decode**가 Latent를 눈에 보이는 이미지로 바꿉니다.
6. **Save Image**가 결과를 미리 보고 파일로 저장합니다.

## 2. 노드 7개 배치하기

빈 캔버스에서 우클릭한 뒤 아래 이름을 검색해 추가합니다.

1. `Load Checkpoint`
2. `CLIP Text Encode` × 2
3. `Empty Latent Image`
4. `KSampler`
5. `VAE Decode`
6. `Save Image`

두 `CLIP Text Encode` 중 하나는 제목을 `Positive`, 다른 하나는 `Negative`로 바꾸면 읽기 쉽습니다.

## 3. 왼쪽 입력과 오른쪽 출력 연결하기

| 출발 노드·출력 | 도착 노드·입력 | 타입 | 전달하는 것 |
|---|---|---|---|
| Load Checkpoint · `MODEL` | KSampler · `model` | `MODEL` | 이미지 생성 모델 |
| Load Checkpoint · `CLIP` | Positive/Negative · `clip` | `CLIP` | 텍스트 인코더 |
| Positive · `CONDITIONING` | KSampler · `positive` | `CONDITIONING` | 원하는 특징 |
| Negative · `CONDITIONING` | KSampler · `negative` | `CONDITIONING` | 피할 특징 |
| Empty Latent Image · `LATENT` | KSampler · `latent_image` | `LATENT` | 시작 Latent와 크기 |
| KSampler · `LATENT` | VAE Decode · `samples` | `LATENT` | 디노이징된 Latent |
| Load Checkpoint · `VAE` | VAE Decode · `vae` | `VAE` | 이미지 디코더 |
| VAE Decode · `IMAGE` | Save Image · `images` | `IMAGE` | 완성 이미지 |

소켓이 연결되지 않으면 대부분 데이터 타입이 다른 것입니다. 출발점과 도착점의 색을 다시 확인하세요.

## 4. 첫 실행값 넣기

### 프롬프트

Positive:

```text
a small red cabin beside a calm lake, pine forest, soft morning light,
cinematic composition, detailed digital illustration
```

Negative:

```text
blurry, low quality, distorted, text, watermark
```

### 모델별 안전한 시작값

| 설정 | SD 1.5 | SDXL Base | 의미 |
|---|---:|---:|---|
| width × height | 512 × 512 | 1024 × 1024 | 모델이 익숙한 기본 해상도 |
| steps | 20 | 25 | 디노이징 반복 횟수 |
| cfg | 7.0 | 6.0 | 프롬프트를 따르는 강도 |
| sampler | euler | euler | 한 단계씩 이동하는 방법 |
| scheduler | normal | normal | 노이즈를 줄이는 시간표 |
| denoise | 1.0 | 1.0 | 새 이미지를 완전히 생성 |
| seed | 123456 | 123456 | 비교를 위한 고정 시작점 |

모델 제작자가 권장값을 제공했다면 그 값을 우선하세요. Flux는 로더와 Guidance 구성이 다르므로 첫 실습을 마친 뒤 [Flux 가이드](../02-models/flux/README.md)로 이동하는 편이 안전합니다.

`Queue Prompt`를 누릅니다. 첫 실행은 모델 로딩 때문에 다음 실행보다 오래 걸릴 수 있습니다.

## 5. 3분 비교 실험: CFG 하나만 바꾸기

같은 프롬프트와 Seed를 유지하고 `cfg`만 바꿔 세 번 생성합니다.

| 실행 | cfg | 기록할 관찰 |
|---|---:|---|
| A | 4.0 | 프롬프트 특징이 얼마나 보이는가? |
| B | 7.0 | 구도와 색이 자연스러운가? |
| C | 11.0 | 대비·채도가 과해지거나 형태가 깨지는가? |

!!! question "관찰 질문"
    세 결과 중 “프롬프트를 가장 강하게 따른 결과”와 “가장 보기 좋은 결과”가 같은가요? 다르다면 CFG는 품질 점수가 아니라 **조건을 밀어붙이는 강도**입니다.

### 실험 기록 템플릿

```text
모델:
프롬프트:
Seed: 123456
변경한 변수: CFG 4 / 7 / 11
가장 안정적인 값:
달라진 점:
다음에 확인할 변수:
```

이 형식을 복사해 GitHub Issue나 개인 노트에 남기면 나중에 워크플로우를 재현하기 쉽습니다.

## 결과가 이상할 때

| 증상 | 가장 먼저 확인 | 다음 행동 |
|---|---|---|
| Queue가 실행되지 않음 | 빨간 테두리 노드·빈 입력 | 해당 입력을 연결하거나 값을 선택 |
| 이미지 대신 노이즈 | VAE 지정 | 체크포인트가 내보낸 VAE를 쓰는지 확인. 별도 VAE라면 모델과 같은 계열인지 확인 |
| 검은 이미지 | VAE 또는 모델 파일 | 체크포인트 기본 VAE로 다시 실행. 그래도 검으면 다른 체크포인트로 교차 확인 |
| 너무 느리거나 OOM | 해상도·batch size | batch 1, 해상도를 한 단계 낮춤 |
| 비교할 때 매번 전부 바뀜 | Seed의 control_after_generate | `fixed`로 변경 |

더 자세한 진단은 [문제 해결 가이드](../05-troubleshooting/README.md)를 참고하세요.

## 완료 기준

다섯 가지를 모두 만족했다면 이 장을 끝낸 것입니다.

- 7개 노드를 직접 배치했다.
- 각 연결이 무엇을 전달하는지 한 문장으로 설명할 수 있다.
- 한 장을 생성했다.
- Seed를 고정하고 CFG만 바꿔 비교했다.
- 관찰 결과를 한 줄 이상 기록했다.

## 다음 단계

- [워크플로우 이해하기](workflow-basics.md) — 각 노드와 설정값의 의미
- [첫 워크플로우 직접 만들기](first-workflow.md) — 참고 없이 구성하고 저장해 재현하기
- [핵심 개념](../01-core-concepts/README.md) — Latent·VAE와 디노이징 원리
