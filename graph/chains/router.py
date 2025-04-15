# Buradaki Amaç: Kullanıcının sorduğu soruyu analiz edip şu iki seçenekten birine yönlendirir:
# "vectorstore" → Mevcut vektör veritabanından bilgi çek (RAG yapısı).
# "websearch" → Cevap için internette araştırma yap.

from typing import Literal

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI


class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""

    datasource: Literal["vectorstore", "websearch"] = Field(
        ...,
        description="Given a user question choose to route it to web search or a vectorstore.",
    )

# Neden Literal: LLM bazen "VectorStore", "Web Search" gibi format dışı şeyler dönebilir.
# Literal sayesinde bu tarz cevaplar geçersiz sayılır.
# burada amacı -> "vectorstore" ya da "websearch" dışında bir şey gelmesin

llm = ChatOpenAI(temperature=0)
structured_llm_router = llm.with_structured_output(RouteQuery)

system = """You are an expert at routing a user question to a vectorstore or web search.
The vectorstore contains documents related to five-star hotels in Istanbul,
including their name, room and bed capacity, address, and contact details like phone and fax.
Use the vectorstore for questions about hotel names, locations, phone numbers, or capacities.
Use web-search for unrelated general topics."""

route_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "{question}"),
    ]
)

question_router = route_prompt | structured_llm_router

