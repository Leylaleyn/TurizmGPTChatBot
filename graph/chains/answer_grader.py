# Burada Amaç:Kullanıcının sorusuna LLM’in verdiği cevabın “soruyu gerçekten yanıtlayıp yanıtlamadığını” değerlendirmek.
# Yani: “Bu cevap gerçekten işe yarar mı, boş mu konuşmuş?”

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.runnables import RunnableSequence
from langchain_openai import ChatOpenAI


class GradeAnswer(BaseModel): # Bu model, LLM’den gelen yanıtı bir bool (doğru/yanlış) olarak bekler.

    binary_score: bool = Field(
        description="Answer addresses the question, 'yes' or 'no'"
    )

# **************** NOT: ********************
# Neden BaseModel Kullandık?
# 👇 Problem: LLM çıktıları genelde “serbest stil” metinlerdir.
# LLM sana döner:
# "Evet, bu cevap oldukça yerinde."
# 😓 Ama senin kodun sadece "evet" ya da "hayır" görmek istiyor olabilir.
# Daha da kötüsü: "Yes.", "yes!", "YES", "Certainly yes.", "Hmm not really." gibi çok çeşitli dönebilir.
# ✅ Çözüm: BaseModel ile Yapı Zorlamak
# "Ey LLM, bana sadece True ya da False döneceksin. Şekil şemal belli. Başka bir şey istemiyorum."
# ******************************************


llm = ChatOpenAI(temperature=0)
structured_llm_grader = llm.with_structured_output(GradeAnswer)

system_prompt = """You are a grader assessing whether an answer addresses / resolves a question \n 
     Give a binary score 'yes' or 'no'. Yes' means that the answer resolves the question."""

answer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "User question: \n\n {question} \n\n LLM generation: {generation}"),
    ]
)

answer_grader: RunnableSequence = answer_prompt | structured_llm_grader