#  Карта технологий


```mermaid
flowchart LR

    %% === STYLES ===
    classDef main fill:#e3f2fd,stroke:#1e88e5,stroke-width:2px,color:#0d47a1;
    classDef branch fill:#e8f5e9,stroke:#43a047,stroke-width:1.5px;
    classDef tech fill:#fff8e1,stroke:#f9a825;
    classDef current fill:#ffe0b2,stroke:#e65100,stroke-width:2px,color:#bf360c;

    %% === Level 0 ===
    U([Пользователь])

    %% === Level 1 ===
    U -- "периодические<br/>задачи" --> W["Использование web-чатов"]
    U -- "повторяемые<br/>однотипные задачи" --> A["Автоматизация AI Agents"]

    %% === Level 2A — Web Chats ===
    W --> W1["ChatGPT"]
    W --> W2["DeepSeek"]
    W --> W3["Qwen (online)"]
    W --> W4["Claude"]
    W --> W5["Gemini"]
    W --> W6["Llama Web UI"]

    %% === Level 2B — Автоматизация ===
    A --> ZC["ZeroCode"]
    A --> PR["Программирование"]

    %% === Level 3A — ZeroCode ===
    ZC --> Z1["Make / Zapier"]
    ZC --> Z2["Flowise / Dify"]
    ZC --> Z3["n8n"]
    ZC --> Z4["No-code AI Tools"]

    %% === Level 3B — Programming ===
    PR --> P1["Без framework"]
    PR --> P2["Использование framework"]

    %% === Level 4A — Without Framework ===
    P1 --> NF1["Python + API LLM"]
    P1 --> NF2["Скрипты вокруг Ollama"]
    P1 --> NF3["Самописные state-machine"]

    %% === Level 4B — Frameworks ===
    P2 --> FG1["LangGraph"]
    P2 --> FG2["CrewAI"]
    P2 --> FG3["Autogen"]

    %% === APPLY STYLES ===
    class U main
    class W,A branch
    class ZC,PR branch
    class P1,P2 branch

    class W1,W2,W3,W4,W5,W6 tech
    class Z1,Z2,Z3,Z4 tech
    class NF1,NF2,NF3 tech
    class FG1,FG2,FG3 tech

    %% Highlight current-focus nodes
    class PR,P2,FG1 current

````