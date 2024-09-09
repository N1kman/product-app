from pydantic import BaseModel


class Language(BaseModel):
    abbr: str
    fullname: str


class LanguageRead(Language):
    id: int


class Translation(BaseModel):
    translated: str
    abbr_lang: str
