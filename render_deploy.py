#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bot Téléfoot optimisé pour Render.com
Version simplifiée pour hébergement cloud
"""

import asyncio
import signal
import sys
import os
from datetime import datetime
from telethon import TelegramClient
from telethon.errors import AuthKeyError, FloodWaitError

# Configuration depuis les variables d'environnement
API_ID = int(os.getenv('API_ID', '29177661'))
API_HASH = os.getenv('API_HASH', 'a8639172fa8d35dbfd8ea46286d349ab')
BOT_TOKEN = os.getenv('BOT_TOKEN', '7573497633:AAHk9K15yTCiJP-zruJrc9v8eK8I9XhjyH4')
ADMIN_ID = int(os.getenv('ADMIN_ID', '1190237801'))

# Import des modules locaux
from user_manager import UserManager
from bot_handlers import BotHandlers

class TelefootRenderBot:
    """Bot Telegram optimisé pour Render.com"""
    
    def __init__(self):
        self.client = None
        self.user_manager = UserManager()
        self.handlers = None
        self.running = False
    
    async def initialize(self):
        """Initialise le client Telegram"""
        try:
            self.client = TelegramClient(
                'bot_session', 
                API_ID, 
                API_HASH
            )
            
            await self.client.start(bot_token=BOT_TOKEN)
            me = await self.client.get_me()
            print(f"🤖 Bot connecté : @{me.username} ({me.id})")
            
            # Initialisation des handlers
            self.handlers = BotHandlers(self.client, self.user_manager)
            
            print("✅ Bot initialisé avec succès")
            return True
            
        except AuthKeyError:
            print("❌ Erreur d'authentification")
            return False
        except Exception as e:
            print(f"❌ Erreur d'initialisation : {e}")
            return False
    
    async def start(self):
        """Démarre le bot"""
        if not await self.initialize():
            return False
        
        self.running = True
        print("🚀 Bot démarré sur Render.com")
        
        try:
            if self.client:
                await self.client.run_until_disconnected()
        except KeyboardInterrupt:
            print("\n⏹️ Arrêt du bot")
        except Exception as e:
            print(f"❌ Erreur : {e}")
        finally:
            await self.stop()
        
        return True
    
    async def stop(self):
        """Arrête le bot"""
        self.running = False
        if self.client and self.client.is_connected():
            await self.client.disconnect()
        print("⏹️ Bot arrêté")

def signal_handler(sig, frame):
    """Gestionnaire de signal"""
    print(f"\n🛑 Signal {sig} reçu")
    sys.exit(0)

async def main():
    """Fonction principale"""
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    bot = TelefootRenderBot()
    
    try:
        await bot.start()
    except Exception as e:
        print(f"❌ Erreur fatale : {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n👋 Au revoir !")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Erreur critique : {e}")
        sys.exit(1)