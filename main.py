from threading import Thread

from balethon import Client
from balethon.conditions import regex
from balethon.objects import InlineKeyboardButton, InlineKeyboard

from mafia import Mafia
from phases import Conversing, Night, Voting, Defending, Judging, LastWords, Execution
import texts
import config

reply_markup1 = InlineKeyboard([
    [InlineKeyboardButton("من میام", "me")],
    [InlineKeyboardButton("من نمیام", "not_me")]
])
reply_markup2 = InlineKeyboard([
    [InlineKeyboardButton("بله", "yes"), InlineKeyboardButton("نه", "no")]
])


class MafiaClient(Client):

    def __init__(self):
        super().__init__(config.TOKEN)
        self.mafia = None
        self.voting_message = None
        self.voting_reply_markup = None


bot = MafiaClient()


def on_phase(client, phase):
    if isinstance(phase, Conversing):
        client.send_message(config.CHAT_ID, f"{texts.conversing_phase_started}\n{texts.time.format(phase.time)}")

    elif isinstance(phase, Night):
        if client.voting_message:
            client.voting_message.delete()
            client.voting_message = None
        client.send_message(config.CHAT_ID, f"{texts.night_phase_started}\n{texts.time.format(phase.time)}")
        for player in client.mafia.players:
            try:
                client.send_message(player.id, "نقش شبت رو انجام بده دا")
            except Exception as error:
                print(f"{player.name}: {error}")

    elif isinstance(phase, Voting):
        buttons = [[InlineKeyboardButton(player.name, f"vote:{i}")] for i, player in enumerate(client.mafia.alive_players)]
        reply_markup = InlineKeyboard(buttons)
        client.voting_reply_markup = reply_markup
        client.voting_message = client.send_message(config.CHAT_ID, f"{texts.voting_phase_started}\n{texts.time.format(phase.time)}", reply_markup=reply_markup)

        from balethon.objects import CallbackQuery, User

        callback_query = CallbackQuery(author=User(id=200, first_name="bot2"), message=client.voting_message, data="vote:0")
        ocq_vote(client, callback_query)

    elif isinstance(phase, Defending):
        if client.voting_message:
            client.voting_message.delete()
            client.voting_message = None
        client.send_message(config.CHAT_ID, f"{texts.voted_player.format(player=phase.player)}\n{texts.defending_phase_started}\n{texts.time.format(phase.time)}")

    elif isinstance(phase, Judging):
        client.voting_message = client.send_message(config.CHAT_ID, f"{texts.judging_phase_started}\n{texts.is_player_guilty.format(player=phase.player)}\n{texts.time.format(phase.time)}", reply_markup=reply_markup2)

    elif isinstance(phase, LastWords):
        if client.voting_message:
            client.voting_message.delete()
            client.voting_message = None
        client.send_message(config.CHAT_ID, f"{texts.last_words_phase_started}\n{texts.player(player=phase.player)}\n{texts.time.format(phase.time)}")

    elif isinstance(phase, Execution):
        phase.player.get_executed()
        client.send_message(config.CHAT_ID, f"{texts.execution_phase_started}\n{texts.player(player=phase.player)}\n{texts.time.format(phase.time)}")


@bot.on_message(chain="delete")
async def delete_messages(client, message):
    if client.mafia is None:
        return

    if isinstance(client.mafia.phase, Night):
        await message.delete()

    elif isinstance(client.mafia.phase, Defending) and client.mafia.phase.player.id != message.author.id:
        await message.delete()

    elif isinstance(client.mafia.phase, LastWords) and client.mafia.phase.player.id != message.author.id:
        await message.delete()

    elif isinstance(client.mafia.phase, Execution) and client.mafia.phase.player.id == message.author.id:
        await message.delete()


@bot.on_command()
def start(client, message):
    client.mafia = Mafia()
    msg = message.reply(texts.who_plays, reply_markup=reply_markup1)

    from balethon.objects import CallbackQuery, User

    for i in range(1, 12):
        callback_query = CallbackQuery(author=User(id=i * 100, first_name=f"bot{i}"), message=msg)
        ocq_me(client, callback_query)


@bot.on_message(chain="print")
def print_message(client, message):
    print(f"{message.author.first_name}: {message.text}")


@bot.on_callback_query(chain="print")
def print_callback_query(client, callback_query):
    print(f"{callback_query.author.first_name}: [{callback_query.data}]")


@bot.on_callback_query(regex("^me$"))
def ocq_me(client, callback_query):
    if not client.mafia.add_player(callback_query.author.id, callback_query.author.first_name):
        return
    if not len(client.mafia.players) >= 12:
        return callback_query.message.edit_text(f"{texts.who_plays}\n{client.mafia}", reply_markup=reply_markup1)
    callback_query.message.edit_text(f"{texts.starting}\n{client.mafia}")
    client.mafia.assign_roles()

    roles = [f"{player}: {type(player).__name__}{player.emoji}" for player in client.mafia.players]
    client.send_message(config.CHAT_ID, "\n".join(roles))

    for player in client.mafia.players:
        try:
            client.send_message(player.id, type(player).__name__)
        except Exception as error:
            print(f"{player.name}: {error}")
    callback_query.message.edit_text(f"{texts.game_started}\n{client.mafia}")
    Thread(target=client.mafia.run, args=(client, on_phase)).start()


@bot.on_callback_query(regex("^not_me$"))
def ocq_not_me(client, callback_query):
    if client.mafia.remove_player(callback_query.author.id):
        return callback_query.message.edit_text(f"{texts.who_plays}\n{client.mafia}", reply_markup=reply_markup1)


@bot.on_callback_query(regex("^vote:"))
def ocq_vote(client, callback_query):
    voted = client.mafia.alive_players[int(callback_query.data[5:])]
    voter, = [player for player in client.mafia.alive_players if player.id == callback_query.author.id]
    client.mafia.phase.vote(client.mafia.alive_players, voter, voted)
    votes = [f"{voter}: {voted}" for voter, voted in zip(client.mafia.phase.voters, client.mafia.phase.voteds)]
    votes = "\n".join(votes)
    print(votes)
    callback_query.message.edit_text(
        f"{texts.voting_phase_started}\n{texts.time.format(client.mafia.phase.time)}\n{votes}",
        reply_markup=client.voting_reply_markup
    )


@bot.on_callback_query(regex("^yes$"))
def ocq_yes(client, callback_query):
    voter, = [player for player in client.mafia.alive_players if player.id == callback_query.author.id]
    if voter in client.mafia.phase.voters:
        client.mafia.phase.unvote(voter)
        choices = dict(enumerate([texts.guilty, texts.innocent]))
        votes = [f"{voter}: {choices[vote]}" for voter, vote in zip(client.mafia.phase.voters, client.mafia.phase.votes)]
        votes = "\n".join(votes)
        callback_query.message.edit_text(
            f"{texts.judging_phase_started}\n{texts.is_player_guilty.format(player=client.mafia.phase.player)}\n{texts.time.format(client.mafia.phase.time)}\n{votes}",
            reply_markup=reply_markup2
        )
    client.mafia.phase.vote(voter, True)
    choices = dict(enumerate([texts.guilty, texts.innocent]))
    votes = [f"{voter}: {choices[vote]}" for voter, vote in zip(client.mafia.phase.voters, client.mafia.phase.votes)]
    votes = "\n".join(votes)
    callback_query.message.edit_text(
        f"{texts.judging_phase_started}\n{texts.is_player_guilty.format(player=client.mafia.phase.player)}\n{texts.time.format(client.mafia.phase.time)}\n{votes}",
        reply_markup=reply_markup2
    )


@bot.on_callback_query(regex("^no$"))
def ocq_no(client, callback_query):
    voter, = [player for player in client.mafia.alive_players if player.id == callback_query.author.id]
    if voter in client.mafia.phase.voters:
        client.mafia.phase.unvote(voter)
        choices = dict(enumerate([texts.guilty, texts.innocent]))
        votes = [f"{voter}: {choices[vote]}" for voter, vote in zip(client.mafia.phase.voters, client.mafia.phase.votes)]
        votes = "\n".join(votes)
        callback_query.message.edit_text(
            f"{texts.judging_phase_started}\n{texts.is_player_guilty.format(player=client.mafia.phase.player)}\n{texts.time.format(client.mafia.phase.time)}\n{votes}",
            reply_markup=reply_markup2
        )
    client.mafia.phase.vote(voter, False)
    choices = dict(enumerate([texts.guilty, texts.innocent]))
    votes = [f"{voter}: {choices[vote]}" for voter, vote in zip(client.mafia.phase.voters, client.mafia.phase.votes)]
    votes = "\n".join(votes)
    callback_query.message.edit_text(
        f"{texts.judging_phase_started}\n{texts.is_player_guilty.format(player=client.mafia.phase.player)}\n{texts.time.format(client.mafia.phase.time)}\n{votes}",
        reply_markup=reply_markup2
    )


if __name__ == "__main__":
    bot.run()
