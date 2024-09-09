from pydantic import BaseModel


class Language(BaseModel):
    abbr: str
    fullname: str


class LanguageRead(Language):
    pass


class Translation(BaseModel):
    translated: str
    lang_abbr: str
