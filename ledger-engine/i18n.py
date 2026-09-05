# ledger-engine/i18n.py

LANGUAGES = {
    "l1": ("English", "en"),
    "l2": ("isiZulu", "zu"),
    "l3": ("Afrikaans", "af"),
    "l4": ("isiXhosa", "xh"),
    "l5": ("Sepedi", "nso"),
    "l6": ("Setswana", "tn"),
    "l7": ("Sesotho", "st"),
    "l8": ("Xitsonga", "ts"),
    "l9": ("siSwati", "ss"),
    "l10": ("Tshivenda", "ve"),
    "l11": ("isiNdebele", "nr"),
    "l12": ("Swahili", "sw"),
    "l13": ("Hausa", "ha"),
    "l14": ("Yoruba", "yo"),
    "l15": ("Amharic", "am"),
    "l16": ("French", "fr"),
    "l17": ("Portuguese", "pt"),
    "l18": ("Spanish", "es"),
}

# Translation Dictionary
# We fully support 'en' and 'zu'. Other languages will default to 'en' for now, 
# but the structure is ready to support them.
TRANSLATIONS = {
    "en": {
        "menu_title": "🏪 *PocketLedger* — Main Menu",
        "menu_prompt": "What would you like to do?",
        "menu_1": "1️⃣ Log a Sale",
        "menu_2": "2️⃣ Log Stock / Restock",
        "menu_3": "3️⃣ Log Loss / Wastage",
        "menu_4": "4️⃣ View Financial Summary",
        "menu_5": "5️⃣ My Health Score",
        "menu_6": "6️⃣ Get Statement (PDF link)",
        "menu_7": "7️⃣ Change Language",
        "menu_footer": 'Just reply with a *number* or type naturally, e.g. "I sold 5 loaves for R50"',
        
        "welcome_back": "👋 Welcome back, *{business_name}*!",
        
        "register_prompt": (
            "👋 Welcome to *PocketLedger*! 📒\n\n"
            "The smart bookkeeper in your pocket.\n\n"
            "To get started, please register your business.\n\n"
            "Reply with:\n"
            "*REGISTER: Your Business Name*\n\n"
            "_Example: REGISTER: Thabo's Spaza_"
        ),
        "register_success": "🎉 *{business_name}* is now registered!",
        "register_error": "❌ Please include a business name.\n\nExample: *REGISTER: Thabo's Spaza*",
        
        "summary_title": "📊 *{business_name} — Financial Summary*",
        "summary_rev": "💰 Total Revenue: R{total_revenue:.2f}",
        "summary_pur": "🛒 Total Purchases: R{total_purchases:.2f}",
        "summary_was": "📉 Total Wastage: R{total_wastage:.2f}",
        "summary_prof": "✅ Gross Profit: R{gross_profit:.2f}",
        "summary_health": "❤️ Health Score: {health:.1f}/100",
        
        "health_title": "❤️ *Your Health Score*",
        "health_excellent": "Excellent! You are building a strong financial identity.",
        "health_good": "Good progress! Keep logging consistently to improve.",
        "health_poor": "Keep logging every sale and purchase to build your score.",
        
        "statement_title": "📋 *Your Statement PDF* — {business_name}",
        "statement_link": "Click this link to download it:\n{statement_url}",
        "statement_warn": "*(Note: You may need to click 'Acknowledge' on the security screen before it downloads)*",
        "statement_err": "❌ Statement links are not available right now.\nPlease ask your admin to set PUBLIC_BASE_URL in the .env file.",
        
        "prompt_sale": (
            "🛍️ *Log a Sale*\n\n"
            "Tell me what you sold!\n\n"
            "_Examples:_\n"
            "• I sold 5 loaves for R50\n"
            "• Fixed a sink for R300\n"
            "• Made 2 dresses for R800\n\n"
            "Just type it naturally 👇"
        ),
        "prompt_stock": (
            "📦 *Log Stock / Restock*\n\n"
            "Tell me what you bought!\n\n"
            "_Examples:_\n"
            "• I bought 10m of fabric for R200\n"
            "• Bought 50 tomatoes for R80\n"
            "• Purchased cement 10 bags for R450\n\n"
            "Just type it naturally 👇"
        ),
        "prompt_loss": (
            "🗑️ *Log Loss / Wastage*\n\n"
            "Tell me what was lost or wasted!\n\n"
            "_Examples:_\n"
            "• 2m of fabric was ruined\n"
            "• 5 tomatoes rotted\n"
            "• Wasted 3 bags of cement from mixing error\n\n"
            "Just type it naturally 👇"
        ),
        
        "tx_success": "✅ *Done! Ledger updated.*",
        "tx_evidence": "📊 Evidence Score: {weight:.1f}",
        "tx_health": "❤️ Health Score: {health:.1f}/100",
        "tx_receipt": "🧾 Receipt: {invoice_url}",
        
        "tx_error": (
            "❌ I couldn't understand that.\n\n"
            "Try saying:\n"
            "• _I sold 5 tomatoes for R40_\n"
            "• _Bought 10m fabric for R200_\n"
        ),
        
        "back_to_menu": "Reply *0* for the main menu.",
        "back_to_menu_short": "Reply *0* to go back to the menu.",
        
        "lang_prompt": "🌐 *Choose your language:*\n\nReply with your choice, e.g. *L2*:\n" + "\n".join(f"*{k.upper()}* - {v[0]}" for k, v in LANGUAGES.items()),
        "lang_success": "✅ Language changed successfully!"
    },
    
    "zu": {
        "menu_title": "🏪 *PocketLedger* — Imenyu Enkulu",
        "menu_prompt": "Ungathanda ukwenzani?",
        "menu_1": "1️⃣ Faka Ukuthengisa",
        "menu_2": "2️⃣ Faka Isitoko",
        "menu_3": "3️⃣ Faka Ukulahlekelwa / Ukumosheka",
        "menu_4": "4️⃣ Buka Isifinyezo Sezezimali",
        "menu_5": "5️⃣ Amaphuzu Ami Ezempilo",
        "menu_6": "6️⃣ Thola Isitatimende (PDF)",
        "menu_7": "7️⃣ Shintsha Ulimi",
        "menu_footer": 'Phendula ngenombolo noma uthayiphe ngokwemvelo, isb. "Ngithengise izinkwa ezihlanu ngo R50"',
        
        "welcome_back": "👋 Siyakwamukela futhi, *{business_name}*!",
        
        "register_prompt": (
            "👋 Siyakwamukela ku *PocketLedger*! 📒\n\n"
            "Umbhalisi wamabhuku ohlakaniphile ephaketheni lakho.\n\n"
            "Ukuze uqale, ngicela ubhalise ibhizinisi lakho.\n\n"
            "Phendula ngokuthi:\n"
            "*REGISTER: Igama Lebhizinisi Lakho*\n\n"
            "_Isibonelo: REGISTER: Thabo's Spaza_"
        ),
        "register_success": "🎉 *{business_name}* isibhalisiwe manje!",
        "register_error": "❌ Ngicela ufake igama lebhizinisi.\n\nIsibonelo: *REGISTER: Thabo's Spaza*",
        
        "summary_title": "📊 *{business_name} — Isifinyezo Sezezimali*",
        "summary_rev": "💰 Imali Engenile Iyonke: R{total_revenue:.2f}",
        "summary_pur": "🛒 Okuthengiwe Sekukonke: R{total_purchases:.2f}",
        "summary_was": "📉 Ukulahlekelwa Sekukonke: R{total_wastage:.2f}",
        "summary_prof": "✅ Inzuzo Yonke: R{gross_profit:.2f}",
        "summary_health": "❤️ Amaphuzu Ezempilo: {health:.1f}/100",
        
        "health_title": "❤️ *Amaphuzu Akho Ezempilo Yebhizinisi*",
        "health_excellent": "Kuhle kakhulu! Wakha umlando omuhle kakhulu wezezimali.",
        "health_good": "Ukhula kahle! Qhubeka nokufaka imininingwane yakho njalo ukuze uthuthuke.",
        "health_poor": "Qhubeka ufaka konke okuthengisayo nokuthengayo ukuze wakhe amaphuzu akho.",
        
        "statement_title": "📋 *Isitatimende Sakho (PDF)* — {business_name}",
        "statement_link": "Chofoza lesi sixhumanisi ukuze usidawunilode:\n{statement_url}",
        "statement_warn": "*(Qaphela: Kungadingeka uchofoze ukuthi 'Acknowledge' esikrinini sokuphepha ngaphambi kokuthi idawunilode)*",
        "statement_err": "❌ Izixhumanisi zesitatimende azitholakali okwamanje.\nNgicela utshele i-admin yakho isethe i-PUBLIC_BASE_URL kufayela le-.env.",
        
        "prompt_sale": (
            "🛍️ *Faka Ukuthengisa*\n\n"
            "Ngitshele ukuthi uthengiseni!\n\n"
            "_Izibonelo:_\n"
            "• Ngithengise izinkwa ezihlanu ngo R50\n"
            "• Ngilungise usinki ngo R300\n"
            "• Ngithunge izingubo ezimbili ngo R800\n\n"
            "Thayipha njengoba ukhuluma 👇"
        ),
        "prompt_stock": (
            "📦 *Faka Isitoko*\n\n"
            "Ngitshele ukuthi uthengeni!\n\n"
            "_Izibonelo:_\n"
            "• Ngithenge indwangu engu-10m ngo R200\n"
            "• Ngithenge utamatisi ongu-50 ngo R80\n"
            "• Ngithenge usimende izikhwama ezingu-10 ngo R450\n\n"
            "Thayipha njengoba ukhuluma 👇"
        ),
        "prompt_loss": (
            "🗑️ *Faka Ukulahlekelwa / Ukumosheka*\n\n"
            "Ngitshele okulahlekile noma okumoshekile!\n\n"
            "_Izibonelo:_\n"
            "• Indwangu engu-2m imoshekile\n"
            "• Utamatisi ongu-5 ubolile\n"
            "• Kumosheke amasaka amathathu kasimende exutshwa kabi\n\n"
            "Thayipha njengoba ukhuluma 👇"
        ),
        
        "tx_success": "✅ *Kwenziwe! I-Ledger ivuselelwe.*",
        "tx_evidence": "📊 Amaphuzu Wobufakazi: {weight:.1f}",
        "tx_health": "❤️ Amaphuzu Ezempilo: {health:.1f}/100",
        "tx_receipt": "🧾 Irisidi: {invoice_url}",
        
        "tx_error": (
            "❌ Angizange ngiqonde lokho.\n\n"
            "Zama ukusho ukuthi:\n"
            "• _Ngithengise utamatisi o-5 ngo R40_\n"
            "• _Ngithenge indwangu engu-10m ngo R200_\n"
        ),
        
        "back_to_menu": "Phendula ngo *0* ukuya kumenyu enkulu.",
        "back_to_menu_short": "Phendula ngo *0* ukuya kumenyu enkulu.",
        
        "lang_prompt": "🌐 *Khetha ulimi lwakho:*\n\nPhendula ngalokhu, isb. *L2*:\n" + "\n".join(f"*{k.upper()}* - {v[0]}" for k, v in LANGUAGES.items()),
        "lang_success": "✅ Ulimi lushintshwe ngempumelelo! / Language changed successfully!"
    }
}

def get_text(lang_code: str, key: str, **kwargs) -> str:
    # Default to English if language or key not found
    lang_dict = TRANSLATIONS.get(lang_code, TRANSLATIONS["en"])
    text = lang_dict.get(key, TRANSLATIONS["en"].get(key, ""))
    if kwargs:
        return text.format(**kwargs)
    return text

def build_menu(lang_code: str) -> str:
    menu = [
        get_text(lang_code, "menu_title"),
        "",
        get_text(lang_code, "menu_prompt"),
        "",
        get_text(lang_code, "menu_1"),
        get_text(lang_code, "menu_2"),
        get_text(lang_code, "menu_3"),
        get_text(lang_code, "menu_4"),
        get_text(lang_code, "menu_5"),
        get_text(lang_code, "menu_6"),
        get_text(lang_code, "menu_7"),
        "",
        get_text(lang_code, "menu_footer")
    ]
    return "\n".join(menu)
