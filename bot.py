import discord
import random
import asyncio
from datetime import datetime

# ========== კონფიგურაცია ==========
BOT_TOKEN = "MTUxNTA4MDM4MzM1ODgzMjcyMg.GDBTcM.7APCQelIYSGF1mOtu0KeckZCTBiM_Y2BF-phvM"
CHANNEL_ID = 1515079588869312522
IMAGE_URL = "https://play-lh.googleusercontent.com/9a25-BAjhctjr19NtViqEI9HkKW7KBh8D6oYKbcgGdYX0rmaIhno3kUOFLvDxaAJDG26FyuiFy-dizbeOaNl0g"
# ===================================

# ========== გადახდის მეთოდები ==========
payment_methods = [
    {"name": "Bitcoin", "emoji": "₿"},
    {"name": "Litecoin", "emoji": "Ł"},
    {"name": "Solana", "emoji": "◎"},
    {"name": "PayPal", "emoji": "💳"},
    {"name": "Zelle", "emoji": "🏦"},
    {"name": "Ethereum", "emoji": "Ξ"},
    {"name": "Dogecoin", "emoji": "Ð"},
    {"name": "Binance Coin", "emoji": "🟡"},
    {"name": "USDT", "emoji": "💵"},
    {"name": "Ripple", "emoji": "💧"},
    {"name": "Cardano", "emoji": "📊"},
    {"name": "Polkadot", "emoji": "🔴"},
    {"name": "Shiba Inu", "emoji": "🐕"},
    {"name": "Western Union", "emoji": "📮"},
    {"name": "MoneyGram", "emoji": "✉️"},
    {"name": "CashApp", "emoji": "💰"},
    {"name": "Venmo", "emoji": "💸"},
    {"name": "Revolut", "emoji": "💎"},
    {"name": "Skrill", "emoji": "⚡"},
    {"name": "Neteller", "emoji": "🌐"},
    {"name": "Perfect Money", "emoji": "💶"},
    {"name": "AdvCash", "emoji": "💷"},
    {"name": "Payoneer", "emoji": "🌍"},
    {"name": "Stripe", "emoji": "💳"},
    {"name": "TransferWise", "emoji": "🔄"},
    {"name": "Tron (TRX)", "emoji": "🌊"},
    {"name": "Dash", "emoji": "🚀"},
    {"name": "Monero", "emoji": "🔒"},
    {"name": "Stellar", "emoji": "⭐"}
]

send_count = 0
interval = 300

def generate_transaction():
    method = random.choice(payment_methods)
    amount = round(random.uniform(5.00, 2000.00), 2)
    rating = round(random.uniform(3.5, 5.0), 1)
    full = int(rating)
    empty = 5 - full
    stars = "★" * full + "☆" * empty
    
    return {
        "order_num": random.randint(1000, 999999),
        "method_name": method["name"],
        "method_emoji": method["emoji"],
        "amount": f"${amount:,.2f} USD",
        "rating": rating,
        "stars": stars,
        "tx_id": ''.join([str(random.randint(0, 9)) for _ in range(28)])
    }

def create_embed(tx):
    description = f"""**✅ Transaction Completed ✔**

**Order #{tx['order_num']}**

**💳 Payment Method**
`{tx['method_emoji']} {tx['method_name']}`

**💰 Deal Amount**
`{tx['amount']}`

**⭐ Trader Rating**
`{tx['stars']} ({tx['rating']}/5)`

**👤 User**
`Hidden for privacy`

**🆔 Order ID**
`{tx['tx_id']}`"""

    embed = discord.Embed(
        description=description,
        color=0x2ECC71,
        timestamp=datetime.utcnow()
    )
    embed.set_thumbnail(url=IMAGE_URL)
    embed.set_footer(text="IGitems Middleman • 24/7 Secure Middleman")
    return embed

client = discord.Client()

@client.event
async def on_ready():
    global send_count
    print("=" * 55)
    print(f"✅ {client.user} | ონლაინია!")
    print(f"📡 სერვერები: {len(client.guilds)}")
    
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        print(f"✅ არხი: #{channel.name}")
        print(f"📝 5 წამში პირველი ტრანზაქცია...")
        await asyncio.sleep(5)
        tx = generate_transaction()
        await channel.send(embed=create_embed(tx))
        send_count += 1
        print(f"✅ [#{send_count}] Order #{tx['order_num']} | {tx['method_name']} | {tx['amount']}")
    else:
        print(f"❌ არხი {CHANNEL_ID} ვერ მოიძებნა!")
    
    client.loop.create_task(auto_send())
    print("=" * 55)

@client.event
async def on_message(message):
    global send_count, interval
    
    if message.author == client.user:
        return
    
    content = message.content.lower()
    
    if content == "!transaction":
        tx = generate_transaction()
        await message.channel.send(embed=create_embed(tx))
        send_count += 1
        await message.add_reaction("✅")
        print(f"✅ [ხელით #{send_count}] Order #{tx['order_num']} | {tx['method_name']}")
    
    elif content == "!stats":
        embed = discord.Embed(
            title="📊 IGitems Middleman - სტატისტიკა",
            description=f"""
**📨 გაგზავნილი ტრანზაქციები:** `{send_count}`
**⏱️ ინტერვალი:** `{interval // 60} წუთი`
**🟢 ბოტის სტატუსი:** `ონლაინი`
**📡 სერვერები:** `{len(client.guilds)}`
**💳 მხარდაჭერილი მეთოდები:** `{len(payment_methods)}`
""",
            color=0x00FF00,
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text="IGitems Middleman")
        embed.set_thumbnail(url=IMAGE_URL)
        await message.channel.send(embed=embed)
    
    elif content == "!channels":
        msg = "**📡 არხები, სადაც ბოტია:**\n"
        for guild in client.guilds:
            for ch in guild.text_channels:
                try:
                    if ch.permissions_for(guild.me).send_messages:
                        msg += f"✅ #{ch.name} | ID: `{ch.id}`\n"
                except:
                    msg += f"✅ #{ch.name} | ID: `{ch.id}`\n"
        await message.channel.send(msg[:2000])
    
    elif content.startswith("!interval"):
        try:
            parts = content.split()
            if len(parts) == 2:
                new_interval = int(parts[1])
                if 1 <= new_interval <= 60:
                    interval = new_interval * 60
                    await message.channel.send(f"✅ ინტერვალი შეიცვალა: **{new_interval} წუთი**")
                    print(f"📡 ინტერვალი: {interval // 60} წუთი")
                else:
                    await message.channel.send("❌ ინტერვალი 1-60 წუთი!")
            else:
                await message.channel.send(f"📡 მიმდინარე ინტერვალი: **{interval // 60} წუთი**")
        except:
            await message.channel.send("❌ გამოიყენე: `!interval 5`")
    
    elif content == "!methods":
        methods_list = "\n".join([f"{m['emoji']} `{m['name']}`" for m in payment_methods[:25]])
        embed = discord.Embed(
            title="💳 მხარდაჭერილი გადახდის მეთოდები",
            description=methods_list,
            color=0x44AAFF
        )
        embed.set_footer(text=f"სულ: {len(payment_methods)} მეთოდი")
        await message.channel.send(embed=embed)
    
    elif content == "!help":
        embed = discord.Embed(
            title="🤖 IGitems Middleman - ბრძანებები",
            description="""
**!transaction** - ახალი ტრანზაქციის გაგზავნა
**!stats** - სტატისტიკის ნახვა
**!methods** - გადახდის მეთოდების სია
**!channels** - არხების სია
**!interval [წუთი]** - ინტერვალის შეცვლა (1-60)
**!help** - ეს მენიუ
""",
            color=0x2ECC71
        )
        embed.set_footer(text="IGitems Middleman • 24/7")
        await message.channel.send(embed=embed)

async def auto_send():
    global send_count, interval
    await client.wait_until_ready()
    
    while True:
        await asyncio.sleep(interval)
        
        channel = client.get_channel(CHANNEL_ID)
        if channel:
            tx = generate_transaction()
            await channel.send(embed=create_embed(tx))
            send_count += 1
            print(f"✅ [ავტო #{send_count}] Order #{tx['order_num']} | {tx['method_name']} | {tx['amount']} | {datetime.now().strftime('%H:%M:%S')}")

client.run(BOT_TOKEN)
