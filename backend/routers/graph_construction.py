from fastapi import APIRouter, HTTPException
from backend.models.projects import Project
from backend.models.tasks import Task

router = APIRouter()

@router.get("/graph")
async def get_graph(project_id: int):
    # Fetch the project
    project = Project.get(project_id)  # Assuming Project.get fetches the project by ID
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Build graph representation
    nodes = []
    edges = []

    for task_id in project.tasks:
        task = Task.get(task_id)
        if task:
            nodes.append({
                "id": task.id,
                "title": task.title,
                "status": task.status
            })
            for dependency in task.dependencies:
                edges.append({"from": dependency, "to": task.id})

    return {"nodes": nodes, "edges": edges}