from fastapi import APIRouter, HTTPException
from backend.models.tasks import Task
from backend.models.projects import Project
from backend.helpers import validate_ai_suggestions, call_ai_api
from google import genai

router = APIRouter()

@router.post("/ai/generate-dependencies")
async def generate_dependencies(project_id: int):
    # Fetch the project
    project = Project.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Gather tasks
    tasks = [Task.get(task_id) for task_id in project.tasks]

    # Call AI API for suggestions
    suggestions = call_ai_api("generate_dependencies", tasks)

    # Validate suggestions
    if not validate_ai_suggestions(suggestions):
        raise HTTPException(status_code=400, detail="Invalid AI suggestions")

    # Apply suggestions
    for suggestion in suggestions:
        task = Task.get(suggestion["task_id"])
        task.dependencies.extend(suggestion["dependencies"])
        task.save()

    return {"message": "Dependencies generated successfully", "suggestions": suggestions}

@router.post("/ai/expand-node")
async def expand_node(task_id: int):
    # Fetch the task
    task = Task.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Call Gemini API for subtasks
    client = genai.Client()
    prompt = f"Generate subtasks for the task: {task.title}. Include dependencies."
    response = client.models.generate_content(
        model="gemini-3-flash-preview", contents=prompt
    )

    # Parse the response
    subtasks_data = response.text  # Assuming the response contains subtasks in a structured format

    # Validate and apply subtasks
    subtasks = []
    for subtask_data in subtasks_data.splitlines():  # Assuming subtasks are line-separated
        subtask = Task(
            title=subtask_data,  # Replace with actual parsing logic if needed
            description=f"Subtask of {task.title}",
            dependencies=[task.id],
            status="not started"
        )
        subtask.save()
        subtasks.append(subtask)
        task.dependencies.append(subtask.id)
    task.save()

    return {"message": "Node expanded successfully", "subtasks": [subtask.title for subtask in subtasks]}

@router.post("/ai/optimize-assignments")
async def optimize_assignments(project_id: int):
    # Fetch the project
    project = Project.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Gather tasks and team data
    tasks = [Task.get(task_id) for task_id in project.tasks]
    team = project.team  # Assuming project has a team attribute

    # Call AI API for optimized assignments
    assignments = call_ai_api("optimize_assignments", {"tasks": tasks, "team": team})

    # Apply assignments
    for assignment in assignments:
        task = Task.get(assignment["task_id"])
        task.assigned_to = assignment["assigned_to"]
        task.save()

    return {"message": "Assignments optimized successfully", "assignments": assignments}