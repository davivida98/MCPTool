const mineflayer = require('mineflayer');
const ProxyAgent = require('proxy-agent');
const utils = require('../utilities/utils');

async function kickBot({ host, port, username, version, proxy, spaces }) {
    let bot;
    try {
        if (proxy.length > 0) {
            bot = mineflayer.createBot({
                host: host,
                port: port,
                username: username,
                version: version,
                agent: new ProxyAgent({ protocol: 'socks5:', host: proxy[0], port: proxy[1] }),
                hideErrors: true
            });
        } else {
            bot = mineflayer.createBot({
                host: host,
                port: port,
                username: username,
                version: version,
                hideErrors: true
            });
        }
    } catch (error) {
        handleConnectionError(error, spaces);
        process.exit(1);
    }

    bot.on('login', () => {
        utils.coloredText(`\n${getSpaces(spaces)}§f§l[§c§l#§f§l] §aThe user ${username} was successfully kicked from the server.`);
        bot.quit();
        process.exit(1);
    });

    bot.on('kicked', (reason) => {
        const message = utils.getTextFromJSON(reason);
        if (message.length === 0) {
            utils.coloredText(`\n${getSpaces(spaces)}§f§l[§c§l#§f§l] The bot was unable to connect to the server due to the following reason: ${reason}`);
        } else {
            utils.coloredText(`\n${getSpaces(spaces)}§f§l[§c§l#§f§l] The bot was unable to connect to the server due to the following reason: ${message.replace(/\s{2,}/g, ' ').replace(/\n/g, ' ')}`);
        }
        bot.quit();
        process.exit(1);
    });

    bot.on('error', (error) => {
        utils.coloredText(`\n${getSpaces(spaces)}§f§l[§c§l#§f§l] The bot was unable to connect to the server due to the following reason: ${error}`);
        process.exit(1);
    });
}

function handleConnectionError(error, spaces) {
    if (error.message.includes('is not supported')) {
        const version = error.message.match(/\d+\.\d+\.\d+/)[0];
        utils.coloredText(`\n${getSpaces(spaces)}§f§l[§c§l#§f§l] §cIncompatible Minecraft version: Version §c§l${version} §cis not currently supported.`);
    } else if (error.message.includes('unsupported protocol version:')) {
        let protocol;
        try {
            protocol = error.message.match(/\d+/)['input'].split(': ')[1];
        } catch {
            protocol = error.message.match(/\d+/);
        }
        if (protocol != null) {
            utils.coloredText(`\n${getSpaces(spaces)}§f§l[§c§l#§f§l] §cIncompatible Minecraft version: Protocol §c§l${protocol} §cis not supported`);
        } else {
            utils.coloredText(`\n${getSpaces(spaces)}§f§l[§c§l#§f§l] §cIncompatible Minecraft version: Protocol is not supported`);
        }
    } else {
        utils.coloredText(`\n${getSpaces(spaces)}§f§l[§c§l#§f§l] §4Error`);
    }
}

module.exports = { kickBot };
