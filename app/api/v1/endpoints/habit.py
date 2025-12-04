from fastapi import APIRouter

from app.api.deps import SessionDep
from app.schemas.habit import HabitCreate, HabitRead, HabitUpdate
from app.crud.habit import habit_crud
from app.services.habit import habit_completely
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


@router.patch('/{habit_id}',
              response_model=HabitRead,
              summary='Обновление привычки',
              description='Эндпоинт служит для различных обновлений привычек',
              response_model_exclude_none=True)
async def update_habit(habit_id: int, habit: HabitUpdate, session: SessionDep):
    result = await habit_completely(habit, habit_id, session)
    return result
