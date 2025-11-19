# ============================
# Импорт стандартных библиотек
# ============================

from io import BytesIO              # Для работы с байтовыми потоками (загрузка изображения графа)
from PIL import Image as PILImage   # Для отображения изображений (графа агента)
import os                           # Для доступа к переменным окружения
from dotenv import load_dotenv      # Для загрузки переменных окружения из .env

# ===================================================
# Импорт компонентов из LangChain / LangGraph / Ollama
# ===================================================

from langchain_ollama import ChatOllama          # Интерфейс взаимодействия с локальными LLM (Ollama)
from langgraph_supervisor import create_supervisor  # Создание супервизора агентов
from langgraph.prebuilt import create_react_agent   # Готовый ReAct-агент
# from langgraph_supervisor import create_supervisor  # Создание супервизора агентов
# from langchain.agents import create_agent           # Новый агент на базе LangChain/LangGraph


# ============================================================
# Загрузка переменных окружения (например, ключей LangSmith)
# ============================================================

load_dotenv()  # Загружаем значения из файла .env

# Считываем переменные окружения, если они нужны для трассировки/логирования
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")

# ====================================================
# Инициализация локальной языковой модели через Ollama
# ====================================================

# Старая модель (пример) была бы такой:
# model = ChatOllama(model="qwen2.5:7b-instruct")

# Используем актуальную модель qwen3:latest
model = ChatOllama(model="qwen3:latest")

# ===========================================================
# Создание инструментов (tools) — функций, доступных агентам
# ===========================================================

def add(a: float, b: float) -> float:
    """Сложение двух чисел. Возвращает сумму a + b."""
    return a + b


def multiply(a: float, b: float) -> float:
    """Умножение двух чисел. Возвращает результат a * b."""
    return a * b


def web_search(query: str) -> str:
    """
    Имитация веб-поиска.
    В реальном проекте здесь был бы вызов реального API поиска (Google/Bing/другое).
    Возвращает заранее подготовленные данные — численность сотрудников FAANG в 2024 году.
    """
    return (
        "Here are the headcounts for each of the FAANG companies in 2024:\n"
        "1. **Facebook (Meta)**: 67,317 employees.\n"
        "2. **Apple**: 164,000 employees.\n"
        "3. **Amazon**: 1,551,000 employees.\n"
        "4. **Netflix**: 14,000 employees.\n"
        "5. **Google (Alphabet)**: 181,269 employees."
    )

# =============================================
# Создаём ReAct-агента для математических задач
# =============================================

math_agent = create_react_agent(
    model=model,              # LLM, управляющая агентом
    tools=[add, multiply],    # Инструменты: сложение и умножение
    name="math_expert",       # Имя агента
    prompt="You are a math expert. Always use one tool at a time."  # Системный промт
)

# math_agent = create_agent(
#     model=model,              # LLM, управляющая агентом
#     tools=[add, multiply],    # Инструменты: сложение и умножение
#     name="math_expert",       # Имя агента
#     system_prompt="You are a math expert. Always use one tool at a time."  # Системный промт
# )

# ======================================================
# Создаём ReAct-агента для исследовательских запросов
# ======================================================

research_agent = create_react_agent(
    model=model,
    tools=[web_search],       # Инструмент: поиск в интернете (симуляция)
    name="research_expert",
    prompt="You are a world class researcher with access to web search. Do not do any math."
)

# research_agent = create_agent(
#     model=model,
#     tools=[web_search],       # Инструмент: поиск в интернете (симуляция)
#     name="research_expert",
#     system_prompt="You are a world class researcher with access to web search. Do not do any math."
# )

# ==================================================
# Создание супервизора, который управляет агентами
# ==================================================

workflow = create_supervisor(
    [research_agent, math_agent],     # Супервизор может выбирать между этими агентами
    model=model,                      # LLM, принимающая решения супервизора
    prompt=(
        "You are a team Supervisor managing a research expert and a math expert. "
        "For current events, use research_agent. "
        "For math problems, use math_agent."
    )
)

# ============================================
# Компиляция workflow в исполняемый граф
# ============================================

app = workflow.compile()

# ================================================================
# Визуализация графа агентов — строим PNG с помощью Mermaid
# ================================================================

graph_bytes = app.get_graph().draw_mermaid_png()  # Получаем байтовый PNG графа
image = PILImage.open(BytesIO(graph_bytes))        # Загружаем изображение в PIL
image.show()                                       # Показываем в стандартном просмотрщике

# =====================================================
# Отправляем запрос в многоагентную систему (workflow)
# =====================================================

result = app.invoke({
    "messages": [
        {
            "role": "user",
            "content": "what's the combined headcount of the FAANG companies in 2024?"
        }
    ]
})

# ============================================================
# Выводим весь диалог (включая действия инструментов агентов)
# ============================================================

for m in result['messages']:
    m.pretty_print()  # Удобный формат вывода
