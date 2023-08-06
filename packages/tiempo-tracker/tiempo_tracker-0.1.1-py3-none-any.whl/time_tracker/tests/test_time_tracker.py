import pytest
import string
from faker import Faker
import random
from time_tracker.time_tracker import TimeTracker
from time_tracker.db import Task, WorkBlock, TrackerDB
from sqlalchemy.orm import sessionmaker

TASKS_NUM = 3
WORK_BLOCKS_PER_TASK = 2
# time is always the same to make tests consistent
# set in epoch seconds
TIME_BASE = 1662374970
MINUTE = 60 # sec
HOUR = 60 * MINUTE

# generate random task name, currently not used to ensure tests consistency
def gen_task_name():
    return ''.join(list(map(
                            lambda _: random.choice(string.ascii_letters), 
                            range(random.randint(3,10))))).capitalize()


@pytest.fixture()
def test_db():
    fake = Faker()

    engine = TrackerDB(':memory:').create()
    Session = sessionmaker(bind=engine)
    session = Session()

    # gen names in list outside fixture so it can be used to check values
    for i in range(1, TASKS_NUM+1):
        session.add(
                    Task(name = f'Task {i}', 
                         description = fake.text(max_nb_chars=40))
                    )
        session.commit()

        for j in range (1, WORK_BLOCKS_PER_TASK+1):
            session.add(
                        WorkBlock(task_id = i,
                                  start_time = TIME_BASE + i * (j * 10 + j) * MINUTE,
                                  finish_time = TIME_BASE + i * (j * 20 + j) * MINUTE)
                        )
        session.commit()

    return session

def test_task_add(test_db):
    task_name = 'Test task'
    time_tracker = TimeTracker(test_db)
    time_tracker.task_add(task_name)

    assert test_db.query(Task).filter(Task.name == task_name).one().name == task_name
    assert len(test_db.query(Task).filter(Task.name == task_name).all()) == 1

    # can't be two tasks with same name
    time_tracker.task_add(task_name)
    assert len(test_db.query(Task).filter(Task.name == task_name).all()) == 1


def test_task_remove(test_db):
    # check if task is removed with all related work blocks
    task_to_delete = 'Task 1'
    task_id = test_db.query(Task).filter(Task.name == task_to_delete).one().id
    tasks_num_before = len(test_db.query(Task).limit(-1).all())

    work_blocks_before = len(test_db.query(WorkBlock).filter(WorkBlock.task_id == task_id).all())

    time_tracker = TimeTracker(test_db)
    time_tracker.task_remove(task_to_delete)
    tasks_num_after = len(test_db.query(Task).limit(-1).all())
    work_blocks_after = len(test_db.query(WorkBlock).filter(WorkBlock.task_id == task_id).all())

    assert tasks_num_after == tasks_num_before - 1
    assert work_blocks_before > 0
    assert work_blocks_after == 0

    # try to delete task that doesn't exist
    time_tracker.task_remove(task_to_delete)


def test_task_start(test_db):
    work_blocks_num_before = len(test_db.query(WorkBlock).limit(-1).all())
    time_tracker = TimeTracker(test_db)
    time_tracker.task_start('Task 1')
    work_blocks_num_after = len(test_db.query(WorkBlock).limit(-1).all())
    active_tasks_num = len(test_db.query(WorkBlock).\
                           filter(WorkBlock.finish_time == None).all())

    assert work_blocks_num_after == work_blocks_num_before + 1
    assert active_tasks_num == 1

    # can't start task that doesn't exist
    time_tracker.task_start('non_existent_task')
    work_blocks_num_after2 = len(test_db.query(WorkBlock).limit(-1).all())
    assert work_blocks_num_after == work_blocks_num_after2


def test_task_start_twice(test_db):
    # start same task twice
    time_tracker = TimeTracker(test_db)
    time_tracker.task_start('Task 1')
    active_task_id1 = test_db.query(WorkBlock).\
                              filter(WorkBlock.finish_time == None).one().task_id
    time_tracker.task_start('Task 1')
    active_task_id2 = test_db.query(WorkBlock).\
                              filter(WorkBlock.finish_time == None).one().task_id
    active_tasks_num = len(test_db.query(WorkBlock).\
                           filter(WorkBlock.finish_time == None).all())

    assert active_tasks_num == 1
    assert active_task_id1 == active_task_id2


def test_task_start_second(test_db):
    # start new task when another is in progress
    time_tracker = TimeTracker(test_db)
    time_tracker.task_start('Task 1')
    active_task_id1 = test_db.query(WorkBlock).\
                              filter(WorkBlock.finish_time == None).one().task_id
    time_tracker.task_start('Task 2')
    work_blocks_num_after = len(test_db.query(WorkBlock).limit(-1).all())
    active_task_id2 = test_db.query(WorkBlock).\
                              filter(WorkBlock.finish_time == None).one().task_id

    assert active_task_id1 ==  1
    assert active_task_id2 ==  2


def test_task_finish(test_db):
    time_tracker = TimeTracker(test_db)

    active_tasks_num_before1 = len(test_db.query(WorkBlock).\
                                 filter(WorkBlock.finish_time == None).all())
    time_tracker.task_start('Task 1')
    active_tasks_num_before = len(test_db.query(WorkBlock).\
                                 filter(WorkBlock.finish_time == None).all())

    time_tracker.task_finish()
    active_tasks_num_after = len(test_db.query(WorkBlock).\
                                 filter(WorkBlock.finish_time == None).all())

    assert active_tasks_num_before1 == 0
    assert active_tasks_num_before == 1
    assert active_tasks_num_after == 0

    # should handle correctly attempt to finish task twice
    time_tracker.task_finish()


def test_task_status(test_db):
    time_tracker = TimeTracker(test_db)
    response = time_tracker.task_status()
    assert response.find('Task in progress') == -1
    assert response.find('No task is active') > -1

    time_tracker.task_start('Task 1')
    response = time_tracker.task_status()
    assert response.find('Task in progress') > -1
    assert response.find('No task is active') == -1

def test_tasks_list(test_db):
    time_tracker = TimeTracker(test_db)
    tasks_list = time_tracker.tasks_list()
    assert set(tasks_list.split('\n')) == set([f'Task {i}' for i in range(1, TASKS_NUM+1)])

def test_tasks_stats(test_db):
    time_tracker = TimeTracker(test_db, epoch_time=TIME_BASE)
    # add task from previous day
    test_db.add(
                WorkBlock(task_id = 1,
                          start_time = TIME_BASE - 24 * HOUR,
                          finish_time = TIME_BASE - 24 * HOUR + 15 * MINUTE)
                )
    test_db.commit()

    time_tracker.tasks_stats()