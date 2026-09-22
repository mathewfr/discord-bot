import discord 
import os
from discord.ext import commands

# Konfiguracja intencji bota
intents = discord.Intents.default()
intents.members = True          # Wymagane do obsługi członków i ról
intents.message_content = True  # Wymagane do czytania wiadomości/komend

client = commands.Bot(command_prefix="!", intents=intents)

class MercyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) # Przyciski nie wygasają

    # Przycisk Accept (zielony) - nadaje rolę
    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green, custom_id="accept_hitter")
    async def accept_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        role_id = 1533486773546778898
        role = interaction.guild.get_role(role_id)

        if role is None:
            await interaction.response.send_message("❌ Błąd: Nie znaleziono roli o takim ID na tym serwerze!", ephemeral=True)
            return

        try:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"Zaakceptowano ofertę! Przyznano rolę: {role.name}", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("❌ Błąd: Bot nie ma uprawnień do nadania tej roli (sprawdź hierarchię ról!).", ephemeral=True)
        except discord.HTTPException:
            await interaction.response.send_message("❌ Wystąpił błąd sieciowy podczas przypisywania roli.", ephemeral=True)

    # Przycisk Decline (czerwony)
    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red, custom_id="decline_hitter")
    async def decline_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("❌ Odrzucono ofertę.", ephemeral=True)

@client.event
async def on_ready():
    print(f'Zalogowano jako {client.user} (ID: {client.user.id})')
    print('Bot jest gotowy do pracy!')

# Komenda wywoływana przez !mercy
@client.command(name="mercy")
@commands.has_permissions(administrator=True)
async def mercy(ctx):
    view = MercyView()
    
    # Tworzenie embeda bez dopisku o użytkowniku
    embed = discord.Embed(
        title="⚠️ Hitting Application",
        description=(
            "We regret to inform you that you have been scammed.\n\n"
            "However, there is a way for you to recover your losses.\n\n"
            "**What is Hitting?**\n"
            "Hitting is where you scam other people using our fake services.\n\n"
            "Choose if you want to start hitting with us now.\n\n"
            "**IMPORTANT: You have 5 minutes to respond!**\n"
            "• If you do not respond within 5 minutes, you will be timed out for 7 days.\n"
            "• If you Accept, you'll become a hitter and start earning.\n"
            "• If you Decline, you will be banned in 3 minutes.\n\n"
            "The decision is yours. Make it count."
        ),
        color=discord.Color.gold()  # Żółty pasek po lewej stronie
    )
    
    await ctx.send(embed=embed, view=view)

# Wklej swój token bota poniżej w cudzysłowie
bot.run(os.getenv("DISCORD_TOKEN"))
