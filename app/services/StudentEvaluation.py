from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import os
from dotenv import load_dotenv


load_dotenv()

api_key=openai.api_key = os.environ.get('OPENAI_KEY_NEW')

class StudentEvaluator:
    def init(self):
        self.store = {}
        self.model = ChatOpenAI(api_key, max_tokens=4000)
        self.searchParser = JsonOutputParser(pydantic_object=self.SearchOutput)

        # Prompt Setup
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You're an assistant who's good at {ability}. follow the format instructions {instructions}, 
                    
                    This is the subjects that the student is taking {subjects}, 
                    
                    and this is the students grades so far {grades}
                    
                    be as comprehensive as you can
                    
                    """,
                ),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{input}"),
            ]
        )
        
        self.runnable = self.prompt | self.model
        self.with_message_history = RunnableWithMessageHistory(
            self.runnable,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="history",
        )
        self.with_message_history_search = self.with_message_history | self.searchParser

    class SearchOutput(BaseModel):
        strengths: str = Field(description="Tell students what subject they're good at and why exactly it is that they're good at it.")
        weaknesses: str = Field(description="Tell students what subject they're weak at and why exactly it is that they're weak at it.")
        recommendation: str = Field(description="Recommendation on what should the student focus on, as well as recommend resources (urls) for them to refer to and improve what they're lacking at.")
        
    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
        return self.store[session_id]
    
    def evaluate_student(self, grades, subjects):
        evaluation_query = None
        try:
            evaluation_query = self.with_message_history_search.invoke(
                {
                    "grades": grades,
                    "subjects": subjects,
                    "ability": "giving analysis to students on their grades. Don't mention the subject names but rather talk in general which aspects they seem to excel at (technical or theoretical)",
                    "input": "",
                    "instructions": str(self.searchParser.get_format_instructions())
                },
                config={"configurable": {"session_id": "abc123"}},
            )
        except Exception as e:
            print("Error: ", e)
        
        return evaluation_query