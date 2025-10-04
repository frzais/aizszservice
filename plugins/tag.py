# Ultroid - UserBot
# Copyright (C) 2021-2025 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
"""
✘ Commands Available -

• `{i}tagall`
    Tag Top 100 Members of chat.

• `{i}tagadmins`
    Tag Admins of that chat.

• `{i}tagowner`
    Tag Owner of that chat

• `{i}tagbots`
    Tag Bots of that chat.

• `{i}tagrec`
    Tag recently Active Members.

• `{i}tagon`
    Tag online Members(work only if privacy off).

• `{i}tagoff`
    Tag Offline Members(work only if privacy off).
"""

from telethon.tl.types import ChannelParticipantAdmin as admin
from telethon.tl.types import ChannelParticipantCreator as owner
from telethon.tl.types import UserStatusOffline as off
from telethon.tl.types import UserStatusOnline as onn
from telethon.tl.types import UserStatusRecently as rec

from . import inline_mention, ultroid_cmd


@ultroid_cmd(
    pattern="tag(on|off|all|bots|rec|admins|owner)( (.*)|$)",
    groups_only=True,
)
async def _(e):
    okk = e.text
    lll = e.pattern_match.group(2)
    o = 0
    nn = 0
    rece = 0
    xx = f"{lll}" if lll else ""
    
    # For tagall, use progressive tagging for large groups
    if "all" in okk:
        await progressive_tagall(e, xx)
        return
    
    # For other tag commands, use original logic
    lili = await e.client.get_participants(e.chat_id, limit=99)
    for bb in lili:
        x = bb.status
        y = bb.participant
        if isinstance(x, onn):
            o += 1
            if "on" in okk:
                xx += f"\n{inline_mention(bb)}"
        elif isinstance(x, off):
            nn += 1
            if "off" in okk and not bb.bot and not bb.deleted:
                xx += f"\n{inline_mention(bb)}"
        elif isinstance(x, rec):
            rece += 1
            if "rec" in okk and not bb.bot and not bb.deleted:
                xx += f"\n{inline_mention(bb)}"
        if isinstance(y, owner):
            xx += f"\n꧁{inline_mention(bb)}꧂"
        if isinstance(y, admin) and "admin" in okk and not bb.deleted:
            xx += f"\n{inline_mention(bb)}"
        if "bot" in okk and bb.bot:
            xx += f"\n{inline_mention(bb)}"
    await e.eor(xx)


async def progressive_tagall(e, message):
    """Progressive tagall for large groups"""
    import asyncio
    
    # Get total member count
    try:
        chat = await e.client.get_entity(e.chat_id)
        total_members = chat.participants_count
    except:
        total_members = 0
    
    if total_members <= 99:
        # Use original method for small groups
        lili = await e.client.get_participants(e.chat_id, limit=99)
        xx = message
        for bb in lili:
            if not bb.bot and not bb.deleted:
                xx += f"\n{inline_mention(bb)}"
        await e.eor(xx)
        return
    
    # Progressive tagging for large groups
    batch_size = 99
    total_batches = (total_members + batch_size - 1) // batch_size
    
    await e.eor(f"🚀 **Starting Progressive Tag All**\n📊 **Total Members:** {total_members}\n📦 **Batches:** {total_batches}\n\n⏳ **Processing...**")
    
    for batch_num in range(total_batches):
        offset = batch_num * batch_size
        
        try:
            # Get participants for this batch
            lili = await e.client.get_participants(e.chat_id, limit=batch_size, offset=offset)
            
            if not lili:
                break
                
            # Build message for this batch
            batch_message = f"📢 **Batch {batch_num + 1}/{total_batches}**\n"
            if message:
                batch_message += f"{message}\n"
            
            # Add mentions for this batch
            for bb in lili:
                if not bb.bot and not bb.deleted:
                    batch_message += f"\n{inline_mention(bb)}"
            
            # Send batch message
            await e.client.send_message(e.chat_id, batch_message)
            
            # Wait between batches to avoid rate limiting
            if batch_num < total_batches - 1:  # Don't wait after last batch
                await asyncio.sleep(2)  # 2 seconds delay between batches
                
        except Exception as ex:
            await e.client.send_message(e.chat_id, f"❌ **Error in batch {batch_num + 1}:** {str(ex)}")
            continue
    
    # Send completion message
    await e.client.send_message(e.chat_id, f"✅ **Progressive Tag All Completed!**\n📊 **Total Batches:** {total_batches}\n👥 **Total Members Tagged:** {total_members}")
