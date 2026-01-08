import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse


def main():
    
    
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`
    
    
    # load env variables and API check
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if api_key is None:
        raise Exception(RuntimeError("API key is not set"))

    client = genai.Client(api_key=api_key)
    
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    
    response = client.models.generate_content(
        model='gemini-2.5-flash', contents=messages
    )
    if response is None:
        raise Exception(RuntimeError("Failed API Request."))
    
    # print question
    print(f"\nUser Prompt: {args.user_prompt}")
    
    #print response token count
    if response.usage_metadata.prompt_token_count is None: # type: ignore
        raise Exception(RuntimeError("Failed API Request."))
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}") # type: ignore 
    
    #print candidate token count
    if response.usage_metadata.candidates_token_count is None: # type: ignore
        raise Exception(RuntimeError("Failed API Request."))
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}") # type: ignore 
    
    print(f"Response: \n{response.text}\n")
    

if __name__ == "__main__":
    main()
