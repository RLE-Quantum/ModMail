import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("!help in DMs"))
    print('Bot is ready to rumble')

@bot.command()
async def help(ctx, *, description):
	if ctx.guild is None:
		initEmbed = discord.Embed(
			title='Ticket Initiated',
			description='Your ticket has been sent to the Rocket Legion staff team and is now being reviewed. Please wait patiently.',
			color=discord.Color.orange()
			)
		await ctx.send(embed=initEmbed)
		
		bot.opener = await bot.fetch_user(ctx.author.id)

		server = bot.get_guild(709362034965348392)
		category = bot.get_channel(734178904692228106)
		owner = server.get_role(709362078040981545)
		head_admin = server.get_role(718186259343736852)
		admin = server.get_role(710849864300232814)
		sen_mod = server.get_role(720649228053119026)

		perms = {
			owner: discord.PermissionOverwrite(read_messages=True, send_messages=True),
			head_admin: discord.PermissionOverwrite(read_messages=True, send_messages=True),
			admin: discord.PermissionOverwrite(read_messages=True, send_messages=True),
			sen_mod: discord.PermissionOverwrite(read_messages=True, send_messages=True),
			server.default_role: discord.PermissionOverwrite(read_messages=False)
		}
		bot.ticket_channel = await server.create_text_channel(f"{ctx.author}", overwrites=perms, category=category)
		bot.logs = server.get_channel(734511351128391962)

		openerEmbed = discord.Embed(
			title='ModMail Ticket',
			description=f'{description}',
			color=discord.Color.green()
			)

		openerEmbed.set_footer(text=f'Ticket opened by {ctx.author}.')

		openLogsEmbed = discord.Embed(
			title='Ticket Opened',
			description=f"Ticket opened by {ctx.author}",
			color=discord.Color.green())
			
		await bot.ticket_channel.send(embed=openerEmbed)
		await bot.logs.send(embed=openLogsEmbed)

@bot.command()
async def reply(ctx, *, description):
    bot.replyEmbed = discord.Embed(
        title='ModMail Ticket',
        description=f'{description}',
        color=discord.Color.green()
            )
                
    bot.replyEmbed.set_footer(text=f"{ctx.author}")

    if ctx.channel == bot.ticket_channel:
        await bot.opener.send(embed=bot.replyEmbed)
        await ctx.send(embed=bot.replyEmbed)
        await ctx.message.delete()
    
    elif isinstance(ctx.channel, discord.DMChannel):
        await ctx.send(embed=bot.replyEmbed)
        await bot.ticket_channel.send(embed=bot.replyEmbed)

@bot.command()
@commands.has_any_role('Head of Administration', 'Administrator', 'Owner', 'Senior Moderator')
async def close(ctx, *, reason=None):
	closeEmbed = discord.Embed(
		title='Ticket Closed',
		description=f'Your ModMail ticket was closed by {ctx.author}. Thanks for using ModMail!',
		color=discord.Color.red())
	closeEmbed.add_field(name='Reason', value=f"{reason}")
	
	closeLogsEmbed = discord.Embed(
		title="Ticket Closed",
		description=f"{reason}",
		color=discord.Color.red())

	await bot.ticket_channel.delete()
	await bot.opener.send(embed=closeEmbed)
	await bot.logs.send(embed=closeLogsEmbed)

@close.error
async def close_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("You didn't provide a reason. `!close <reason>`.")

@reply.error
async def reply_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("You didn't provide a message to send the staff team. `!reply <message>`.")

@help.error
async def help_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("You didn't provide a message to send the staff team. `!help <message>`.")

bot.run(token)