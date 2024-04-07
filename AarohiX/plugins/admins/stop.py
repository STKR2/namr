from pyrogram import filters
from pyrogram.types import Message
from strings.filters import command
from AarohiX import app
from pyrogram.errors import UserNotParticipant
from pyrogram.errors import ChatAdminRequired
from AarohiX.core.call import Dil
from AarohiX.utils.database import set_loop
from AarohiX.utils.decorators import AdminRightsCheck
from AarohiX.utils.inline import close_markup 
from config import Muntazer 

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
                    f"\n<b>عذرا عزيزي ↜ {msg.from_user.mention}</b>\nلا تستطيع استخدام الامر انت لم تشترك في قناه البوت",
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(f"{channel_title}", url=link)]
                    ])
                )
                await msg.stop_propagation()
    except ChatAdminRequired:
        print(f"I'm not admin in the MUST_JOIN chat {Muntazer}!")

# الكود لإيقاف الموسيقى 
@app.on_message(command(["ايقاف", "اوكف", "كافي", "انهاء"]) ) 
@AdminRightsCheck 
async def stop_music(cli, message: Message, _, chat_id): 
    if not len(message.command) == 1: 
        return  
    await must_join_channel(cli, message) 
    await Dil.stop_stream(chat_id) 
    await set_loop(chat_id, 0) 
    await message.reply_text( 
        _["admin_5"].format(message.from_user.mention), reply_markup=close_markup(_) 
    )
