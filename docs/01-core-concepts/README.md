[문서 지도](../README.md)

# 핵심 개념 이해하기

> AI 이미지 생성의 기초 원리를 정리합니다. 용어는 처음 접하는 분도 이해할 수 있도록 풀어 서술하되, 설명은 정확성을 우선합니다.

## 이 장에서 배우는 것

- Latent는 AI가 이미지를 다루기 쉽게 압축한 상태이고, VAE가 이미지와 Latent 사이를 오갑니다.
- SD 계열은 UNet, Flux는 Transformer 구조를 사용합니다. 포트 타입이 같아도 내부 구조는 다릅니다.

<div class="guide-meta" markdown>
**대상** AI 이미지 생성의 원리가 궁금한 입문자~중급자 · **사전 이해** 필요 없음 · **시간** 30분

**이럴 때 읽으세요** 노드를 연결할 줄은 알지만 왜 그렇게 연결하는지 궁금할 때.
</div>

## 1. Latent Image

Latent는 이미지를 압축한 상태입니다. 사람 눈에는 보이지 않습니다.

우리가 보는 1024×1024 이미지는 100만 개가 넘는 픽셀로 이루어집니다. AI가 이 픽셀을 직접 다루면 연산량이 지나치게 많습니다. 그래서 이미지를 작은 크기로 압축한 Latent 공간에서 작업한 뒤, 마지막에 다시 원본 크기로 복원합니다.

압축의 효과는 처리량에서 드러납니다.

| 비교 | 일반 이미지 (512×512) | Latent (64×64) |
|------|----------------------|----------------|
| 처리할 데이터 | 786,432개 (512×512×3) | 16,384개 (64×64×4) |
| 데이터 양 | 기준 | 약 1/48 |
| 화면 표시 | 가능 | 불가능(압축 상태) |

다루는 데이터가 약 48분의 1로 줄어듭니다. 실제 생성 속도가 그만큼 빨라지지는 않습니다. 픽셀을 직접 다루는 방식과 계산량의 자릿수가 다르다는 점만 확인하면 됩니다.

전체 생성 흐름에서 Latent의 위치는 다음과 같습니다.

1. **빈 Latent** — 0으로 채워진 빈 작업 공간. 아직 노이즈도 없습니다
2. **KSampler** — `seed`로 시작 노이즈를 만들어 넣고, 그 노이즈를 이미지로 바꾸는 과정
3. **완성된 Latent** — 아직 압축 상태라 보이지 않음
4. **VAE Decode** — 압축 해제
5. **일반 이미지** — 이제 볼 수 있음

정리하면, Latent는 보이지 않는 압축 공간이며 AI 연산에 최적화된 형태입니다. 결과를 보려면 반드시 VAE Decode로 압축을 풀어야 하고, Empty Latent는 아무것도 없는 시작점입니다.

## 2. VAE

VAE(Variational AutoEncoder)는 이미지와 Latent를 서로 변환하는 도구입니다.

| 역할 | 노드 | 입력 | 출력 | 사용 시점 |
|------|------|------|------|-----------|
| 압축 | VAE Encode | 일반 이미지 | Latent | 기존 이미지를 수정할 때 |
| 복원 | VAE Decode | Latent | 일반 이미지 | 결과를 확인할 때(필수) |

두 작업의 차이는 앞쪽에 VAE Encode가 붙느냐입니다.

```mermaid
%%{init: {"flowchart": {"curve": "linear", "nodeSpacing": 55, "rankSpacing": 70, "padding": 12}, "themeVariables": {"fontSize": "14px"}} }%%
graph LR
    A1["Empty Latent"] --> A2[KSampler] --> A3[VAE Decode] --> A4["Image<br/>신규 생성"]
    B1[Image] --> B2["VAE Encode"] --> B3[KSampler] --> B4[VAE Decode] --> B5["Image<br/>기존 이미지 수정"]
```

새 이미지를 만들 때는 빈 Latent에서 시작하므로 VAE Encode가 필요 없습니다. 기존 이미지를 고칠 때는 그 이미지를 먼저 Latent로 압축해야 KSampler가 다룰 수 있습니다.

KSampler는 Latent(압축 상태)를 출력하므로 반드시 VAE Decode를 거쳐야 합니다. Save Image는 `IMAGE`만 받기 때문에, 빠뜨리면 **선 자체가 연결되지 않습니다.**

- 연결 불가: KSampler → Save Image (타입이 다릅니다)
- 올바름: KSampler → VAE Decode → Save Image

## 3. 아키텍처 비교: UNet vs Transformer

AI 이미지 생성 모델의 근본 구조는 크게 두 가지입니다. UNet은 주변을 중심으로 처리하고, Transformer는 전체를 한 번에 참조합니다.

| 항목 | UNet (SD 1.5/SDXL) | Transformer (Flux) |
|------|--------------------|--------------------|
| 기반 | CNN | Self-Attention |
| 처리 방식 | 지역적(주변 위주) | 전역적(전체 동시 참조) |
| 위치 관계 표현 | 좌우·앞뒤를 혼동하는 경우가 있음 | 패치끼리 서로 참조해 상대적으로 잘 유지 |
| 파라미터 수 | 약 1B(SD 1.5) ~ 3.5B(SDXL) | 약 12B(FLUX.1) |
| 속도·메모리 | 파라미터가 적어 가벼움 | 파라미터가 많아 무거움 |

### UNet — 부분을 중심으로 처리

UNet은 이미지를 단계적으로 압축했다가 다시 복원하는 U자 형태의 구조입니다. 주변 픽셀을 중심으로 처리하므로 국소적인 디테일에 강한 대신, 전체 맥락 파악은 상대적으로 약합니다.

```mermaid
%%{init: {"flowchart": {"curve": "linear", "nodeSpacing": 55, "rankSpacing": 70, "padding": 12}, "themeVariables": {"fontSize": "14px"}} }%%
graph LR
    A[입력] --> B[압축] --> C[더 압축] --> D["최대 압축<br/>핵심 정보만"]
    D --> E[복원] --> F[더 복원] --> G[출력]
    B -. skip connection .-> F
    C -. skip connection .-> E
```

이름이 U자인 이유는 내려갔다가 다시 올라오는 모양 때문입니다. 점선은 **skip connection**으로, 압축하며 잃은 세부를 복원 단계에 다시 전달합니다.

예를 들어 "왼쪽에 빨간 사과, 오른쪽에 초록 사과" 같은 프롬프트에서 색과 대상은 잘 그리지만 좌우 위치를 혼동할 때가 있습니다.

### Transformer — 전체를 동시에 참조

Transformer는 이미지를 여러 패치로 나누고 모든 패치가 서로 정보를 교환합니다. 멀리 떨어진 두 패치도 한 단계 안에서 서로를 참조하므로, 좌우·앞뒤 같은 위치 관계가 계산에 함께 들어갑니다.

```
이미지를 패치로 분할한 뒤 모든 패치가 상호 참조

[패치1] ↔ [패치2] ↔ [패치3]
   ↕         ↕         ↕
[패치4] ↔ [패치5] ↔ [패치6]
```

같은 "왼쪽/오른쪽" 프롬프트에서 Transformer 기반 모델(Flux)은 좌우가 뒤바뀌는 빈도가 낮습니다.

## 4. 모델 구성 요소

ComfyUI에서 자주 혼동되는 세 개념입니다.

| 개념 | 무엇인가 | 화면에서 만나는 곳 |
|------|------|-----------|
| UNet/DiT | 노이즈를 예측해 제거하는 신경망 구조 | 파일이 아니라 모델 내부 구조 |
| Checkpoint | 학습이 끝난 모델 파일 | `models/checkpoints/`의 `.safetensors` |
| Load 노드 | 그 파일을 VRAM에 올리는 노드 | `Load Checkpoint` |

**UNet/DiT**는 노이즈를 예측해 제거하는 신경망 구조입니다. 파일 이름으로 고르는 대상이 아니라 체크포인트 안에 들어 있는 구조이며, 사용자가 직접 다루지 않습니다.

**Checkpoint**는 학습이 끝난 전체 모델 파일입니다. 내부에 UNet/DiT(엔진), VAE(압축 도구), Text Encoder(텍스트 이해)가 함께 들어 있습니다. 예: `realisticVision_v60.safetensors`.

**Load 노드**는 이 파일을 RAM/VRAM에 올려 워크플로우에서 사용할 수 있게 합니다.

SD 계열과 Flux는 이 구성 요소를 다루는 방식이 다릅니다.

| 구분 | SD 1.5/SDXL | Flux |
|------|-------------|------|
| 로드 노드 | Load Checkpoint | Load Diffusion Model |
| 폴더 | models/checkpoints/ | models/diffusion_models/ |
| 구조 | UNet | DiT (Transformer) |
| 파일 구성 | 통합(한 파일) | 분리(여러 파일) |

## 5. 자주 묻는 질문

**Steps를 100으로 올리면 더 좋아지나요?**
어느 지점부터 개선이 멈추는지는 모델·sampler·scheduler에 따라 다릅니다. 모델 제작자가 권장 steps를 적어 두었다면 그 값을 사용합니다. 없다면 Seed를 고정하고 20·30·40을 만들어 나란히 놓습니다. 차이가 더 보이지 않는 지점이 그 모델의 상한입니다. distilled 계열은 4~8 steps를 사용하므로 이 범위가 적용되지 않습니다.

**VAE Decode를 하지 않으면 어떻게 되나요?**
KSampler의 출력을 Save Image에 바로 연결할 수 없습니다. Latent는 압축 상태이므로 반드시 VAE Decode로 풀어야 이미지가 됩니다.

**Flux가 SD보다 항상 나은가요?**
목적에 따라 다릅니다. Flux는 파라미터가 약 12B이고 파일을 세 종류로 나눠 받으며 VRAM 요구가 큽니다. SD 1.5는 약 1B에 파일 하나이고 4~6GB에서도 돌아갑니다. 같은 프롬프트를 두 계열에서 한 장씩 만들어 보고 정하세요.

**Empty Latent 크기는 어떻게 정하나요?**
모델의 학습 해상도로 지정합니다. 학습 크기와 크게 다르면 품질이 떨어집니다.

| 모델 | 권장 크기 |
|------|-----------|
| SD 1.5 | 512×512 |
| SDXL | 1024×1024 |
| Flux | 1024×1024 |

## 완료 기준

네 가지를 모두 만족했다면 이 장을 끝냈습니다.

- Latent가 무엇이고 왜 사용하는지 한 문장으로 말할 수 있다.
- VAE Encode와 VAE Decode를 각각 언제 사용하는지 구분할 수 있다.
- UNet과 Transformer가 무엇이 다른지 설명할 수 있다.
- Checkpoint 안에 무엇이 들어 있는지, Flux는 왜 파일이 나뉘는지 말할 수 있다.

## 다음 단계

- [CLIP과 Contrastive Learning](./clip-contrastive-learning.md) — 텍스트 해석 원리
- [디노이징 프로세스](./denoising-process.md) — 노이즈가 이미지가 되는 단계
- [02. 모델 가이드](../02-models/README.md) — 모델 계열별 사용법
- [04. 워크플로우 예제](../04-workflows/README.md) — 적용 사례
- [용어 사전](../GLOSSARY.md) — 용어 정의

---

[홈](../README.md) · [시작하기](../00-getting-started/README.md)
