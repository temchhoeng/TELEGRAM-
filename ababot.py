import edge_tts
from googletrans import Translator
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = "8610381240:AAF70uEadOgRvqY686pzbPRgnxBzFfCpcwE"

translator = Translator()
WebAppInfo(url="https://servicepremuim.netlify.app")

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎙 Open Translator", web_app=WebAppInfo(url="https://your-netlify-url.netlify.app"))]
    ]
    await update.message.reply_text("Open Translator App:", reply_markup=InlineKeyboardMarkup(keyboard))

# HANDLE WEB DATA
async def handle_webapp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.message.web_app_data.data

    text, voice = data.split("|")

    # translate to English
    translated = translator.translate(text, dest="en").text

    filename = "voice.mp3"

    # generate voice
    tts = edge_tts.Communicate(translated, voice)
    await tts.save(filename)

    # send audio
    await update.message.reply_audio(audio=open(filename, "rb"), caption=translated)

# RUN
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp))

print("Running...")
app.run_polling()