import time
import openai
from config import cfg

class LLMIntegration:
    def __init__(self):
        self.model = cfg.llm_model
        self.temperature = cfg.temperature
        self.token_limit = cfg.token_limit

    def generate_response(self, prompt, max_tokens=50):
        messages = [
            {"role": "system", "content": "You are a seasoned data analyst with years of experience with SQL databases, python programming and Business Analytics."},
            {"role": "user", "content": prompt}
        ]
        num_retries = 5
        for attempt in range(num_retries):
            try:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=messages,
                    temperature=self.temperature,
                    max_tokens=max_tokens
                )
                return response.choices[0].message["content"].strip()
            except openai.error.RateLimitError:
                if cfg.debug_mode:
                    print("API Rate Limit Reached. Waiting 20 seconds...")
                time.sleep(20)
            except openai.error.APIError as e:
                # Handle other API errors
                pass

# Example usage
if __name__ == "__main__":
    llm = LLMIntegration()
    prompt = "Translate the following natural language query into SQL: What are the total sales for product A?"
    response = llm.generate_response(prompt)
    print(f"Generated Response: {response}")
