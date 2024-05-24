from pyrogram import filters 
from pyrogram.types import Message 
from strings.filters import command 
from AarohiX import app 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from config import Muntazer 
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden 
from AarohiX.core.call import Dil
from AarohiX.utils.database import set_loop 
from AarohiX.utils.decorators import AdminRightsCheck 
from AarohiX.utils.inline import close_markup 
 
@app.on_message(filters.incoming & filters.private, group=-1) 
async def must_join_channel(app, msg):
    if not Muntazer:
        return
    try:
        if msg.from_user is None:
            return
        try:
            await app.get_chat_member(Muntazer, msg.from_user.id)
        except UserNotParticipant:
            if Muntazer.isalpha():
                link = "https://t.me/" + Muntazer
            else:
                chat_info = await app.get_chat(Muntazer)
                link = chat_info.invite_link
            try:
                await msg.reply(
                    f"~︙عليك الأشتراك في قناة البوت \n~︙قناة البوت : @{Muntazer}.",
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("< Source >", url=link)]
                    ])
                )
                await msg.stop_propagation()
            except ChatWriteForbidden:
                pass
    except ChatAdminRequired:
        print(f"I m not admin in the MUST_JOIN chat {Muntazer}!")

 
# الكود لإيقاف الموسيقى  
@app.on_message(command(["ايقاف", "اوكف", "كافي", "انهاء"])) 
async def stop_music(cli, message: Message): 
    if not len(message.command) == 1: 
        return 
    # التحقق من الاشتراك في القناة 
    await must_join_channel(cli, message) 
    # إيقاف الموسيقى
    await Dil.stop_stream(message.chat.id) 
    await set_loop(message.chat.id, 0) 
    # الرد على الرسالة بنجاح الإيقاف
    await message.reply_text( 
        _["admin_5"].format(message.from_user.mention), reply_markup=close_markup(_) 
    )
