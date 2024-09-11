import copy
import enum


from pydantic import BaseModel
from transformers import MarianMTModel, MarianTokenizer

from src.domain.interfaces.translator import IAsyncTranslator
from src.domain.language import LanguageEnum

tokenizer_ru = MarianTokenizer.from_pretrained(
    "Helsinki-NLP/opus-mt-en-ru",
    clean_up_tokenization_spaces=True,
)
model_ru = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-en-ru")

tokenizer_de = MarianTokenizer.from_pretrained(
    "Helsinki-NLP/opus-mt-en-de",
    clean_up_tokenization_spaces=True,
)
model_de = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-en-de")

convert_model = {
    "ru": model_ru,
    "de": model_de,
}

convert_tokenizer = {
    "ru": tokenizer_ru,
    "de": tokenizer_de,
}


class MBartTranslator(IAsyncTranslator):

    def translate_str(self, string: str, target_lang: LanguageEnum):
        if target_lang == LanguageEnum.EN:
            return string
        model = convert_model.get(target_lang.value)
        tokenizer = convert_tokenizer.get(target_lang.value)
        encoded = tokenizer(string, return_tensors="pt", truncation=True)
        generated_tokens = model.generate(
            **encoded,
            max_length=400,
            num_return_sequences=1,
        )
        res = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
        return res[0]

    def translate_obj(self, obj: BaseModel, target_lang: LanguageEnum):
        translated_obj = copy.deepcopy(obj)

        for field, value in obj.__dict__.items():
            if not isinstance(value, enum.Enum) and isinstance(value, str):
                setattr(translated_obj, field, self.translate_str(value, target_lang))

            if isinstance(translated_obj, list):
                for item in translated_obj:
                    if isinstance(item, str):
                        item = self.translate_str(item, target_lang)
                    elif isinstance(item, BaseModel):
                        item = self.translate_obj(item, target_lang)

            if isinstance(translated_obj, dict):
                for key, val in translated_obj.items():
                    if isinstance(val, str):
                        translated_obj[key] = self.translate_str(val, target_lang)
                    if isinstance(val, BaseModel):
                        translated_obj[key] = self.translate_obj(val, target_lang)

            if isinstance(value, BaseModel):
                setattr(translated_obj, field, self.translate_obj(value, target_lang))

        return translated_obj
