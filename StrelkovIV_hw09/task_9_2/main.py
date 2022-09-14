# Прикрутить бота к задачам с предыдущего семинара:
# Создать калькулятор для работы с рациональными и комплексными числами, организовать меню,
# добавив в неё систему логирования
# Создать телефонный справочник с возможностью импорта и экспорта данных в нескольких форматах.

from telegram.ext import Updater, ConversationHandler, MessageHandler, Filters
import bot_commands

updater = Updater(input("HASH: "))

conv_handler = ConversationHandler(
        entry_points=bot_commands.COMMAND_HANDLER_SETTINGS['entry_points'],
        states=bot_commands.COMMAND_HANDLER_SETTINGS['states'],
        fallbacks=bot_commands.COMMAND_HANDLER_SETTINGS['fallbacks'],
        per_message=False
    )

# Добавляем `ConversationHandler` в диспетчер, который будет использоваться для обработки обновлений
updater.dispatcher.add_handler(conv_handler)
updater.dispatcher.add_handler(MessageHandler(Filters.text, callback=bot_commands.text_message_callback))
updater.dispatcher.add_handler(MessageHandler(Filters.document, callback=bot_commands.doc_message_callback))
# for command, handler in COMMANDS.items():
#     updater.dispatcher.add_handler(CommandHandler(command, handler))

print('server start')
updater.start_polling()
updater.idle()
