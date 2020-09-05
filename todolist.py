

from datetime import timedelta
from sqlalchemy import create_engine
engine = create_engine('sqlite:///todo.db?check_same_thread=False')

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today().date())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()


def main_menu():
    menu = "1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add Task\n6) Delete task\n0) Exit"
    print(menu)
    user_input = int(input())
    if user_input == 1:
        today = datetime.today().date()
        rows = session.query(Table).filter(Table.deadline == today).all()
        if len(rows) == 0:
            print()
            print("Today " + str(today.day) + " " + today.strftime("%b"))
            print("Nothing to do!")
            print()
            main_menu()
        else:
            print()
            print("Today:")
            for row in rows:
                print(str(row.id) + ". " + row.task)
            print()
            main_menu()
    elif user_input == 2:
        print()
        weekdays = ("Monday", "Tuesday", "Wednesday", "Thursday",
                    "Friday", "Saturday", "Sunday")
        for day in range(0, 7):
            temp_day = datetime.today().date() + timedelta(days=day)
            rows = session.query(Table).filter(Table.deadline == temp_day).all()
            if len(rows) == 0:
                print("{} {} {}:".format(weekdays[temp_day.weekday()], str(temp_day.day),
                                         temp_day.strftime("%b")))
                print("Nothing to do!")
                print()
            else:
                for row in rows:
                    print("{} {} {}:".format(weekdays[temp_day.weekday()], str(temp_day.day),
                                             temp_day.strftime("%b")))
                    print(str(row.id) + ". " + row.task)
                print()
        main_menu()
    elif user_input == 3:
        print()
        rows = session.query(Table).order_by(Table.deadline).all()
        print("All tasks:")
        for row in rows:
            row_id = row.id
            row_task = row.task
            row_month_num = row.deadline.day
            row_month_name = row.deadline.strftime("%b")
            print(f"{row_id}. {row_task}. {row_month_num} {row_month_name}")
        print()
        main_menu()
    elif user_input == 4:
        today = datetime.today().date()
        rows = session.query(Table).filter(Table.deadline < today).order_by(Table.deadline).all()
        if len(rows) == 0:
            print()
            print("Missed tasks:")
            print("Nothing is missed!")
            print()
            main_menu()
        else:
            print()
            print("Missed tasks:")
            x = 1
            for row in rows:
                row_task = row.task
                row_month_num = row.deadline.day
                row_month_name = row.deadline.strftime("%b")
                print(str(x) + ". " + row_task + ". " + str(row_month_num) + " " + row_month_name)
                x += 1
            print()
            main_menu()
    elif user_input == 5:

        print()
        print("Enter task")
        task_input = input()
        print("Enter deadline")
        deadline_input = input()
        deadline_input_date = datetime.strptime(deadline_input, "%Y-%m-%d")
        new_row = Table(task=task_input, deadline=deadline_input_date)
        session.add(new_row)
        session.commit()
        print("The task has been added!")
        print()
        main_menu()
    elif user_input == 6:
        print()
        rows = session.query(Table).order_by(Table.deadline).all()
        print("Choose the number of the task you want to delete:")
        x = 1
        for row in rows:
            row_task = row.task
            row_month_num = row.deadline.day
            row_month_name = row.deadline.strftime("%b")
            print(str(x) + ". " + row_task + ". " + str(row_month_num) + " " + row_month_name)
            x += 1
        user_input = int(input())
        row_to_delete = rows[user_input - 1]
        session.delete(row_to_delete)
        session.commit()
        print("The task has been deleted!")
        print()
        main_menu()
    elif user_input == 0:
        print()
        print("Bye!")


if __name__ == '__main__':
    main_menu()
