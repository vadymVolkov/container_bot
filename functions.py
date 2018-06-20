import telebot
import commands

tbl = {}


class Function:
    def __init__(self, bot):
        self.bot = bot

    def main_menu(self, message):
        user_id = message.from_user.id
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Посмотреть список Таблиц')
        user_markup.row('Создать новую Таблицу')
        self.bot.send_message(user_id, 'Добро пожаловать! Выберите команду:', reply_markup=user_markup)

    def get_list_of_db(self, message):
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('В главное меню')
        user_id = message.from_user.id
        db_list = commands.get_tables_list_message()
        self.bot.send_message(user_id, db_list)
        self.bot.send_message(user_id, 'Напиши имя таблицы с которой хочешь работать', reply_markup=user_markup)

    def select_table(self, message):
        user_id = message.from_user.id
        db_from_list = commands.get_table_by_name(message.text)
        table_name = db_from_list[1]
        tbl['table name'] = table_name
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        is_exel_file_upload = db_from_list[3]
        is_table_active = db_from_list[2]
        is_file_format = db_from_list[4]
        is_file_in_db = db_from_list[5]
        if is_exel_file_upload == 1:
            if is_file_format == 1:
                if is_file_in_db == 1:
                    if is_table_active == 0:
                        user_markup.row('Активировать')
                    else:
                        user_markup.row('Деактивировать')
                else:
                    user_markup.row('Загрузить данные из exel файла в таблицу')
            else:
                user_markup.row('Форматировать exel файл')
        else:
            user_markup.row('Загрузить exel файл на сервер для таблицы')
        user_markup.row('Удалить таблицу')
        user_markup.row('В главное меню')
        msg = self.bot.send_message(user_id, 'Вы выбрали таблицу: ' + table_name + '\nЧто хотити с ней сделать?',
                                    reply_markup=user_markup)
        self.bot.register_next_step_handler(msg, self.table_commands)

    def table_commands(self, message):
        user_id = message.from_user.id
        response = message.text
        table_name = tbl['table name']
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        empty_keyboard = telebot.types.ReplyKeyboardRemove(selective=False)
        if response == 'Удалить таблицу':
            user_markup.row('В главное меню')
            commands.delete_table_by_name(table_name)
            self.bot.send_message(user_id, 'Таблица удалена', reply_markup=user_markup)
        elif response == 'Загрузить exel файл на сервер для таблицы':
            user_markup = telebot.types.ReplyKeyboardRemove()
            msg = self.bot.send_message(user_id, 'Отправь документ с данными на сегодняшний день',
                                        reply_markup=user_markup)
            self.bot.register_next_step_handler(msg, self.file_upload)
        elif response == 'Загрузить данные из exel файла в таблицу':
            user_markup.row('Продолжить работу с таблицей-' + table_name)
            user_markup.row('Посмотреть список Таблиц')
            user_markup.row('В главное меню')
            action_string = 'typing'
            file_name = table_name + '.xlsx'
            self.bot.send_message(user_id, 'Подождите идет загрузка файла', reply_markup=empty_keyboard)
            self.bot.send_chat_action(user_id, action_string)
            self.bot.send_message(user_id, 'Подождите еще немног', reply_markup=empty_keyboard)
            self.bot.send_chat_action(user_id, action_string)
            self.bot.send_message(user_id, 'Я напишу когда закончу', reply_markup=empty_keyboard)
            self.bot.send_chat_action(user_id, action_string)
            status = commands.upload_file_in_database(file_name, table_name)
            if status:
                commands.set_file_in_db_status(True, table_name)
                self.bot.send_message(user_id, 'Файл успешно загружен в таблицу', reply_markup=user_markup)
            else:
                self.bot.send_message(user_id, ' Произошла ошибка', reply_markup=user_markup)
        elif response == 'Форматировать exel файл':
            self.bot.send_message(user_id, 'Начинаем обработку файла, ожидайте команд',
                                  reply_markup=empty_keyboard)
            commands.delete_empty_city_cells_rows_file(table_name + '.xlsx')
            self.bot.send_message(user_id, 'Пустые ячейки удалены. Переходим к проверки имен городов',
                                  reply_markup=empty_keyboard)
            commands.change_city_name(table_name + '.xlsx')
            self.bot.send_message(user_id, 'Первый этап проверки пройден. Переходим ко второму этапу',
                                  reply_markup=empty_keyboard)
            unknown_city = commands.get_unique_unknown_citys(table_name + '.xlsx')
            tbl['unknown_city'] = unknown_city
            unknown_city_length = len(unknown_city)
            if unknown_city_length > 0:
                user_markup.row('Продолжить')
                user_markup.row('В главное меню')
                msg = self.bot.send_message(user_id,
                                            'Было найдено ' + str(unknown_city_length) + ' неизвестных городов',
                                            reply_markup=user_markup)
                self.bot.register_next_step_handler(msg, self.unknown_city_formating_step1)
            else:
                user_markup.row('Продолжить работу с таблицей-' + table_name)
                user_markup.row('Посмотреть список Таблиц')
                user_markup.row('В главное меню')
                commands.set_file_format_status(True, table_name)
                self.bot.send_message(user_id, 'Форматирование окончено.',
                                      reply_markup=user_markup)
        elif response == 'Активировать':
            user_markup.row('Продолжить работу с таблицей-' + table_name)
            user_markup.row('Посмотреть список Таблиц')
            user_markup.row('В главное меню')
            commands.set_table_status(True, table_name)
            self.bot.send_message(user_id, 'Таблица активирована.',
                                  reply_markup=user_markup)
        elif response == 'Деактивировать':
            user_markup.row('Продолжить работу с таблицей-' + table_name)
            user_markup.row('Посмотреть список Таблиц')
            user_markup.row('В главное меню')
            commands.set_table_status(False, table_name)
            self.bot.send_message(user_id, 'Таблица деактивирована.',
                                  reply_markup=user_markup)

    def create_new_table_step1(self, message):
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_id = message.from_user.id
        table_name = commands.name_generator()
        table_status = commands.check_table_in_db_by_name(table_name)
        if table_status:
            user_markup.row('В главное меню')
            self.bot.send_message(user_id, 'Таблица на сегодня уже есть', reply_markup=user_markup)
        else:
            user_markup.row('Создать таблицу')
            user_markup.row('В главное меню')
            msg = self.bot.send_message(user_id, 'Таблица будет создана под именем: ' + table_name,
                                        reply_markup=user_markup)
            self.bot.register_next_step_handler(msg, self.create_new_table_step2)

    def create_new_table_step2(self, message):
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('В главное меню')
        user_id = message.from_user.id
        if message.text == 'Создать таблицу':
            result = commands.create_new_table()
            if result:
                self.bot.send_message(user_id, 'Таблица была успешно создана', reply_markup=user_markup)
            else:
                self.bot.send_message(user_id, 'Произошла ошибка', reply_markup=user_markup)

    def file_upload(self, message):
        user_id = message.from_user.id
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        table_name = tbl['table name']
        user_markup.row('Продолжить работу с таблицей-' + table_name)
        user_markup.row('Посмотреть список Таблиц')
        user_markup.row('В главное меню')
        file_id = message.document.file_id
        file_info = self.bot.get_file(file_id)
        downloaded_file = self.bot.download_file(file_info.file_path)
        file_name = tbl['table name'] + '.xlsx'
        with open('data/' + file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
        commands.set_file_upload_status(True, table_name)
        self.bot.send_message(user_id, 'Документ получен', reply_markup=user_markup)

    def unknown_city_formating_step1(self, message):
        user_id = message.from_user.id
        empty_keyboard = telebot.types.ReplyKeyboardRemove(selective=False)
        unknown_city = tbl['unknown_city']
        msg = self.bot.send_message(user_id, 'Что это за город ' + unknown_city[0] + '?',
                                    reply_markup=empty_keyboard)
        self.bot.register_next_step_handler(msg, self.unknown_city_formating_step2)

    def unknown_city_formating_step2(self, message):
        user_id = message.from_user.id
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        empty_keyboard = telebot.types.ReplyKeyboardRemove(selective=False)
        table_name = tbl['table name']
        unknown_city = tbl['unknown_city']
        unknown_city_name = unknown_city[0]
        unknown_city.pop(0)
        entered_original_city_name = message.text
        tbl['unknown_city'] = unknown_city
        original_city_name_from_city_list = commands.check_if_original_city_in_city_table(entered_original_city_name)
        if original_city_name_from_city_list:
            commands.add_possible_city_name_to_original(original_city_name_from_city_list, unknown_city_name)
        else:
            commands.add_new_original_city_name_and_possible(entered_original_city_name, unknown_city_name)
        if len(unknown_city) > 0:
            msg = self.bot.send_message(user_id, 'Что это за город ' + unknown_city[0] + '?',
                                  reply_markup=empty_keyboard)
            self.bot.register_next_step_handler(msg, self.unknown_city_formating_step2)
        else:
            user_markup.row('Продолжить работу с таблицей-' + table_name)
            user_markup.row('Посмотреть список Таблиц')
            user_markup.row('В главное меню')
            commands.set_file_format_status(True, table_name)
            self.bot.send_message(user_id, 'Форматирование окончено.',
                                  reply_markup=user_markup)
