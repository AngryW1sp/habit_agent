from fastapi import APIRouter, HTTPException

from app.api.deps import SessionDep
from app.schemas.habit import HabitComplete, HabitCreate, HabitRead, HabitUpdate
from app.crud.habit import habit_crud
from app.services.habit import complete_habit_for_today, create_habit_service, habit_update, remove_habit
router = APIRouter(prefix='/habits', tags=['habits'])


@router.get('/',
            response_model=list[HabitRead],
            summary='Список привычек',
            description='Эндпоинт для получения списка привычек')
async def get_habits(session: SessionDep) -> list[HabitRead]:
    result = await habit_crud.get_multi(session)
    return result


@router.get('/not_complete',
            response_model=list[HabitRead],)
async def get_not_complete_habits(session: SessionDep):
    result = await habit_crud.get_not_complete(session)
    return result


@router.post('/complete/{habit_id}',
             response_model=HabitRead)
async def complete_habit(session: SessionDep, habit_id, habit_in: HabitComplete):
    result = await complete_habit_for_today(session, habit_id, habit_in)
    return result


@router.get('/{habit_id}',
            response_model=HabitRead,
            summary='Получение привычки по id',
            description='Эндпоинт для получения конкретной привычки')
async def get_habit(habit_id: int, session: SessionDep) -> HabitRead:
    result = await habit_crud.get(session, habit_id)
    return result


@router.post('/',
             response_model=HabitRead,
             status_code=201,
             summary='Создать привычку',
             description='Эндпоинт для создания новой привычки',)
async def create_habit(habit: HabitCreate, session: SessionDep) -> HabitRead:
    result = await create_habit_service(session, habit)
    return result


@router.patch('/{habit_id}',
              response_model=HabitRead,
              summary='Обновление привычки',
              description='Эндпоинт служит для различных обновлений привычек',
              response_model_exclude_none=True)
async def update_habit(habit_id: int, habit: HabitUpdate, session: SessionDep):
    result = await habit_update(habit, habit_id, session)
    return result


@router.delete('/{habit_id}',
               response_model=HabitRead,
               summary='Удаление привычки',
               description='Эндпоинт для удаления привычки')
async def delete_habit(session: SessionDep, habit_id):
    result = await remove_habit(session, habit_id)
    return result
