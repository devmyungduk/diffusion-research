[홈](../../README.md) · [문서 지도](../../README.md)

# Flux Quick Reference

> Flux 파이프라인에서 자주 찾는 값들을 한곳에 모았습니다. 개념 설명은 [Flux 모델 가이드](README.md), 실전 구현은 [Flux 실전 구현](flux-practical.md)을 참고하세요.

[← Flux 모델 가이드](README.md)

---

### 필수 파일 위치

| 파일 타입 | 위치 | 예시 |
|:---:|:---:|:---:|
| **Diffusion Models** | `ComfyUI/models/diffusion_models/` | flux1-dev.safetensors |
| **Text Encoders** | `ComfyUI/models/text_encoders/` | t5xxl_fp16.safetensors |
| **VAE** | `ComfyUI/models/vae/` | ae.safetensors |
| **LoRA** | `ComfyUI/models/loras/` | flux-lora-*.safetensors |
| **Style Models** | `ComfyUI/models/style_models/` | flux1-redux-dev.safetensors |
| **ControlNet** | `ComfyUI/models/controlnet/` | flux-depth-v3.safetensors |
| **CLIP Vision** | `ComfyUI/models/clip_vision/` | `sigclip_vision_patch14_384.safetensors` |
| **GGUF 양자화 모델** | `ComfyUI/models/unet/` | flux1-dev-Q6_K.gguf |

GGUF만 `unet/`을 쓰는 예외입니다. `.safetensors` 형식의 Flux 본체는 위 표대로 `diffusion_models/`에 둡니다.

### 기본 Flux 파라미터

| 파라미터 | 권장값 | 설명 |
|:---:|:---:|:---:|
| **Resolution** | 1024×1024 | Native 해상도 |
| **FluxGuidance** | 3.5 | FLUX.1 dev 공식 예제의 비교 시작값 |
| **KSampler CFG** | 1.0 | FLUX.1 공식 기본 구성에서 고전 CFG 비활성화 |
| **Steps** | 20~30 | 품질/속도 균형 |
| **Sampler** | Euler | 안정적 |
| **Scheduler** | Simple | 기본값 |

### Troubleshooting

| 문제 | 원인 | 해결책 |
|:---:|:---:|:---:|
| **Out of Memory** | VRAM 부족 | FP8 모델, 해상도 낮춤 |
| **Redux 결과 이상** | CLIP Vision 오류 | `sigclip_vision_patch14_384.safetensors` 확인 |
| **ControlNet 안 됨** | SD ControlNet 사용 | Flux 전용 사용 |
| **FLUX.1 dev 기본 결과와 다름** | guidance 경로 또는 KSampler cfg 구성 차이 | 공식 기본 구성의 guidance 경로와 `cfg=1.0` 확인 |
| **생성 속도 느림** | FP16 + 고해상도 | FP8, 작은 해상도 테스트 |

### 최소 시스템 요구사항

??? note "시스템 요구사항 표 펼치기"
    | 구성요소 | 최소 | 권장 |
    |:---:|:---:|:---:|
    | **VRAM** | 12 GB (FP8) | 24 GB (FP16) |
    | **RAM** | 16 GB | 32 GB+ |
    | **Storage** | 40 GB | 100 GB |
    | **GPU** | RTX 3060 12GB | RTX 4090 |

### 모델 약어 정리

??? note "약어표 펼치기"
    | 약어 | 전체 이름 | 설명 |
    |:---:|:---:|:---:|
    | **T5** | Text-to-Text Transfer Transformer | 텍스트 인코더 |
    | **CLIP** | Contrastive Language-Image Pre-training | 이미지-텍스트 매칭 |
    | **VAE** | Variational AutoEncoder | 이미지 압축/복원 |
    | **CFG** | Classifier-Free Guidance | 프롬프트 충실도 |
    | **LoRA** | Low-Rank Adaptation | 경량 파인튜닝 |
    | **FP8/FP16** | Float Point 8/16 | 모델 정밀도 |

---

[홈](../../README.md) · [문서 지도](../../README.md) · [Flux 모델 가이드](README.md)
