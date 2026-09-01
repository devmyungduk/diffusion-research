*[KSampler]: 노이즈 제거 과정을 실행하는 핵심 노드입니다. Steps, CFG, Sampler 등을 설정합니다.
*[KSamplerAdvanced]: add_noise, start_at_step, end_at_step을 직접 지정하는 샘플러 노드입니다.
*[SamplerCustomAdvanced]: noise, guider, sampler, sigmas, latent_image 다섯 입력을 각각 받는 샘플러 노드입니다.
*[BasicGuider]: 모델과 conditioning을 묶어 샘플러에 넘기는 노드입니다. negative 입력 포트가 없습니다.
*[FluxGuidance]: CONDITIONING에 guidance 값을 얹어 FLUX.1 dev에 넘기는 노드입니다.
*[StyleModelApply]: conditioning, style_model, clip_vision_output을 받아 새 CONDITIONING을 만드는 노드입니다.
*[ModelSamplingFlux]: FLUX.1에서 해상도에 맞춰 sigma 스케줄을 조정하는 노드입니다.
*[EmptySD3LatentImage]: Flux·SD3 계열에서 빈 Latent를 만드는 노드입니다.
*[CLIP]: 텍스트와 이미지를 같은 의미 공간에 놓도록 학습한 모델입니다. 프롬프트를 숫자로 바꿉니다.
*[CLIP Vision]: CLIP의 이미지 인코더 부분입니다. 참조 이미지를 임베딩으로 바꿉니다.
*[ControlNet]: 윤곽선·포즈·깊이 같은 이미지 구조를 제어하는 보조 모델입니다.
*[IPAdapter]: 참조 이미지를 CLIP Vision으로 인코딩해 MODEL을 수정하는 제어 기법입니다.
*[Redux]: FLUX.1을 이미지로 조건화하는 어댑터입니다.
*[LoRA]: 거대 모델을 효율적으로 미세조정하는 기술 또는 그 결과물 파일입니다.
*[VAE]: 이미지(Pixel 공간)와 Latent(압축 공간) 사이를 변환하는 도구입니다.
*[Checkpoint]: 학습이 끝난 AI 모델 파일 전체입니다. UNet, VAE, CLIP이 함께 들어 있습니다.
*[Conditioning]: 프롬프트를 텍스트 인코더가 변환한 결과로, 모델이 참고하는 조건 데이터입니다.
*[Seed]: 난수 생성의 기준이 되는 숫자입니다. 고정하면 같은 결과를 재현할 수 있습니다.
*[Steps]: 디노이징을 반복하는 횟수입니다. 20~30에서 시작합니다.
*[CFG]: 프롬프트 조건을 얼마나 강하게 밀어붙일지 정하는 값입니다. 품질 점수가 아닙니다.
*[Denoise]: 전체 샘플링 구간 중 어느 정도를 사용할지 정하는 KSampler의 값입니다.
*[Sampler]: 각 단계에서 Latent를 다음 상태로 갱신하는 계산 방법입니다.
*[Scheduler]: 전체 Steps에 노이즈 수준(sigma)을 어떻게 배분할지 정하는 시간표입니다.
*[Bypass]: 노드의 계산을 건너뛰고 입력을 그대로 출력으로 넘기는 상태입니다. 단축키 Ctrl + B.
*[Mute]: 노드가 출력을 내보내지 않는 상태입니다. 단축키 Ctrl + M. 뒤쪽 노드는 실행되지 않습니다.
*[Reroute]: 연결선의 경유점 역할만 하는 노드입니다. 데이터를 바꾸지 않습니다.
*[Note]: 캔버스에 글을 적어 두는 노드입니다. 실행에 참여하지 않고 워크플로우 .json에 함께 저장됩니다.
*[버킷]: 모델이 학습한 해상도 목록의 각 항목입니다. 목록을 벗어나면 구도가 왜곡되거나 같은 대상이 반복됩니다.
*[GGUF]: 양자화한 모델을 담는 파일 형식입니다. ComfyUI에서는 unet/ 폴더에 둡니다.
*[safetensors]: 모델 파일 형식입니다. 체크포인트·LoRA·VAE가 모두 이 확장자를 씁니다.
*[OOM]: 그래픽카드 메모리가 부족해 생성이 중단되는 오류입니다.
*[VRAM]: 그래픽카드에 달린 메모리입니다. 모델·해상도·배치 크기가 여기에 들어가야 합니다.
*[Batch Count]: Run 버튼 옆의 숫자입니다. 한 번 누를 때 큐에 몇 개 넣을지 정합니다.
*[Batch Size]: 한 번 실행할 때 만들 이미지 장수입니다. Empty Latent Image에서 지정합니다.
*[Auto Queue]: Run 버튼의 Run options에 있는 자동 반복 설정입니다.
*[Mask Editor]: ComfyUI 안에서 이미지 위에 마스크를 그리는 편집기입니다.
*[Subgraph]: 노드 여러 개를 노드 하나로 접는 기능입니다. 프론트엔드 1.24.3 이상에서 동작합니다.
*[Fit View]: 워크플로우 전체나 선택한 노드가 화면에 들어오도록 시야를 맞추는 기능입니다. 단축키는 마침표 키입니다.
*[Trigger Word]: 일부 LoRA가 학습 때 함께 쓴 단어입니다. 프롬프트에 적어야 화풍이 나타납니다.
*[Refiner]: 1단계 샘플링을 끊고 남은 구간을 다른 모델이나 conditioning으로 이어 마무리하는 구성입니다.
*[Inpainting]: 이미지의 일부 영역을 마스크로 지정해 그 부분만 다시 생성하는 작업입니다.
*[Outpainting]: 원본 이미지 바깥으로 화면을 넓혀 없던 영역을 새로 생성하는 작업입니다.
*[Upscale]: 생성된 이미지를 더 큰 해상도로 확대하는 작업입니다.
*[UNet]: Stable Diffusion(v1.5, XL)의 핵심 아키텍처입니다. 노이즈를 예측하고 제거합니다.
*[Embedding]: 텍스트나 이미지를 숫자의 나열(벡터)로 변환한 데이터입니다.
*[Inference]: 학습된 모델을 사용해 실제 결과물을 만들어내는 과정입니다.
*[T5XXL]: FLUX.1이 쓰는 텍스트 인코더입니다. 프롬프트를 큰 임베딩으로 바꿉니다.
*[sigma]: 각 denoising 단계에서 남아 있는 노이즈의 크기를 나타내는 값입니다.
*[timestep]: 모델을 학습할 때 노이즈 수준을 가리키는 시간 좌표입니다. ComfyUI의 Steps와 다릅니다.
*[seq_len]: 텍스트 인코더가 프롬프트를 토큰으로 나눴을 때의 토큰 개수입니다.
*[control_after_generate]: 한 장을 생성한 뒤 seed를 어떻게 바꿀지 정하는 KSampler의 위젯입니다.
*[strength_type]: StyleModelApply의 위젯입니다. multiply와 attn_bias 중에서 고릅니다.
*[ComfyUI-Manager]: 커스텀 노드를 설치·갱신·제거·비활성화하는 확장입니다.
*[Cancel current run]: 실행 중인 작업을 멈추는 버튼입니다. 단축키 Ctrl + Alt + Enter.
*[Queue Prompt]: Run 버튼의 예전 이름입니다.
*[Differential Diffusion]: 마스크의 밝기에 따라 픽셀마다 denoise 강도를 다르게 적용하는 기법입니다.
*[전처리기]: 입력 이미지를 ControlNet이 받는 형식으로 바꾸는 노드입니다.
*[양자화]: 모델 가중치를 더 적은 비트로 바꿔 저장하는 것입니다. 파일 크기와 VRAM 요구가 줄어듭니다.
*[미니맵]: 워크플로우 전체를 축소해 보여 주는 작은 지도입니다.
