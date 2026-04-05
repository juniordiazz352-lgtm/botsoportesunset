import discord
from discord.ext import commands
from bot.core.db import conn, cursor

from bot.views.ticket_panel import TicketPanelView
from bot.views.form_panel import FormPanelView


class PanelCreator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ✅ Crear panel
    @commands.hybrid_command(name="crear_panel")
    async def crear_panel(self, ctx, nombre: str, tipo: str, titulo: str, color: int, rol: discord.Role = None, *, descripcion: str):
        tipo = tipo.lower()

        if tipo not in ["ticket", "form"]:
            return await ctx.send("❌ Tipo inválido")

        cursor.execute(
            "INSERT INTO panels (nombre, tipo, titulo, descripcion, color, rol_id) VALUES (?, ?, ?, ?, ?, ?)",
            (nombre, tipo, titulo, descripcion, color, rol.id if rol else None)
        )
        conn.commit()

        await ctx.send(f"✅ Panel `{nombre}` creado")

    # ➕ Agregar botón
    @commands.hybrid_command(name="agregar_boton")
    async def agregar_boton(self, ctx, panel: str, label: str, tipo: str):
        tipo = tipo.lower()

        if tipo not in ["ticket", "form"]:
            return await ctx.send("❌ Tipo inválido")

        cursor.execute(
            "INSERT INTO panel_buttons (panel_nombre, label, estilo, tipo) VALUES (?, ?, ?, ?)",
            (panel, label, 1, tipo)
        )
        conn.commit()

        await ctx.send("✅ Botón agregado")

    # 📋 Ver paneles
    @commands.hybrid_command(name="ver_paneles")
    async def ver_paneles(self, ctx):
        cursor.execute("SELECT nombre, tipo FROM panels")
        data = cursor.fetchall()

        if not data:
            return await ctx.send("❌ No hay paneles")

        texto = "\n".join([f"• {n} ({t})" for n, t in data])
        await ctx.send(f"📋 Paneles:\n{texto}")

    # 🚀 Publicar panel (MULTI BOTONES)
    @commands.hybrid_command(name="publicar_panel")
    async def publicar_panel(self, ctx, nombre: str):
        cursor.execute("SELECT * FROM panels WHERE nombre=?", (nombre,))
        panel = cursor.fetchone()

        if not panel:
            return await ctx.send("❌ No existe")

        _, nombre, tipo, titulo, descripcion, color, rol_id = panel

        embed = discord.Embed(
            title=titulo,
            description=descripcion,
            color=color
        )

        # 🔘 crear view dinámica
        view = discord.ui.View(timeout=None)

        cursor.execute("SELECT label, tipo FROM panel_buttons WHERE panel_nombre=?", (nombre,))
        botones = cursor.fetchall()

        for label, tipo_boton in botones:

            async def callback(interaction: discord.Interaction, tipo_boton=tipo_boton):
                # 🔐 check rol
                if rol_id:
                    if rol_id not in [r.id for r in interaction.user.roles]:
                        return await interaction.response.send_message("❌ No tienes permiso", ephemeral=True)

                if tipo_boton == "ticket":
                    from bot.views.ticket_panel import TicketPanelView
                    await TicketPanelView().children[0].callback(interaction)

                elif tipo_boton == "form":
                    from bot.views.form_panel import FormPanelView
                    await FormPanelView().children[0].callback(interaction)

            button = discord.ui.Button(label=label, style=discord.ButtonStyle.primary)
            button.callback = callback
            view.add_item(button)

        await ctx.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(PanelCreator(bot))
