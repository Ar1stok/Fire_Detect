import logging

from video_process import Processing
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

TOKEN = "WRITE_YOUR_TOKEN"

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

VIDEO = range(1)

process = Processing('video', 'frames')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """start command processing."""
    await update.message.reply_text(
        "Привет👋 \n" \
        "Я бот который пока что делит видео на кадры, но скоро он будет определять огонь на видео\n" \
        "Команды которые можно использовать:\n" \
        "- start - активация бота и просмотра команд\n" \
        "- info - для тех, кому интересно познакомится или почитать о проекте \n" \
        "- detect - пишешь команду, кидаешь видео и получаешь результат\n" \
        "- cancel - для отмены команды detect",
        reply_markup=ReplyKeyboardRemove()
    )


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Info about our project and team."""
    user = update.message.from_user
    logger.info("User %s: Ask info about our project", user.first_name)
    await update.message.reply_text(
        "Данный бот по сути являтся облегченной версией продукта детекции огня, также хочется отметить, " \
        "что бот будет отключен на следующий день после презентации продукта, если хотите ознакомится с ним позже, пишите нам об этом\n" \
        "По ссылке ниже вы можете ознакомится с информацией о нас и о нашем проекте: \nhttps://github.com/Ar1stok/Fire_Detect \n" \
        "Наши контакты:\n" \
        "<a href='https://t.me/Ar1stock'>Крылов Павел</a>\n" \
        "<a href='https://t.me/VeloR_139'>Сичкарь Иван</a>\n" \
        "<a href='https://t.me/Shaman1641'>Назаров Данил</a>", 
        reply_markup=ReplyKeyboardRemove(), parse_mode="HTML"
    )


async def detection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Command to start the def video."""
    user = update.message.from_user
    logger.info("User %s: Want to send a video", user.first_name)
    await update.message.reply_text(
        "Отправь мне видео, но не более 20 секунд, иначе видео не обработается🫠",
        reply_markup=ReplyKeyboardRemove(),
    )

    return VIDEO


async def video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Wait and start process video."""
    user = update.message.from_user
    video_file = await update.message.video.get_file()
    await video_file.download_to_drive(f"video/obj_{user.id}.mp4")
    logger.info("Video of %s: %s", user.first_name, f"obj_{user.id}.mp4")
    await update.message.reply_text(
        f"Видео получено! Обрабатываем..."
    )
    
    duration = process.duration(f"obj_{user.id}.mp4")
    if duration > 21:
        await update.message.reply_text(
            "Ваше видео более 20 секунд, отправьте другое😑"
        )
        return VIDEO
    
    fire_count = process.detection(f"obj_{user.id}.mp4")
    logger.info(f"Video of {user.first_name} processed, on the video {fire_count} fire frames" )
    if not fire_count:
        await update.message.reply_text(
            "Огня не обнаружено❌"
        )
    else:
        await update.message.reply_text(
            "Огонь обнаружен🔥"
        )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """End conversation or cancel command 'detect'."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Галя, у нас отмена", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Add conversation handler with the states
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CommandHandler("info", info),
            CommandHandler("detect", detection),
        ],
        states={
            VIDEO: [
                MessageHandler(filters.VIDEO, video),
                CommandHandler("cancel" ,cancel),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()