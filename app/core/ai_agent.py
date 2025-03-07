import json
from openai import OpenAI
from ..core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

async def generate_task_description(brief: str) -> dict:
    """
    Generate a detailed task description and priority from a brief using OpenAI's GPT model.
    """
    prompt = f"""
    Based on this brief: {brief}

    1. Generate a detailed task description that:
       - Is clear and concise
       - Includes key objectives
       - Mentions important considerations
       - Is professional in tone

    2. Suggest a priority level (ONLY respond with exactly one of: "Low", "Medium", "High")
       Consider:
       - Task urgency
       - Business impact
       - Complexity

    Format your response as JSON with two fields:
    - description: your detailed description
    - priority: one of ["Low", "Medium", "High"]
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )
        content = response.choices[0].message.content
        if content is None:
            raise ValueError("No content received from OpenAI")
        
        result = json.loads(content)
        return {
            "description": result["description"].strip(),
            "priority": result["priority"]
        }
    except Exception as e:
        raise ValueError(f"Error generating description: {str(e)}")

