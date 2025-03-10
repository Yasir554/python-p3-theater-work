from sqlalchemy import ForeignKey, Column, Integer, String, Boolean, MetaData, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

engine = create_engine("sqlite:///moringa_theater.db")

session = sessionmaker(bind=engine)
session = session()

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Auditions(Base):
    __tablename__ = 'auditions'

    id = Column(Integer, primary_key=True)
    actor = Column(String, nullable=False)
    location = Column(String, nullable=False)
    phone = Column(Integer, nullable=False)
    hired = Column(Boolean, default=False)

    role_id = Column(Integer, ForeignKey("roles.id"))
    role=relationship("Role", back_populates="audition")

    def call_back(self):
        self.hired = True
        session.add(self)
        session.commit()

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    
    audition=relationship("Auditions", back_populates="role", cascade="all, delete")

    @property
    def actors(self):
        return [audition.actor for audition in self.audition]
    
    @property
    def locations(self):
        return [audition.location for audition in self.audition]
    
    def lead(self):
        hired_audition = [audition for audition in self.audition if audition.hired]
        if hired_audition:
            return hired_audition[0]
        else:
            return "no actor has been hired for this role" 
    
    def understudy(self):
        hired_audition = [audition for audition in self.audition if audition.hired]
        if len(hired_audition) > 1:
            return hired_audition[1]
        else:
            return "no actor has been hired for this role"

Base.metadata.create_all(engine)