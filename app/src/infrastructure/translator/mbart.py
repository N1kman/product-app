import asyncio
import copy
import enum

from pydantic import BaseModel
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

from src.domain.interfaces import Language, ITranslator
from src.domain.interfaces.translator import IAsyncTranslator

model_name = "facebook/mbart-large-50-many-to-many-mmt"
model = MBartForConditionalGeneration.from_pretrained(model_name)
tokenizer = MBart50TokenizerFast.from_pretrained(model_name)


class MBartTranslator(IAsyncTranslator):

    @staticmethod
    async def async_translate_str(string: str, src_lang: Language, target_lang: Language):
        tokenizer.src_lang = src_lang.value
        encoded = await asyncio.to_thread(tokenizer, string, return_tensors="pt")
        generated_tokens = await asyncio.to_thread(model.generate, **encoded,
                                                   forced_bos_token_id=tokenizer.lang_code_to_id[
                                                       target_lang.value])
        res = await asyncio.to_thread(tokenizer.batch_decode, generated_tokens, skip_special_tokens=True)
        return res[0]

    async def async_translate_obj(self, obj: BaseModel, src_lang: Language, target_lang: Language):
        translated_obj = copy.deepcopy(obj)
        tokenizer.src_lang = src_lang.value

        for field, value in obj.__dict__.items():
            if not isinstance(value, enum.Enum) and isinstance(value, str):
                setattr(translated_obj, field, await self.async_translate_str(value, src_lang, target_lang))

            if isinstance(translated_obj, list):
                for item in translated_obj:
                    if isinstance(item, str):
                        item = await self.async_translate_str(item, src_lang, target_lang)
                    if isinstance(item, BaseModel):
                        item = await self.async_translate_obj(item, src_lang, target_lang)

            if isinstance(translated_obj, dict):
                for key, val in translated_obj.items():
                    if isinstance(val, str):
                        translated_obj[key] = await self.async_translate_str(val, src_lang, target_lang)
                    if isinstance(val, BaseModel):
                        translated_obj[key] = await self.async_translate_obj(val, src_lang, target_lang)

            if isinstance(value, BaseModel):
                setattr(translated_obj, field, await self.async_translate_obj(value, src_lang, target_lang))

        return translated_obj
