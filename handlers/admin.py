import os
import sys
import time
import psutil
import platform
import subprocess
from pyrogram import Client
from pyrogram.types import Message
from app.config import ADMIN_IDS
from database.db import get_global_stats, add_sudo, del_sudo
from utils.auth import is_admin

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time

def get_cpu_model():
    try:
        command = "cat /proc/cpuinfo | grep 'model name' | head -1 | cut -d: -f2"
        model = subprocess.check_output(command, shell=True).decode().strip()
        return model
    except:
        return platform.processor()

def get_distro_name():
    try:
        command = "cat /etc/os-release | grep PRETTY_NAME | cut -d= -f2 | tr -d '\"'"
        distro = subprocess.check_output(command, shell=True).decode().strip()
        return distro
    except:
        return f"{platform.system()} {platform.release()}"

def get_package_count():
    try:
        if os.path.exists("/usr/bin/dpkg"):
            cmd = "dpkg -l | grep -c ^ii"
            mgr = "dpkg"
        elif os.path.exists("/usr/bin/rpm"):
            cmd = "rpm -qa | wc -l"
            mgr = "rpm"
        else:
            return "N/A"
        count = subprocess.check_output(cmd, shell=True).decode().strip()
        return f"{count} ({mgr})"
    except:
        return "N/A"

async def server_info(c: Client, m: Message):
    if not await is_admin(m.from_user.id):
        return

    uname = platform.uname()
    host_name = uname.node
    kernel = uname.release
    os_info = get_distro_name()

    boot_time_timestamp = psutil.boot_time()
    uptime_seconds = int(time.time() - boot_time_timestamp)
    uptime_str = get_readable_time(uptime_seconds)

    cpu_model = get_cpu_model()
    cpu_freq = psutil.cpu_freq()
    cpu_freq_str = f"{cpu_freq.current/1000:.2f} GHz" if cpu_freq else "N/A"
    cpu_count = psutil.cpu_count(logical=True)

    mem = psutil.virtual_memory()
    mem_total = f"{mem.total / (1024 ** 3):.2f} GiB"
    mem_used = f"{mem.used / (1024 ** 3):.2f} GiB"
    mem_percent = mem.percent

    disk = psutil.disk_usage('/')
    disk_total = f"{disk.total / (1024 ** 3):.2f} GiB"
    disk_used = f"{disk.used / (1024 ** 3):.2f} GiB"
    disk_percent = disk.percent

    swap = psutil.swap_memory()
    swap_total = f"{swap.total / (1024 ** 3):.2f} GiB"
    swap_used = f"{swap.used / (1024 ** 3):.2f} GiB"
    swap_percent = swap.percent

    shell = os.environ.get("SHELL", "N/A").split("/")[-1]
    term = os.environ.get("TERM", "N/A")
    locale = os.environ.get("LANG", "N/A")
    packages = get_package_count()

    msg = f"""
**🖥️ Server Status**
```text
OS:       {os_info}
Host:     {host_name}
Kernel:   {kernel}
Uptime:   {uptime_str}
Packages: {packages}
Shell:    {shell}
Terminal: {term}
Locale:   {locale}

CPU:      {cpu_model} ({cpu_count}) @ {cpu_freq_str}
Memory:   {mem_used} / {mem_total} ({mem_percent}%)
Swap:     {swap_used} / {swap_total} ({swap_percent}%)
Disk (/): {disk_used} / {disk_total} ({disk_percent}%)

Local IP: Hidden
```
"""
    await m.reply_text(msg, quote=True)


async def log_file_handler(c: Client, m: Message):
    if not await is_admin(m.from_user.id):
        return

    log_file = "anime_sage.log"

    if not os.path.exists(log_file):
        await m.reply_text("⚠️ Log file not found.", quote=True)
        return

    try:
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            last_lines = "".join(lines[-15:])

        if len(last_lines) > 950:
            last_lines = last_lines[-950:] + "\n...(truncated)"

        await m.reply_document(
            document=log_file,
            caption=f"📜 **System Logs**\n\n**Last Lines:**\n```\n{last_lines}```"
        )

    except Exception as e:
        await m.reply_text(f"Error reading logs: {str(e)}", quote=True)


async def admin_panel(c: Client, m: Message):
    if not await is_admin(m.from_user.id):
        return

    total_users, total_recs = await get_global_stats()

    msg = (
        f"👮‍♂️ Admin Control Panel\n"
        f"──────────────────────\n"
        f"👥 Total Users: {total_users}\n"
        f"🤖 Total Recs: {total_recs}\n"
        f"──────────────────────\n"
        f"📡 Status: Online ✅\n\n"
        f"Commands:\n"
        f"• /server - Server Resources\n"
        f"• /logs - Log File\n"
        f"• /addadmin [ID] - Add Admin\n"
        f"• /deladmin [ID] - Remove Admin"
    )

    await m.reply_text(msg, quote=True)


async def add_admin_handler(c: Client, m: Message):
    if m.from_user.id not in ADMIN_IDS:
        return

    if len(m.command) < 2:
        await m.reply_text("⚠️ Usage: /addadmin <user_id>", quote=True)
        return

    try:
        target_id = int(m.command[1])
        await add_sudo(target_id)
        await m.reply_text(f"✅ User {target_id} promoted to Admin.", quote=True)
    except ValueError:
        await m.reply_text("⚠️ Invalid ID.", quote=True)


async def del_admin_handler(c: Client, m: Message):
    if m.from_user.id not in ADMIN_IDS:
        return

    if len(m.command) < 2:
        await m.reply_text("⚠️ Usage: /deladmin <user_id>", quote=True)
        return

    try:
        target_id = int(m.command[1])
        await del_sudo(target_id)
        await m.reply_text(f"🗑️ User {target_id} removed from Admins.", quote=True)
    except ValueError:
        await m.reply_text("⚠️ Invalid ID.", quote=True)
