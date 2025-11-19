# 🧠 Fully Local Multi-Agent System (Supervisor) на Qwen3 + LangGraph

**Supervisor — строгий контроль над мультиагентной системой**

---

> Основано на материале:  
> 🎥 “Fully Local Multi-Agent Systems with LangGraph” — https://www.youtube.com/watch?v=4oC1ZKa9-Hs  
> 📘 LangGraph Swarm: https://github.com/langchain-ai/langgraph-swarm-py  
> 📘 LangGraph Supervisor: https://github.com/langchain-ai/langgraph-supervisor-py  
> 📝 Конспект: https://mirror-feeling-d80.notion.site/...

---

## 📌 Описание проекта

Этот пример демонстрирует, как построить **локальную мультиагентную систему** с архитектурой **Supervisor**, используя:

- 🧠 **Ollama** (локальная LLM `qwen3:latest`)
- 🧩 **LangGraph Supervisor** (`langgraph_supervisor`)
- 🔄 **ReAct-агентов** с инструментами
- 🖼 **Визуализацию графа** (Mermaid → PNG через Pillow)
- 🧪 **Интеграцию с LangSmith** (опционально)

В системе есть два агента и Supervisor:

1. **research_agent**
   - выполняет имитацию поиска в интернете;
   - через инструмент `web_search(query)` возвращает данные о компаниях.

2. **math_agent**
   - решает математические задачи;
   - через инструменты:
     - `add(a, b)`
     - `multiply(a, b)`

**Supervisor** решает:

- если запрос связан с фактами / данными → отправить в `research_agent`;
- если запрос связан с вычислением → отправить в `math_agent`.

🎯 Пример задачи:

> "What’s the combined headcount of the FAANG companies in 2024?"

Supervisor → research_agent (`web_search`) → Supervisor → math_agent (`add`) → итоговая сумма.

---

## 🧠 Что даёт архитектура Supervisor

Когда одна LLM делает всё:

- она может вызвать неправильный инструмент;
- «забыть» контекст;
- запутаться в шагах рассуждений.

Решение — **разделить ответственность**:

- `research_agent` отвечает за поиск и текстовые факты;
- `math_agent` отвечает за арифметику;
- **Supervisor** управляет **кто, когда и что делает**.

---

## 🧩 Архитектура Supervisor

```mermaid
flowchart TD
    U([Пользователь]) --> S["Supervisor (LLM)"]
    S --> A1["Research Agent"]
    S --> A2["Math Agent"]
    A1 --> S
    A2 --> S
    S --> U
````

✔ строгий контроль
✔ понятная маршрутизация запросов
✔ подходит для бизнес-систем и продакшн-сценариев

---

## 📂 Структура папки

```text
Python/Supervisor
├─ supervisor_math_research.py
├─ Images
│  ├─ graph.png
│  ├─ DeBug_01.png
│  ├─ LangGraphStudio_01.png
│  └─ LangGraphStudio_02.png
└─ README.md
```

---

## 🔧 Краткий обзор кода

### Инициализация модели

```python
from langchain_ollama import ChatOllama
model = ChatOllama(model="qwen3:latest")
```

### Инструменты

```python
def add(a: float, b: float) -> float: ...
def multiply(a: float, b: float) -> float: ...
def web_search(query: str) -> str: ...
```

`web_search` имитирует реальный веб-поиск и возвращает подготовленный текст про FAANG.

### Агенты

```python
from langgraph.prebuilt import create_react_agent

math_agent = create_react_agent(
    model=model,
    tools=[add, multiply],
    name="math_expert",
    prompt="You are a math expert. Always use one tool at a time."
)

research_agent = create_react_agent(
    model=model,
    tools=[web_search],
    name="research_expert",
    prompt="You are a world class researcher with access to web search. Do not do any math."
)
```

### Supervisor

```python
from langgraph_supervisor import create_supervisor

workflow = create_supervisor(
    [research_agent, math_agent],
    model=model,
    prompt=(
        "You are a team Supervisor managing a research expert and a math expert. "
        "For current events, use research_agent. "
        "For math problems, use math_agent."
    )
)

app = workflow.compile()
```

### Визуализация графа

```python
graph_bytes = app.get_graph().draw_mermaid_png()
image = PILImage.open(BytesIO(graph_bytes))
image.show()
```

### Вызов системы

```python
result = app.invoke({
    "messages": [
        {"role": "user", "content": "what's the combined headcount of the FAANG companies in 2024?"}
    ]
})

for m in result["messages"]:
    m.pretty_print()
```

---

## 📦 Требования и установка

### 1. Системные требования

* Python **3.11**
* Установленный **Ollama**
* Локальная модель:

```bash
ollama pull qwen3:latest
```

### 2. Установка зависимостей

(из корня репозитория)

```bash
cd C:\_AI\LocalMultiAgents_01

pip install -r requirements.txt
pip install -U "langgraph-cli[inmem]"
pip install python-dotenv pillow
```

---

## 🚀 Запуск проекта

### Шаг 1. Активация виртуального окружения (Windows)

```bash
cd C:\_AI\LocalMultiAgents_01\venv\Scripts
activate
cd ..\..
```

### Шаг 2. Переход в папку Supervisor и запуск

```bash
cd Python\Supervisor

python.exe supervisor_math_research.py
```

После запуска:

* откроется PNG с графом агентов;
* в консоль выведется детальный диалог (включая tool-calls).

---

## 🧪 LangGraph Studio

Для визуальной отладки мультиагентного графа:

```bash
langgraph dev
```

Features:

* визуальный граф агентов и переходов;
* наблюдение за сообщениями и состояниями;
* ручной запуск и отладка сценариев.

---

## 🐞 Отладка через LangSmith (опционально)

В `.env` можно указать:

```env
LANGSMITH_API_KEY=...
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=multi-agent-supervisor-demo
```

После этого:

* все шаги выполнения будут доступны в веб-интерфейсе LangSmith;
* можно видеть цепочку вызовов Supervisor → Agents → Tools.

Пример ссылки (шаблон):

* [https://smith.langchain.com/](https://smith.langchain.com/)...

Скриншоты:

![graph.png](Images/graph.png)

![DeBug_01.png](Images/DeBug_01.png)

![LangGraphStudio_01.png](Images/LangGraphStudio_01.png)

![LangGraphStudio_02.png](Images/LangGraphStudio_02.png)

---

## 🎯 Итоги

Этот пример показывает:

* как создать двух агентов с разными ролями;
* как управлять ими через Supervisor;
* как использовать локальные модели (Qwen3) через Ollama;
* как визуализировать и отлаживать мультиагентный граф (LangGraph Studio + LangSmith).

Это хороший шаблон для **продакшн-ориентированных** мультиагентных систем с жёстким контролем маршрутизации.