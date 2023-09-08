from utils.utils import fixDate, fixTime


def start_message(username):
    return "Hey **{username}**!" \
        "\nBenvenuto nel bot ufficiale di Craftopoly.\n" \
        "Qui puoi gestire i tuoi ticket senza necessariamente entrare in game".replace("{username}", username)


def connect_message_success(username):
    return "✅ Hai connesso con successo il tuo Craftopoly ID ({username}).\n" \
           "Fai il comando !ticket per interagire con i tickets".replace("{username}", username)


def ticket_successfully_created():
    return "✅ Hai creato con successo un ticket"


def ticket_successfully_closed():
    return "✅ Hai chiuso con successo questo ticket"


def ticket_successfully_commented():
    return "✅ Hai commentato con successo questo ticket"


def ticket_already_open():
    return "❌  Hai già un ticket aperto, chiudilo per aprirne un altro."


def ticket_closed():
    return "❌ Questo ticket è chiuso"


def ticket_already_closed():
    return "❌ Questo ticket è già chiuso"


def wrong_command_use():
    return "❌ Uso scorretto del comando"


def ticket_not_found():
    return "❌ Non è stato trovato alcun ticket con questo ID"


def user_already_connected():
    return "❌ Hai già connesso il tuo account telegram al tuo Craftopoly ID."


def user_code_not_found():
    return "❌ Codice non valido, riprova o richiedi un nuovo codice su minecraft"


def no_enough_permissions():
    return "❌ Non hai abbastanza permessi per eseguire questo comando"


def ticket_info(page, ticket):
    status = "Aperto\n" if ticket['open'] else "Chiuso\n"
    closed_on = "  • **Chiuso il**: " + fixDate(ticket['closed_on'].split(" ")[0]) + " alle " + \
                fixTime(ticket['closed_on'].split(" ")[1]) if not ticket['open'] else ""

    styledTicket = "• **Ticket #"+str(ticket['ticket_id']) + "**  (Pagina " + page + ")" + \
                   "\n\n" + "  • **Stato**: " + status + "  • **Player**: "+ticket['owner']['username'] + "\n" + \
                   "  • **Aperto il**: " + fixDate(ticket['created_on'].split(" ")[0]) + " alle " + \
                   fixTime(ticket['created_on'].split(" ")[1]) + "\n" + closed_on + "\n\n "

    messages = "    **Messaggi**:\n"
    for message in ticket['messages']:
        messages += "     **|** " + message['owner']['username'] + " ➜ " + message['content'] + "\n"

    return styledTicket + messages


def ticket_list_info(page, tickets):
    res = "**Tickets**  (Pagina " + page + ")\n\n"
    for tick in tickets:
        status = "[Aperto]" if tick['open'] else "[Chiuso]"
        res += status + "** #"+str(tick['ticket_id']) + \
           " **" + tick['owner']['username'] + " ➜ " + (
                   tick['message'] if len(tick['message']) < 34 else tick['message'][0:34]+"..."
               ) + "\n"
    return res


def not_connected():
    return "❌ Errore, prima di eseguire comandi devi connettere il tuo account telegram al tuo Craftopoly ID. Entra sul server minecraft e fai il comando **/connect-telegram**"


def error():
    return "❌ Errore durante l'esecuzione del comando, riprovare."


def help_message():
    return "**Tickets** \n\n" \
           "  • !ticket create <messaggio> ➜ Crea un ticket\n" \
           "  • !ticket list <pagina> ➜ Guarda i tuoi ticket\n" \
           "  • !ticket info <ticketId> pagina> ➜ Visualizza un ticket\n" \
           "  • !ticket comment <tticketId> <commento> ➜ Commenta un ticket\n" \
           "  • !ticket close <;ticketId> ➜ Chiudi un ticket\n"