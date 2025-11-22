#  Карта технологий


```mermaid
flowchart LR

    %% --- Level 0 ---
    U([Пользователь])

    %% --- Level 1: две дороги ---
    U --> W["Использование web-чатов"]
    U --> A["Автоматизация"]

    %% --- Level 2A: Использование web-чатов ---
    W --> W1["ChatGPT"]
    W --> W2["DeepSeek"]
    W --> W3["Qwen (online)"]
    W --> W4["Claude"]
    W --> W5["Gemini"]
    W --> W6["Llama Web UI"]

    %% --- Level 2B: Автоматизация ---
    A --> ZC["ZeroCode"]
    A --> PR["Программирование"]

    %% --- Level 3A: ZeroCode ---
    ZC --> Z1["Make / Zapier"]
    ZC --> Z2["Flowise / Dify"]
    ZC --> Z3["n8n"]
    ZC --> Z4["No-code AI Tools"]

    %% --- Level 3B: Программирование ---
    PR --> P1["Без framework"]
    PR --> P2["Использование framework"]

    %% --- Level 4A: Без framework ---
    P1 --> NF1["Python + API LLM"]
    P1 --> NF2["Скрипты вокруг Ollama"]
    P1 --> NF3["Самописные state-machine"]

    %% --- Level 4B: Framework пути ---
    P2 --> FG1["LangGraph"]
    P2 --> FG2["CrewAI"]
    P2 --> FG3["Autogen"]

    %% --- Styling ---
    classDef main fill:#e3f2fd,stroke:#1e88e5,stroke-width:2px,color:#0d47a1;
    classDef branch fill:#e8f5e9,stroke:#43a047,stroke-width:1.5px;
    classDef tech fill:#fff8e1,stroke:#f9a825;

    class U main
    class W,A branch
    class ZC,PR branch
    class P1,P2 branch

    class W1,W2,W3,W4,W5,W6 tech
    class Z1,Z2,Z3,Z4 tech
    class NF1,NF2,NF3 tech
    class FG1,FG2,FG3 tech

````