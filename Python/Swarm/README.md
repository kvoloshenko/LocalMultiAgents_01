# 🤖 Fully Local Multi-Agent Swarm with LangGraph

## Пример мультиагентной системы Alice ↔ Bob на локальной модели Qwen3 (Ollama)

---

> Основано на курсе:  
> 📺 **“Fully Local Multi-Agent Systems with LangGraph”**  
> https://www.youtube.com/watch?v=4oC1ZKa9-Hs  
>  
> Конспект:  
> https://mirror-feeling-d80.notion.site/Fully-Local-Multi-Agent-1b5808527b178066bde0ed981b27998c

---

## 📘 Описание проекта

Этот пример демонстрирует, как создать **полностью локальную мультиагентную систему** типа **Swarm (Рой)** с двумя агентами:

- **Alice** — эксперт по сложению, использует инструмент `add(a, b)`.
- **Bob** — «пират», который сам не считает и передаёт математические задачи Alice.

Ключевые особенности:

- 🧠 **LangGraph Swarm** (`langgraph_swarm`) для роевой архитектуры.
- 🔄 **ReAct-агенты** с инструментами и механизмом **handoff** (передача управления).
- 🖥 **Локальная LLM** через **Ollama** (`qwen3:latest`).
- 🧠 **Память** диалога через `InMemorySaver` (checkpoint).
- 🖼 **Визуализация графа** (Mermaid → PNG).
- 🧩 **LangGraph Studio** (`langgraph dev`) для интерактивной отладки.
- 🐞 **LangSmith** (опционально) для трассировки.

---

## 🧩 Что такое Swarm

Swarm — это мультиагентная архитектура, где **нет единого центрального контроллера**.  
Каждый агент:

- может вызывать инструменты;
- может передавать управление другим агентам (handoff);
- участвует в общем диалоге.

Схема:

```mermaid
flowchart LR
    User --> Alice
    Alice -- handoff --> Bob
    Bob -- handoff --> Alice
    Alice --> User
````

В отличие от Supervisor:

* **Supervisor** = строгое централизованное управление.
* **Swarm** = распределённая, гибкая передача управления между агентами.

---

## 📂 Структура папки

```text
Python/Swarm
├─ swarm_flight_hotel.py
├─ Images
│  ├─ swarm_flight_hotel_graph.PNG
│  ├─ DeBug_01.png
│  ├─ DeBug_02.png
│  ├─ DeBug_03.png
│  └─ DeBug_04.png
└─ README.md
```

---

## 🔧 Краткий обзор кода (`swarm_flight_hotel.py`)

### Инициализация

```python
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent
from langgraph_swarm import create_handoff_tool, create_swarm

model = ChatOllama(model="qwen3:latest")
checkpointer = InMemorySaver()
```

### Инструмент

```python
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b
```

### Агент Alice

```python
alice = create_react_agent(
    model,
    [
        add,
        create_handoff_tool(agent_name="Bob")
    ],
    prompt="You are Alice, an addition expert.",
    name="Alice",
)
```

* знает, как складывать числа;
* может передать управление Bob.

### Агент Bob

```python
bob = create_react_agent(
    model,
    [
        create_handoff_tool(
            agent_name="Alice",
            description="Transfer to Alice, she can help with math"
        )
    ],
    prompt="You are Bob, you speak like a pirate.",
    name="Bob",
)
```

* говорит как пират;
* не решает математику сам, а передаёт задачи Alice.

### Создание Swarm

```python
workflow = create_swarm(
    [alice, bob],
    default_active_agent="Alice"
)

app = workflow.compile(checkpointer=checkpointer)
```

### Визуализация графа

```python
graph_bytes = app.get_graph().draw_mermaid_png()
image = PILImage.open(BytesIO(graph_bytes))
image.show()
```

### Диалог в одной сессии (`thread_id`)

```python
config = {"configurable": {"thread_id": "1"}}

turn_1 = app.invoke(
    {"messages": [{"role": "user", "content": "i'd like to speak to Bob"}]},
    config,
)
print(turn_1)

turn_2 = app.invoke(
    {"messages": [{"role": "user", "content": "what's 5 + 7?"}]},
    config,
)
print(turn_2)
```

---

## 💬 Как работает диалог

### Шаг 1

Пользователь:

> "i'd like to speak to Bob"

* Активный агент по умолчанию: **Alice**
* Alice вызывает `handoff` → управление переходит к Bob.
* Теперь активный агент: **Bob**

### Шаг 2

Пользователь:

> "what's 5 + 7?"

* Активный агент: Bob
* Bob понимает, что не умеет считать → вызывает `handoff` к Alice.
* Alice:

  * вызывает инструмент `add(5, 7)`;
  * возвращает результат (**12**) пользователю.

Благодаря `thread_id="1"` состояние диалога (кто активен, история сообщений) сохраняется между вызовами `app.invoke`.

---

## 🧠 Память (Memory) в Swarm

В этом примере используется:

```python
checkpointer = InMemorySaver()
app = workflow.compile(checkpointer=checkpointer)
```

* `InMemorySaver` — хранит состояние (включая активного агента) в оперативной памяти.
* Один и тот же `thread_id` обеспечивает **multi-turn диалог** с сохранением контекста.

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
pip install langgraph-swarm langchain-ollama pillow python-dotenv
```

---

## 🚀 Запуск проекта

### Шаг 1. Активировать виртуальное окружение (Windows)

```bash
cd C:\_AI\LocalMultiAgents_01\venv\Scripts
activate
cd ..\..
```

### Шаг 2. Перейти в папку Swarm и запустить пример

```bash
cd Python\Swarm

python.exe swarm_flight_hotel.py
```

После этого:

* откроется PNG с графом агентов (Alice ↔ Bob);
* в консоль будут выведены результаты `turn_1` и `turn_2`.

Скриншоты:
![swarm_flight_hotel_graph.PNG](Images/swarm_flight_hotel_graph.PNG)

![DeBug_01.png](Images/DeBug_01.png)

![DeBug_02.png](Images/DeBug_02.png)

![DeBug_03.png](Images/DeBug_03.png)

![DeBug_04.png](Images/DeBug_04.png)

---

## 🧩 LangGraph Studio

Для визуальной работы с графом:

```bash
langgraph dev
```

* Откроется интерфейс по адресу `http://localhost:8123`
* Можно:

  * просматривать граф;
  * запускать и отлаживать сценарии Swarm;
  * анализировать шаги и сообщения.

---

## 🐞 Отладка через LangSmith (опционально)

Добавьте в `.env`:

```env
LANGCHAIN_TRACING_V2=true
LANGSMITH_API_KEY=...
LANGCHAIN_PROJECT="AliceBobSwarm"
```

После этого:

* все вызовы `app.invoke` будут логироваться в LangSmith;
* можно подробно анализировать handoff и работу агентов.

---

## 📚 Полезные ресурсы

* LangGraph Swarm: [https://github.com/langchain-ai/langgraph-swarm-py](https://github.com/langchain-ai/langgraph-swarm-py)
* LangGraph Supervisor: [https://github.com/langchain-ai/langgraph-supervisor-py](https://github.com/langchain-ai/langgraph-supervisor-py)
* Документация по multi-agent: [https://langchain-ai.github.io/langgraph/concepts/multi_agent](https://langchain-ai.github.io/langgraph/concepts/multi_agent)
* Видео-курс: [https://www.youtube.com/watch?v=4oC1ZKa9-Hs](https://www.youtube.com/watch?v=4oC1ZKa9-Hs)
* Конспект: [https://mirror-feeling-d80.notion.site/Fully-Local-Multi-Agent-1b5808527b178066bde0ed981b27998c](https://mirror-feeling-d80.notion.site/Fully-Local-Multi-Agent-1b5808527b178066bde0ed981b27998c)

---

## 🎯 Итоги

Этот пример — отличный старт для:

* изучения **роевых мультиагентных систем**;
* экспериментов с **локальными моделями** через Ollama;
* построения гибких AI-сценариев, где несколько агентов динамически делят между собой задачи.