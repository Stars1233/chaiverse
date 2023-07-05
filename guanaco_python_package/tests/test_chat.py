import mock

from chai_guanaco.chat import Bot, BotConfig

@mock.patch('chai_guanaco.chat.requests')
def test_chat(mock_request):
    submission_id = 'test-model'
    developer_key = 'CR-devkey'

    config_bot = BotConfig(
        memory='Bot memory',
        prompt='Bot prompt',
        first_message='this is the first message',
        bot_label='Bot name')

    bot = Bot(submission_id, developer_key, config_bot)

    output = {'model_input': 'some_input', 'model_output': 'how are you?'}
    response = mock_request.post.return_value
    response.status_code = 200
    response.json.return_value = output

    out = bot.response('hey!')
    assert out == output

    expected_payload = {
        "memory": 'Bot memory',
        "prompt": 'Bot prompt',
        "chat_history": ['bot: this is the first message', 'user: hey!'],
        "bot_name": 'Bot name',
        "user_name": "You",
    }
    expected_url = "https://guanaco-submitter.chai-research.com/submissions/test-model/chat"
    expected_headers = {"Authorization": "Bearer CR-devkey"}
    mock_request.post.assert_called_once_with(
        url=expected_url,
        json=expected_payload,
        headers=expected_headers)

    bot.response('I am fine')
    expected_payload = {
        "memory": 'Bot memory',
        "prompt": 'Bot prompt',
        "chat_history": ['bot: this is the first message', 'user: hey!', 'bot: how are you?', 'user: I am fine'],
        "bot_name": 'Bot name',
        "user_name": "You",
    }
    mock_request.post.assert_called_with(
        url=expected_url,
        json=expected_payload,
        headers=expected_headers)
