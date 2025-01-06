from enum import StrEnum


class ExtraButton(StrEnum):
    OFFICIAL_SOURCE = "📚 بر اساس منابع رسمی"
    USER_EXPERIENCES = "👥 بر اساس تجربیات دیگران"


class MenuButtons(StrEnum):
    IMMIGRATION_QUESTION = "❓ در مورد مهاجرت سوال دارم"
    JOB_SEARCH = "💼 دنبال موقعیت‌های شغلی می‌گردم"
    RESUME_REVIEW = "📝 می‌خوام رزومه‌ی منو بررسی کنی"
    CASH_BALANCE = "💰 موجودی کیف پول"
    INCREASE_CREDIT = "💳 افزایش اعتبار"
    SUPPORT = "📞 پشتیبانی"
    LANGUAGE = "🌐 Language"
    HOME = "🏠 بازگشت به منو اصلی"


class MessageEnum(StrEnum):
    WELCOME = (
        "سلام، من السا هستم!\n"
        "چطور میتونم کمکتون کنم...؟"
    )

    LEGAL_RESPONSE = (
        "بسیار خوب؛ جواب سؤالاتت رو میخوای بر اساس اطلاعات مراجع رسمی و معتبر "
        "بدهم، یا بر اساس گفته‌ها و تجربیات سایر افراد...؟"
    )

    LANGUAGE_RESPONSE = (
        "این دکمه فعلا الکیه کاریش نداشته باش تا بعدا یه فکری براش "
        "بکنیم(در حال توسعه اشیم😊)"
    )

    JOB_SEARCH = (
        "من می‌تونم در پیداکردن بهترین موقعیت‌های شغلی بهت کمک کنم. "
        "فقط کافیه عنوان شغلی مد نظرت رو بهم بگی..."
    )

    IMMIGRATION_QUESTION = (
        "بسیار خوب؛ جواب سؤالاتت رو میخوای بر اساس اطلاعات مراجع رسمی و "
        "معتبر بدهم، یا بر اساس گفته‌ها و تجربیات سایر افراد...؟"
    )

    RESUME_RESPONSE = "رزومتو بفرست تا بررسی کنم"

    INCREASE_CREDIT = (
        "خوشحالیم میخوای یه پولی بره تو جیب ما.\n"
        "خیلی خوشحال تر که برنامه برات کمک کننده بوده که راضی به "
        "جمایت شدی.\n"
        "روی لینک زیر کلیک کن و هرچقدر که کرمته بهمون کمکم کن\n\n"
        "https://daramet.com/elsea"
    )

    CASH_BALANCE = (
        "! 😊{}عزیز\n"
        "خوشحالم که به بخش بالانس حسابت سر زدی! می‌خواهم بهت بگم که "
        "حسابت بینهایت است و می‌تونی هرچقدر که دوست داری ازش استفاده کنی.\n"
        "اینجا هستیم تا بهت کمک کنیم و تجربه‌ای عالی برات فراهم کنیم!\n\n"
        "اگر هم خواستی به ما کمک کنی و پولی پرداخت کنی، خوشحال می‌شیم!\n\n"
        "می‌تونی به بخش افزایش اعتبار مراجعه کنی و ببینی چطور می‌تونی "
        "به ما کمک کنی. هر کمکی از طرف تو ارزشمند و دلگرم‌کننده است!\n\n"
        "با آرزوی بهترین‌ها برای تو! 💖"
    )

    SUPPORT = (
        "{}عزیز! 🌟\n"
        "اگر به هر دلیلی با مشکلی مواجه شدی یا سوالی داری، اصلاً نگران "
        "نباش! ما اینجا هستیم تا بهت کمک کنیم. فقط کافیه به آیدی\n"
        "🆔: @Elsa_imigration_support\n"
        "پیام بدی و ما سریعاً بهت پاسخ می‌دیم.\n"
        "ما همیشه در کنار تو هستیم و آماده‌ایم تا هر کمکی که نیاز داری "
        "رو برات فراهم کنیم. پس با خیال راحت به ما پیام بده!\n"
        "با آرزوی روزهای خوب برای تو! 💌"
    )

    LEGAL_RESPONSE_BOT = (
        "بسیار عالی؛ حالا می‌تونی هر سؤالی که می‌خوای رو بپرسی و من بر "
        "اساس اطلاعات مراجع رسمی بهت جواب میدم. برای اطمینان بیشتر اسم "
        "و لینک منبع رو هم در انتهای جواب برات می‌نویسم."
    )

    EXPERIENCE_RESPONSE_BOT = (
        "خوبه؛ حالا می‌تونی هر سؤالی که می‌خوای رو بپرسی و من بر اساس "
        "گفته‌های دیگران بهت جواب میدم."
    )
