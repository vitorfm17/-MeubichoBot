#-- coding: utf-8 --
#bibliotecas
import requests 
import telebot
from telebot import types
import pymysql 

#conexão com o banco
conn = pymysql.connect(host='127.0.0.1', 
unix_socket='/opt/lampp/var/mysql/mysql.sock',
user='root',
passwd=None,
db='MeuBichoBot')

cur = conn.cursor() #conexao com o xampp

#dados de conexão a api do Telegram
API_TOKEN = '1275538427:AAH_qFIypkskwC6QsD0-0cqnNoA1bKKi6Iw'
bot = telebot.TeleBot(API_TOKEN)

user_dict = {}
pet_dict = {}
class User:
    def __init__(self,name):
        self.name = name
        self.endereco = None
        self.telefone = None

class Pet:
    def __init__(self,petname):
        self.petname = petname
        self.tipo = None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    cid = message.chat.id #pegar id da conversa
    #teste se está cadastrado
    cur.execute("USE MeuBichoBot")
    cur.execute("SELECT * FROM usuario where chatid =" + str(cid))
    #cur.execute("SELECT * FROM usuario where chatid =0000")
    chat_id = cur.fetchone()
    if chat_id is None:
        #vai para o fluxo de cadastro
        msg = bot.reply_to(message,"Hmm... Vejo que é o seu primeiro contato. Precisaremos fazer um breve cadastro para continuar. Ao final não deixe de guardar o ID que será gerado, ele poderá ser usado para agilizar o seu atendimento em todos os canais de atendimento e nas lojas presenciais.😃")
        bot.send_message(cid,"Primeiramente, me informe o seu nome: ")
        bot.register_next_step_handler(msg,name_step)
    else:
        #vai para o menu
        cur.execute("USE MeuBichoBot")
        cur.execute("SELECT nome FROM usuario where chatid =" + str(cid))
        aux1 = cur.fetchone()
        aux2 = str(aux1)
        aux3 = aux2[:-3]
        chat_nome = aux3[2:]
        print(chat_nome)
        msg = bot.reply_to(message,"Olá, " + str(chat_nome) + "! Que legal falar com você novamente. Clique em /menu para continuar.") 
        #bot.register_next_step_handler(msg,menu_step)

#fluxo de cadastro
def name_step(message):
    try:
        cid = message.chat.id
        name = message.text 
        user = User(name) 
        user_dict[cid] = user
        msg = bot.reply_to(message,"Agora informe o seu endereço completo (rua, número, complemento e bairro):")
        bot.register_next_step_handler(msg,endereco_step)

    except Exception as e:
        msg = bot.reply_to(message,"Algo deu errado. Entre em contato com (21) 2447-0486 para que possamos ajudar. Ou clique em /start para tentar novamente.")
        print(e)

def endereco_step(message):
    try:
        cid = message.chat.id
        endereco = message.text
        user = user_dict[cid]
        user.endereco = endereco
        msg = bot.reply_to(message,"Precisamos também do número do seu celular, com o DDD e somente os números:")
        bot.register_next_step_handler(msg,tel_step)

    except Exception as e:
        msg = bot.reply_to(message,"Algo deu errado. Entre em contato com (21) 2447-0486 para que possamos ajudar. Ou clique em /start para tentar novamente.")
        print(e)

def tel_step(message):
    try:
        cid = message.chat.id
        telefone = message.text
        if not telefone.isdigit():
			msg = bot.reply_to(message,"Somente números são aceitos! Informe o seu celular:")
			bot.register_next_step_handler(msg,tel_step)
			return
        user = user_dict[cid]
        user.telefone = telefone
        
        #inserindo os dados no banco
        cur.execute("USE MeuBichoBot") 
        sql = "insert into usuario (nome, chatid, endereco, telefone) values (%s,%s,%s,%s)"
        val = (user.name,cid,user.endereco,user.telefone)
        cur.execute(sql,val)
        conn.commit()

        #confirmar cadastro
        cur.execute("USE MeuBichoBot")
        cur.execute("SELECT id_usuario FROM usuario where chatid =" + str(cid))
        aux1 = cur.fetchone()
        aux2 = str(aux1)
        aux3 = aux2[:-2]
        user_id = aux3[1:]
        print(user_id)
       
        
        msg = bot.reply_to(message,"Que legal, seu cadastro foi bem sucedido. O seu ID é: " + user_id + ". \nAgora vamos cadastrar o seu animal de estimação.")
        bot.send_message(cid,"Informe o nome do seu amiguinho: ")
        bot.register_next_step_handler(msg,name_pet_step)

    except Exception as e:
        msg = bot.reply_to(message,"Algo deu errado. Entre em contato com (21) 2447-0486 para que possamos ajudar. Ou clique em /start para tentar novamente.")
        print(e)

def name_pet_step(message):
    try:
        cid = message.chat.id
        petname = message.text 
        pet = Pet(petname) 
        pet_dict[cid] = pet
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Gato','Cachorro','Ave','Roedor')
        msg = bot.reply_to(message,'Seu pet é de qual espécie?', reply_markup=markup)
        bot.register_next_step_handler(msg,tipo_especie)

    except Exception as e:
        msg = bot.reply_to(message,"Algo deu errado. Entre em contato com (21) 2447-0486 para que possamos ajudar. Ou clique em /start para tentar novamente.")
        print(e)

def tipo_especie(message):
    try:
        cid = message.chat.id
        tipo = message.text
        pet = pet_dict[cid]
        if (tipo == u'Gato') or (tipo == u'Cachorro') or (tipo == u'Ave') or (tipo == u'Roedor'):
		pet.tipo = tipo
	else:
		raise Exception()
            
        #pegar user_id
        cur.execute("USE MeuBichoBot")
        cur.execute("SELECT id_usuario FROM usuario where chatid =" + str(cid))
        aux1 = cur.fetchone()
        aux2 = str(aux1)
        aux3 = aux2[:-2]
        user_id = aux3[1:]
        print(user_id)
        
        #inserindo os dados no banco
        cur.execute("USE MeuBichoBot") 
        sql = "insert into pet (nome, tutor, especie) values (%s,%s,%s)"
        val = (pet.petname,user_id,pet.tipo)
        cur.execute(sql,val)
        conn.commit()    
        
        msg = bot.reply_to(message,"Perfeito! Obrigado pelas informações. Fique atento a este canal, enviaremos frequentemente informações do seu interesse e promoções super especiais para fazer a alegria do seu amiguinho. /n/nClique em /menu para continuar.")


    except Exception as e:
        msg = bot.reply_to(message,"Algo deu errado. Entre em contato com (21) 2447-0486 para que possamos ajudar. Ou clique em /start para tentar novamente.")
        print(e)

#fluxo de opções do menu        
@bot.message_handler(commands=['menu'])
def send_menu(message):
    cid = message.chat.id 
    bot.send_message(cid,"Selecione a opção que reflete como posso te assistir neste momento: \n1. Lojas: /lojas \n2. Fazer um Pedido: /pedidos \n3. Cadastrar um pet: /pet")

@bot.message_handler(commands=['lojas'])
def send_menu(message):
    cid = message.chat.id 
    bot.send_message(cid,"Atualmente atendemos em duas lojas: \n\nQUINTINO: Av. Dom Hélder Câmara, 9648 - Quintino Bocaiuva, Rio de Janeiro - RJ, 21380-007 \nAtendimento: Seg - Sex (08h - 19h) \nSab (08h - 17h) \nDomingo (08h - 13h) \n\n\nMADUREIRA:  Rua Maria José, 751 - Madureira, Rio de Janeiro - RJ, 21341-140 \nAtendimento: Seg - Sex (08h - 19h) \nSab (08h - 17h) \n\nRetornar ao menu principal: /menu")

@bot.message_handler(commands=['pedidos'])
def send_menu(message):
    cid = message.chat.id 
    bot.send_message(cid,"Por enquanto para fazer um pedido é necessário fazer contato através do nosso telefone. Não deixe de informar o ID do seu cadastro para agilizar o atendimento: +552124470486 \n\nRetornar ao menu principal: /menu")

@bot.message_handler(commands=['pet'])
def send_menu(message):
    cid = message.chat.id 
    msg = bot.reply_to(message,"Para cadastrar um novo Pet informe o nome do seu amiguinho ou clique em /menu para retorna ao menu principal:")
    bot.register_next_step_handler(msg,name_pet_step)

bot.polling() #escuta usuário