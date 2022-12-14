# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# The entire source code is OSSRPL except 'whois' which is MPL
# License: MPL and OSSRPL
""" Userbot module for getting info about any user on Telegram(including you!). """

import os

from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location

from userbot import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register


@register(pattern=r"^\.whois(?: |$)(.*)", outgoing=True)
async def who(event):

    await event.edit(
        "`Sit tight while I steal some data from *Global Network Zone*...`"
    )

    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)

    replied_user = await get_user(event)
    if replied_user is None:
        await event.edit(
            "`This is anonymous admin in this group.\nCan't fetch the info`"
        )
        return

    try:
        photo, caption = await fetch_info(replied_user, event)
    except AttributeError:
        await event.edit("`Could not fetch info of that user.`")
        return

    message_id_to_reply = event.message.reply_to_msg_id

    if not message_id_to_reply:
        message_id_to_reply = None

    try:
        await event.client.send_file(
            event.chat_id,
            photo,
            caption=caption,
            link_preview=False,
            force_document=False,
            reply_to=message_id_to_reply,
            parse_mode="html",
        )

        if not photo.startswith("http"):
            os.remove(photo)
        await event.delete()

    except TypeError:
        await event.edit(caption, parse_mode="html")


async def get_user(event):
    """Get the user from argument or replied message."""
    if event.reply_to_msg_id and not event.pattern_match.group(1):
        previous_message = await event.get_reply_message()
        if previous_message.sender_id is None and not event.is_private:
            return None
        replied_user = await event.client(
            GetFullUserRequest(previous_message.sender_id)
        )
    else:
        user = event.pattern_match.group(1)

        if user.isnumeric():
            user = int(user)

        if not user:
            self_user = await event.client.get_me()
            user = self_user.id

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user
        try:
            user_object = await event.client.get_entity(user)
            replied_user = await event.client(GetFullUserRequest(user_object.id))
        except (TypeError, ValueError) as err:
            return await event.edit(str(err))

    return replied_user


async def fetch_info(replied_user, event):
    """Get details from the User object."""
    replied_user_profile_photos = await event.client(
        GetUserPhotosRequest(
            user_id=replied_user.full_user.id, offset=42, max_id=0, limit=80
        )
    )
    replied_user_profile_photos_count = (
        "Person needs help with uploading profile picture."
    )
    try:
        replied_user_profile_photos_count = replied_user_profile_photos.count
    except AttributeError:
        pass
    user_id = replied_user.full_user.id
    first_name = replied_user.users[0].first_name
    last_name = replied_user.users[0].last_name
    try:
        dc_id, _ = get_input_location(replied_user.full_user.profile_photo)
    except Exception as e:
        dc_id = "Couldn't fetch DC ID!"
        str(e)
    common_chat = replied_user.full_user.common_chats_count
    username = replied_user.users[0].username
    user_bio = replied_user.full_user.about
    is_bot = replied_user.users[0].bot
    restricted = replied_user.users[0].restricted
    verified = replied_user.users[0].verified
    photo = await event.client.download_profile_photo(
        user_id, TEMP_DOWNLOAD_DIRECTORY + str(user_id) + ".jpg", download_big=True
    )
    first_name = (
        first_name.replace("\u2060", "")
        if first_name
        else ("This User has no First Name")
    )
    last_name = (
        last_name.replace("\u2060", "") if last_name else ("This User has no Last Name")
    )
    username = f"@{username}" if username else ("This User has no Username")
    user_bio = "This User has no About" if not user_bio else user_bio

    caption = "<b>INFO PENGGUNA:</b>\n\n"
    caption += f"Nama Depan: {first_name}\n"
    caption += f"Nama Belakang: {last_name}\n"
    caption += f"Username: {username}\n"
    caption += f"Data Center ID: {dc_id}\n"
    caption += f"Jumlah Foto Profil: {replied_user_profile_photos_count}\n"
    caption += f"Apakah Bot: {is_bot}\n"
    caption += f"Apakah Dibatasi: {restricted}\n"
    caption += f"Diverifikasi oleh Durov: {verified}\n"
    caption += f"ID: <code>{user_id}</code>\n\n"
    caption += f"Bio: \n<code>{user_bio}</code>\n\n"
    caption += f"Obrolan yang sama dengan pengguna ini: {common_chat}\n"
    caption += f"Tautan Permanen Ke Profil: "
    caption += f'<a href="tg://user?id={user_id}">Disini</a>'

    return photo, caption


CMD_HELP.update(
    {
        "whois": ">`.whois <username> or reply to someones text with .whois`"
        "\nUsage: Gets info of an user."
    }
)
