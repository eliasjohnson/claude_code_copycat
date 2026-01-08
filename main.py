import os
from dotenv import load_dotenv
from google import genai
import argparse


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`

    # load env variables
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if api_key is None:
        raise Exception(RuntimeError("API key is not set"))
    
    #establish client
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model='gemini-2.5-flash', contents=args.user_prompt
    )
    # print question
    print(f"\nUser Prompt: {args.user_prompt}")
    
    #print response token count
    if response.usage_metadata.prompt_token_count is None: # type: ignore
        raise Exception(RuntimeError("Failed API Request."))
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}") # type: ignore 
    
    if response.usage_metadata.candidates_token_count is None: # type: ignore
        raise Exception(RuntimeError("Failed API Request."))
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}") # type: ignore 
    
    print(f"Response: \n{response.text}\n")
    

    

if __name__ == "__main__":
    main()
