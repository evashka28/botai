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
    print(out)
    #print(type(out))
    answer = right_format(out)
    #outdict = fix_parser.parse(out)
    #retry_parser = RetryWithErrorOutputParser.from_llm(parser=parser, llm=llm)
    #outdict =retry_parser.parse_with_prompt(out, question)
    #an = outdict.answer
    #print(an)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=answer)


async def admin(update, context: ContextTypes.DEFAULT_TYPE):
    conversation = LLMChain(llm=llm, prompt=prompt_end, verbose=True)
    out = conversation.predict()
    answer = out
    #outdict = fix_parser_end.parse(out)
    #print(type(outdict))
    print(type(out))
    await context.bot.send_message(chat_id=update.effective_chat.id, text=out)


if __name__ == "__main__":
    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('admin', admin))
    application.add_handler(MessageHandler(filters.TEXT, handle_message))
    application.run_polling()