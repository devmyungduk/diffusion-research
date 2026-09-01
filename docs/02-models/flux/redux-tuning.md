[문서 지도](../../README.md)

# Redux 확인과 비교 실험

> 불러온 Redux 예제가 어떻게 연결되어 있는지 확인하고, 값을 하나씩 바꿔 결과를 비교합니다.

## 이 장에서 배우는 것

- 참조 이미지 조건과 텍스트 조건이 어느 노드에서 합쳐지는지
- 공식 예제가 사용하는 시작값과 그 값을 그대로 두는 이유
- 참조 이미지·프롬프트·guidance·strength를 하나씩 바꿔 비교하는 절차

<div class="guide-meta" markdown>
**대상** 공식 Redux 예제를 불러와 한 장을 만들어 본 사용자 · **사전 이해** [FLUX.1 작업 선택과 Redux 실습](flux-practical.md) · **시간** 20분

**이럴 때 읽으세요** 예제는 돌아가는데 참조 이미지의 영향을 조절하고 싶을 때, 또는 결과가 예제와 다를 때.
</div>

## 1. 노드와 포트 확인

화면에서 노드 위치를 외우기보다 출력 타입이 어느 입력으로 들어가는지 확인합니다. 불러온 예제가 정상 동작한다면 지금 다 확인할 필요는 없습니다. **결과가 이상할 때 아래를 펼쳐 하나씩 대조하세요.**

세 갈래로 나뉩니다.

- **참조 이미지 조건** — Load Image에서 출발해 Style Model Apply로
- **텍스트 조건** — 프롬프트에서 출발해 FluxGuidance를 거쳐 Style Model Apply로
- **샘플링과 이미지 출력** — 두 조건이 합쳐진 뒤 SamplerCustomAdvanced에서 이미지까지

??? note "포트 연결 확인 — 참조 이미지 조건"
    | 보내는 출력 | 받는 입력 | 확인할 값 |
    |---|---|---|
    | CLIP Vision Loader `CLIP_VISION` | CLIP Vision Encode `clip_vision` | `sigclip_vision_patch14_384.safetensors` |
    | Load Image `IMAGE` | CLIP Vision Encode `image` | 사용할 참조 이미지 |
    | CLIP Vision Encode `CLIP_VISION_OUTPUT` | Style Model Apply `clip_vision_output` | 포트 타입 일치 |
    | Style Model Loader `STYLE_MODEL` | Style Model Apply `style_model` | `flux1-redux-dev.safetensors` |

??? note "포트 연결 확인 — 텍스트 조건"
    | 보내는 출력 | 받는 입력 | 역할 |
    |---|---|---|
    | Dual CLIP Loader `CLIP` | CLIP Text Encode `clip` | 프롬프트 인코딩 |
    | CLIP Text Encode `CONDITIONING` | FluxGuidance `conditioning` | 텍스트 조건 전달 |
    | FluxGuidance `CONDITIONING` | Style Model Apply `conditioning` | guidance가 포함된 텍스트 조건 전달 |
    | Style Model Apply `CONDITIONING` | BasicGuider `conditioning` | 텍스트와 참조 이미지 조건을 sampler에 전달 |

??? note "포트 연결 확인 — 샘플링과 이미지 출력"
    | 보내는 출력 | 받는 입력 | 역할 |
    |---|---|---|
    | Load Diffusion Model `MODEL` | ModelSamplingFlux `model` | FLUX.1 모델 전달 |
    | ModelSamplingFlux `MODEL` | BasicGuider `model` | FLUX 샘플링 설정이 적용된 모델 전달 |
    | ModelSamplingFlux `MODEL` | BasicScheduler `model` | 모델에 맞는 sigma schedule 계산 |
    | RandomNoise `NOISE` | SamplerCustomAdvanced `noise` | Seed로 만든 시작 노이즈 |
    | BasicGuider `GUIDER` | SamplerCustomAdvanced `guider` | 최종 conditioning과 모델 전달 |
    | KSamplerSelect `SAMPLER` | SamplerCustomAdvanced `sampler` | sampler 알고리즘 전달 |
    | BasicScheduler `SIGMAS` | SamplerCustomAdvanced `sigmas` | 스텝별 노이즈 수준 전달 |
    | EmptySD3LatentImage `LATENT` | SamplerCustomAdvanced `latent_image` | 생성 크기와 batch 전달 |
    | SamplerCustomAdvanced `output` | VAE Decode `samples` | 생성된 latent 전달 |
    | Load VAE `VAE` | VAE Decode `vae` | latent 디코딩 |
    | VAE Decode `IMAGE` | Save Image `images` | 이미지 저장 |

## 2. 공식 예제의 시작값

다음 값은 공식 Redux 예제 이미지에 저장된 워크플로우의 설정입니다. 모든 이미지에서 가장 좋은 값이라는 뜻이 아니라, 예제를 재현하기 위한 시작점입니다.

| 노드 | 설정 | 예제 값 |
|---|---|---:|
| FluxGuidance | `guidance` | `3.5` |
| ModelSamplingFlux | `max_shift` | `1.15` |
| ModelSamplingFlux | `base_shift` | `0.5` |
| ModelSamplingFlux | `width`, `height` | `1024`, `1024` |
| KSamplerSelect | `sampler_name` | `euler` |
| BasicScheduler | `scheduler` | `simple` |
| BasicScheduler | `steps` | `20` |
| BasicScheduler | `denoise` | `1.0` |
| EmptySD3LatentImage | `width`, `height`, `batch_size` | `1024`, `1024`, `1` |
| RandomNoise | `noise_seed` | `958831004022715` |

`StyleModelApply`의 `strength`·`strength_type`은 노드 기본값인 `1.0`·`multiply`를 그대로 사용합니다. 불러온 워크플로우에서 다른 값으로 되어 있다면 그 값이 우선이며, 비교 실험 전에 무엇으로 설정돼 있는지 먼저 확인하세요.

`SamplerCustomAdvanced`에는 `cfg` 위젯이 없습니다. 공식 예제에서는 `BasicGuider`가 최종 conditioning을 전달합니다. `cfg=1.0`은 KSampler를 사용할 때의 값입니다. 이 노드에는 없습니다.

`ModelSamplingFlux`와 `EmptySD3LatentImage`의 너비·높이는 같은 생성 크기를 사용합니다. 해상도를 바꿀 때 한쪽만 바꾸지 않습니다.

## 3. 첫 비교 실험

먼저 공식 예제를 한 번 실행해 모델과 연결이 정상인지 확인합니다. 공식 PNG의 `RandomNoise`는 생성 후 Seed 동작이 `randomize`로 저장되어 있으므로, 비교 실험 전에 다음 절차로 기준을 다시 만듭니다.

1. `RandomNoise`의 Seed를 기록합니다.
2. 생성 후 Seed 동작을 `fixed`로 바꿉니다.
3. 한 번 더 실행해 비교용 기준 이미지를 저장합니다.
4. 아래 표에 따라 한 번에 하나만 바꿉니다.

| 비교 | 고정할 항목 | 바꿀 항목 | 관찰할 내용 |
|---|---|---|---|
| A | 모델·Seed·프롬프트·샘플링 설정 | 참조 이미지 | 색, 형태, 구도 중 무엇이 달라지는가 |
| B | 모델·Seed·참조 이미지·샘플링 설정 | 프롬프트 | 텍스트 지시가 어떤 요소를 바꾸는가 |
| C | 모델·Seed·참조 이미지·프롬프트 | guidance | 지시 반영과 화면의 자연스러움이 어떻게 달라지는가 |
| D | 나머지 전부 | `StyleModelApply`의 `strength` | 참조 이미지의 영향이 얼마나 강해지거나 약해지는가 |

D를 진행할 때는 기본값 `1.0`에서 출발해 작은 폭으로 올리거나 내립니다. `strength_type`까지 동시에 바꾸면 어느 쪽이 결과를 바꿨는지 구분할 수 없습니다.

??? note "기록 양식 — 비교 결과를 남기는 표"
    | 항목 | 기록 |
    |---|---|
    | 기본 모델·정밀도 |  |
    | 참조 이미지 |  |
    | 프롬프트 |  |
    | Seed |  |
    | guidance |  |
    | sampler·scheduler·steps |  |
    | 참조 이미지에서 유지된 요소 |  |
    | 프롬프트로 바뀐 요소 |  |
    | 다음에 바꿀 한 가지 |  |

## 4. 문제 해결

??? warning "증상별 확인 순서"
    | 증상 | 확인 순서 |
    |---|---|
    | CLIP Vision 모델을 찾지 못함 | 1. 파일명 확인<br>2. `models/clip_vision/` 위치 확인<br>3. ComfyUI 재시작 |
    | Style Model을 찾지 못함 | 1. `flux1-redux-dev.safetensors` 확인<br>2. `models/style_models/` 위치 확인 |
    | `StyleModelApply`에서 strength를 찾을 수 없음 | ComfyUI가 오래된 버전일 수 있습니다. 업데이트한 뒤 노드를 다시 추가해 `strength`·`strength_type` 위젯이 보이는지 확인 |
    | 참조 이미지의 영향이 보이지 않음 | 1. Load Image 연결<br>2. CLIP Vision Encode 출력<br>3. Style Model Apply 출력<br>4. BasicGuider 입력 확인 |
    | 프롬프트를 바꿔도 차이가 없음 | CLIP Text Encode 출력이 FluxGuidance와 Style Model Apply를 거쳐 BasicGuider로 들어가는지 확인 |
    | `cfg` 입력을 찾을 수 없음 | 공식 예제의 SamplerCustomAdvanced 구성인지 확인. `cfg`는 이 노드의 입력이 아닙니다. |
    | 결과가 비교할 때마다 크게 바뀜 | RandomNoise의 Seed와 생성 후 Seed 동작을 고정 |

??? question "복습 Q&A"
    **Q. Redux는 스타일 전송 전용인가요?**  
    A. 아닙니다. 공식 용도는 참조 이미지로 FLUX.1 dev 또는 schnell을 조건화해 이미지 변형을 만드는 것입니다.

    **Q. Style Model Apply의 권장 strength는 얼마인가요?**  
    A. 노드 기본값은 `1.0`이며 이것이 공식 예제의 출발점입니다. 모든 이미지에 맞는 권장값은 없으므로, 나머지를 고정하고 이 값만 바꿔 비교해 정합니다.

    **Q. FluxGuidance는 참조 이미지를 인코딩하나요?**  
    A. 아닙니다. 텍스트 conditioning에 FLUX guidance 값을 설정합니다. 참조 이미지는 CLIP Vision Encode와 Redux style model 경로에서 처리됩니다.

    **Q. 공식 예제는 KSampler를 사용하나요?**  
    A. 현재 공식 Redux 예제 이미지는 `SamplerCustomAdvanced`, `BasicGuider`, `KSamplerSelect`, `BasicScheduler`를 조립해 사용합니다.

    **Q. guidance 3.5가 항상 최적인가요?**  
    A. 아닙니다. 공식 예제를 재현하는 시작값입니다. 같은 Seed와 나머지 설정을 고정하고 비교합니다.

## 완료 기준

네 가지를 모두 만족했다면 이 장을 끝냈습니다.

- `StyleModelApply`의 세 입력과 출력, 그리고 `strength`·`strength_type` 위젯을 설명할 수 있다.
- Redux 구성과 KSampler 구성을 섞지 않고 sampler 입력을 확인할 수 있다.
- 한 번에 변수 하나만 바꾼 비교 결과를 기록했다.
- 결과가 어긋났을 때 어느 포트부터 확인할지 안다.

## 다음 단계와 공식 자료

- [FluxGuidance 이해와 사용](fluxguidance-pipeline.md) — 텍스트 guidance 비교
- [KSampler·KSamplerAdvanced·SamplerCustomAdvanced](../../03-advanced-techniques/samplers/ksampler-vs-advanced.md) — sampler 노드 구분
- [ControlNet 아키텍처](../../03-advanced-techniques/controlnet/controlnet-architecture.md) — 구조 조건이 필요할 때
- [ComfyUI 공식 FLUX 예제](https://comfyanonymous.github.io/ComfyUI_examples/flux/) — Redux 워크플로우와 모델 위치
- [ComfyUI StyleModelApply 노드 페이지](https://docs.comfy.org/built-in-nodes/StyleModelApply) — 문서 페이지가 현재 노드보다 늦게 갱신될 수 있으므로 위젯 목록은 화면의 노드를 기준으로 확인

---

[문서 지도](../../README.md) · [Flux 모델 가이드](README.md)
