# Ultroid - UserBot
# Copyright (C) 2021-2025 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

from telethon.tl.custom import Button

from . import asst, get_string, ultroid_cmd


@ultroid_cmd(pattern="ultroid$")
async def ultroid_menu(ult):
    """Open Ultroid help menu via inline handler."""
    try:
        results = await ult.client.inline_query(asst.me.username, "ultd")
        return await results[0].click(ult.chat_id)
    except BaseException:
        # Fallback simple menu
        buttons = [
            [
                Button.url("• Repo •", url="https://github.com/TeamUltroid/Ultroid"),
                Button.url("• Support •", url="t.me/UltroidSupportChat"),
            ],
            [Button.inline(get_string("help_10"), data="close")],
        ]
        await ult.eor("Ultroid Userbot", buttons=buttons)


@ultroid_cmd(pattern="repo$")
async def repo_links(ult):
    """Show repository and support links."""
    text = "**Ultroid Userbot**\n"
    text += "- GitHub: https://github.com/TeamUltroid/Ultroid\n"
    text += "- Support: t.me/UltroidSupportChat"
    buttons = [
        [
            Button.url("• Repo •", url="https://github.com/TeamUltroid/Ultroid"),
            Button.url("• Support •", url="t.me/UltroidSupportChat"),
        ]
    ]
    await ult.eor(text, buttons=buttons, link_preview=False)

 