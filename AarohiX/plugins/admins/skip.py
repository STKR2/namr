from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, Message
import config
from AarohiX import YouTube, app
from AarohiX.core.call import Dil
from AarohiX.misc import db
from pyrogram.errors import UserNotParticipant
from strings.filters import command
from AarohiX.utils.database import get_loop
from AarohiX.utils.decorators import AdminRightsCheck
from AarohiX.utils.inline import close_markup, stream_markup
from AarohiX.utils.stream.autoclear import auto_clean
from AarohiX.utils.thumbnails import get_thumb
from config import Muntazer, BANNED_USERS

async def get_channel_title(client, channel_id):
    try:
        chat_info = await client.get_chat(channel_id)
        return chat_info.title
    except Exception as e:
        print("Error:", e)
        return None

@app.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channel(cli, msg: Message):
    if not Muntazer:
        return
    try:
        try:
            await cli.get_chat_member(Muntazer, msg.from_user.id)
        except UserNotParticipant:
            if Muntazer.isalpha():
                link = "https://t.me/" + Muntazer
            else:
                link = Muntazer_invite_link 
            channel_title = await get_channel_title(cli, Muntazer)
            if channel_title:
                await msg.reply(
                    f"عذرا عزيزي ↜ {msg.from_user.mention} \nلا تستطيع استخدام الامر انت لم تشترك في قناه البوت",
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(f"{channel_title}", url=link)]
                    ])
                )
                await msg.stop_propagation()
    except ChatAdminRequired:
        print(f"I'm not admin in the MUST_JOIN chat {Muntazer}!")

@app.on_message(
    command(["skip", "تخطي", "سكب", "cnext"]) & filters.group & ~BANNED_USERS
)
@AdminRightsCheck
async def skip(cli, message: Message, _, chat_id):
    if not Muntazer:
        return
    try:
        await cli.get_chat_member(Muntazer, message.from_user.id)
    except UserNotParticipant:
        if Muntazer.isalpha():
            link = "https://t.me/" + Muntazer
        else:
            link = Muntazer_invite_link
        channel_title = await get_channel_title(cli, Muntazer)
        if channel_title:
            await message.reply(
                f"عذرا عزيزي ↜ {message.from_user.mention} \nلا تستطيع استخدام الامر انت لم تشترك في قناه البوت .",
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(f"{channel_title}", url=link)]
                ])
            )
        return

    if not len(message.command) < 2:
        loop = await get_loop(chat_id)
        if loop != 0:
            return await message.reply_text(_["admin_8"])
        state = message.text.split(None, 1)[1].strip()
        if state.isnumeric():
            state = int(state)
            check = db.get(chat_id)
            if check:
                count = len(check)
                if count > 2:
                    count = int(count - 1)
                    if 1 <= state <= count:
                        for x in range(state):
                            popped = None
                            try:
                                popped = check.pop(0)
                            except:
                                return await message.reply_text(_["admin_12"])
                            if popped:
                                await auto_clean(popped)
                            if not check:
                                try:
                                    await message.reply_text(
                                        text=_["admin_6"].format(
                                            message.from_user.mention,
                                            message.chat.title,
                                        ),
                                        reply_markup=close_markup(_),
                                    )
                                    await Dil.stop_stream(chat_id)
                                except:
                                    return
                                break
                    else:
                        return await message.reply_text(_["admin_11"].format(count))
                else:
                    return await message.reply_text(_["admin_10"])
            else:
                return await message.reply_text(_["queue_2"])
        else:
            return await message.reply_text(_["admin_9"])
    else:
        check = db.get(chat_id)
        popped = None
        try:
            popped = check.pop(0)
            if popped:
                await auto_clean(popped)
            if not check:
                await message.reply_text(
                    text=_["admin_6"].format(
                        message.from_user.mention, message.chat.title
                    ),
                    reply_markup=close_markup(_),
                )
                try:
                    return await Anony.stop_stream(chat_id)
                except:
                    return
        except:
            try:
                await message.reply_text(
                    text=_["admin_6"].format(
                        message.from_user.mention, message.chat.title
                    ),
                    reply_markup=close_markup(_),
                )
                return await Anony.stop_stream(chat_id)
            except:
                return

        queued = check[0]["file"]
        title = (check[0]["title"]).title()
        user = check[0]["by"]
        streamtype = check[0]["streamtype"]
        videoid = check[0]["vidid"]
        status = True if str(streamtype) == "video" else None
        db[chat_id][0]["played"] = 0
        exis = (check[0]).get("old_dur")
        if exis:
            db[chat_id][0]["dur"] = exis
            db[chat_id][0]["seconds"] = check[0]["old_second"]
            db[chat_id][0]["speed_path"] = None
            db[chat_id][0]["speed"] = 1.0          
