from langchain.chat_models import ChatVertexAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import HumanMessage, SystemMessage

chat = ChatVertexAI()


chain = LLMChain(llm=chat, prompt=chat_prompt)

chain.run(input_language="English", output_language="French", text="I love programming.")