[홈](../README.md) · [시작하기](README.md) · [이전: 노드 다루기](node-basics.md) · [다음: 워크플로우 이해](workflow-basics.md)

# 실행과 중단

> 워크플로우를 큐에 넣어 실행하고, 도중에 멈추고, 쌓인 작업을 확인합니다.

## 이 장에서 배우는 것

- 실행은 즉시 시작되는 것이 아니라 큐(대기열)에 들어갑니다. 여러 번 눌러 여러 작업을 쌓아 둘 수 있습니다.
- 실행 중인 작업은 `Cancel current run`으로 멈춥니다.
- 값을 바꿔 가며 연속으로 큐에 넣으면 비교할 결과를 순서대로 만들 수 있습니다.

<div class="guide-meta" markdown>
**대상** [노드 다루기](node-basics.md)까지 마친 사용자 · **사전 이해** [빠른 시작](quick-start.md)의 7노드 워크플로우 · **시간** 10분

**이럴 때 읽으세요** 실행이 오래 걸려 멈추고 싶을 때, 또는 값을 바꾼 여러 결과를 연속으로 만들고 싶을 때.
</div>

## 1. 실행

화면 우측 상단이 실행·큐 제어 영역입니다.

| 조작 | 동작 |
|---|---|
| `Run` 버튼 클릭 | 현재 워크플로우를 큐에 넣습니다 |
| `Ctrl + Enter` (macOS `⌘ + Enter`) | 위와 같습니다 |
| `Ctrl + Shift + Enter` (macOS `⌘ + Shift + Enter`) | 큐의 맨 앞에 넣습니다. 대기 중인 작업보다 먼저 실행됩니다 |
| `Shift` + `Run` 버튼 클릭 | 위와 같습니다. 버튼 설명에 `Run workflow (Shift to queue at front)`로 표시됩니다 |

예전 버전과 바깥 자료는 이 버튼을 `Queue Prompt`로 부릅니다. 현재 화면 표기는 `Run`입니다.

### 반복 횟수 — `Batch Count`

`Run` 버튼 옆의 숫자가 `Batch Count`입니다. 이 수만큼 같은 워크플로우가 큐에 들어갑니다. 한 번에 넣을 수 있는 최대값은 `Settings → Queue Button → Batch count limit`이고 기본값은 100입니다.

KSampler의 `control_after_generate`가 `randomize`이면 회차마다 Seed가 바뀝니다. `fixed`이면 같은 조건으로 반복합니다.

### 자동 반복 — `Auto Queue`

`Run` 버튼 안의 `˅`(`Run options`)를 열면 `Auto Queue` 세 가지가 나옵니다.

| 값 | 동작 |
|---|---|
| `Disabled` | 자동으로 큐에 넣지 않습니다 |
| `Instant` | 생성이 끝나면 곧바로 다시 큐에 넣습니다 |
| `On Change` | 값을 바꾸면 그때 큐에 넣습니다 |

`On Change`는 값을 고치는 시점에 실행을 시작합니다. 값 하나만 바꿔 비교할 때는 `Disabled`로 두고 직접 누릅니다. 바꾼 값이 맞는지 확인한 뒤에 실행됩니다.

### 실행되는 범위

실행을 누르면 ComfyUI가 출력 노드에서 거꾸로 필요한 노드만 골라 실행합니다. 앞선 실행에서 입력과 위젯 값이 바뀌지 않은 노드는 저장해 둔 결과를 사용합니다. 값을 하나도 바꾸지 않고 두 번 실행하면 두 번째는 샘플링을 건너뛰고 `Save Image`만 실행됩니다.

## 2. 중단

실행 중에는 실행 영역의 버튼이 중단 버튼으로 바뀝니다. 버튼 설명에 `Cancel current run`으로 표시되며, 단축키는 `Ctrl + Alt + Enter`(macOS `⌘ + Alt + Enter`)입니다. 둘 다 지금 실행 중인 작업 하나를 멈춥니다.

`Auto Queue`를 `Instant`로 두고 실행 중이면 버튼이 `Stop Run (Instant)`으로 표시됩니다. 이 버튼을 누르면 자동 반복이 멈춥니다.

멈춘 시점까지 계산한 Latent는 이미지로 저장되지 않습니다. 중간 결과를 보려면 다시 실행해야 합니다.

## 3. 큐 확인

`Q`를 누르면 큐 사이드바가 열리고, 다시 누르면 닫힙니다. 대기 중인 작업과 실행이 끝난 기록이 여기에 나옵니다.

| 대상 | 조작 |
|---|---|
| 대기 중인 작업 하나 | 그 항목의 `Cancel job` |
| 대기 중인 작업 전체 | `Clear queue` |

기록을 몇 개까지 남길지는 `Settings → Queue → Queue history size`에서 정합니다. 기본값은 100이고, 값을 키우면 페이지를 열 때 메모리를 더 사용합니다.

어떤 값으로 만든 결과인지는 큐 목록에 남지 않습니다. 기록을 남기는 방법은 [저장과 재현](save-and-reproduce.md)에 있습니다.

## 4. 한 변수 실험 — 큐에 쌓아 비교하기

[빠른 시작](quick-start.md)에서 만든 워크플로우를 엽니다. KSampler의 `control_after_generate`를 `fixed`로 두고 Seed를 고정합니다.

`cfg`만 바꿔 가며 세 번 실행합니다.

| 순서 | 조작 | 큐 상태 |
|---|---|---|
| 1 | `cfg`를 6으로 두고 `Ctrl + Enter` | 작업 1개 |
| 2 | `cfg`를 7로 바꾸고 `Ctrl + Enter` | 작업 2개 |
| 3 | `cfg`를 8로 바꾸고 `Ctrl + Enter` | 작업 3개 |

세 작업이 순서대로 실행됩니다. 실행이 끝나기를 기다렸다가 값을 바꿀 필요가 없습니다. 큐에 넣은 시점의 값이 각 작업에 기록되기 때문입니다.

!!! question "관찰 질문"
    2번을 큐에 넣은 직후 `cfg`를 8로 바꿨습니다. 2번 작업은 어떤 값으로 실행되나요?

## 5. 문제 해결

| 증상 | 확인 순서 |
|---|---|
| `Run`을 눌러도 실행되지 않음 | 빨간 테두리 노드나 빈 입력이 있는지 확인. [빠른 시작](quick-start.md)의 문제 해결 표 참조 |
| 중단했는데 이미지가 남지 않음 | 중단한 실행은 저장 단계까지 가지 않습니다. 처음부터 다시 실행합니다 |
| 세 번 실행했는데 결과가 모두 다름 | `control_after_generate`가 `randomize`이면 Seed가 매번 바뀝니다. `fixed`로 바꿉니다 |
| 두 번째 실행이 너무 빨리 끝남 | 값이 바뀌지 않은 노드는 다시 계산하지 않습니다. 바꾼 값이 실제로 들어갔는지 확인 |
| 멈췄는데 계속 실행됨 | `Auto Queue`가 `Instant`나 `On Change`인지 확인. `Disabled`로 바꿉니다 |
| 한 번 눌렀는데 여러 장이 나옴 | `Run` 버튼 옆 `Batch Count`가 1인지 확인 |
| 단축키가 동작하지 않음 | `Settings → Keybinding`에서 현재 값을 확인 |

## 완료 기준

네 가지를 모두 만족했다면 이 장을 끝냈습니다.

- `Run` 버튼과 `Ctrl + Enter`로 각각 실행해 봤다.
- 실행 중인 작업을 `Cancel current run`으로 멈춰 봤다.
- `Q`로 큐 사이드바를 열어 대기 목록과 기록을 확인했다.
- Seed를 고정하고 `cfg`만 바꾼 세 작업을 큐에 쌓아 결과를 비교했다.

## 다음 단계

- [워크플로우 이해하기](workflow-basics.md) — 각 노드와 설정값의 의미
- [저장과 재현](save-and-reproduce.md) — 어떤 값으로 만든 결과인지 남기는 방법
- [용어 사전](../GLOSSARY.md) — Run·큐·Seed의 정의

---

[홈](../README.md) · [시작하기](README.md) · [이전: 노드 다루기](node-basics.md) · [다음: 워크플로우 이해](workflow-basics.md)
