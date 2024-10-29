from fastapi import FastAPI
from fastapi import APIRouter, UploadFile, File
from prilavok import AddToysValidator, DeleteToysValidator, EditToysValidator, Image

from typing import List

from database.prilavokservice import (add_toy_photo_db, edit_toy_db, add_toy_db,
                                      get_exact_toy_db, get_all_toys_db, delete_toy_db)

toy_router = APIRouter(prefix='/игрушка', tags=['Управление игрушками'])


@toy_router.post('/добовление игрушки')
async def add_toy(data: AddToysValidator):
    result = add_toy_db(**data.model_dump())

    if result:
        return {'message': result}
    else:
        return {'message': 'Такая игрушка уже есть в бд'}


@toy_router.get('/получение игрушки')
async def get_exact_toy(toy_id: int = 0):
    if toy_id == 0:
        toys = get_all_toys_db()
        return {'toys': toys}
    else:
        toy = get_exact_toy_db(toy_id)
        return {'toy': toy}


@toy_router.delete('/удаление игрушки')
async def delete_toy(data: DeleteToysValidator):
    result = delete_toy_db(**data.model_dump())

    if result:
        return {'message': result}
    else:
        return {'message': 'Игрушка не найдена'}


@toy_router.put('/изменение инфо об игрушке')
async def edit_toy(data: EditToysValidator):
    change_data = data.model_dump()

    result = edit_toy_db(**change_data)
    if result:
        return {'message': result}
    else:
        return {'message': "Игрушка не найдена"}


@toy_router.post('/добавление картинки для игрушки')
async def add_photo(toy_id: int, toy_photo: UploadFile = File(...)):
    with open(f'media_igreshel/{toy_photo.filename}', 'wb+') as file:
        photo_igrushek = await toy_photo.read()
        file.write(photo_igrushek)

    photo = add_toy_photo_db(toy_id=toy_id, toy_photo=f'/media/{toy_photo.filename}')

    return {'message': {"Картинка успешно сохранена": photo}}
