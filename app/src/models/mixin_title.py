from sqlalchemy import Column, String


class MixinTitle:
    title = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
