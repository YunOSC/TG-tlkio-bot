const coffeeScript = require('coffee-script')
const TelegramBot = require('node-telegram-bot-api')
const TklioClient = require('tlkio-client')

let courseMode = false
const tlkUrl = 'tlk.io/yunosc-test'
const tlBot = new TlkioClient({
    room: 'yunosc-test',
    user: {
        nickname: 'AsukaMeowMeowMeow'
    }
}) 

tlBot.on('message', (msg) => {
    console.log(msg)
})


const token = '652483905:AAEPmruMxQAvI0weh2zL4R8-_VY6QwYYxJ0'
const tgBot = new TelegramBot(token, {
    polling: true,
    filepath: false
})

tgBot.onText(/\/info/, (msg, match) => {
    const chatId = msg.chat.id
    tgBot.sendMessage(chatId, tlkUrl)
})

tgBot.onText(/\/course toggle/, (msg, match) => {
    const chatId = msg.chat.id
    const executor = msg.from.username
    courseMode = !courseMode
    if (courseMode) {
        console.log(executor + ' turned on course mode.')
        tgBot.sendMessage(chatId, 'Course Mode is on.\nNow passing all message from ' + tlkUrl + ' to here.\nAny message in Telegram starts with @ will send to tlk\nIf you want to anonymous just use @# to send message')
    } else {
        console.log(executor + ' turned off course mode.')
        tgBot.sendMessage(chatId, 'Course Mode is off.\nAll messages would not send to each other.')
    }
})

tgBot.onText(/\/echo (.+)/, (msg, match) => {
    console.log(msg);
})

tgBot.onText(/@(.+)/, (msg, match) => {
    const chatID = msg.chat.id
    
})
