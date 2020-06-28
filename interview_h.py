#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)

from base_h import (to_main, new_update)
from functions import remove_keyboard
from database import (Feedback, User)
from base import (INTERVIEW, INTERVIEW_MORE, texts, keyboards, config)


def inter_1(update, context):
	d = update.callback_query.data.split('_')
	context.user_data['1_mark'] = d[2]

	remove_keyboard(update, context)
	keyb = [[InlineKeyboardButton(n, callback_data=f'interview_2_{n}') for n in range(1, config['marks_count'])]]
	keyb.append([InlineKeyboardButton(keyboards['interview']['send'], callback_data='interview_save')])
	context.user_data['m_id'] = update.callback_query.edit_message_text(texts['interview']['mark_2'], reply_markup=InlineKeyboardMarkup(keyb)).message_id
	return INTERVIEW


def inter_2(update, context):
	d = update.callback_query.data.split('_')
	context.user_data['2_mark'] = d[2]

	keyb = [[InlineKeyboardButton(keyboards['interview']['send'], callback_data='interview_save')]]
	context.user_data['m_id'] = update.callback_query.edit_message_text(texts['interview']['to_do'], reply_markup=InlineKeyboardMarkup(keyb)).message_id
	return INTERVIEW_MORE


def interview_other(update, context):
	context.user_data['txt'] = update.message.text
	return save_marks(update, context)


def save_marks(update, context):
	Feedback.create(chat_id=update._effective_chat.id, mark_1=context.user_data['1_mark'], mark_2=context.user_data.get('2_mark'), txt=context.user_data.get('txt')).save()

	s = texts['interview']['oper'].replace('<c>', str(update._effective_chat.id)).replace('<1s>', str(context.user_data['1_mark'])).replace('<2s>', str(context.user_data.get('2_mark'))).replace('<txt>', str(context.user_data.get('txt')))
	opers = User.select().where(User.is_oper)
	
	for oper in opers:
		context.bot.send_message(oper.chat_id, s)

	context.bot.edit_message_text(chat_id=update._effective_chat.id, message_id=context.user_data['m_id'], text=texts['interview']['saved'])
	return to_main(update, context)
