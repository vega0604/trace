from fastapi import APIRouter, UploadFile, HTTPException
import csv
from io import StringIO
from backend.models.projects import Project
from backend.models.tasks import Task
from backend.helpers import create_person_class

router = APIRouter()

@router.post("/parse-task")
async def parse_task(file: UploadFile):
    if file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV file.")

    content = await file.read()
    csv_content = StringIO(content.decode("utf-8"))
    reader = csv.DictReader(csv_content)

    tasks = []
    project_id = None

    for row in reader:
        try:
            task_id = int(row["id"])
            title = row["title"]
            description = row["description"]
            tags = row["tags"].split(",")
            assigned_to = row["assigned_to"].split(",")
            status = row["status"]
            created_at = row["created_at"]
            updated_at = row["updated_at"]
            due_date = row["due_date"]

            # Ensure all assigned people have classes
            for email in assigned_to:
                create_person_class(email.strip())

            # Create task instance
            task = Task(
                id=task_id,
                title=title,
                description=description,
                tags=tags,
                assigned_to=assigned_to,
                status=status,
                created_at=created_at,
                updated_at=updated_at,
                due_date=due_date
            )
            tasks.append(task)

        except KeyError as e:
            raise HTTPException(status_code=400, detail=f"Missing column in CSV: {e}")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid data format: {e}")

    # Create project instance
    project = Project(id=project_id, tasks=[task.id for task in tasks])

    return {"message": "Tasks and project parsed successfully.", "project": project}
