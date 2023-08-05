from pathlib import Path
from typing import Optional

from pydantic import AnyUrl, BaseModel, DirectoryPath, FileUrl, PostgresDsn
from sqlmodel import Field, SQLModel


class SshUrl(AnyUrl):
    allowed_schemes = {"ssh"}
    user_required = True


class SshRemote(BaseModel):
    url: SshUrl


class SqliteDsn(FileUrl):
    allowed_schemes = {"sqlite"}


class SqliteConn(BaseModel):
    dir: DirectoryPath
    file: Path
    url: SqliteDsn

    @classmethod
    def builder(cls, dir: DirectoryPath, file: Path):
        url: SqliteDsn = f"sqlite:///{dir}/{file}"  # pyright:ignore
        return cls(dir=dir, file=file, url=url)


class PostgresConn(BaseModel):
    url: PostgresDsn


class Host(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


# class Task(SQLModel):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     full_name: Optional[str] = Field(nullable=False)
#     version: int

#     @validator("full_name", always=True)
#     def generate_full_name(cls, x):
#         return f"{cls.__module__}.{cls.__qualname__}"

# class SpeTask(Task):
#     pass
