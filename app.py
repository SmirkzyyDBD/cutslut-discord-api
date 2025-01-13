import discord, os, asyncio
from threading import Thread
from discord.ext import commands
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = "+", intents = intents)

app = Flask(__name__)

CORS(app, resources={ # cors bc everything dies otherwise
    r"/*": {
        "origins": ["https://cutslut.app", "https://egirls.date"], # bhvr.gay in the fututure mayabe (they are gay)
        "methods": ["GET"],
        "allow_headers": ["Authorization", "Content-Type"]
    }
})

API_KEY = os.getenv("API_KEY")
GUILD_ID = int(os.getenv("GUILD_ID", 0)) # if not in the server, guild ID will be 0
BOT_TOKEN = os.getenv("BOT_TOKEN")
WELCOME_WEBHOOK = os.getenv("WELCOME_WEBHOOK")

user_status_data = {} # store thingt data for users ;))

def fetch_user(user_id):
    user_data = user_status_data.get(user_id, {})
    return {
        "status": user_data.get("status", "offline"),
        "activities": user_data.get("activities", []),
        "username": user_data.get("username", "Unknown"),
        "display_name": user_data.get("display_name", "Unknown"),
        "profile_picture": user_data.get("profile_picture", ""),
    }

@app.route("/api/v1/userStatus", methods=["GET"])
def get_user():
    api_key = request.headers.get("Authorization")
    if api_key != API_KEY:
        return jsonify({"Error": "Unauthorized"}), 401
    
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"Error": "user_id not provided"}), 400 
    
    user_status = asyncio.run(fetch_user_status(user_id))
    if user_status:
        return jsonify(user_status)
    else:
        return jsonify({"Error": "User not found"}), 404

async def fetch_user_status(user_id):
    guild = discord.utils.get(bot.guilds, id = GUILD_ID)
    if guild:
        member = guild.get_member(int(user_id))
        if member:
            activities = []
            for activity in member.activities:
                if isinstance(activity, discord.CustomActivity):
                    activity_data = {
                        "name": activity.name,
                        "type": "CustomActivity",
                        "state": activity.state,
                        "large_image_url": None,
                        "small_image_url": None
                    }
                else:  # Handle other rich presence activities
                    activity_data = {
                        "name": activity.name,
                        "type": str(activity.type),
                        "details": getattr(activity, "details", None),
                        "state": getattr(activity, "state", None),
                        "large_image_url": getattr(activity, "large_image_url", None),
                        "small_image_url": getattr(activity, "small_image_url", None)
                    }
                activities.append(activity_data)
            return {
                "status": str(member.status),
                "activities": activities,
                "username": member.name,
                "display_name": member.display_name,
                "profile_picture": str(member.avatar.url),
            }
    return None

@bot.event
async def on_ready():
    print(f"[+] {bot.user} is online")
    
@bot.event
async def on_member_join(member):
    # Send a message using a webhook for easier intagration
    webhook_url = WELCOME_WEBHOOK
    embed = discord.Embed (
        title = member.guild.name,
        description = f"Welcome {member.name} to the {member.guild.name} Discord server!\nPlease familiarize yourself with the rules.",
        color = discord.Color.black()
    )
    embed.set_thumbnail(url = member.avatar.url if member.avatar else member.default_avatar.url)
    embed.set_footer(text = f"User ID: {member.id}")
    
    async with discord.Webhook.from_url(webhook_url, adapter=discord.RequestsWebhookAdapter()) as webhook:
        await webhook.send(embed = embed, username="cutslut.app")

async def main():
    if not BOT_TOKEN or not API_KEY or GUILD_ID == 0:
        raise Exception("Bot token or API key not found. Make sure they're set in '.env'")
    
    # we need to start flask in a diff thread so the discord bot doesnt stop the flask app running
    flask_thread = Thread(target = app.run, kwargs = {"host": "0.0.0.0", "port": 80,})
    flask_thread.daemon = True 
    flask_thread.start() 
    
    # now we can start the bot 
    await bot.start(BOT_TOKEN)
    
if __name__ == "__main__":
    asyncio.run(main())