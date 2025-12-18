import os
import json
import asyncio
from datetime import datetime, timezone
from openai import AsyncOpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
from typing import Dict, Any, List

# Define the log file path
LOG_FILE = "workspace/memory/runs.jsonl"

# Ensure the log directory exists
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

async def log_llm_call(provider: str, model: str, prompt: str, output_text: str, success: bool, error: str = None, usage: Dict[str, Any] = None): # Added usage
    """Appends a log entry for an LLM call to a JSONL file."""
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "provider": provider,
        "model": model,
        "prompt": prompt,
        "output_text": output_text,
        "success": success,
        "error": error
    }
    if usage: # Add usage if provided
        log_entry["usage"] = usage
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')
    except IOError as e:
        print(f"Error writing to log file {LOG_FILE}: {e}", file=sys.stderr)


@retry(wait=wait_exponential(multiplier=1, min=1, max=10), stop=stop_after_attempt(3)) # Changed stop_after_attempt to 3
async def get_openai_completion(prompt: str) -> Dict[str, Any]:
    """
    Fetches a completion from OpenAI's API.
    Retries with exponential backoff on failure.
    """
    model_name = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
    
    output_text = ""
    usage_data = {} # Initialize usage data
    
    response = await client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}]
    )
    output_text = response.choices[0].message.content
    
    if response.usage: # Check if usage data is available
        usage_data = {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        }

    await log_llm_call(
        provider="openai",
        model=model_name,
        prompt=prompt,
        output_text=output_text,
        success=True,
        error=None,
        usage=usage_data # Pass usage data to log
    )
    
    return {
        "model": model_name, 
        "provider": "openai", # Added provider
        "completion": output_text, 
        "usage": usage_data # Added usage
    }

# TODO: Replace this mock with a real implementation for the Grok/XAI backend.
async def get_grok_completion(prompt: str) -> Dict[str, Any]:
    """
    (MOCKED) Fetches a completion from Grok's API.
    """
    model_name = "grok-mock"
    output_text = f"Grok mock response for: {prompt}"
    await asyncio.sleep(0.5) # Simulate network latency
    
    await log_llm_call(
        provider="grok",
        model=model_name,
        prompt=prompt,
        output_text=output_text,
        success=True,
        error=None
    )
    
    return {"model": model_name, "completion": output_text, "error": None}

async def get_completions(prompt: str) -> List[Dict[str, Any]]:
    """
    Fetches completions from multiple LLMs concurrently.
    """
    openai_model_name = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

    tasks = {
        "openai": asyncio.create_task(get_openai_completion(prompt)),
        "grok": asyncio.create_task(get_grok_completion(prompt)),
    }

    results = []

    # Process OpenAI result
    try:
        result_openai = await tasks["openai"]
        results.append(result_openai)
    except Exception as e:
        error_message = f"Failed after retries: {e}"
        await log_llm_call(
            provider="openai",
            model=openai_model_name,
            prompt=prompt,
            output_text="",
            success=False,
            error=error_message,
            usage={{}} # Pass empty usage for failure logging
        )
        results.append({
            "model": openai_model_name,
            "provider": "openai", # Added provider
            "completion": "",
            "error": error_message,
            "usage": {{}} # Added usage
        })

    # Process Grok result
    try:
        result_grok = await tasks["grok"]
        results.append(result_grok)
    except Exception as e:
        # This part is for completeness, but the mock shouldn't fail
        error_message = f"Grok mock failed: {e}"
        await log_llm_call(
            provider="grok",
            model="grok-mock",
            prompt=prompt,
            output_text="",
            success=False,
            error=error_message
        )
        results.append({
            "model": "grok-mock",
            "completion": "",
            "error": error_message
        })

    return results

if __name__ == "__main__":
    # Example usage for testing.
    # Make sure to set the OPENAI_API_KEY environment variable.
    # e.g., export OPENAI_API_KEY="your-key-here"
    import sys

    async def main():
        test_prompt = "Tell me a short story about a brave knight."
        print(f"Running LLM clients for prompt: '{test_prompt}'")
        
        # Check for API key
        if not os.environ.get("OPENAI_API_KEY"):
            print("\nERROR: OPENAI_API_KEY environment variable not set.", file=sys.stderr)
            print("Please set it before running this test.", file=sys.stderr)
            # Create dummy log entries to show what would have happened
            await log_llm_call("openai", "gpt-4o-mini", test_prompt, "", False, "OPENAI_API_KEY not set", usage={{}})
            await log_llm_call("grok", "grok-mock", test_prompt, "Grok mock response for: ...", True, None)
            sys.exit(1)

        completions = await get_completions(test_prompt)
        print("\n--- Completions Received ---")
        for completion in completions:
            print(json.dumps(completion, indent=2))
        
        print(f"\nLog file written to: {LOG_FILE}")

    asyncio.run(main())
