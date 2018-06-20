import telebot
import commands
import time

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
        db_list = commands.get_tables_list_message_for_client()
        self.bot.send_message(user_id, db_list)
        self.bot.send_message(user_id, 'Напиши имя таблицы с которой хочешь работать', reply_markup=user_markup)

    def select_table(self, message):
        user_id = message.from_user.id
        db_from_list = commands.get_table_by_name(message.text)
        table_name = db_from_list[1]
        tbl['table name'] = table_name
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Найти контейнер по городу')
        user_markup.row('В главное меню')

        msg = self.bot.send_message(user_id, 'Вы выбрали таблицу: ' + str(table_name) + '\nЧто хотити с ней сделать?',
                                    reply_markup=user_markup)
        self.bot.register_next_step_handler(msg, self.table_commands)

    def table_commands(self, message):
        user_id = message.from_user.id
        response = message.text
        empty_keyboard = telebot.types.ReplyKeyboardRemove(selective=False)
        if response == 'Найти контейнер по городу':
            msg = self.bot.send_message(user_id, 'В каком городе искать контейнер?', reply_markup=empty_keyboard)
            self.bot.register_next_step_handler(msg, self.find_container_by_city_name)

    def find_container_by_city_name(self, message):
        table_name = tbl['table name']
        user_id = message.from_user.id
        response = message.text
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        container_list = commands.get_container_list_by_city_name_in_table(table_name, response)
        if container_list:
            user_markup.row('Продолжить работу с таблицей-' + table_name)
            user_markup.row('Посмотреть список Таблиц')
            user_markup.row('В главное меню')
            self.bot.send_message(user_id, 'В этом городе найдено:', reply_markup=user_markup)
            for container in container_list:
                text = ''
                for b in container:
                    text = text + str(b) + ' '
                self.bot.send_message(user_id, text, reply_markup=user_markup)
                time.sleep(1)



        else:
            user_markup.row('Продолжить работу с таблицей-' + table_name)
            user_markup.row('Посмотреть список Таблиц')
            user_markup.row('В главное меню')
            self.bot.send_message(user_id, 'В этом городе контейнеров ненайдено', reply_markup=user_markup)
