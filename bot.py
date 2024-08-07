from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackContext
import json

# Substitua 'YOUR_TOKEN' pelo token do seu bot
TOKEN = '7227344806:AAGsi2PITxi6ab51w7WL79PsV9YLmNBWYAg'
GAME_URL = 'https://7f86-2804-1690-9c1-9900-706d-8f91-38ce-9251.ngrok-free.app'  # Substitua pelo URL fornecido pelo ngrok

# Função para carregar usuários do arquivo JSON
def load_users():
    try:
        with open('users.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Função para salvar usuários no arquivo JSON
def save_users(users):
    with open('users.json', 'w') as file:
        json.dump(users, file, indent=4)

async def start(update: Update, context: CallbackContext) -> None:
    users = load_users()
    user_id = str(update.message.from_user.id)
    user_name = update.message.from_user.username or update.message.from_user.first_name  # Garantir que temos um nome

    if user_id not in users:
        users[user_id] = {'id': user_id, 'name': user_name, 'tokens': 0}
        save_users(users)
    else:
        users[user_id]['name'] = user_name  # Atualizar o nome se necessário

    game_url = f"{GAME_URL}?user_id={user_id}&user_name={user_name}"
    keyboard = [[InlineKeyboardButton("Lançar Jogo", web_app=WebAppInfo(url=game_url))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Clique no botão abaixo para jogar!', reply_markup=reply_markup)

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

if __name__ == '__main__':
    main()
