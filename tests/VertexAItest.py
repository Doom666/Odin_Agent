from langchain.llms import VertexAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

import time
llm = VertexAI(project="white-sign-398014")


template = """Please, explain me what {subject} is as if I was really really stupid."""
prompt = PromptTemplate(template=template, input_variables=["subject"])
chain = LLMChain(llm=llm, prompt=prompt)


while True:
    respponse = chain.predict(subject=input("What do you want to learn from me, inferior carbon object?"))
    time.sleep(3)
    print(respponse)
    time.sleep(3)
    template2 = """Please, explain in a ridiculously simpler manner this text: {subject} """
    prompt2 = PromptTemplate(template=template2, input_variables=["subject"])
    chain2 = LLMChain(llm=llm, prompt=prompt2)
    chain2.predict(subject=respponse)
    time.sleep(3)