import discord
import os
import time

from database import cursor, db, connect

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

    
    if message.author == client.user:        return
    

    


    msgFull = message.content
    msgAuthor = message.author.name + '#' + message.author.discriminator
    msgServer = message.guild.name


    if msgFull.lower().startswith('&fact'):

        ts = time.time()
        print(f'Fact Start: {ts}')


        connect()
        
        sql = ('SELECT Fact, Name FROM Facts WHERE Server=%s ORDER BY RAND() LIMIT 1')
        cursor.execute(sql, (msgServer,))
        result = cursor.fetchone()


        if not result:
            await message.channel.send('No facts have been added. Use the add command to add some.')
        else:
            authorSplit = result[1].split('#')
            authorUser = discord.utils.get(message.guild.members, name = authorSplit[0], discriminator= authorSplit[1])

            await message.channel.send(f'`{result[0]}`\n\n-submitted by {authorUser.mention}')

        
        ts = time.time()
        print(f'Fact End: {ts}')

        
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


        ts = time.time()
        print(f'Add Start: {ts}')

        connect()

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

        ts = time.time()
        print(f'Add End: {ts}')

    
    if msgFull.lower().startswith('&list'):
        ts = time.time()
        print(f'List Start: {ts}')
        
        connect()

        sql = ('SELECT Fact FROM Facts WHERE Server = %s AND Name = %s')
        cursor.execute(sql,(msgServer,msgAuthor))
        result = cursor.fetchall()
        

        i=1
        outputStr =  message.author.mention + "'s facts\n```"
        
        if not result:
            outputStr += 'You have added no facts! Get to adding!```'
            await message.channel.send(outputStr)
        else:
            for fact in result:
                outputStr += str(i) + '. ' + fact[0] + '\n\n'
                i += 1
        
            brokenUpOutput = []
            firstRun = True
            markdown = ''


            while len(outputStr) > 0:                                                              #This loop will populate brokenUpOutput which is a list that breaks up]
                                                                                                    #   outputStr into approximately 1800 character chunks. Discord has a
                                                                                                    #   character limit of 2000. There are three possibilities that I am
                                                                                                    #   accounting for. Less than 1800 characters, where I just place the whole
                                                                                                    #   string in the list and end the loop. Greater than 1800 characters and there 
                                                                                                    #   is a space character after the 1800 index. I split the string at that space
                                                                                                    #   and place the first part into the list and rerun the loop with the remaining
                                                                                                    #   part. Finally, Greater than 1800 characters and there is a no space character
                                                                                                    #   after the 1800 index. I split it at the 1800 mark and put the rest back in
                                                                                                    #   outputStr. Considered recursive function to do this, elected not to as
                                                                                                    #   this code will never be reused elsewhere.
                if(len(outputStr)>=1800):                                                          
                    spaceIndex = outputStr.find(' ',1800)                                       
                    if spaceIndex >= 0:
                        brokenUpOutput.append(markdown + outputStr[0:spaceIndex] + '```')
                        outputStr = outputStr[spaceIndex+1:len(outputStr)]
                    
                    else:
                        brokenUpOutput.append(markdown + outputStr[0:1800] + '```')
                        outputStr = outputStr[1800:len(outputStr)]
                else:
                    brokenUpOutput.append(markdown + outputStr + '```')
                    outputStr = ''
                
                if(firstRun):
                    markdown='```'
                    firstRun=False

            for output in brokenUpOutput:
                
                await message.channel.send(output)
        ts = time.time()
        print(f'List End: {ts}')
     
    if msgFull.lower().startswith('&delete'):
        
        ts = time.time()
        print(f'Delete Start: {ts}')

        connect()

        msg = msgFull
        msg = msg[7:]
        msg = msg.strip()

        sql = ('SELECT count(*) FROM Facts WHERE Name=%s')
        cursor.execute(sql,(msgAuthor,))
        count = int(cursor.fetchone()[0])


        if msg.isdigit():
            msgInt = int(msg)
            if msgInt > 0 and msgInt <= count:
                sql = ('DELETE FROM Facts WHERE FactID = (SELECT FactID FROM (SELECT FactID FROM Facts WHERE Name=%s AND Server=%s ORDER BY FactID LIMIT 1 OFFSET %s) AS tbl)')
                cursor.execute(sql,(msgAuthor,msgServer, msgInt-1))
                db.commit()

                await message.channel.send('Fact deleted!')
            else:
                await message.channel.send('Invalid Selection')
        else:
            await message.channel.send('Selection Must Be A Number')
        
        ts = time.time()
        print(f'Delete End: {ts}')


client.run(os.getenv("DISCORD_TOKEN"))

#db.close()