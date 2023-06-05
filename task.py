from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()


def todays_tasks():
    print("Today {}:".format(datetime.today().strftime("%d %b")))
    dates_tasks(datetime.today().date())


def dates_tasks(date):
    rows = session.query(Task).filter(Task.deadline == date).all()
    [print(f"{i}. {row}") for i, row in enumerate(rows, 1)] if rows else print("Nothing to do!")


def weeks_tasks():
    for i in range(7):
        consecutive_date = datetime.today().date() + timedelta(days=i)
        print(f"\n{consecutive_date.strftime('%A %d %b')}:")
        dates_tasks(consecutive_date)


def all_tasks():
    print("All tasks:")
    list_tasks(session.query(Task).order_by(Task.deadline).all())


def missed_tasks():
    print('Missed tasks:')
    rows = session.query(Task).filter(Task.deadline < datetime.today().date()).order_by(Task.deadline).all()
    list_tasks(rows) if rows else print('All tasks have been completed!')


def add_task():
    task = input("Enter a task\n")
    deadline = datetime.strptime(input("Enter a deadline\n"), "%Y-%m-%d").date()
    session.add(Task(task=task, deadline=deadline))
    session.commit()
    print("The task has been added!")


def list_tasks(tasks):
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task}. {task.deadline.strftime('%-d %b')}")


def delete_task():
    rows = session.query(Task).order_by(Task.deadline).all()
    if rows:
        print("Choose the number of the task you want to delete:")
        session.delete(rows[int(input(list_tasks(rows))) - 1])
        session.commit()
        print("The task has been deleted!")
    else:
        print("Nothing to delete")


options = {1: todays_tasks, 2: weeks_tasks, 3: all_tasks, 4: missed_tasks, 5: add_task, 6: delete_task}
