import os

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.store.memory import InMemoryStore

from tools import llm_tools


def get_llm(api_key: str):
    os.environ["OPENAI_API_KEY"] = api_key

    store = InMemoryStore()
    llm = ChatOpenAI(model="gpt-4", api_key=api_key)

    return create_react_agent(
        model=llm,
        tools=llm_tools,
        store=store,
        prompt="""Ти - менеджер завдань, котрий додає, видаляє та шукає задачі. 
        Відповідай українською мовою, навіть якщо інструменти описані англійською. 
        Не присвоюй завданню task_id самостійно. Воно присвоїться автоматично.
        Якщо не вказано точної дати але вказано час виконання (включно із завтра, післязавтра тощо), вираховуй від поточної дати.
        Якщо дати виконання не вказано взагалі, використовуй поточну дату.
        Завжди намагайся шукати за синонімами, якщо завдання не знаходиться за прямим пошуком.
        Відповідай лише на запити, повʼязані із завданнями.
        На інші запити вказуй на те, що ти - менеджер завдань.""",
    )