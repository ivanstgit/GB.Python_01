import os.path
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, CallbackQueryHandler
import calculator
import telbook

current_command: str

LEVEL_0 = 0
LEVEL_1_CALC = 1
LEVEL_1_TELBOOK = 2
LEVEL_2_TELBOOK = 3
TMP_FOLDER = 'temp'
COMMAND_PATH_DELIMITER = '-'


def log(update: Update, context: CallbackContext) -> None:
    log_txt = update.message.text if update.message else update.to_json()
    with open(os.path.join(TMP_FOLDER, 'log.csv'), 'a') as logfile:
        logfile.write(f'{update.effective_user.first_name},{update.effective_user.id}, {log_txt}\n')


def start_command(update: Update, context: CallbackContext):
    log(update, context)
    context.user_data['current_command'] = None
    if update.message:
        update.message.reply_text(text="Выберите программу", reply_markup=InlineKeyboardMarkup(LEVEL_0_KEYBOARD))
    elif update.callback_query:
        query = update.callback_query
        query.answer()
        query.edit_message_text(text="Выберите программу", reply_markup=InlineKeyboardMarkup(LEVEL_0_KEYBOARD))
    return LEVEL_0


def end_command(update: Update, context: CallbackContext):
    log(update, context)
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Выход")
    context.user_data['current_command'] = None
    return ConversationHandler.END


def help_command(update: Update, context: CallbackContext) -> None:
    log(update, context)
    update.message.reply_text(f'/calc\n/telbook\n/help')


def calc_command(update: Update, context: CallbackContext):
    log(update, context)
    if update.message:
        update.message.reply_text(calculator.get_help())
    elif update.callback_query:
        context.user_data['current_command'] = 'calc'
        query = update.callback_query
        query.answer()
        query.edit_message_text(text=calculator.get_help(), reply_markup=InlineKeyboardMarkup(LEVEL_1_CALC_KEYBOARD))
    return LEVEL_1_CALC


def telbook_command(update: Update, context: CallbackContext):
    # обработка кнопок для работы с файлами
    log(update, context)
    if update.message:
        update.message.reply_text(telbook.init())
    elif update.callback_query:
        context.user_data['current_command'] = 'telbook'
        query = update.callback_query
        query.answer()
        tb_path = query.data.split(COMMAND_PATH_DELIMITER)
        tb_command = '' if len(tb_path) == 1 else tb_path[1]
        if tb_command == '':
            message_text = telbook.init()
        elif tb_command == 'qa':
            message_text = telbook.abort()
            query.edit_message_text(text=message_text,
                                    reply_markup=InlineKeyboardMarkup(LEVEL_0_KEYBOARD))
            context.user_data.clear()
            return LEVEL_0
        elif tb_command == 'qw':
            message_text = telbook.commit()
            query.edit_message_text(text=message_text,
                                    reply_markup=InlineKeyboardMarkup(LEVEL_0_KEYBOARD))
            context.user_data.clear()
            return LEVEL_0
        elif tb_command == 'e':
            local_file_name = os.path.join(TMP_FOLDER, str(update.effective_user.id) + '.txt')
            message_text = telbook.export_file(local_file_name)
            context.bot.send_document(query.message.chat_id,
                                      document=open(local_file_name, 'r', encoding=telbook.BASE_ENCODING))
        else:
            message_text = telbook.get_help(tb_command)

        context.user_data['telbook_command'] = tb_command

        query.edit_message_text(text=message_text,
                                reply_markup=InlineKeyboardMarkup(LEVEL_1_TELBOOK_KEYBOARD))
    return LEVEL_1_TELBOOK


def text_message_callback(update: Update, context: CallbackContext):
    log(update, context)
    print(context.user_data.get('current_command'))
    if context.user_data.get('current_command') == 'calc':
        update.message.reply_text(
            text=calculator.execute_command(update.message.text),
            reply_markup=InlineKeyboardMarkup(LEVEL_1_CALC_KEYBOARD))
    elif context.user_data.get('current_command') == 'telbook' \
            and context.user_data.get('telbook_command') == 'set_sep':
        update.message.reply_text(
            text=telbook.set_separators(update.message.text),
            reply_markup=InlineKeyboardMarkup(LEVEL_1_TELBOOK_KEYBOARD))
    # return None


def doc_message_callback(update: Update, context: CallbackContext):
    log(update, context)
    if context.user_data.get('current_command') == 'telbook' \
            and context.user_data.get('telbook_command') == 'i':
        # import
        in_file = update.message.effective_attachment.get_file()
        local_file_name = os.path.join(TMP_FOLDER, str(update.effective_user.id) + '.txt')
        in_file.download(local_file_name)
        update.message.reply_text(
            text=telbook.import_file(local_file_name),
            reply_markup=InlineKeyboardMarkup(LEVEL_1_TELBOOK_KEYBOARD))


COMMANDS = {
    'start': start_command,
    'help': help_command,
    'calc': calc_command,
    'telbook': telbook_command,
    'end': end_command
}

LEVEL_0_KEYBOARD = [
    [
        InlineKeyboardButton("Калькулятор", callback_data='calc'),
        InlineKeyboardButton("Телефонный справочник", callback_data='telbook')
    ]
]

LEVEL_1_CALC_KEYBOARD = [
    [
        InlineKeyboardButton("Выход", callback_data='end'),
        InlineKeyboardButton("В начало", callback_data='start')
    ]
]

LEVEL_1_TELBOOK_KEYBOARD = list([[InlineKeyboardButton(op_txt,
                                                       callback_data=COMMAND_PATH_DELIMITER.join(['telbook', op]))]
                                 for op, op_txt in telbook.INPUT_OPERATIONS.items()])

COMMAND_HANDLER_SETTINGS = {
    'entry_points': [CommandHandler('start', COMMANDS['start'])],
    'states': {  # словарь состояний разговора, возвращаемых callback функциями
        LEVEL_0: [
            CallbackQueryHandler(COMMANDS['calc'], pattern='^' + 'calc' + '$'),
            CallbackQueryHandler(COMMANDS['telbook'], pattern='^' + 'telbook' + '$'),
        ],
        LEVEL_1_CALC: [
            CallbackQueryHandler(COMMANDS['start'], pattern='^' + 'start' + '$'),
            CallbackQueryHandler(COMMANDS['end'], pattern='^' + 'end' + '$'),
        ],
        LEVEL_1_TELBOOK: [
            CallbackQueryHandler(COMMANDS['telbook'], pattern='^' + 'telbook_' + '*'),
            CallbackQueryHandler(COMMANDS['start'], pattern='^' + 'start' + '$'),
            CallbackQueryHandler(COMMANDS['end'], pattern='^' + 'end' + '$'),
        ],
    },
    'fallbacks': [CommandHandler('start', COMMANDS['start'])]
}
