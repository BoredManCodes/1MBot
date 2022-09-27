import aiohttp

from core.base import CustomClient

from naff import (
    Embed,
    Extension,
    InteractionContext,
    slash_command,
)


class CommandExtension(Extension):
    bot: CustomClient

    @slash_command(name="meme", description="Sends a meme")
    async def meme(self, ctx: InteractionContext):
        async with aiohttp.ClientSession() as session:
            meme_api = "https://meme-api.herokuapp.com/gimme"
            while True:
                async with session.get(meme_api) as resp:
                    meme = await resp.json()
                    # API provides no way to request SFW only, so we repeat until we get a SFW one
                    if not meme["nsfw"]:
                        break

        # adds an embed to the message
        embed = Embed(
            title=meme["title"],
            url=meme["postLink"],
            description=f"From r/{meme['subreddit']}",
            image=meme["url"],
            footer="Is this accidentally NSFW? Ping a team member.",
        )

        # respond to the interaction
        await ctx.send(embeds=embed)


def setup(bot: CustomClient):
    """Let naff load the extension"""

    CommandExtension(bot)
