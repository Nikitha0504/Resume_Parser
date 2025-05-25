# import libraries

from openai import OpenAI
import yaml
import json
api_key = None
CONFIG_PATH = r"config.yaml"

with open(CONFIG_PATH) as file:
    data = yaml.load(file, Loader=yaml.FullLoader)
    api_key = data['OPENAI_API_KEY']

def ats_extractor(resume_text):
    # Load API key from config.yaml
    try:
        with open("config.yaml", "r") as file:
            config = yaml.safe_load(file)
        openai.api_key = config.get("openai_api_key")
    except Exception as e:
        return json.dumps({"error": f"Failed to load API key: {e}"})

    # Prompt to extract structured data
    prompt = f"""
    Extract the following fields from the resume text:
    - Name
    - Email
    - Phone
    - Skills
    - Experience
    - Education

    Resume:
    {resume_text}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )
        content = response['choices'][0]['message']['content']
        return json.dumps(json.loads(content))  # assumes output is valid JSON
    except Exception as e:
        return json.dumps({"error": str(e)})
