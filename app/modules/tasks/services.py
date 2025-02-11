from sqlmodel import Session, select
from app.core.database import engine
from app.modules.tasks.model import TaskDB
from app.modules.tasks.shemas import TaskCreate


def get_tasks_service(user_id: int):
    with Session(engine) as session:
        tasks = session.exec(select(TaskDB).where(
            TaskDB.user_id == user_id)).all()
    return tasks


def get_task_service(task_id: int):
    with Session(engine) as session:
        task = session.exec(select(TaskDB).where(
            TaskDB.id == task_id)).first()
    return task


def create_task_service(task: TaskCreate):
    db_task = TaskDB(**task.model_dump())
    with Session(engine) as session:
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
    return db_task


def update_task_service(task_id: int, task: TaskCreate):
    db_task = get_task_service(task_id)

    if db_task is None:
        return None

    for key, value in task.model_dump().items():
        if value is not None:
            setattr(db_task, key, value)

    with Session(engine) as session:
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
    return db_task


def delete_task_service(task_id: int):
    db_task = get_task_service(task_id)
    if db_task is None:
        return None
    with Session(engine) as session:
        session.delete(db_task)
        session.commit()
    return db_task
