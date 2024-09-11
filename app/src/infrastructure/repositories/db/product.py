from sqlalchemy import select, func

from src.domain import LanguageEnum
from src.domain.entities import ProductRead, ProductReadWithTranslations, ProductWithTranslations, Translation, \
    ProductUpdateWithTranslations
from src.domain.interfaces.repository import IProductRepository
from src.infrastructure.models import ProductORM, TranslationORM
from src.infrastructure.repositories.db import DBRepository


class DBProductRepository(DBRepository, IProductRepository):

    async def add(
            self,
            product: ProductWithTranslations,
    ) -> ProductReadWithTranslations:
        table_id = ProductORM.__table__
        query = (
            select(
                func.coalesce(
                    func.max(TranslationORM.field_id),
                    0
                )
            )
            .filter(
                TranslationORM.table_id == table_id
            )
        )
        max_field_id = self.session.execute(query).scalar()

        product_orm = ProductORM(
            name_id=max_field_id + 1,
            description_id=max_field_id + 2,
            price=product.price,
            amount=product.amount,
            category_id=product.category_id,
            manufacturer_id=product.manufacturer_id,
        )
        self.session.add(product_orm)

        list_of_name_translations = list()
        for name in product.name:
            new_translation = TranslationORM(
                table_id=table_id,
                field_abbr=product_orm.name_id,
                lang_abbr=name.lang_abbr,
                translated=name.translated,
            )
            self.session.add(new_translation)
            list_of_name_translations.append(new_translation)

        list_of_description_translations = list()
        for description in product.description:
            new_translation = TranslationORM(
                table_id=table_id,
                field_abbr=product_orm.description_id,
                lang_abbr=description.lang_abbr,
                translated=description.translated,
            )
            self.session.add(new_translation)
            list_of_description_translations.append(new_translation)

        self.session.flush()

        product_read = ProductReadWithTranslations(
            id=product_orm.id,
            name=[Translation.model_validate(name, from_attributes=True)
                  for name in list_of_name_translations],
            description=[Translation.model_validate(description, from_attributes=True)
                         for description in list_of_description_translations],
            price=product_orm.price,
            amount=product_orm.amount,
            manufacturer_id=product_orm.manufacturer_id,
            category_id=product_orm.category_id,
        )

        return product_read

    async def delete(
            self, id: int
    ) -> None:
        pass

    async def update(
            self,
            id: int,
            product: ProductUpdateWithTranslations,
    ) -> ProductReadWithTranslations:
        pass

    async def get(
            self,
            id: int,
            language: LanguageEnum
    ) -> ProductRead:
        pass

    async def get_all(
            self,
            language: LanguageEnum
    ) -> list[ProductRead]:
        pass
