import logging

from sqlalchemy.orm import declarative_base


logger = logging.getLogger(__file__)

Base = declarative_base()
metadata = Base.metadata



