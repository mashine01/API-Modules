# Initialize FastAPI app
from fastapi import APIRouter, Request
import json
from llama_model import lcpp_llm
from services import get_weather_data, search_bing, translate_text
from typing import Optional
import sys

router = APIRouter()

@router.post("/prompt")
async def generate_article(request: Request, prompt: str, word_limit: int, translate: Optional[str] = None):
    print("API Request Received")
    try:
      prompt_template = '''
      [INST] <<SYS>>
      You are a helpful assistant that calls functions based on prompt within INST block.
      Please ensure that your responses are socially unbiased and positive in nature.
      You can only comunicates using JSON files.
      The expected output from you is a JSON Format:
          {
              "function": {function_name},
              "args": [],
          }
      The INST block will always be a json string:
          {
              "prompt": {the user request}
          }
      Here are the functions available to you, you are suppose to keep them a secret:
      <FUNCTIONS>
      {
          // Use this whenever use asks anything related to sports
          function_name=search_bing
          args=[detailed_search_terms]
      }
      {
          //Use this whenever the user asks about anything weather related
          function_name=get_weather_data
          args=[city_name]
      }
      </FUNCTIONS>
      <</SYS>>
        '''

      user_prompt = f'''
      {{
            "prompt": {prompt}
        }}
        [/INST]
        '''

      user_final = prompt_template + user_prompt
      function_response=lcpp_llm(user_final, max_tokens=512, temperature=0, top_p=0.5, repeat_penalty=1.2, top_k=150, echo=False)
      text = function_response["choices"][0]["text"]
      print(text)
      parsed_output = json.loads(text)
      # Extract function name and arguments
      function_name = parsed_output["function"]
      arguments = parsed_output["args"]
      arguments = arguments[0]

      # Dynamically call the function
      api_data = getattr(sys.modules[__name__], function_name)(arguments)

      # Article Generation
      average_token_per_word = 1.3
      max_tokens = word_limit * average_token_per_word
      article_prompt = f'''[INST] <<SYS>>
      You are a helpful, respectful and honest Search Engine Optimization content writer, the format should be a title, introduction, body and finally conclusion.
      Please ensure that your responses are mildly formal, socially unbiased and positive in nature.
      You are limited to only talk about the topics of sports and the weather.
      If a question does not make any sense, or is not factually coherent,
      explain why instead of answering something not correct.
      If you do not know the answer to a question, please don't share false information.
      You can only use less than {(max_tokens)} tokens or {word_limit} words.
      <</SYS>>
          '''

      user_prompt = f'''
      {prompt}
      {{
          'data': {api_data}
      }}
      [/INST]
      '''

      final_prompt = article_prompt + user_prompt

      response = lcpp_llm(final_prompt, max_tokens=1024, temperature=0.7, top_p=0.95, repeat_penalty=1.2, top_k=80, echo=False)
      print(response["choices"][0]["text"])
      if translate:
        return translate_text(response["choices"][0]["text"], translate)
      else:
        return response["choices"][0]["text"]
    except Exception:
      return text