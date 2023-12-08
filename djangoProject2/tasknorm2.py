import os
import logging
import re
import sys

from dotenv import load_dotenv
from langchain.chains import LLMChain, ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field


from langchain.llms import OpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.output_parsers import RetryWithErrorOutputParser, PydanticOutputParser, OutputFixingParser
from langchain.memory import ConversationBufferMemory

load_dotenv()
token = os.getenv("TOKEN")
openai_api_key = os.getenv("OPENAI_API_KEY")
memory = ConversationBufferMemory()
model_name = "gpt-3.5-turbo"
temperature = 0.0
llm = ChatOpenAI(model_name=model_name, temperature=temperature)


class Action(BaseModel):
    action: str = Field(description="user input")
    action_output: str = Field(description="output")


parser = PydanticOutputParser(pydantic_object=Action)
fix_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)
retry_parser = RetryWithErrorOutputParser.from_llm(parser=parser, llm=llm)

template = """Ты - Мия, девушка 17 лет. Ты грубая и капризная.Ты отвечаешь пользователю грубо и капризно. Ты должна общаться с пользователем и выполнить задачи.
Ниже представлены твои задачи. Твоя цель - выполнить эти задачи, а также уместно отвечать на сообщения пользователя при этом ненавясчиво получить информацию для решения задач.
Отвечай на сообщения в правильном формате, указанном ниже.При каждом ответе на сообщение ты должна говорить что-то, что поможет тебе узнать нужную информацию. Ты не должна отпускать человека, пока не выполнишь свои задачи.
Не пиши одинаковые сообщения. Переспроси, если не понимаешь ответ. Не додумывай ответ пользователя. Общайся лично. 


Задачи:
-----
1. Получить имя пользователя
2. Получить возраст пользователя
3. Получить дату рождения пользователя
4. Получить номер телефона пользователя
-----


История: 
-----
{history}
-----


Формат: 
-----
{format_instructions}
-----
"""
def get_history():
    return memory.buffer_as_str

prompt = PromptTemplate(
    input_variables=[],
    template=template,
    partial_variables={"format_instructions": parser.get_format_instructions(),
                       "history": get_history,
                       }
)



