
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any
from chains import *

app = FastAPI()

# Define the input schema using Pydantic
class BrainInput(BaseModel):
    query: str
    num: int

# Define the Brain function as it is
def Brain(query,num):
    number_of_sim = {1: "one", 2: "two"}
    num = number_of_sim[num]
    sugested_fonts = Font_creator(query)
    sugested_fonts_fonts_sp = splitter(sugested_fonts, output_parser)
    main_dict = {}
    secandry_dict = {}
    for font in sugested_fonts_fonts_sp:
        secandry_dict = {}
        main_pairer = font['font_family']
        result_p = Font_pairer(main_pairer, num)
        split_p = splitter(result_p, output_parser)
        secandry_dict["main_font"] = font
        secandry_dict["Paired_fonts"] = split_p
        main_dict[main_pairer] = secandry_dict
    return main_dict

# Create an endpoint to handle the request
@app.post("/brain")
def process_brain(input_data: BrainInput):
    result = Brain(input_data.query, input_data.num)
    return result
