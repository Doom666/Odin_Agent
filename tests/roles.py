from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


def inner_voice(input):
    llm = OpenAI(temperature=0.9)
    prompt = PromptTemplate(
        input_variables=["message"],
        template="This is a test prompt template {message}",
    )

    chain = LLMChain(llm=llm, prompt=prompt)
    answer = chain.run(input)
    return answer

def iv_emotion(input):
    llm = OpenAI(temperature=0.9)
    prompt = PromptTemplate(
        input_variables=["message"],
        template="""
        You are an expert emotional analyst, your job is to read a text and answer with the 3 strongest emotions the writer is feeling and their score from 0 to 10.
        Dimension              examples
        Aversion/attraction:  Fear-Love:
        Past reflection :     Guilt-Proud:
        Present reflection:   Sad-Happy:
        Future reflection:  Anxious-Confident:
        Change:          Angry-Creative:
        Exploration:   Bored-fascinated:
        





        Example:
        Message: I look forward to get it done!
        Answer: Happiness:7  {message}""",
    )

    chain = LLMChain(llm=llm, prompt=prompt)
    answer = chain.run(input)
    return answer