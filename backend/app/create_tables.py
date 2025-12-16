from app.database import Base, engine
from app.models.user import User  # Import all your models here

Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
