[문서 지도](../../README.md)

# Flux 모델 변형 비교

> 제어 워크플로우에서 사용하는 Flux 모델(Dev/Fill), 정밀도(FP16/FP8), 양자화(GGUF) 선택 기준을 정리합니다.

## 이 장에서 배우는 것

- Dev는 범용, Fill은 인페인팅·아웃페인팅 전용입니다. Fill로는 Text-to-Image를 할 수 없습니다.
- 정밀도를 낮추면 VRAM 요구가 줄고 품질이 조금씩 떨어집니다. 내 VRAM에서 돌아가는 가장 높은 정밀도를 고르면 됩니다.

<div class="guide-meta" markdown>
**대상** Flux를 사용하려는데 파일 선택에서 막힌 사용자 · **사전 이해** 자신의 GPU VRAM 용량 · **시간** 10분

**이럴 때 읽으세요** Flux 파일 종류가 너무 많아 무엇을 받아야 할지 모를 때.
</div>

## 1. 모델 버전

| 모델 | 목적 | 라이선스 | 크기 (FP16) | 크기 (FP8) |
|:-----|:-----|:--------|:------------|:-----------|
| **Flux.1 Pro** | API 전용 | Closed-source (API only) | 공개 없음 | 공개 없음 |
| **Flux.1 Dev** | 고품질 | 비상업용 | ~23GB | ~12GB |
| **Flux.1 Fill** | Inpainting/Outpainting | 비상업용 | ~23GB | 공식 배포 없음 |
| **Flux.1 Schnell** | 빠른 생성 (4 steps) | Apache 2.0 | ~23GB | ~12GB |

크기는 Black Forest Labs가 배포하는 원본 기준입니다. `공식 배포 없음`이라고 적힌 칸도 커뮤니티가 만든 양자화본이 있을 수 있으므로, 받기 전 해당 배포 페이지에서 파일 크기와 대상 모델을 확인하세요.

## 2. FP16 vs FP8 비교

| 특징 | FP16 | FP8 |
|:-----|:-----|:----|
| **품질** | 최대 디테일 | 약간 감소 (실용적) |
| **속도** | 느림 | 더 빠름(아래 측정값 참고) |
| **VRAM** | 24GB+ | 12GB+ |
| **파일 크기** | ~23GB | ~12GB |
| **용도** | 디테일 중시 | 효율성 중시 |

**참고 측정값 (RTX 4080 Super, 50 steps, 1회만 측정):**
```
FP16: 약 95초
FP8:  약 55초
```

한 환경에서 한 번만 잰 값입니다. GPU·해상도·steps·다른 노드 구성에 따라 달라지므로, 순서(FP8이 더 빠르다)만 참고하고 자기 환경에서 직접 재보세요.

## 3. Flux.1 Dev vs Fill

| 특징 | Flux.1 Dev | Flux.1 Fill |
|:-----|:-----------|:------------|
| **Text-to-Image** | 지원 | **불가** |
| **Inpainting** | 표준 노드로 가능 | 전용 최적화 |
| **Outpainting** | 표준 노드로 가능 | 전용 최적화 |
| **성능** | 범용 | Inpainting 전문 |
| **사용 시기** | 일반 생성 | 기존 이미지 편집 |

!!! warning "Flux.1 Fill로는 새 이미지를 만들 수 없습니다"
    Fill은 기존 이미지의 일부를 채우는 전용 모델입니다. 프롬프트만으로 처음부터 그림을 만들려면 Dev를 사용하세요.

## 4. 선택 가이드

| 상황 | 추천 모델 | 이유 |
|:-----|:---------|:-----|
| **VRAM ≤ 16GB** | **Flux Dev FP8** | 단일 파일, 빠름, 실용적 품질 |
| **VRAM ≥ 24GB** | Flux Dev FP16 | 최대 품질 |
| **Inpainting만** | Flux Fill | 전용 최적화 |
| **Text-to-Image 필요** | Flux Dev | Fill로는 할 수 없습니다 |
| **극저사양** | GGUF Q4/Q5 | 6-8GB VRAM 가능. GGUF는 `models/unet/`에 둡니다 |

## 5. 양자화 옵션

정밀도를 낮출수록 파일과 VRAM 요구가 줄고 품질이 조금씩 떨어집니다. 아래는 **선택 순서**를 잡기 위한 정성적 정리입니다.

| 포맷 | 품질 경향 | VRAM 기준 | 비고 |
|:-----|:-----|:-----|:-----|
| **FP16** | 기준 | 24GB+ | 원본 정밀도 |
| **FP8** | 기준에 근접 | 12GB+ | 용량 대비 실용적 |
| **GGUF Q8** | 기준에 근접 | 12GB+ | FP16과 차이가 작음 |
| **GGUF Q6** | 약간 저하 | 10GB+ | 무난한 타협 |
| **GGUF Q5** | 저하 | 8GB+ | 저사양에서 선택 |
| **GGUF Q4** | 눈에 띄는 저하 | 6GB+ | 형태·글자 깨짐이 늘어남 |

품질을 백분율로 비교한 표가 커뮤니티에 돌지만 측정 기준이 제각각입니다. 숫자를 외우기보다, 자기 VRAM에서 **돌아가는 가장 높은 정밀도**를 고르고 같은 Seed로 한 장씩 비교해 보세요.

**확인 방법:** FP16과 FP8의 차이가 자신의 작업에서 문제가 되는지는 직접 봐야 합니다. 같은 Seed·프롬프트·steps로 두 정밀도를 한 장씩 만들어 나란히 놓고 판단하세요.

## 6. 설치 설정 (권장)

파일 배치는 **어떤 형태의 Flux 파일을 받았는지**에 따라 다릅니다. 두 가지를 섞지 마세요.

**(A) 올인원 체크포인트 한 개를 받은 경우** — 텍스트 인코더와 VAE가 파일 안에 포함되어 있습니다.

```
ComfyUI/models/checkpoints/flux1-dev-fp8.safetensors

로더: Load Checkpoint 하나
```

**(B) 파일이 나뉜 구성을 받은 경우** — 아래 세 종류를 각각 받아 배치합니다.

```
ComfyUI/models/diffusion_models/flux1-dev.safetensors
ComfyUI/models/text_encoders/clip_l.safetensors
ComfyUI/models/text_encoders/t5xxl_fp8_e4m3fn.safetensors
ComfyUI/models/vae/ae.safetensors

로더: Load Diffusion Model + Dual CLIP Loader + Load VAE
```

GGUF 파일은 예외적으로 `ComfyUI/models/unet/`에 둡니다. 자세한 배치는 [Flux 빠른 참조](../../02-models/flux/quick-reference.md#필수-파일-위치)를 참고하세요.

## 완료 기준

세 가지를 모두 만족했다면 이 장을 끝냈습니다.

- 내 VRAM에 맞는 정밀도를 골랐다.
- 받은 파일이 올인원 체크포인트인지 분리 구성인지 구분하고 알맞은 폴더에 넣었다.
- Fill 모델로는 Text-to-Image를 할 수 없다는 점을 안다.

## 다음 단계

- [Flux 모델 가이드](../../02-models/flux/README.md) — 세대별 라인업과 파이프라인
- [ControlNet 아키텍처](controlnet-architecture.md) — 제어 워크플로우 연결

---

[문서 지도](../../README.md) · [ControlNet 아키텍처](controlnet-architecture.md)
