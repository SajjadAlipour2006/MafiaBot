from threading import Thread

from balethon import Client
from balethon.conditions import regex
from balethon.objects import InlineKeyboardButton, InlineKeyboard

from mafia import Mafia
from phases import Conversing, Night, Voting, Defending, Judging, LastWords
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
        client.send_message(config.CHAT_ID, f"فاز گفتگو شروع شد\nزمان: {phase.time}")

    elif isinstance(phase, Night):
        if client.voting_message:
            client.voting_message.delete()
            client.voting_message = None
        client.send_message(config.CHAT_ID, f"فاز شب شروع شد\nزمان: {phase.time}")

    elif isinstance(phase, Voting):
        buttons = [[InlineKeyboardButton(player.name, f"vote:{i}")] for i, player in enumerate(client.mafia.players)]
        reply_markup = InlineKeyboard(buttons)
        client.voting_reply_markup = reply_markup
        client.voting_message = client.send_message(config.CHAT_ID, f"فاز رای گیری شروع شد\nزمان: {phase.time}", reply_markup=reply_markup)

        from balethon.objects import CallbackQuery, User

        callback_query = CallbackQuery("1", User(20, first_name="bot2"), client.voting_message, data="vote:0")
        ocq_vote(client, callback_query)

    elif isinstance(phase, Defending):
        if client.voting_message:
            client.voting_message.delete()
            client.voting_message = None
        client.send_message(config.CHAT_ID, f"بازیکن {phase.player} با رای گیری انتخاب شد\nفاز دفاع شروع شد\nزمان: {phase.time}")

    elif isinstance(phase, Judging):
        client.voting_message = client.send_message(config.CHAT_ID, f"فاز قضاوت شروع شد\nآیا {phase.player} گناهکار است؟\nزمان: {phase.time}", reply_markup=reply_markup2)

    elif isinstance(phase, LastWords):
        if client.voting_message:
            client.voting_message.delete()
            client.voting_message = None
        client.send_message(config.CHAT_ID, f"فاز حرف آخر برای {phase.player} شروع شد\nزمان: {phase.time}")


@bot.on_command()
def start(client, message):
    client.mafia = Mafia()
    msg = message.reply("کی میاد مافیا", reply_markup=reply_markup1)

    from balethon.objects import CallbackQuery, User

    callback_query = CallbackQuery("1", User(100, first_name="bot1"), msg)
    ocq_me(client, callback_query)

    callback_query = CallbackQuery("1", User(20, first_name="bot2"), msg)
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
    players = "\n".join(str(player) for player in client.mafia.players)
    if not len(client.mafia.players) >= 3:
        return callback_query.message.edit_text(f"کی میاد مافیا\n{players}", reply_markup=reply_markup1)
    callback_query.message.edit_text(f"در حال شروع بازی...\n{players}")
    client.mafia.assign_roles()
    for player in client.mafia.players:
        try:
            client.send_message(player.id, type(player).__name__)
        except Exception as error:
            print(f"{player.name}: {error}")
    callback_query.message.edit_text(f"بازی شروع شد\n{players}")
    Thread(target=client.mafia.run, args=(client, on_phase)).start()


@bot.on_callback_query(regex("^not_me$"))
def ocq_not_me(client, callback_query):
    if client.mafia.remove_player(callback_query.author.id):
        players = "\n".join(str(player) for player in client.mafia.players)
        return callback_query.message.edit_text(f"کی میاد مافیا\n{players}", reply_markup=reply_markup1)


@bot.on_callback_query(regex("^vote:"))
def ocq_vote(client, callback_query):
    voted = client.mafia.players[int(callback_query.data[5:])]
    voter, = [player for player in client.mafia.players if player.id == callback_query.author.id]
    client.mafia.phase.vote(client.mafia.players, voter, voted)
    votes = [f"{voter}: {voted}" for voter, voted in zip(client.mafia.phase.voters, client.mafia.phase.voteds)]
    votes = "\n".join(votes)
    print(votes)
    callback_query.message.edit_text(
        f"فاز رای گیری شروع شد\nزمان: {client.mafia.phase.time}\n{votes}",
        reply_markup=client.voting_reply_markup
    )


@bot.on_callback_query(regex("^yes$"))
def ocq_yes(client, callback_query):
    voter, = [player for player in client.mafia.players if player.id == callback_query.author.id]
    if voter in client.mafia.phase.voters:
        client.mafia.phase.unvote(voter)
        votes = [f"{voter}: {'گناهکار' if vote else 'بیگناه'}" for voter, vote in
                 zip(client.mafia.phase.voters, client.mafia.phase.votes)]
        votes = "\n".join(votes)
        callback_query.message.edit_text(
            f"فاز قضاوت شروع شد\nآیا {client.mafia.phase.player} گناهکار است؟\nزمان: {client.mafia.phase.time}\n{votes}",
            reply_markup=reply_markup2
        )
    client.mafia.phase.vote(voter, True)
    votes = [f"{voter}: {'گناهکار' if vote else 'بیگناه'}" for voter, vote in
             zip(client.mafia.phase.voters, client.mafia.phase.votes)]
    votes = "\n".join(votes)
    callback_query.message.edit_text(
        f"فاز قضاوت شروع شد\nآیا {client.mafia.phase.player} گناهکار است؟\nزمان: {client.mafia.phase.time}\n{votes}",
        reply_markup=reply_markup2
    )


@bot.on_callback_query(regex("^no$"))
def ocq_no(client, callback_query):
    voter, = [player for player in client.mafia.players if player.id == callback_query.author.id]
    if voter in client.mafia.phase.voters:
        client.mafia.phase.unvote(voter)
        votes = [f"{voter}: {'گناهکار' if vote else 'بیگناه'}" for voter, vote in
                 zip(client.mafia.phase.voters, client.mafia.phase.votes)]
        votes = "\n".join(votes)
        callback_query.message.edit_text(
            f"فاز قضاوت شروع شد\nآیا {client.mafia.phase.player} گناهکار است؟\nزمان: {client.mafia.phase.time}\n{votes}",
            reply_markup=reply_markup2
        )
    client.mafia.phase.vote(voter, False)
    votes = [f"{voter}: {'گناهکار' if vote else 'بیگناه'}" for voter, vote in
             zip(client.mafia.phase.voters, client.mafia.phase.votes)]
    votes = "\n".join(votes)
    callback_query.message.edit_text(
        f"فاز قضاوت شروع شد\nآیا {client.mafia.phase.player} گناهکار است؟\nزمان: {client.mafia.phase.time}\n{votes}",
        reply_markup=reply_markup2
    )


if __name__ == "__main__":
    bot.run()