import os 
import streamlit as st 
from langchain.llms import VertexAI 
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain 
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper 
from langchain.output_parsers import CustomOutputParser
from langchain.agents import AgentAction, AgentFinish

# API


# App framework
st.title('🦜🔗 Actionsteps Creator')
prompt = st.text_input('What do you want to accomplish?') 

# Prompt templates
title_template = PromptTemplate(
    input_variables = ['topic'], 
    template='Write me a list of action steps necessary to take in order to accomplish: {topic}'
)

script_template = PromptTemplate(
    input_variables = ['title', 'wikipedia_research'], 
    template='write me a youtube video script based on this title TITLE: {title} while leveraging this wikipedia reserch:{wikipedia_research} '
)
# Parser
# Create an instance of the CustomOutputParser
output_parser = CustomOutputParser()

# Parse the LLM output
llm_output = "Action 1: Search\nAction 1 Input 1: Population of Canada in 2023\nObservation: The current population of Canada is 38,658,314 as of Wednesday, April 12, 2023, based on Worldometer elaboration of the latest United Nations data. I now know the final answer\nFinal Answer: Arrr, there be 38,658,314 people livin' in Canada as of 2023!"
parsed_output = output_parser.parse(llm_output)

# Access the action steps
action_steps = []
if isinstance(parsed_output, AgentFinish):
    final_answer = parsed_output.return_values["output"]
    print("Final Answer:", final_answer)
else:
    while isinstance(parsed_output, AgentAction):
        action_steps.append(parsed_output)
        parsed_output = output_parser.parse(parsed_output.log)

# Print the action steps
for i, action_step in enumerate(action_steps):
    print(f"Action {i+1}: {action_step.tool}")
    print(f"Action {i+1} Input {i+1}: {action_step.tool_input}")
    print()
# Memory 
title_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')
script_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')


# Llms
llm = VertexAI() 
title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True, output_key='title', memory=title_memory)
script_chain = LLMChain(llm=llm, prompt=script_template, verbose=True, output_key='script', memory=script_memory)

wiki = WikipediaAPIWrapper()

# Show stuff to the screen if there's a prompt
if prompt: 
    title = title_chain.run(prompt)
    wiki_research = wiki.run(prompt) 
    script = script_chain.run(title=title, wikipedia_research=wiki_research)

    st.write(title) 
    st.write(script) 

    with st.expander('Title History'): 
        st.info(title_memory.buffer)

    with st.expander('Script History'): 
        st.info(script_memory.buffer)

    with st.expander('Wikipedia Research'): 
        st.info(wiki_research)