#!/usr/bin/env python
import argparse, time, sys
from openai import OpenAI

def main(base_url: str, model: str, api_key: str):
    '''
    Healthcheck script for vLLM like
    
    curl {base_url} 
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer {api_key}" \
      -d '{"model": {model}, "prompt": "I", "max_tokens": 1}'
    '''

    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
    )

    start_time = time.time()
    model = model or client.models.list().data[0].id
    client.completions.create(model=model, prompt="I", max_tokens=1)
    end_time = time.time()

    print("{} completed in {} seconds.".format(model, end_time - start_time))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=main.__doc__)

    parser.add_argument("--base_url", default='http://localhost:8000/v1', const='http://localhost:8000/v1', nargs='?', type=str, help="Base URL of the vLLM API server (default: %(default)s)")
    parser.add_argument("--model", const=None, nargs='?', type=str, help="Model name to use for the healthcheck (default: The first listed model)")
    parser.add_argument("--api_key", default='_', const='_', nargs='?', type=str, help="API key to use for the healthcheck (default: %(default)s)")
    
    args = parser.parse_args()
    try:
        main(base_url=args.base_url, model=args.model, api_key=args.api_key)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)