from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
import io
from userbot import bot, CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern="^.stog$")
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("Balas di Sticker!!")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.edit("Balas di Sticker!!")
        return
    chat = "@@Sticker2GIFBot"
    await event.edit("Convert to gif..")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(
                    incoming=True,
                    from_users=2055431272))
            msg = await event.client.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.reply("unblock me @@Sticker2GIFBot to work")
            return
        if response.text.startswith("I understand only stickers"):
            await event.edit("Sorry i cant't convert it")
        else:
            await event.delete()
            await bot.send_read_acknowledge(conv.chat_id)
            await event.client.send_message(event.chat_id, response.message)
            await event.client.delete_message(conv.chat_id, [msg.id, response.id])


CMD_HELP.update(
    {
        "stickers_v2": ">`.stog`"
        "\nUsage: Reply .stog to a sticker and convert to a gif "
