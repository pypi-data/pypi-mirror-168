import time
from telebot import types


def middle_emoji_wait(bot, call):
	generic_edit_message_text(bot, call, '⏳', None)
	time.sleep(0.2)


def middle_emoji_save(bot, call):
	generic_edit_message_text(bot, call, '💾', None)
	time.sleep(0.2)


def confirm_dialog(yes_callback_data_str, no_callback_data_str):
	markup = types.InlineKeyboardMarkup(row_width=2)
	markup.add(
		types.InlineKeyboardButton(text='确定', callback_data=yes_callback_data_str),
		types.InlineKeyboardButton(text='取消', callback_data=no_callback_data_str)
	)
	return markup


def button_list_one_column(button_list):
	markup = types.InlineKeyboardMarkup(row_width=1)
	for button in button_list:
		markup.add(
			types.InlineKeyboardButton(text=button[0], callback_data=button[1])
		)

	return markup


def button_list_two_column(button_list):
	markup = types.InlineKeyboardMarkup(row_width=2)
	rows = int(len(button_list) / 2)

	for i in range(rows):
		markup.add(
			types.InlineKeyboardButton(text=button_list[i * 2][0], callback_data=button_list[i * 2][1]),
			types.InlineKeyboardButton(text=button_list[i * 2 + 1][0], callback_data=button_list[i * 2 + 1][1])
		)

	if (len(button_list) % 2) == 1:
		markup.add(
			types.InlineKeyboardButton(text=button_list[-1][0], callback_data=button_list[-1][1]),
			types.InlineKeyboardButton(text=' ', callback_data='nothing******')
		)

	return markup


def button_list_three_column(button_list):
	markup = types.InlineKeyboardMarkup(row_width=3)
	rows = int(len(button_list) / 3)

	for i in range(rows):
		markup.add(
			types.InlineKeyboardButton(text=button_list[i * 3][0], callback_data=button_list[i * 3][1]),
			types.InlineKeyboardButton(text=button_list[i * 3 + 1][0], callback_data=button_list[i * 3 + 1][1]),
			types.InlineKeyboardButton(text=button_list[i * 3 + 2][0], callback_data=button_list[i * 3 + 2][1])
		)

	if (len(button_list) % 3) == 1:
		markup.add(
			types.InlineKeyboardButton(text=button_list[-1][0], callback_data=button_list[-1][1]),
			types.InlineKeyboardButton(text=' ', callback_data='nothing******'),
			types.InlineKeyboardButton(text=' ', callback_data='nothing******')
		)

	if (len(button_list) % 3) == 2:
		markup.add(
			types.InlineKeyboardButton(text=button_list[-2][0], callback_data=button_list[-2][1]),
			types.InlineKeyboardButton(text=button_list[-1][0], callback_data=button_list[-1][1]),
			types.InlineKeyboardButton(text=' ', callback_data='nothing******')
		)

	return markup


def generic_edit_message_text(bot, call, text_str, markup):
	if markup is None:
		bot.edit_message_text(
			text=text_str,
			disable_web_page_preview=True,
			chat_id=call.from_user.id,
			message_id=call.message.message_id,
			parse_mode='HTML'
		)
	else:
		bot.edit_message_text(
			text=text_str,
			disable_web_page_preview=True,
			chat_id=call.from_user.id,
			message_id=call.message.message_id,
			parse_mode='HTML',
			reply_markup=markup
		)


def generic_send_message(bot, tg_user_id, text_str, markup):
	if markup is None:
		bot.send_message(
			text=text_str,
			disable_web_page_preview=True,
			chat_id=tg_user_id,
			parse_mode='HTML'
		)
	else:
		bot.send_message(
			text=text_str,
			disable_web_page_preview=True,
			chat_id=tg_user_id,
			parse_mode='HTML',
			reply_markup=markup
		)


def generic_edit_message_text_by_message_id(bot, chat_id, message_id, text_str, markup):
	if markup is None:
		bot.edit_message_text(
			text=text_str,
			disable_web_page_preview=True,
			chat_id=chat_id,
			message_id=message_id,
			parse_mode='HTML'
		)
	else:
		bot.edit_message_text(
			text=text_str,
			disable_web_page_preview=True,
			chat_id=chat_id,
			message_id=message_id,
			parse_mode='HTML',
			reply_markup=markup
		)


def generic_delete_message(bot, tg_user_id, message_id):
	bot.delete_message(
		chat_id=tg_user_id,
		message_id=message_id
	)
