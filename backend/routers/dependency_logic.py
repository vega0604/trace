from fastapi import APIRouter, HTTPException
from backend.models.tasks import Task
from backend.models.projects import Project
from backend.helpers import detect_cycles

router = APIRouter()

@router.post("/tasks/{task_id}/done")
async def mark_task_done(task_id: int):
    # Fetch the task
    task = Task.get(task_id)  # Assuming Task.get fetches the task by ID
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update task status
    task.status = "done"
    task.save()

    # Recompute blocked states for dependent tasks
    dependent_tasks = Task.get_dependents(task_id)
    for dependent in dependent_tasks:
        if all(Task.get(dep_id).status == "done" for dep_id in dependent.dependencies):
            dependent.status = "ready"
            dependent.save()

    # Detect cycles (if any)
    project = Project.get(task.project_id)
    if detect_cycles(project.tasks):
        raise HTTPException(status_code=400, detail="Cycle detected in dependencies")

    # Update project status if all tasks are done
    if all(t.status == "done" for t in project.tasks):
        project.status = "done"
        project.save()

    return {"message": "Task marked as done", "task": task}