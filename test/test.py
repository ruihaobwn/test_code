from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql://root:mysql@localhost/test')
Base = declarative_base()

class User(Base):
     __tablename__ = 'users'

     id = Column(Integer, primary_key=True)
     name = Column(String(20))
     fullname = Column(String(20))
     password = Column(String(20))

     def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
                             self.name, self.fullname, self.password)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

ed_user = User(name='ed',fullname='Ed Jones',password='edspassword')
session.add(ed_user)
our_user=session.query(User).filter_by(name='ed').first()
print our_user

session.add_all([
	 User(name='wendy', fullname='Wendy Williams', password='foobar'),
     User(name='mary', fullname='Mary Contrary', password='xxg527'),
     User(name='fred', fullname='Fred Flinstone', password='blah')
])

ed_user.password='Hello'


Hello World!



