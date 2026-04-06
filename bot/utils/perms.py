from discord.ext import commands

OWNER_ID = 1272066173810380861
STAFF_ROLE_ID = 1472478801710678258

def is_admin():

    async def predicate(ctx):

        # owner
        if ctx.author.id == OWNER_ID:
            return True

        # roles
        if any(role.id == STAFF_ROLE_ID for role in ctx.author.roles):
            return True

        raise commands.CheckFailure("❌ No tenés permisos")

    return commands.check(predicate)
