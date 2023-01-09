from telegram import Update
import telegram.ext
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, ContextTypes, CallbackContext

TOKEN = ''

# assistant list
assistant = []


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('''به بات دستیار خوش آمدید🎉

این بات برای کمک به اعضای گروه ساخته شده و شما میتوانید با اضافه کردن ربات به گروه خود از امکانات این ربات  استفاده کنید

دستورات ربات:

/q : 

کاربران گروه میتوانند با دستور q سوال خودشون رو بپرسند و ربات به صورت خودکار دستیار ها رو منشن میکنه تا پیام شما راحت تر توسط اون ها دیده بشه پیامتون گم نشه

/add : 

با استفاده دستور add و منشن کردن کاربر مورد نظر ، اون کاربر در لیست دستیار ها قرار میگیرد.
 تنها ادمین گروه توانایی اضافه کردن دستیار به لیست را دارد.

/remove : 

با استفاده دستور remove و منشن کردن کاربر مورد نظر ، اون کاربر  از لیست دستیار ها حذف میشود.
 تنها ادمین گروه توانایی حذف کردن دستیار از لیست را دارد.

/list :

با استفاده از دستور list میتوانید لیست دستیار ها را مشاهده کنید.
 تنها ادمین گروه توانایی دیدن لیست را دارد.


''')


# Add assistant
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat.type == "private":
        await update.message.reply_text(
            'این دستور فقط در گروه کار میکند ! برای استفاده ربات را به گروه اضافه کنید !')
    else:
        print(assistant)
        user_message = update.message.text.lstrip("/add")
        chat_admins = await update.effective_chat.get_administrators()
        print(await update.effective_chat.get_member_count())
        if update.effective_user in (admin.user for admin in chat_admins):
            if user_message in assistant:
                await update.message.reply_text(f'این کاربر درحال حاضر در لیست دستیار ها وجود دارد')
            elif "@" in user_message and 4 < len(user_message) < 32:
                assistant.append(user_message)
                await update.message.reply_text(f'کاربر با موفقیت به لیست اضافه شد')

            else:
                await update.message.reply_text(f'خطا ! لطفا یکی از اعضا را منشن کنید')

        else:
            user_name = update.message.from_user.full_name
            user_id = update.message.from_user['id']
            await update.message.reply_text(
                f'کاربر [{user_name}](tg://user?id={user_id}) تنها ادمین گروه توانایی اضافه کردن دستیار جدید را دارد',
                parse_mode=ParseMode.MARKDOWN_V2)


# Ask question

async def question(update: Update, context: CallbackContext) -> None:
    if update.effective_chat.type == "private":
        await update.message.reply_text(
            'این دستور فقط در گروه کار میکند ! برای استفاده ربات را به گروه اضافه کنید !')
    else:
        user_message = update.message.text.lstrip("/add")
        if len(user_message) > 3:
            if not assistant:
                await update.message.reply_text(f"متاسفانه لیست دستیار های این گروه خالی است!")
            else:
                await update.message.reply_text("یک سوال جدید برای شما!\n" + "\n".join(assistant))
        else:
            user_name = update.message.from_user.full_name
            user_id = update.message.from_user['id']
            await update.message.reply_text(
                f'کاربر [{user_name}](tg://user?id={user_id})  متن سوال نمیتواند کمتر از سه کاراکتر باشد',
                parse_mode=ParseMode.MARKDOWN_V2)


async def list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat.type == "private":
        await update.message.reply_text(
            'این دستور فقط در گروه کار میکند ! برای استفاده ربات را به گروه اضافه کنید !')

    else:
        chat_admins = await update.effective_chat.get_administrators()
        if update.effective_user in (admin.user for admin in chat_admins):
            if not assistant:
                await update.message.reply_text(f"متاسفانه لیست دستیار های این گروه خالی است!")
            else:
                await update.message.reply_text("لیست دستیار ها :\n" + "\n".join(assistant))
        else:
            user_name = update.message.from_user.full_name
            user_id = update.message.from_user['id']
            await update.message.reply_text(
                f' کاربر [{user_name}](tg://user?id={user_id}) تنها ادمین گروه توانایی دیدن لیست دستیار ها را دارد',
                parse_mode=ParseMode.MARKDOWN_V2)


async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat.type == "private":
        await update.message.reply_text(
            'این دستور فقط در گروه کار میکند ! برای استفاده ربات را به گروه اضافه کنید !')
    else:
        user_message = update.message.text.lstrip("/remove")
        chat_admins = await update.effective_chat.get_administrators()
        if update.effective_user in (admin.user for admin in chat_admins):
            if "@" in user_message and len(user_message) < 32 and user_message in assistant:
                assistant.remove(user_message)
                await update.message.reply_text(f'این کاربر با موفقیت از لیست دستیار ها حذف شد !')
                print(assistant)
            else:
                await update.message.reply_text(f'این کاربر در لیست وجود ندارد!')
        else:
            user_name = update.message.from_user.full_name
            user_id = update.message.from_user['id']
            await update.message.reply_text(
                f' کاربر [{user_name}](tg://user?id={user_id}) تنها ادمین گروه توانایی حذف کردن دستیار را دارد',
                parse_mode=ParseMode.MARKDOWN_V2)


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(telegram.ext.CommandHandler("start", start))
app.add_handler(telegram.ext.CommandHandler("help", start))
app.add_handler(telegram.ext.CommandHandler("q", question))
app.add_handler(telegram.ext.CommandHandler("add", add))
app.add_handler(telegram.ext.CommandHandler("list", list))
app.add_handler(telegram.ext.CommandHandler("remove", remove))

if __name__ == '__main__':
    app.run_polling()
