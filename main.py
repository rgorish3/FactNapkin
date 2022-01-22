import discord
import os

from database import cursor, db

from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()                                 #Sets up the intent which allows the bot to see the other users in the server
intents.members = True                                              #

client = discord.Client(intents=intents)

@client.event

async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    
    if message.author == client.user:
        return
    

    msgFull = message.content
    msgAuthor = message.author.name + '#' + message.author.discriminator
    msgServer = message.guild.name


    if msgFull.lower().startswith('&fact'):
        
        sql = ('SELECT Fact, Name FROM Facts WHERE Server=%s ORDER BY RAND() LIMIT 1')
        cursor.execute(sql, (msgServer,))
        result = cursor.fetchone()


        if not result:
            await message.channel.send('No facts have been added. Use the add command to add some.')
        else:
            authorSplit = result[1].split('#')
            authorUser = discord.utils.get(message.guild.members, name = authorSplit[0], discriminator= authorSplit[1])

            await message.channel.send(f'`{result[0]}`\n\n-submitted by {authorUser.mention}')
        
    if msgFull.lower().startswith('&about'):
        await message.channel.send('FactNapkin is a bot that will dispense random facts of potentially dubious accuracy.')
    
    if msgFull.lower().startswith('&help'):

        commands= 'COMMANDS:\n----------------\n'
        commands+='**fact** - Returns a random fact.\n'
        commands+='**add** - Add a fact.\n'
        commands+='**list** - Lists all facts user has added.\n'
        commands+='**delete** - Delete a fact you added (use number shown by list command)\n'
        commands+='**about** - Information about FactNapkin.'
        await message.channel.send(commands)

    if msgFull.lower().startswith('&add'):

        msg = msgFull
        msg = msg[4:]
        msg = msg.strip()

        if msg.isspace() or msg=="":
            await message.channel.send('No fact was submitted')
        else:
            sql = ('INSERT INTO Facts(Fact,Name,Server) VALUES (%s,%s,%s)')
            cursor.execute(sql,(msg, msgAuthor, msgServer))
            db.commit()
            await message.channel.send('Fact added!')
    
    if msgFull.lower().startswith('&list'):

        sql = ('SELECT Fact FROM Facts WHERE Server = %s AND Name = %s')
        cursor.execute(sql,(msgServer,msgAuthor))
        result = cursor.fetchall()
        

        i=1
        outputStr =  message.author.mention + "'s facts\n```"
        
        if not result:
            outputStr += 'You have added no facts! Get to adding!'
        else:
            for fact in result:
                outputStr += str(i) + '. ' + fact[0] + '\n'
                i += 1

        outputStr += '```'
        
        await message.channel.send(outputStr)

    if msgFull.lower().startswith('&delete'):

        msg = msgFull
        msg = msg[7:]
        msg = msg.strip()

        sql = ('SELECT count(*) FROM Facts WHERE Name=%s')
        cursor.execute(sql,(msgAuthor,))
        count = int(cursor.fetchone()[0])


        if msg.isdigit():
            msgInt = int(msg)
            if msgInt > 0 and msgInt <= count:
                sql = ('DELETE FROM Facts WHERE FactID = (SELECT FactID FROM (SELECT FactID FROM Facts WHERE Name=%s ORDER BY FactID LIMIT 1 OFFSET %s) AS tbl)')
                cursor.execute(sql,(msgAuthor, msgInt-1))
                db.commit()

                await message.channel.send('Fact deleted!')
            else:
                await message.channel.send('Invalid Selection')
        else:
            await message.channel.send('Selection Must Be A Number')


client.run(os.getenv("DISCORD_TOKEN"))

db.close()