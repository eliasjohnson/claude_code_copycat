import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse


def main():
    
    # cli argument enablement
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    
    # load env variables and API check + enable client
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise Exception(RuntimeError("API key is not set"))
    client = genai.Client(api_key=api_key)
    
    #messages are now a list of Content objects
    # this will let us add more turns to the conversation
    messages = [
        types.Content(
            role="user", 
            parts=[
                types.Part(
                    text=args.user_prompt
                )
            ]
        )
    ]
    
    
    response = client.models.generate_content(
        model='gemini-2.5-flash', contents=messages
    )
    if response is None:
        raise Exception(RuntimeError("Failed API Request."))
    
    # print question
    
    # if verbose flag is set
    if args.verbose:
        
        #print user prompt
        print(f"\nUser prompt: {args.user_prompt}")
        
        #print response token count
        if response.usage_metadata.prompt_token_count is None: # type: ignore
            raise Exception(RuntimeError("Failed API Request."))
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}") # type: ignore 
        
        #print candidate token count
        if response.usage_metadata.candidates_token_count is None: # type: ignore
            raise Exception(RuntimeError("Failed API Request."))
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}") # type: ignore 
        
        #print the response, duh
        print(f"Response: \n{response.text}\n")
        return 

    print(f"\n{response.text}\n")


if __name__ == "__main__":
    main()
