import discord, os, asyncio, time, aiohttp
from threading import Thread
from discord.ext import commands
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from datetime import datetime

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = "+", intents = intents)

app = Flask(__name__)

CORS(app, resources={ # cors bc everything dies otherwise
    r"/*": {
        "origins": ["https://cutslut.app", "https://egirls.date"], # bhvr.gay in the fututure mayabe (they are gay)
        "methods": ["GET", "POST"],
        "allow_headers": ["Authorization", "Content-Type"]
    }
})

API_VERSION = os.getenv("API_VERSION")
API_KEY = os.getenv("API_KEY")
GUILD_ID = int(os.getenv("GUILD_ID", 0)) # if not in the server, guild ID will be 0
BOT_TOKEN = os.getenv("BOT_TOKEN")
WELCOME_WEBHOOK = os.getenv("WELCOME_WEBHOOK")
API_HEALTH = os.getenv("API_HEALTH")
WEBSITE_URL = os.getenv("WEBSITE_URL")

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
    
@app.route("/api/v1/version", methods = ["GET"])
def version():
    return jsonify({"version": API_VERSION}), 200
    
@app.route("/api/v1/healthcheck", methods = ["GET"])
def health_check():
    return jsonify({"health": "Alive"}), 200 

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
    
async def get_status_indicator(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if data.get("health") == "Alive":
                    return ":white_check_mark:"
            return ":x:"
    except Exception as e:
        return f":x: Error: {e}"

def current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
    embed = discord.Embed (
        title = member.guild.name,
        description = f"Welcome {member.name} to the {member.guild.name} Discord server!\nPlease familiarize yourself with the rules.",
        color = discord.Color.black()
    )
    embed.set_thumbnail(url = member.avatar.url if member.avatar else member.default_avatar.url)
    embed.set_footer(text = f"User ID: {member.id}")
    
    async with discord.Webhook.from_url(WELCOME_WEBHOOK, adapter=discord.RequestsWebhookAdapter()) as webhook:
        await webhook.send(embed = embed, username="cutslut.app")
        
@bot.command()
async def status(ctx, service: str = "all"):
    async with aiohttp.ClientSession() as session:
        results = {}

        if service in ["all", "api"]:
            api_start = time.monotonic()
            try:
                async with session.get(API_HEALTH) as response:
                    api_time = (time.monotonic() - api_start) * 1000  # convert it to ms
                    api_status = get_status_indicator(response.status)
                    api_version = await session.get(API_VERSION)
                    version_info = await api_version.json()
                    api_version_str = version_info.get("version", "Unknown")
                    results["API"] = f"{api_status} Operational ({api_time:.2f}ms), Version: {api_version_str}"
            except Exception as e:
                results["API"] = f":cross_mark: Error: {str(e)}"

        if service in ["all", "web"]:
            web_start = time.monotonic()
            try:
                async with session.get(WEBSITE_URL) as response:
                    web_time = (time.monotonic() - web_start) * 1000 
                    web_status = get_status_indicator(response.status)
                    results["Website"] = f"{web_status} Online ({web_time:.2f}ms)"
            except Exception as e:
                results["Website"] = f":cross_mark: Error: {str(e)}"

        status_report = ":bar_chart: **Status Report**\n"
        status_report += "\n".join([f"{key}: {value}" for key, value in results.items()])
        status_report += f"\nLast checked: {current_timestamp()}"

        await ctx.send(status_report) # TODO: turn this into an embed

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