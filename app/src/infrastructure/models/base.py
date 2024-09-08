from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


class Base(DeclarativeBase):
    __abstract__ = True

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        cols = [f'{col}={getattr(self, col)}' for indx, col in enumerate(self.__table__.columns.keys()) if
                col in self.repr_cols or indx < self.repr_cols_num]
        return f'<{self.__class__.__name__} {",".join(cols)}>'
