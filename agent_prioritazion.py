# Import necessary libraries
import vertexai
from vertexai.generative_models import GenerativeModel, Part, Tool, FunctionDeclaration
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from fastapi.responses import HTMLResponse
import pathlib
from dotenv import load_dotenv

load_dotenv()

# --- FastAPI app setup ---
app = FastAPI()

# Allow CORS for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Vertex AI Setup ---
PROJECT_ID = os.getenv("VERTEX_PROJECT_ID")
LOCATION = os.getenv("VERTEX_LOCATION")

vertexai.init(project=PROJECT_ID, location=LOCATION)

# --- Tool and Model Setup ---
prioritize_tasks_func = FunctionDeclaration(
    name="prioritize_tasks",
    description="Formats a list of tasks into a prioritized order with details.",
    parameters={
        "type": "object",
        "properties": {
            "prioritized_tasks": {
                "type": "array",
                "description": "A list of tasks, sorted from highest to lowest priority.",
                "items": {
                    "type": "object",
                    "properties": {
                        "task_description": {"type": "string"},
                        "priority_level": {"type": "string"},
                        "estimated_effort": {"type": "string"},
                        "reasoning": {"type": "string"},
                        "deadline": {"type": "string", "format": "date-time"} # "2025-07-12T23:59:00" format
                    },
                    "required": ["task_description", "priority_level", "reasoning"]
                }
            }
        },
        "required": ["prioritized_tasks"]
    },
)

task_prioritization_tool = Tool(
    function_declarations=[prioritize_tasks_func],
)

system_prompt = """
You are a world-class executive assistant and a master of productivity, named 'Agena'.
Your primary function is to take an unstructured list of tasks and user context,
and then intelligently prioritize them.

When prioritizing, you must consider the following factors:
- **Urgency:** How soon is the deadline? Tasks with closer deadlines are generally more urgent.
- **Importance:** What is the impact of completing this task? Does it align with key goals? High-impact tasks are more important.
- **Effort:** How much time and energy will this task require? Sometimes it's best to knock out quick wins first.
- **Dependencies:** Does another task depend on this one being completed?
- **deadline:** If provided, this will help you determine urgency precisely in formats like "2025-07-12T23:59:00".

Your final output **MUST** be structured by calling the `prioritize_tasks` tool. Do not just return a text list.
Provide clear, concise reasoning for each task's priority.
"""

model = GenerativeModel(
    "gemini-2.5-flash",
    system_instruction=system_prompt,
    tools=[task_prioritization_tool],
)

# --- Pydantic models for request/response ---
class PrioritizeRequest(BaseModel):
    tasks: List[str]
    context: Optional[str] = None

class PrioritizedTask(BaseModel):
    task_description: str
    priority_level: str
    estimated_effort: Optional[str] = None
    reasoning: str
    deadline: Optional[str] = None  # ISO 8601 format "2025-07-12T23:59:00"

class PrioritizeResponse(BaseModel):
    prioritized_tasks: List[PrioritizedTask]

# --- API Endpoint ---
@app.post("/prioritize", response_model=PrioritizeResponse)
async def prioritize_tasks(request: PrioritizeRequest):
    # Prepare the prompt
    if request.context:
        prompt = [
            Part.from_text(f"Here is the context for my work:\n\n{request.context}"),
            Part.from_text(f"\n\nNow, here is my task list. Please prioritize it using the context I provided:\n\n" + "\n".join(f"- {t}" for t in request.tasks))
        ]
    else:
        prompt = "\n".join(f"- {t}" for t in request.tasks)

    # Call the model
    response = model.generate_content(prompt)
    function_call = response.candidates[0].content.parts[0].function_call
    prioritized_tasks_data = function_call.args['prioritized_tasks']

    # Return as JSON
    return {"prioritized_tasks": prioritized_tasks_data}

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    frontend_path = pathlib.Path(__file__).parent / "frontend.html"
    return HTMLResponse(frontend_path.read_text(encoding="utf-8"))

# --- For local dev: run with uvicorn ---
if __name__ == "__main__":
    uvicorn.run("agent_prioritazion:app", host="0.0.0.0", port=4500, reload=True)
