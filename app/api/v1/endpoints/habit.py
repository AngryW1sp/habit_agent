from fastapi import APIRouter

from app.api.deps import SessionDep
from app.schemas.habit import HabitCreate, HabitRead
from app.crud.habit import habit_crud
router = APIRouter(prefix='/habits', tags=['habits'])


@router.get('/',
            response_model=list[HabitRead],
            summary='Список привычек',
            description='Эндпоинт для получения списка привычек')
async def get_habits(session: SessionDep) -> list[HabitRead]:
    result = await habit_crud.get_multi(session)
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
    result = await habit_crud.create(session, habit)
    return result
