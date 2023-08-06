from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
Base = declarative_base()


class Task(Base):
   __tablename__ = 'tasks'
   
   id = Column(Integer, primary_key=True)
   name = Column(String)
   description = Column(String)
   children = relationship("WorkBlock", cascade="all,delete", backref="tasks")


class WorkBlock(Base):
   __tablename__ = 'work_blocks'
   
   id = Column(Integer, primary_key=True)
   task_id = Column(Integer, ForeignKey("tasks.id"))
   start_time = Column(Integer)
   finish_time = Column(Integer)

class TrackerDB:
   def __init__(self, db_name):
      self.db_name = db_name
      self.testing = False

   def connect(self):
      engine = self._engine()
      Session = sessionmaker(bind=engine)
      return Session()

   def create(self):
      engine = self._engine()
      self.meta_data = MetaData()
      self._create_tasks_table()
      self._create_work_block_table()
      self.meta_data.create_all(engine)
      return engine

   def _engine(self):
      if self.testing:
         return create_engine(f"sqlite+pysqlite:///{self.db_name}",
                              echo=True, future=True)
      else:
         return create_engine(f"sqlite+pysqlite:///{self.db_name}", future=True)

   def _create_tasks_table(self):
      return Table(
       'tasks', self.meta_data,
       Column('id', Integer, primary_key=True),
       Column('name', Integer),
       Column('description', Integer)
    )

   def _create_work_block_table(self):
      return Table(
       'work_blocks', self.meta_data,
       Column('id', Integer, primary_key=True),
       Column('task_id', Integer),
       Column('start_time', Integer),
       Column('finish_time', Integer)
    )
