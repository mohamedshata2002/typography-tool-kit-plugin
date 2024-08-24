from langchain_google_genai import GoogleGenerativeAI
from api_key import GOOGLE_API_KEY
import os 
from langchain.document_loaders import CSVLoader
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import pandas as pd
from langchain.output_parsers import ResponseSchema ,StructuredOutputParser



os.environ["google_api_key"] =GOOGLE_API_KEY
fonts =pd.read_csv("fonts.csv")
fonts = fonts.sample(frac=1).reset_index(drop=True)
model=GoogleGenerativeAI(model="gemini-1.0-pro",temperature=0)

def Parser():
    font_family  = ResponseSchema(name="font_family",description="The family of the font")
    font_Style= ResponseSchema(name="Style",description="The style of the font")
    reason= ResponseSchema(name="reason",description="why you use it")

    output_parser = StructuredOutputParser(response_schemas=[font_family,font_Style,reason])
    return output_parser


output_parser = Parser()
def Font_creator(query):
    template = "You are a font expert I want you to help me with choosing a font style \
        I will give you font styles and the query to choose the website and tell me why you choose it based on   grouping ,font personalities ,x height  \
            the font styles : {fonts}\
                the query : {query} \
                    return  three differnt font styles it in  json format  and return it on that instruction"
    prompt = ChatPromptTemplate.from_template(template)

    chain = ({"fonts":RunnablePassthrough(),"query":RunnablePassthrough(),"inst":RunnablePassthrough()}|
            prompt|model|StrOutputParser())
    return chain.invoke({"fonts":fonts,"query":query,"inst":output_parser.get_format_instructions()})



def split_on_json(input_string):
    return input_string.split("{")


def splitter(input,parser):
    sperator_template = "transfer the query  into json \
    query:{jsons} \
    the instrution of the json :{inst}"
    sperator_prompt = ChatPromptTemplate.from_template(sperator_template)
    sperator_chain = ({"jsons":RunnablePassthrough(),"inst":RunnablePassthrough()}|
            sperator_prompt|model|parser)
    fonts = []
    input = split_on_json(input)
    test =input[1:]
    
    for query  in test:
        font_ex = sperator_chain.invoke({"jsons":query,"inst":parser.get_format_instructions()})
        fonts.append(font_ex)
    return fonts
    
    
    
def Font_pairer(font,number):
    template ="you are font expert I will give you a font style I want you to suggest {number} font styles that can be pair with it from pairs of font styles\
 based on x-height,Similar contrast,Similar width,Similar mood,Similar style at least the font you suggest must have not less than two  of these categories  and not more than three of these categories \
     the font style I want you to find a pair from :{font},\
         the font styles that you are search from is :{fonts}\
             return json file and the instruction for the json :{inst}"
    prompt = ChatPromptTemplate.from_template(template)
    chain = ({"font":RunnablePassthrough(),"fonts":RunnablePassthrough(),"inst":RunnablePassthrough(),"number":RunnablePassthrough()}|
            prompt|model|StrOutputParser())
    return chain.invoke({"font":font,"fonts":fonts,"inst":output_parser.get_format_instructions(),"number":number})
