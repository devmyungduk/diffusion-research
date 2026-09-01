[문서 지도](../../README.md)

# FLUX.1 텍스트 인코더와 데이터 공간

> FLUX.1이 프롬프트를 어떻게 받아들이고, 텍스트 조건과 이미지 압축 공간이 어떻게 다른지 정리합니다.

## 이 장에서 배우는 것

- T5XXL과 CLIP이 각각 무엇을 맡는지
- 정밀도에 따른 텍스트 인코더 파일 선택 기준
- 텍스트 조건(Vector Space)과 이미지 압축 공간(Latent Space)의 차이

<div class="guide-meta" markdown>
**대상** FLUX.1 파이프라인을 구성해 봤고 내부 동작이 궁금한 사용자 · **사전 이해** [Flux 모델 가이드](README.md)의 로더 구성 · **시간** 15분

**이럴 때 읽으세요** 텍스트 인코더 파일을 어느 정밀도로 받을지 고민될 때, 또는 두 "공간"이 헷갈릴 때.
</div>

## 텍스트 인코더

### T5XXL 이해

T5는 Text-to-Text Transfer Transformer의 약자입니다.

| 구성 | 의미 | 설명 |
|---|---|---|
| **T5** | Text-to-Text Transfer Transformer | Google AI 2019년 모델 |
| **XXL** | eXtra eXtra Large | 11B parameters |

#### T5의 역할

T5XXL은 프롬프트 문장을 받아 `[seq_len × 4096]` 크기의 임베딩으로 바꾸고, Flux 모델은 이 임베딩을 생성 과정의 지침으로 사용합니다. 문장이 길고 문맥이 복잡해도 CLIP보다 넓은 범위를 한 번에 인코딩합니다.

#### T5XXL 파일 크기

| 파일명 | 크기 | 정밀도 | 권장 RAM |
|---|---|---|---|
| `t5xxl_fp16.safetensors` | 9.79 GB | 16-bit | 32GB+ |
| `t5xxl_fp8_e4m3fn_scaled.safetensors` | ~4.9 GB | 8-bit | <32GB |

**선택 가이드:**

- RAM 32GB 이상 → **FP16** (9.79GB, 원본 정밀도)
- RAM 32GB 미만 → **FP8** (약 4.9GB)

### CLIP 이해

CLIP은 Contrastive Language-Image Pre-training의 약자입니다.

#### 이름이 가리키는 것

| 부분 | 뜻 | 무엇을 말하는가 |
|:---|:---|:---|
| **Contrastive** | 대조 | 맞는 (이미지, 캡션) 짝은 가깝게, 틀린 짝은 멀게 학습합니다 |
| **Language-Image** | 언어–이미지 | 텍스트와 이미지를 같은 임베딩 공간에 놓습니다 |
| **Pre-training** | 사전 학습 | 특정 작업에 맞추기 전에 대규모 데이터로 먼저 학습합니다 |

#### Flux의 이중 텍스트 인코더

Flux는 두 인코더를 함께 사용합니다.

- **CLIP**: Text → 768차원 임베딩
- **T5XXL**: Text → 4096차원 임베딩

**역할 분담:**
- **CLIP**: 768차원 pooled 출력 하나를 만듭니다. 짧은 키워드 나열에 대응합니다.
- **T5XXL**: 토큰마다 4096차원 벡터를 만듭니다. 긴 문장의 어순과 수식 관계가 여기에 담깁니다.

---

## Vector Space와 Latent Space

### 두 공간의 차이

| 구분 | Vector Space | Latent Space |
|---|---|---|
| **생성자** | Text Encoder (T5/CLIP) | VAE Encoder |
| **표현 대상** | 텍스트 의미/개념 | 이미지 시각 정보 |
| **차원** | (seq_len, 4096) | (128, 128, 16) — FLUX.1을 1024×1024로 생성할 때 |
| **역할** | 무엇을 생성할지 | 이미지가 어떻게 보일지 |
| **공간 타입** | Semantic embedding | Compressed visual |

### Flux 전체 파이프라인

1. **Text Prompt** — 사용자 입력 ("a cat wearing a hat")
2. **T5XXL + CLIP Encoder** — 텍스트를 4096차원 벡터로 변환 (Vector Space)
3. **Random Noise** (128×128×16) — 생성 시작점
4. **Flux Diffusion Model** — 텍스트 벡터로 guided denoising (Latent Space)
5. **Denoised Latent** (128×128×16) — 정제된 latent
6. **VAE Decoder** — latent을 이미지로 복원
7. **Final Image** (1024×1024×3 RGB) — 출력

!!! note "이 숫자는 FLUX.1 · 1024×1024 기준입니다"
    `128×128×16`은 모든 모델의 공통 규격이 아닙니다. 해상도가 바뀌면 앞의 두 숫자가 바뀌고, 세대가 바뀌면 채널 수와 축소 비율까지 달라집니다. 자세한 내용은 [디노이징 프로세스](../../01-core-concepts/denoising-process.md#3-u-net과-transformer-구분)를 참고하세요.

### 관계 이해

**질문:** 텍스트 벡터가 Latent로 변환되는 걸까요?

**답:** 아닙니다. 벡터는 Latent가 만들어지는 **방향을 안내**할 뿐, 그 자체가 Latent가 되지는 않습니다.

| 설명 | 판정 | 이유 |
|---|---|---|
| 벡터가 Latent로 변환된다 | 틀림 | 두 데이터는 서로 변환되지 않습니다 |
| 벡터가 Latent 생성을 안내한다 | 맞음 | 생성 방향을 제시합니다 |
| 서로 다른 공간이다 | 맞음 | 표현 대상과 목적이 다릅니다 |

## 완료 기준

세 가지를 모두 만족했다면 이 장을 끝냈습니다.

- T5XXL과 CLIP의 역할 분담을 설명할 수 있다.
- 내 RAM에 맞는 T5XXL 정밀도를 골랐다.
- 텍스트 벡터가 Latent로 변환되는 것이 아니라 생성 방향을 안내한다는 점을 설명할 수 있다.

## 다음 단계

- [FluxGuidance 이해와 사용](fluxguidance-pipeline.md) — guidance 값 비교
- [FLUX.1 작업 선택과 Redux 실습](flux-practical.md) — 참조 이미지 작업
- [빠른 참조](quick-reference.md) — 파일 위치와 시작값

---

[홈](../../README.md) · [Flux 모델 가이드](README.md)
