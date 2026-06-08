import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, filters, ContextTypes
)

# ─── SOZLAMALAR ───────────────────────────────────────────
BOT_TOKEN = "8524305049:AAEfCnJyqKv0piD7f6M1vB3VUhbCUERbv9g"
ADMIN_ID  = 7057888549   # Farhod ning chat_id
# ─────────────────────────────────────────────────────────

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ─── /start KOMANDASI (mijoz uchun)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name or "Mehmon"

    welcome_text = (
        f"👋 Salom, *{name}*!\n\n"
        "🎯 *VibeMedia* — Samarqand SMM agentligiga xush kelibsiz!\n\n"
        "Biz sizning brendingizni ijtimoiy tarmoqlarda kuchli qilamiz.\n\n"
        "📌 *Xizmatlarimiz:*\n"
        "• 📱 SMM Boshqaruvi\n"
        "• 🎬 Video Kontent\n"
        "• 🎯 Targeted Reklama\n"
        "• 🎨 Brend Identitet\n\n"
        "Quyidagi tugmalardan birini tanlang 👇"
    )

    keyboard = [
        [
            InlineKeyboardButton("🌐 Saytimiz", url="https://vibemedia.uz"),
            InlineKeyboardButton("📞 Bog'lanish", callback_data="contact"),
        ],
        [
            InlineKeyboardButton("💼 Xizmatlar", callback_data="services"),
            InlineKeyboardButton("💰 Narxlar", callback_data="pricing"),
        ],
        [
            InlineKeyboardButton("📝 Ariza topshirish", callback_data="apply"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        welcome_text,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

# ─── TUGMA BOSILGANDA
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "contact":
        text = (
            "📞 *Bog'lanish ma'lumotlari:*\n\n"
            "👤 Farhod — Founder & CEO\n"
            "📱 Telegram: @farhodvibe\n"
            "☎️ Telefon: +998 88 396 33 31\n"
            "📍 Samarqand, O'zbekiston\n\n"
            "Ish vaqti: Du-Shan, 09:00–18:00"
        )
        keyboard = [[InlineKeyboardButton("⬅️ Orqaga", callback_data="back")]]

    elif data == "services":
        text = (
            "💼 *Bizning xizmatlar:*\n\n"
            "1️⃣ *SMM Boshqaruvi* — Instagram, Telegram, TikTok, Facebook\n\n"
            "2️⃣ *Video Kontent* — Reels, Shorts, Klipler\n\n"
            "3️⃣ *Targeted Reklama* — Meta Ads, TikTok Ads, Google Ads\n\n"
            "4️⃣ *Kontent Strategiya* — Reja va vizual identitet\n\n"
            "5️⃣ *Analitika & Hisobot* — KPI, Reach, ROI\n\n"
            "6️⃣ *Brend Identitet* — Logo, rang palitasi, brand book"
        )
        keyboard = [
            [InlineKeyboardButton("📝 Ariza topshirish", callback_data="apply")],
            [InlineKeyboardButton("⬅️ Orqaga", callback_data="back")]
        ]

    elif data == "pricing":
        text = (
            "💰 *Narx rejalari:*\n\n"
            "🟢 *Starter* — 990,000 so'm/oy\n"
            "• 1 tarmoq, 12 post, oylik hisobot\n\n"
            "🔥 *Professional* — 2,500,000 so'm/oy\n"
            "• 3 tarmoq, 30 post, 4 Reels, reklama\n\n"
            "💎 *Enterprise* — 5,000,000+ so'm/oy\n"
            "• Barcha platformalar, full paket\n\n"
            "_Batafsil ma'lumot uchun ariza qoldiring_"
        )
        keyboard = [
            [InlineKeyboardButton("📝 Ariza topshirish", callback_data="apply")],
            [InlineKeyboardButton("⬅️ Orqaga", callback_data="back")]
        ]

    elif data == "apply":
        text = (
            "📝 *Ariza topshirish:*\n\n"
            "Quyidagi ma'lumotlarni yuboring:\n\n"
            "1. Ismingiz\n"
            "2. Telefon raqamingiz\n"
            "3. Biznesingiz nomi\n"
            "4. Kerakli xizmat\n\n"
            "📌 *Yoki saytimiz orqali to'ldiring:*\n"
            "https://vibemedia.uz/#contact\n\n"
            "_Tez orada @farhodvibe bog'lanadi!_"
        )
        keyboard = [[InlineKeyboardButton("⬅️ Orqaga", callback_data="back")]]

    elif data == "back":
        # /start ga qaytish
        await query.message.delete()
        # start ni qayta chaqiramiz
        fake_update = Update(
            update_id=update.update_id,
            message=query.message
        )
        keyboard = [
            [
                InlineKeyboardButton("🌐 Saytimiz", url="https://vibemedia.uz"),
                InlineKeyboardButton("📞 Bog'lanish", callback_data="contact"),
            ],
            [
                InlineKeyboardButton("💼 Xizmatlar", callback_data="services"),
                InlineKeyboardButton("💰 Narxlar", callback_data="pricing"),
            ],
            [InlineKeyboardButton("📝 Ariza topshirish", callback_data="apply")],
        ]
        await query.message.reply_text(
            "Asosiy menyu 👇",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    # Admin tugmalari (faqat admin uchun)
    elif data.startswith("call_"):
        user_id = data.split("_")[1]
        await query.edit_message_reply_markup(
            InlineKeyboardMarkup([[
                InlineKeyboardButton("✅ Qo'ng'iroq qilindi", callback_data="done")
            ]])
        )
        return

    elif data == "done":
        await query.edit_message_reply_markup(
            InlineKeyboardMarkup([[
                InlineKeyboardButton("✔️ Bajarildi", callback_data="noop")
            ]])
        )
        return

    elif data == "noop":
        return

    else:
        text = "❓ Noma'lum buyruq"
        keyboard = [[InlineKeyboardButton("⬅️ Orqaga", callback_data="back")]]

    await query.edit_message_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ─── SAYTDAN KELGAN ARIZA (bot ga xabar kelganda)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    user = msg.from_user
    text = msg.text or ""

    # Agar bu admin o'zi yozgan bo'lsa — ignore
    if user.id == ADMIN_ID:
        return

    # Mijozga avtomatik javob
    auto_reply = (
        "✅ *Xabaringiz qabul qilindi!*\n\n"
        "Tez orada *@farhodvibe* siz bilan bog'lanadi.\n"
        "Odatda *1 soat* ichida javob beramiz.\n\n"
        "⏰ Ish vaqti: Du–Shan, 09:00–18:00\n\n"
        "_VibeMedia — Samarqand SMM Agentlik_ 🚀"
    )
    await msg.reply_text(auto_reply, parse_mode="Markdown")

    # Adminga xabar + tugmalar
    admin_text = (
        f"🔔 *Yangi xabar keldi!*\n\n"
        f"👤 Ism: {user.full_name}\n"
        f"🆔 Username: @{user.username or '—'}\n"
        f"📱 User ID: `{user.id}`\n\n"
        f"💬 *Xabar:*\n{text}"
    )
    admin_keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("💬 Javob yozish", url=f"tg://user?id={user.id}"),
            InlineKeyboardButton("✅ Ko'rib chiqildi", callback_data="done"),
        ]
    ])
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=admin_text,
        parse_mode="Markdown",
        reply_markup=admin_keyboard
    )

# ─── SAYTDAN KELGAN ARIZA (webhook uchun maxsus handler)
# Saytdagi forma bot ga xabar yuboradi, bot CHAT_ID = ADMIN_ID
# Lekin xabar bot nomidan kelganda admin_id ga forward qilamiz
async def handle_web_form(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sayt formasi orqali kelgan arizalar"""
    msg = update.message
    if not msg:
        return

    user = msg.from_user
    text = msg.text or ""

    # Agar ariza matni bo'lsa (saytdan kelgan formatda)
    if "Yangi ariza" in text or "Ism:" in text:
        # Adminga tugmali xabar
        admin_keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📞 Qo'ng'iroq", callback_data=f"call_{user.id}"),
                InlineKeyboardButton("✅ Ko'rib chiqildi", callback_data="done"),
            ]
        ])
        # Arizaga emoji va formatni yangilash
        formatted = (
            f"📋 *YANGI ARIZA — VibeMedia*\n"
            f"{'─'*30}\n"
            f"{text}\n"
            f"{'─'*30}\n"
            f"⚡️ Tez javob bering!"
        )
        await msg.reply_text(
            formatted,
            parse_mode="Markdown",
            reply_markup=admin_keyboard
        )
    else:
        await handle_message(update, context)

# ─── MAIN
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_web_form))

    print("✅ VibeMedia Bot ishga tushdi!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
