### Telegram API emulator

### Model:
```
    User: username, id (incremental by user), active (boolean), last_message_id
    Bot: botname, token, id (incremental)
    Chat: username, botname, id (incremental)
```

### Redis entities
```
    users:<user_id>
    bots:<botname>
    chats:<chat_id>
    last_chat_id: int
    last_user_id: int
```
