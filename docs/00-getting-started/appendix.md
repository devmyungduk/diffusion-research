[🏠 홈](../../README.md) | [📚 시작 가이드](README.md) | [⬅️ PART III](part-03-advanced-features.md)

---

# 부록

---

## 용어 정리

| 용어 | 설명 |
|------|------|
| **Checkpoint** | 학습 완료된 AI 모델 파일 (.safetensors, .ckpt) |
| **Latent** | 압축된 이미지 상태 (사람이 볼 수 없음) |
| **VAE** | 이미지 압축/복원 도구 (Encode/Decode) |
| **CLIP** | 텍스트를 AI가 이해하는 형태로 변환 |
| **UNet** | SD 1.5/SDXL의 이미지 생성 아키텍처 |
| **Transformer/DiT** | Flux의 이미지 생성 아키텍처 |
| **Prompt** | 원하는 이미지를 설명하는 텍스트 |
| **Negative Prompt** | 원하지 않는 요소를 설명하는 텍스트 |
| **Steps** | 이미지를 다듬는 횟수 (높을수록 정밀) |
| **CFG (Scale)** | 프롬프트 준수 강도 (7-8 권장) |
| **Sampler** | 노이즈 제거 알고리즘 (euler, dpmpp_2m 등) |
| **Scheduler** | 노이즈 제거 일정 (normal, karras 등) |
| **Seed** | 랜덤 시작점 (같은 숫자 = 비슷한 결과) |
| **Denoise** | 노이즈 제거 강도 (1.0 = 완전 생성) |
| **LoRA** | 스타일 미세조정 플러그인 (10-200MB) |
| **ControlNet** | 구조 제어 도구 (1-2GB) |
| **Conditioning** | CLIP이 변환한 프롬프트 데이터 |
| **Batch Size** | 한 번에 생성할 이미지 개수 |

---

## 참고 자료

### 공식 문서
- [ComfyUI GitHub](https://github.com/comfyanonymous/ComfyUI)
- [Stable Diffusion 공식 문서](https://stability.ai)
- [Flux 모델 문서](https://blackforestlabs.ai)

### 학습 자료
- [ComfyUI YouTube 튜토리얼](https://youtube.com/results?search_query=comfyui+tutorial)
- [Hugging Face 모델 허브](https://huggingface.co)

### 유용한 도구
- [ComfyUI Manager](https://github.com/ltdrdata/ComfyUI-Manager) - 노드 관리
- [ComfyUI Workflows](https://comfyworkflows.com) - 워크플로우 공유
- [OpenPose Editor](https://github.com/fkunn1326/openpose-editor) - 포즈 편집

---

## 마무리

이 가이드는 ComfyUI를 처음 시작하는 분들을 위한 것입니다.

---

**작성일:** 2025년 11월  
**버전:** 1.0  
**대상:** ComfyUI 초보자 ~ 중급자

[⬆️ 목차로 돌아가기](#-목차)

---

**끝**

---


---

[🏠 홈](../../README.md) | [📚 시작 가이드](README.md) | [⬅️ PART III](part-03-advanced-features.md)
