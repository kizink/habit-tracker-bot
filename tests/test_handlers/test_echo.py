import pytest

from unittest.mock import AsyncMock

from main import echo_handler


@pytest.mark.asyncio
async def test_text_message():
    text = 'perfect message is here'
    message_mock = AsyncMock(text=text)
    await echo_handler(message=message_mock)
    message_mock.answer.assert_called_with(text)


@pytest.mark.asyncio
async def test_non_text_message():
    message_mock = AsyncMock(text=None)
    await echo_handler(message=message_mock)
    message_mock.answer.assert_called_with('Ooops')
