[문서 지도](../../README.md)

# Sampler와 Scheduler 비교

> 같은 모델과 프롬프트에서도 Sampler와 Scheduler에 따라 결과가 달라집니다. 이름을 외우는 대신 두 설정을 분리해 비교합니다.

## 이 장에서 배우는 것

- Sampler와 Scheduler는 ComfyUI에서 별개 항목입니다. 다른 도구의 `DPM++ 2M Karras`는 두 값을 붙인 표기입니다.
- 절대적인 품질 순위는 없습니다. 조건을 고정하고 한 항목씩 바꿔 직접 비교해야 합니다.

<div class="guide-meta" markdown>
**대상** 어떤 Sampler를 선택해야 할지 고민하는 입문자 · **사전 이해** KSampler 노드를 한 번 이상 실행해 본 사용자 · **시간** 15분

**이럴 때 읽으세요** 목록에 있는 이름이 너무 많아 무엇을 골라야 할지 모를 때.
</div>

## 먼저 구분할 것

- **Sampler:** 각 노이즈 수준에서 latent를 다음 상태로 갱신하는 수치 해법
- **Scheduler:** 전체 steps에 노이즈 수준, 즉 sigma를 어떻게 배치할지 정하는 규칙

ComfyUI의 KSampler에서는 `sampler_name`과 `scheduler`가 별도 항목입니다. 예를 들어 다른 도구의 `DPM++ 2M Karras`라는 표기는 ComfyUI에서 다음처럼 나눕니다.

```text
sampler_name: dpmpp_2m
scheduler: karras
```

## 주요 Sampler의 성향

아래 내용은 선택을 시작하기 위한 경향입니다. 모델, steps, scheduler, 해상도에 따라 결과가 달라지므로 절대적인 품질 순위로 사용하지 않습니다.

| UI 값 | 특징 | 비교할 때 볼 점 |
|---|---|---|
| `euler` | 단순하고 빠른 기준선 | 적은 steps에서 형태와 디테일 |
| `euler_ancestral` | 각 단계에 확률적 성분을 사용하는 ancestral 방식 | 질감 변화와 steps 증가 시 결과 변화 |
| `heun` | 예측과 보정을 사용하는 방식 | 추가 모델 호출에 비해 경계와 질감이 나아지는지 |
| `dpmpp_2m` | 이전 단계 정보를 활용하는 다단계 방식 | 중간 steps에서 세부 묘사와 안정성 |
| `ddim` | DDIM 갱신 규칙 | 기준 환경에서의 형태 유지와 속도 |

`heun`처럼 한 step에 모델을 두 번 호출할 수 있는 방식은 같은 steps라도 실행 시간이 더 길 수 있습니다. 따라서 steps 숫자만 보고 속도를 비교하지 않습니다.

## Scheduler의 역할

| UI 값 | 특징 | 확인할 점 |
|---|---|---|
| `normal` | 모델이 사용하는 기본 노이즈 구간을 steps에 배치 | 첫 기준선으로 사용하기 쉬움 |
| `karras` | Karras 방식으로 sigma를 배치 | 같은 sampler·steps에서 디테일과 대비 변화 |
| `exponential` | sigma를 지수적으로 배치 | 중간·후반 단계의 변화 |

지원되는 scheduler와 권장 조합은 모델 및 ComfyUI 버전에 따라 달라질 수 있습니다. 목록에 보이지 않는 값을 문서만 보고 넣지 말고 현재 UI에서 고를 수 있는 값을 사용합니다.

## 입문용 비교 실습

먼저 기준 결과를 하나 만듭니다.

```yaml
seed: 123456
control_after_generate: fixed
steps: 25
cfg: 6.0
sampler_name: euler
scheduler: normal
denoise: 1.0
```

그다음 한 번에 하나만 바꿉니다.

1. 모델·VAE·프롬프트·Seed·해상도·Steps·CFG를 고정합니다.
2. `sampler_name`만 `euler`, `heun`, `dpmpp_2m`으로 바꿉니다.
3. 가장 살펴볼 가치가 있는 sampler 하나를 고릅니다.
4. 그 sampler를 고정하고 `scheduler`만 `normal`, `karras`로 바꿉니다.
5. 실행 시간, 전체 구도, 경계, 작은 질감, 프롬프트 반영을 기록합니다.

| 실험 | sampler_name | scheduler | 기록할 내용 |
|---|---|---|---|
| 기준 | `euler` | `normal` | 실행 시간·구도·세부 묘사 |
| A | `heun` | `normal` | 기준 대비 개선과 시간 증가 |
| B | `dpmpp_2m` | `normal` | 형태와 질감 변화 |
| C | 선택한 sampler | `karras` | scheduler만 바꾼 차이 |

실제 실행 결과를 기록하지 않은 상태에서 특정 조합을 “가장 좋다”고 결론내리지 않습니다.

## 자주 생기는 혼동

| 혼동 | 확인 방법 |
|---|---|
| `dpmpp_2m_karras`를 sampler 값에서 찾음 | `dpmpp_2m`과 `karras`를 두 항목에 나누어 선택 |
| steps가 같으니 속도도 같다고 생각함 | sampler별 모델 호출 횟수와 실제 실행 시간 비교 |
| steps를 늘리면 항상 좋아진다고 생각함 | 고정 Seed로 20·25·30 steps를 비교하고 개선이 멈추는 지점 확인 |
| 같은 Seed면 모든 환경에서 픽셀까지 같다고 생각함 | 모델 파일, 정밀도, 장치, 라이브러리와 ComfyUI 버전까지 기록 |
| sampler를 바꾸면서 scheduler도 함께 바꿈 | 원인을 구분할 수 있도록 한 번에 하나만 변경 |

## Q&A 점검

**Q. 입문자는 어떤 조합으로 시작하면 되나요?**  
A. 설치한 모델의 공식 워크플로우가 있으면 그 설정을 우선합니다. 별도 권장이 없으면 현재 UI에서 지원되는 `euler + normal`을 기준선으로 만들고 한 항목씩 비교하세요.

**Q. `dpmpp_2m + karras`가 항상 더 좋은가요?**  
A. 아닙니다. 프롬프트, 모델, 해상도, steps에 따라 선호가 달라집니다. 고정 조건 비교 결과로 선택해야 합니다.

**Q. 같은 Seed로 DDIM을 사용하면 어떤 컴퓨터에서도 완전히 같은가요?**  
A. 보장할 수 없습니다. 같은 환경에서는 재현성이 높지만 장치, 정밀도, 최적화, 라이브러리 버전과 비결정적 연산이 결과에 영향을 줄 수 있습니다.

**Q. KSamplerAdvanced나 SamplerCustomAdvanced가 품질을 자동으로 높이나요?**  
A. 아닙니다. 두 노드는 구간이나 구성 요소를 더 세밀하게 제어합니다. 같은 sampler와 schedule이면 노드 이름 자체가 품질을 높이지 않습니다.

## 완료 기준

네 가지를 모두 만족했다면 이 장을 끝냈습니다.

- Sampler와 Scheduler가 각각 무엇을 정하는지 구분할 수 있다.
- `euler + normal` 기준 결과를 만들고 sampler만 바꿔 비교했다.
- 그다음 sampler를 고정하고 scheduler만 바꿔 비교했다.
- steps가 같아도 sampler에 따라 실행 시간이 다를 수 있다는 점을 안다.

## 다음 단계

- [KSampler·KSamplerAdvanced·SamplerCustomAdvanced](ksampler-vs-advanced.md) — 노드별 입력과 구간 제어
- [디노이징 프로세스](../../01-core-concepts/denoising-process.md) — 학습 timestep, 추론 step, sigma 구분
- [워크플로우 이해하기](../../00-getting-started/workflow-basics.md) — 설정값의 의미

---

[문서 지도](../../README.md)
