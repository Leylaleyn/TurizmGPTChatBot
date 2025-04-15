# Buradaki Amaç: GraphState aslında her adımda grafın anlık durumunu tutan bir yapı. Bu state içinde şu bilgiler bulunuyor:
# question: Kullanıcıdan gelen soru.
# generation: LLM tarafından üretilen cevap.
# web_search: Web'den bilgi toplama işleminin gerekip gerekmediği bilgisini tutuyor.
# documents: Arama sonucunda veya veritabanından çekilen belgelerin listesi.


from typing import List, TypedDict


class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        generation: LLM generation
        web_search: whether to add search
        documents: list of documents
    """

    question: str
    generation: str
    web_search: bool
    documents: List[str]