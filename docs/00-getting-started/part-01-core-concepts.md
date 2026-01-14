# PART I - 핵심 개념 (요약)

> AI 이미지 생성의 기초 개념을 빠르게 훑어봅니다.

[🏠 홈](../../README.md) | [📚 시작 가이드](README.md) | [➡️ PART II (실전)](part-02-workflow-practice.md)

---

## ⚠️ 문서 이동 알림

이 문서는 **빠른 요약본**입니다. 더 깊이 있는 설명과 최신 정보는 아래의 **정본(Canonical) 문서**에서 관리됩니다.

👉 **[이곳을 클릭하여 정본 문서(Core Concepts)를 읽어주세요!](../01-core-concepts/README.md)**

---

## 📝 1분 요약

시간이 없다면 아래 핵심 내용만 기억하고 넘어가세요.

### 1. Latent Image (잠재 이미지)
- AI는 거대한 이미지를 직접 다루지 않고, **압축된 설계도(Latent)** 상태에서 작업합니다.
- 덕분에 속도가 50배 이상 빠릅니다.
- **Latent**는 우리 눈에 보이지 않는 압축 데이터입니다.

### 2. VAE (Variational AutoEncoder)
- **Latent ↔ 이미지** 변환기입니다.
- 작업이 끝난 후 **VAE Decode**를 해야만 실제 이미지를 볼 수 있습니다.
- "이미지가 안 나와요!" → 대부분 VAE Decode를 빼먹어서 그렇습니다.

### 3. Checkpoint (모델 파일)
- 학습이 완료된 AI 모델 파일(.safetensors)입니다.
- 모델 안에는 **UNet(화가)**, **CLIP(번역가)**, **VAE(압축기)**가 모두 들어있습니다.

---

## 📚 더 깊이 배우기

궁금한 점이 있다면 아래 정본 문서에서 상세 내용을 확인하세요.

- **[Latent와 VAE 상세 원리](../01-core-concepts/README.md#1-latent-image---ai의-비밀-작업실)**
- **[UNet vs Transformer (Flux) 차이](../01-core-concepts/README.md#3-아키텍처-비교-unet-vs-transformer)**
- **[이미지가 만들어지는 과정 (Denoising)](../01-core-concepts/denoising-process.md)**

---

[➡️ PART II - 워크플로우 실전으로 이동하기](part-02-workflow-practice.md)
