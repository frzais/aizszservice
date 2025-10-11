# Ultroid - UserBot
# Copyright (C) 2021-2025 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
"""
✘ Commands Available -

• `{i}addpayment` (reply to QRIS image/document)
   Save your QRIS to database for later use.

• `{i}payment`
   Show your saved QRIS.

• `{i}payment <nominal>`
   Show your saved QRIS with caption including the nominal.
   Example: `{i}payment 10` -> Rp 10.000
"""

from pyUltroid.fns.tools import get_file_link
from pyUltroid.dB.filestore_db import get_stored_msg

from . import LOGS, get_string, udB, ultroid_cmd


PAYMENT_KEY = "PAYMENT_QRIS"


def _format_rupiah(amount: int) -> str:
    # Format 10000 as 10.000 using thousands separator styled for ID
    return f"{amount:,}".replace(",", ".")


@ultroid_cmd(pattern="addpayment$")
async def add_payment(e):
    r = await e.get_reply_message()
    if not (r and r.media):
        return await e.eor("`Reply a QRIS image/document to save`", time=5)

    log_chat = udB.get_key("LOG_CHANNEL")
    if not log_chat:
        return await e.eor("`LOG_CHANNEL is not set. Please set it first.`", time=7)

    note = await e.eor(get_string("com_1"))
    try:
        qris_hash = await get_file_link(r)
    except Exception as er:
        LOGS.exception(er)
        return await note.edit("`Failed to store QRIS. Check LOG_CHANNEL access.`")

    udB.set_key(PAYMENT_KEY, qris_hash)
    await note.edit("**QRIS saved successfully.**\nUse `{i}payment` to display it.")


@ultroid_cmd(pattern="payment( (.*)|$)")
async def show_payment(e):
    arg = (e.pattern_match.group(1) or "").strip()

    qris_hash = udB.get_key(PAYMENT_KEY)
    if not qris_hash:
        return await e.eor("`No QRIS saved yet. Use {i}addpayment first.`", time=7)

    log_chat = udB.get_key("LOG_CHANNEL")
    if not log_chat:
        return await e.eor("`LOG_CHANNEL is not set. Please set it first.`", time=7)

    msg_id = get_stored_msg(qris_hash)
    if not msg_id:
        return await e.eor("`Stored QRIS not found. Save again with {i}addpayment.`", time=7)

    try:
        src = await e.client.get_messages(log_chat, ids=msg_id)
    except Exception as er:
        LOGS.exception(er)
        return await e.eor("`Unable to fetch stored QRIS from LOG_CHANNEL.`", time=7)

    caption = "Silakan scan QRIS untuk transfer."
    if arg:
        # Accept inputs like "10", "10k", "10.000", "10000", etc.
        raw = arg.lower().replace("rp", "").replace(" ", "")
        if raw.endswith("k"):
            raw = raw[:-1] + "000"
        digits = "".join(ch for ch in raw if ch.isdigit())
        if digits:
            try:
                amount = int(digits)
                caption = f"Silakan scan QRIS untuk transfer: Rp {_format_rupiah(amount)}"
            except Exception:
                pass

    await e.client.send_file(e.chat_id, src.media, caption=caption, reply_to=e.reply_to_msg_id or None)

