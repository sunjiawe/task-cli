from openai import OpenAI
import os

# Learn more about calling the LLM: https://the-pocket.github.io/PocketFlow/utility_function/llm.html
def call_llm(prompt):
    if os.environ.get('DEBUG_MODE') == 'true':
        print(f"--- PROMPT ---\n{prompt}\n--- END PROMPT ---")
    from openai import OpenAI
    client = OpenAI(api_key=os.environ.get("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
    r = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}]
    )
    return r.choices[0].message.content
    
if __name__ == "__main__":
    prompt = "What is the meaning of life?"
    print(call_llm(prompt))
