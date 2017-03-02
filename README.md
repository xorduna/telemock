### Telegram API emulator
tested with python 3.5

### Model:
```
    User: username, first_name, last_name, id (incremental by user), active (boolean), last_message_id
    Bot: botname, token, id (incremental)
    Chat: username, botname, active (boolean), id (incremental)
```

### Redis entities
```
    users:<username>
    bots:<botname>
    chats:<chat_id>
    last_chat_id: int
    last_user_id: int
```
