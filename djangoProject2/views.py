import datetime
import logging
from datetime import date, timedelta


from djangoProject2.tasknorm2 import *
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Здравствуйте")


async def handle_message(update, context):
    question = update.message.text

    memory.chat_memory.add_user_message(question)

    conversation = LLMChain(llm=llm, prompt=prompt, verbose=True)
    #print(conversation)
    out = conversation.predict()
    memory.chat_memory.add_ai_message(out)
    print(memory.load_memory_variables({}))
    #print(out)
    #print(type(out))
    answer = out
    outdict = fix_parser.parse(out)
    print(type(outdict))
    an = outdict.action_output
    print(an)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=an)


if __name__ == "__main__":
    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT, handle_message))
    application.run_polling()