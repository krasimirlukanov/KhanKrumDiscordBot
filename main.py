import json
import discord


bot = discord.Bot(intents=discord.Intents.all())


guild_ids = [1089990515946164254]


@bot.event
async def on_ready():
    print("Ok!")


@bot.slash_command(name="meeting", description="Schedule a meeting.", guild_ids=guild_ids)
async def meeting(ctx: discord.ApplicationContext, date, hour):
    channel = bot.get_channel(1090304686545969212)
    embed = discord.Embed(colour=discord.Colour.random())
    embed.title = f"Meeting!!! - Date: {date} - Hour: {hour}"
    embed.set_footer(icon_url=ctx.user.avatar, text=f"Meeting requested by {ctx.user.name}")
    await ctx.respond("Ok!")
    await channel.send(embed=embed)


@bot.slash_command(name="purge", description="Purges a channel with the provided limit.", guild_ids=guild_ids)
async def purge(ctx: discord.ApplicationContext,
                limit: discord.Option(int, description="How many messages do you want to be deleted?")):
    await ctx.channel.purge(limit=limit)
    await ctx.respond(f"{limit} messages were deleted by {ctx.author.mention}.")
    await ctx.message.delete()


@bot.slash_command(name="assign_task", description="Assign a task to a user.", guild_ids=guild_ids)
async def assign_task(ctx: discord.ApplicationContext, user: discord.Member, task):
    channel = bot.get_channel(1090309876846186626)
    with open('tasks.json', 'r') as f:
        tasks = json.load(f)

    embed = discord.Embed(colour=discord.Colour.random(), title=f"Task - {user.name}")
    embed.add_field(name="Task:", value=task)
    embed.add_field(name="Task ID:", value=str(get_last_task_id(user)))
    embed.set_thumbnail(url=user.avatar)
    msg = await channel.send(embed=embed)
    msg_id = msg.id

    try:
        tasks[str(user.id)]['tasks'][get_last_task_id(user)] = task
        tasks[str(user.id)]['msg_ids'][get_last_task_id(user)] = msg_id
    except KeyError:
        tasks[str(user.id)] = {}
        tasks[str(user.id)]['tasks'] = {}
        tasks[str(user.id)]['tasks'][get_last_task_id(user)] = task

        tasks[str(user.id)]['msg_ids'] = {}
        tasks[str(user.id)]['msg_ids'][get_last_task_id(user)] = msg_id

    with open('tasks.json', 'w') as f:
        json.dump(tasks, f)

    await ctx.respond("Ok.")


@bot.slash_command(name="remove_task", description="Remove a task from a user.", guild_ids=guild_ids)
async def remove_task(ctx: discord.ApplicationContext, user: discord.Member, task_id):
    done_channel = bot.get_channel(1090333425136828418)
    with open('tasks.json', 'r') as f:
        tasks = json.load(f)

    msg_id = tasks[str(user.id)]["msg_ids"][task_id]
    msg = bot.get_message(msg_id)
    await msg.delete()
    await done_channel.send(msg.content)
    try:
        del tasks[str(user.id)]['tasks'][task_id]
        del tasks[str(user.id)]['msg_ids'][task_id]
        await ctx.respond(f"Removed task {task_id} from {user.mention}.")
    except KeyError:
        await ctx.respond(f"No task matching the provided ID for this user.")

    with open('tasks.json', 'w') as f:
        json.dump(tasks, f)
    await ctx.respond("Ok!")


def get_last_task_id(user: discord.Member):
    user_id = str(user.id)
    with open('tasks.json', 'r') as f:
        tasks = json.load(f)
        try:
            ids: dict = tasks[user_id]['tasks']
            num = list(ids.keys())[-1]
            return int(num) + 1
        except IndexError:
            return 0
        except KeyError:
            return 0


bot.run("MTA5MDMwMTgxMTAxMDgzMDQ3Nw.GBldhk.Xko2zTAi8aZ377MyMyREp1i0N7LBWN6fn2sGAE")
