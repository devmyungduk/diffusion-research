[홈](../README.md) · [시작하기](README.md) · [이전: 설치](installation.md) · [다음: 캔버스 다루기](canvas-basics.md)

# 모델 준비

> 체크포인트 파일 하나를 받아 알맞은 폴더에 넣고, ComfyUI 목록에 나타나는지 확인합니다.

## 이 장에서 배우는 것

- 처음 받을 모델은 VRAM이 정합니다. 8GB 미만이면 SD 1.5, 8GB 이상이면 SDXL입니다.
- 모델은 종류별로 다른 폴더에 들어갑니다. 확장자가 모두 `.safetensors`라 파일 이름만으로는 구분되지 않습니다.

<div class="guide-meta" markdown>
**대상** ComfyUI를 설치했고 모델이 아직 없는 사용자 · **사전 이해** [설치](installation.md) · **시간** 15분

**이럴 때 읽으세요** 어떤 모델을 받아야 할지 모르거나, 넣었는데 `Load Checkpoint` 목록에 보이지 않을 때.
</div>

## 1. 모델 폴더 열기

모델은 `ComfyUI/models/` 아래에 둡니다. 이 폴더의 실제 위치는 설치 방식마다 다릅니다.

- **데스크톱 앱**: 앱 메뉴에서 **Help → Open Folder → Open Model Folder**를 선택하면 해당 폴더가 바로 열립니다.
- **포터블·수동 설치**: 압축을 풀거나 `git clone`한 `ComfyUI` 폴더 안의 `models`입니다.

## 2. 모델 내려받기

처음이라면 아래 둘 중 **하나만** 받습니다. VRAM이 8GB 미만이면 SD 1.5, 8GB 이상이면 SDXL입니다.

| 모델 | 받을 파일 | 크기 | |
|---|---|---:|---|
| SD 1.5 | `v1-5-pruned-emaonly-fp16.safetensors` | 2.1GB | [내려받기](https://huggingface.co/Comfy-Org/stable-diffusion-v1-5-archive/resolve/main/v1-5-pruned-emaonly-fp16.safetensors) |
| SDXL | `sd_xl_base_1.0.safetensors` | 6.9GB | [내려받기](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors) |

`내려받기`를 누르면 저장이 바로 시작됩니다. 표에 적힌 크기만큼 받으므로 연결 상태를 먼저 확인하세요. 받은 파일은 다음 절의 `checkpoints/`에 넣습니다.

저장소 페이지를 직접 열면 파일이 많습니다. SDXL 저장소에는 57개가 있고 그중 `.safetensors`가 18개입니다. `unet/`·`vae/`·`text_encoder/` 폴더 안의 파일과, 이름이 한 글자 다른 `sd_xl_base_1.0_0.9vae.safetensors`는 ComfyUI가 사용하는 체크포인트가 아닙니다. 위 표의 이름과 같은 것을 받으세요.

??? note "저장소에서 직접 고를 때 · 다른 모델을 찾을 때"

    저장소 페이지에서 고르는 순서입니다.

    1. 저장소를 엽니다 — [SD 1.5](https://huggingface.co/Comfy-Org/stable-diffusion-v1-5-archive) · [SDXL](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0)
    2. `Files and versions` 탭을 누릅니다.
    3. 파일 이름 오른쪽의 내려받기 아이콘을 누릅니다.

    다른 모델은 [Hugging Face](https://huggingface.co)와 [Civitai](https://civitai.com)에서 찾습니다. 앞쪽은 제작사가 올린 원본이고, 뒤쪽은 커뮤니티가 다듬은 화풍이라 예시 이미지에 설정값이 함께 올라옵니다. Civitai는 모델 페이지 오른쪽의 `Download` 버튼으로 받습니다.

    한 페이지에 파일이 여러 개면 이름의 표기로 고릅니다. `.ckpt`는 여는 과정에서 코드가 실행될 수 있으므로 같은 모델이면 `.safetensors`를 받습니다. `fp16`은 `fp32`의 절반 크기이고, 제작자가 따로 안내하지 않으면 fp16을 고릅니다. `pruned`는 추가 학습용 데이터를 뺀 판이라 이미지 생성만 한다면 이쪽입니다.

## 3. 종류별 폴더에 넣기

<div class="filetree filetree--icon" markdown>

- `ComfyUI/models/`
    - `checkpoints/` <span class="filetree__note">SD 1.5·SDXL 체크포인트</span>
    - `vae/` <span class="filetree__note">별도 VAE 파일</span>
    - `loras/` <span class="filetree__note">LoRA 파일</span>
    - `controlnet/` <span class="filetree__note">ControlNet 모델</span>
    - `text_encoders/` <span class="filetree__note">CLIP·T5 등 텍스트 인코더. Flux에서 사용합니다</span>
    - `diffusion_models/` <span class="filetree__note">Flux 등 diffusion 모델 본체</span>

</div>

!!! warning "확장자로는 종류를 구분할 수 없습니다"
    체크포인트·LoRA·VAE·텍스트 인코더·업스케일러가 **모두 `.safetensors`** 확장자를 사용합니다. 확장자만 보고 폴더를 고르면 잘못 들어갑니다. 파일 이름만 보고 판단하지 말고, 내려받은 페이지에 적힌 모델 종류를 확인한 뒤 넣으세요.

> 구버전 ComfyUI나 오래된 튜토리얼은 `clip/`·`unet/`이라는 이름을 사용합니다. 현재 표준은 `text_encoders/`·`diffusion_models/`이며, ComfyUI는 구 폴더도 계속 읽으니 로더 목록이 비어 보이면 파일이 반대쪽 폴더에 있는지 확인하세요. (GGUF 파일은 예외적으로 `unet/`을 사용합니다.)

## 4. ComfyUI에 인식시키기

ComfyUI가 실행 중인 상태에서 파일을 넣었다면 목록이 자동으로 갱신되지 않습니다. 브라우저 화면에서 **`r` 키를 눌러 노드 정의를 새로 읽거나**, ComfyUI를 재시작합니다.

## 5. 제대로 들어갔는지 확인하기

`Load Checkpoint` 노드를 하나 추가하고 `ckpt_name` 목록을 엽니다. 방금 넣은 파일 이름이 보이면 성공입니다.

목록이 비어 있다면 순서대로 확인합니다.

1. 4번의 새로고침을 했는지
2. 파일이 `checkpoints/`가 아닌 다른 폴더에 들어갔는지
3. 열어 본 `models` 폴더가 실제로 ComfyUI가 사용하는 경로인지 (설치가 여러 개면 경로가 각각 다릅니다)

??? note "모델이 많아진 뒤에 — 하위 폴더와 다른 드라이브"

    `checkpoints/` 안에 하위 폴더를 만들어 나눠 담아도 ComfyUI가 함께 읽습니다. 목록에는 `풍경/model.safetensors`처럼 폴더 이름이 앞에 붙어 나오므로 같은 이름의 다른 판을 구분할 수 있습니다.


    모델 파일이 커서 설치 드라이브가 부족하면, `models` 폴더를 옮기지 않고 **검색 경로를 추가**할 수 있습니다. ComfyUI 폴더의 `extra_model_paths.yaml.example`을 `extra_model_paths.yaml`로 복사한 뒤 경로를 적으면, 다른 드라이브나 다른 프로그램의 모델 폴더를 함께 읽습니다. 설정 후에는 ComfyUI를 재시작합니다.

    Flux 같은 최신 모델은 파일이 여러 개로 나뉘어 각각 다른 폴더에 들어갑니다. 자세한 배치는 [Flux 가이드](../02-models/flux/README.md)에 있습니다.

## 완료 기준

세 가지를 모두 만족했다면 이 장을 끝냈습니다.

- 체크포인트 파일을 하나 이상 `checkpoints/` 폴더에 넣었다.
- `Load Checkpoint` 노드를 추가하고 `ckpt_name` 목록에서 그 파일 이름을 확인했다.
- 파일을 넣은 뒤 목록에 반영하려면 `r` 키를 누르거나 재시작해야 한다는 점을 확인했다.

## 다음 단계

- [캔버스 다루기](canvas-basics.md) — 캔버스 이동과 시야 조정
- [5분 빠른 시작](quick-start.md) — 노드를 연결해 첫 이미지 생성
- [문제 해결](../05-troubleshooting/README.md) — 모델을 넣었는데 결과가 이상할 때

---

[홈](../README.md) · [시작하기](README.md) · [이전: 설치](installation.md) · [다음: 캔버스 다루기](canvas-basics.md)
