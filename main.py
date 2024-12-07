import os
import discord
from discord.ext import commands
import asyncio
from myserver import server_on

# ตั้งค่า Client
intents = discord.Intents.default()
intents.members = True  # ให้บอทสามารถเข้าถึงข้อมูลสมาชิกได้

bot = commands.Bot(command_prefix="!", intents=intents)



@bot.command()
async def poke(ctx, member: discord.Member):
    # ตรวจสอบว่า member อยู่ในห้องเสียงหรือไม่
    if not member.voice:
        await ctx.send(f"{member.mention} is not currently in a voice channel.")
        return

    # เก็บห้องเริ่มต้นที่สมาชิกอยู่
    original_channel = member.voice.channel

    # หาห้องเสียงทั้งหมดในเซิร์ฟเวอร์ที่ไม่มีสมาชิกอยู่
    voice_channels = [channel for channel in ctx.guild.voice_channels if channel != original_channel and len(channel.members) == 0]

    # ตรวจสอบห้องเสียงที่ว่างในเซิร์ฟเวอร์
    if not voice_channels:
        await ctx.send("No available empty voice channels to move.")
        return

    # ย้ายสมาชิกไปยังห้องต่าง ๆ 5 รอบ
    for i in range(4):  # ย้าย 4 รอบแรก
        if not voice_channels:
            await ctx.send(f"No available empty channels to move to for round {i+1}.")
            return

        # เลือกห้องที่ว่าง
        channel_to_move = voice_channels.pop(0)  # เอาห้องแรกที่ว่างออกจากรายการ
        await member.move_to(channel_to_move)
        await ctx.send(f'{member.mention} has been poked and moved to {channel_to_move.name} (Round {i + 1}).')

        # รอระยะเวลา 3 วินาทีระหว่างการย้าย
        await asyncio.sleep(3)

        # หาห้องเสียงที่ว่างใหม่สำหรับรอบถัดไป
        voice_channels = [channel for channel in ctx.guild.voice_channels if channel != original_channel and len(channel.members) == 0]

    # ย้ายกลับไปที่ห้องเดิมในรอบสุดท้าย
    await member.move_to(original_channel)
    await ctx.send(f'{member.mention} has been poked and moved back to the original channel: {original_channel.name} (Round 5).')

# ให้บอทรัน

server_on()

bot.run(os.getenv('TOKEN'))
