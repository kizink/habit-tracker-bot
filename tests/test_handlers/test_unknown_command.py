import pytest
import locale

from unittest.mock import AsyncMock, call, ANY
from keyboards import common_keyboards
from routers.FSM_states import Form
from routers.unknown_message import handle_unknown_message


@pytest.mark.asyncio
async def test_unknown_command(state_mock):
    locale.setlocale(locale.LC_CTYPE, ("ru_RU", "UTF-8"))
    command = '\\some_unknown_command'
    message_mock = AsyncMock(
        text=command,
        answer=AsyncMock()
    )

    await handle_unknown_message(message=message_mock, state=state_mock)

    message_mock.answer.assert_has_awaits(
        [
            call(
                text=f"Нераспознанная команда: {command}",
                reply_markup=ANY,
            ),
            call(
                text="Выберите действие",
                reply_markup=common_keyboards.get_menu_kb()
            )
        ]
    )
    state_mock.set_state.assert_called_with(Form.buttons)
