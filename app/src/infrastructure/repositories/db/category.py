from sqlalchemy import select, func, delete, and_

from src.domain import LanguageEnum
from src.domain.entities import (
    CategoryRead,
    CategoryWithTranslations,
    CategoryReadWithTranslations,
    CategoryUpdateWithTranslations,
)
from src.domain.entities.language import Translation
from src.domain.interfaces.repository import ICategoryRepository
from src.infrastructure.models import CategoryORM, TranslationORM
from src.infrastructure.repositories.db import DBRepository
from src.infrastructure.repositories.exceptions import BadRequest, NoSuchItem


class DBCategoryRepository(DBRepository, ICategoryRepository):
    async def add(
            self,
            category: CategoryWithTranslations
    ) -> CategoryReadWithTranslations:
        table_id = CategoryORM.__tablename__
        query = (
            select(
                func.coalesce(
                    func.max(
                        TranslationORM.field_id
                    ),
                    0
                )
            )
            .filter(
                TranslationORM.table_id == table_id
            )
        )
        max_field_id = await self.session.execute(query)
        max_field_id = max_field_id.scalar()

        category_orm = CategoryORM(
            name_id=max_field_id + 1,
        )
        self.session.add(category_orm)

        list_of_name_translations = list()
        for name in category.name:
            new_translation = TranslationORM(
                table_id=table_id,
                field_id=category_orm.name_id,
                lang_abbr=name.lang_abbr,
                translated=name.translated,
            )
            self.session.add(new_translation)
            list_of_name_translations.append(new_translation)

        await self.session.flush()

        category_read = CategoryReadWithTranslations(
            id=category_orm.id,
            name=[Translation.model_validate(name, from_attributes=True)
                  for name in list_of_name_translations],
        )

        return category_read

    async def delete(self, id: int) -> None:
        query = (
            select(
                CategoryORM
            )
            .filter(
                CategoryORM.id == id
            )
        )
        result = await self.session.execute(query)
        category_orm: CategoryORM = result.scalars().first()

        if category_orm is None:
            raise BadRequest(f"Category with id {id} not found")

        stmt = (
            delete(
                TranslationORM
            )
            .where(
                TranslationORM.field_id == category_orm.name_id
            )
        )

        await self.session.execute(stmt)
        await self.session.delete(category_orm)

    async def update(self, id: int, category: CategoryUpdateWithTranslations) -> CategoryReadWithTranslations:
        query = (
            select(
                CategoryORM
            )
            .filter(
                CategoryORM.id == id
            )
        )
        result = await self.session.execute(query)
        category_orm: CategoryORM = result.scalars().first()

        if category_orm is None:
            raise BadRequest(f"Category with id {id} not found")

        stmt = (
            select(
                TranslationORM
            )
            .filter(
                TranslationORM.field_id == category_orm.name_id
            )
        )
        result = await self.session.execute(stmt)
        list_of_name_translations: list[TranslationORM] = result.scalars().all()

        if len(category.name) > 0:
            for new_name in category.name:
                for old_name in list_of_name_translations:
                    if old_name.lang_abbr == new_name.lang_abbr:
                        old_name.translated = new_name.translated
                        break

        category_read = CategoryReadWithTranslations(
            id=category_orm.id,
            name=[Translation.model_validate(name, from_attributes=True)
                  for name in list_of_name_translations],
        )
        return category_read

    async def get(self, id: int, language: LanguageEnum) -> CategoryRead:
        query = (
            select(
                CategoryORM
            )
            .filter(
                CategoryORM.id == id
            )
        )
        result = await self.session.execute(query)
        category_orm: CategoryORM = result.scalars().first()

        if category_orm is None:
            raise BadRequest(f"Category with id {id} not found")

        stmt = (
            select(
                TranslationORM
            )
            .filter(
                and_(
                    TranslationORM.field_id == category_orm.name_id,
                    TranslationORM.lang_abbr == language.value,
                )
            )
        )
        result = await self.session.execute(stmt)
        name: TranslationORM = result.scalars().first()

        if name is None:
            raise NoSuchItem(f"Category with id {id} does not have translation in {language.value}")

        category_read = CategoryRead(
            id=category_orm.id,
            name=name.translated,
        )

        return category_read

    async def get_all(self, language: LanguageEnum) -> list[CategoryRead]:
        query = (
            select(
                CategoryORM
            )
        )
        result = await self.session.execute(query)
        categories_orm: list[CategoryORM] = result.scalars().all()

        if len(categories_orm) <= 0:
            raise NoSuchItem(f"Categories not found")

        stmt = (
            select(
                TranslationORM
            )
            .filter(
                and_(
                    TranslationORM.table_id == CategoryORM.__tablename__,
                    TranslationORM.lang_abbr == language.value,
                )
            )
        )
        result = await self.session.execute(stmt)
        names: list[TranslationORM] = result.scalars().all()

        if len(names) <= 0:
            raise NoSuchItem(f"Categories do not have translations in {language.value}")

        categories_read = list()

        for category_orm in categories_orm:
            for name in names:
                if category_orm.name_id == name.field_id:
                    categories_read.append(
                        CategoryRead(
                            id=category_orm.id,
                            name=name.translated,
                        )
                    )
                    break

        return categories_read
