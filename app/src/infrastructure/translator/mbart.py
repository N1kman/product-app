import asyncio
import copy

from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

from src.domain.interfaces import Language, ITranslator
from src.domain.interfaces.translator import IAsyncTranslator

model_name = "facebook/mbart-large-50-many-to-many-mmt"
model = MBartForConditionalGeneration.from_pretrained(model_name)
tokenizer = MBart50TokenizerFast.from_pretrained(model_name)


class MBartTranslator(ITranslator, IAsyncTranslator):
    async def async_translate_obj(self, obj: object, src_lang: Language, target_lang: Language):
        translated_obj = copy.deepcopy(obj)
        tokenizer.src_lang = src_lang.value

        for field, value in obj.__dict__.items():
            if isinstance(value, str):
                tokenizer.src_lang = src_lang.value
                encoded = await asyncio.to_thread(tokenizer, value, return_tensors="pt")
                generated_tokens = await asyncio.to_thread(model.generate, **encoded,
                                                           forced_bos_token_id=tokenizer.lang_code_to_id[
                                                               target_lang.value])
                res = await asyncio.to_thread(tokenizer.batch_decode, generated_tokens, skip_special_tokens=True)
                setattr(translated_obj, field, res[0])

        return translated_obj

    def translate_obj(self, obj: object, src_lang: Language, target_lang: Language):
        translated_obj = copy.deepcopy(obj)
        tokenizer.src_lang = src_lang.value

        for field, value in obj.__dict__.items():
            if isinstance(value, str):
                encoded = tokenizer(value, return_tensors="pt")
                generated_tokens = model.generate(
                    **encoded,
                    forced_bos_token_id=tokenizer.lang_code_to_id[target_lang.value]
                )
                res = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
                setattr(translated_obj, field, res)

        return translated_obj
