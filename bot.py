from telegram import Update
from telegram.ext import Application , CommandHandler ,ContextTypes , MessageHandler , filters
import sqlite3
from deep_translator import googletranslator

TOKEN ="8723401814:AAFeMFSM0BRFalkfFzi-boZ2RkdVxRyReak"

async def start(update: Update , context):
    user = update.effective_user
    try:
        con = sqlite3.connect('users.db')
        c = con.cursor()
        c.execute("INSERT OR REPLACE INTO users (user_id, first_name, last_seen) VALUES (?,? datetime('now'))"
                  (user.id, user.first_name))

        con.commit()
        con.close()
    except Exception as e:
        print(f"khata dar data base:{e}")
        print(user.first_name)
   
    await update.message.reply_text(f"Hello my friend \nTell me {user.first_name}:what do you want me to translate for you")

async def stats(update: Update , context):
    con = sqlite3.connect('users.db')
    c = con.cursor()
    c.execute("SELECT COUNT(*) FROM users")    
    count = c.fetchone()[0]
    con.close()
    await update.message.reply_text(f"bitches number: {count}")



async def translataing(update: Update, context:ContextTypes.DEFAULT_TYPE)-> None:
    """Translate the user message"""
    text = update.message.text
    try:
        translated = googletranslator(source = 'auto' , target='de')tranlate(text)

        await  update.message.reply_text(f"{text} means {translated.text} in Deutsch \nwhat else?")
    except Exception as e:
        await update.message.text("khata rokh dad")


def main():
    print("this shit is booting...")
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start",start))
    application.add_handler(CommandHandler("stats",stats))
    application.add_handler(CommandHandler("me",me))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translataing))
    application.run_polling()

if __name__ == "__main__":
    main()
