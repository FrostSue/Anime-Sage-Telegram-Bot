import os
import sys
import time
import psutil
import platform
from pyrogram import Client
from pyrogram.types import Message
from app.config import ADMIN_IDS
from database.db import get_global_stats

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

async def server_info(c: Client, m: Message):
    if m.from_user.id not in ADMIN_IDS:
        return

    uname = platform.uname()
    os_name = f"{uname.system} {uname.release}"
    host_name = uname.node
    kernel = uname.release
    
    boot_time_timestamp = psutil.boot_time()
    uptime_seconds = int(time.time() - boot_time_timestamp)
    uptime_str = get_readable_time(uptime_seconds)

    cpu_freq = psutil.cpu_freq()
    cpu_freq_str = f"{cpu_freq.current:.2f} Mhz" if cpu_freq else "N/A"
    cpu_count = psutil.cpu_count(logical=True)
    cpu_percent = psutil.cpu_percent(interval=0.1)

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

    py_ver = sys.version.split()[0]
    
    msg = f"""
**🖥️ Server Status**
```text
OS:      {os_name}
Host:    {host_name}
Kernel:  {kernel}
Uptime:  {uptime_str}
Python:  v{py_ver}

CPU:     {uname.processor} ({cpu_count} Core) @ {cpu_percent}%
Memory:  {mem_used} / {mem_total} ({mem_percent}%)
Disk:    {disk_used} / {disk_total} ({disk_percent}%)
Swap:    {swap_used} / {swap_total} ({swap_percent}%)

Local IP: Hidden
```
"""

    await m.reply_text(msg, quote=True)

async def log_file_handler(c: Client, m: Message):
    if m.from_user.id not in ADMIN_IDS:
        return

    log_file = "anime_sage.log"

    if not os.path.exists(log_file):
        await m.reply_text("⚠️ Log file not found.", quote=True)
        return

    try:
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            last_lines = "".join(lines[-15:])

        await m.reply_document(
            document=log_file,
            caption=f"📜 **System Logs**\n\n**Last Lines:**\n```\n{last_lines}```"
        )
    except Exception as e:
        await m.reply_text(f"Error reading logs: {str(e)}", quote=True)

async def admin_panel(c: Client, m: Message):
    if m.from_user.id not in ADMIN_IDS:
        return

    total_users, total_recs = await get_global_stats()

    msg = (
        f"👮‍♂️ **Admin Control Panel**\n"
        f"──────────────────────\n"
        f"👥 **Total Users:** `{total_users}`\n"
        f"🤖 **Total Recs:** `{total_recs}`\n"
        f"──────────────────────\n"
        f"📡 **Status:** Online ✅\n\n"
        f"Commands:\n"
        f"• `/server` - Server Resources\n"
        f"• `/logs` - Log File"
    )

    await m.reply_text(msg, quote=True)
