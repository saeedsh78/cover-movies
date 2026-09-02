# ------------------------------------------------------
#  BILINGUAL TEXT TABLE: key -> (english, persian)
# ------------------------------------------------------
TEXTS = {
    # navigation
    "nav.movies": ("Movies", "فیلم‌ها"),
    "nav.series": ("TV Series", "سریال‌ها"),
    "nav.api": ("API Keys", "کلیدهای API"),
    "nav.about": ("About", "درباره"),
    "brand.sub": ("MEDIA ORGANIZER", "MEDIA ORGANIZER"),

    # theme / language / ui size
    "theme.label": ("Theme", "تم"),
    "theme.dark": ("Dark", "تاریک"),
    "theme.light": ("Light", "روشن"),
    "lang.en": ("EN", "EN"),
    "lang.fa": ("فا", "فا"),
    "scale.label": ("UI Size", "اندازهٔ رابط"),

    # pages
    "movie.title": ("Movies", "فیلم‌ها"),
    "movie.sub": ("Fetch poster, icon and info — then organize the folder.", "دریافت پوستر، آیکون و اطلاعات — سپس مرتب‌سازی خودکار پوشه."),
    "series.title": ("TV Series", "سریال‌ها"),
    "series.sub": ("Sort episodes into season folders with posters and info.", "چیدمان قسمت‌ها در پوشه‌های فصل، همراه با پوستر و اطلاعات."),
    "api.title": ("API Keys", "کلیدهای API"),
    "api.sub": ("Connect OMDB and TMDB to fetch movie data.", "اتصال به OMDB و TMDB برای دریافت اطلاعات."),
    "about.title": ("About", "درباره"),
    "about.sub": ("Cover Movies", "کاور موویز"),

    # field labels (eyebrow style)
    "lbl.path": ("PATH", "مسیر"),
    "lbl.id": ("IMDB / TMDB ID", "شناسهٔ IMDB / TMDB"),
    "lbl.omdb": ("OMDB API KEY", "کلید OMDB"),
    "lbl.tmdb": ("TMDB API KEY", "کلید TMDB"),
    "lbl.token": ("TMDB READ ACCESS TOKEN", "توکن دسترسی TMDB"),
    "mode.file": ("File", "فایل"),
    "mode.folder": ("Folder", "پوشه"),

    # hints
    "hint.id": ("Optional — an IMDB id (tt…) or TMDB id gives an exact match.", "اختیاری — با وارد کردن شناسهٔ IMDB (tt…) یا TMDB، نتیجه دقیق‌تر می‌شود."),
    "hint.movie.folder": ("Folder mode scans the folder and organizes every movie file inside it.", "حالت پوشه، کل پوشه را می‌گردد و همهٔ فایل‌های فیلم داخل آن را پردازش می‌کند."),
    "hint.movie.file": ("File mode processes a single movie; without an ID the filename is used for the search.", "حالت فایل یک فیلم را پردازش می‌کند؛ بدون شناسه، از نام فایل برای جست‌وجو استفاده می‌شود."),
    "hint.series.folder": ("Episodes are sorted into season folders (S01, S02, …). Unmatched episodes go to “other”.", "قسمت‌ها در پوشه‌های فصل (S01، S02 و…) مرتب می‌شوند؛ قسمت‌های ناشناس به پوشهٔ other می‌روند."),

    # buttons
    "btn.process.movie": ("Process Movie", "پردازش فیلم"),
    "btn.process.series": ("Process Series", "پردازش سریال"),
    "btn.stop": ("Stop", "توقف"),
    "btn.stopping": ("Stopping…", "در حال توقف…"),
    "btn.browse": ("Browse", "انتخاب"),
    "btn.save": ("Save Keys", "ذخیرهٔ کلیدها"),
    "btn.test": ("Test Keys", "آزمودن کلیدها"),
    "btn.github": ("GitHub Project", "پروژهٔ گیت‌هاب"),
    "btn.show": ("Show", "نمایش"),
    "btn.hide": ("Hide", "مخفی"),

    # dialogs / placeholders
    "dlg.folder": ("Select Folder", "انتخاب پوشه"),
    "dlg.file": ("Select Video File", "انتخاب فایل ویدیویی"),
    "ph.id": ("e.g. tt1375666 or 27205", "مثلاً tt1375666 یا 27205"),
    "ph.path": ("Path to a file or folder…", "مسیر فایل یا پوشه…"),

    # processing status (console header)
    "status.idle": ("Ready", "آماده"),
    "status.scanning": ("Scanning {detail}", "مرور {detail}"),
    "status.searching": ("Searching “{detail}”", "جست‌وجوی «{detail}»"),
    "status.info": ("Fetching info: {detail}", "دریافت اطلاعات: {detail}"),
    "status.poster": ("Downloading poster: {detail}", "دانلود پوستر: {detail}"),
    "status.cast": ("Fetching cast: {detail}", "دریافت بازیگران: {detail}"),
    "status.organize": ("Organizing files", "چیدمان فایل‌ها"),
    "status.season": ("Season {detail} poster", "پوستر فصل {detail}"),
    "status.testing": ("Testing keys…", "آزمودن کلیدها…"),
    "status.saved": ("Saved", "ذخیره شد"),
    "status.done": ("Done", "انجام شد"),
    "status.failed": ("Failed", "ناموفق"),
    "status.cancelled": ("Cancelled", "لغو شد"),

    # log lines
    "log.start": ("Processing started", "پردازش شروع شد"),
    "log.found": ("Matched: {detail}", "پیدا شد: {detail}"),
    "log.not_found": ("No match for “{detail}”", "نتیجه‌ای برای «{detail}» پیدا نشد"),
    "log.no_video": ("No video files in {detail}", "فایل ویدیویی در {detail} پیدا نشد"),
    "log.skip_file": ("Skipped (unrecognized name): {detail}", "رد شد (نام ناشناخته): {detail}"),
    "log.other": ("Moved to “other”: {detail}", "به پوشهٔ other منتقل شد: {detail}"),
    "log.icon": ("Folder icon set: {detail}", "آیکون پوشه تنظیم شد: {detail}"),
    "log.poster_fail": ("Poster download failed", "دانلود پوستر ناموفق بود"),
    "log.cast_saved": ("{detail} cast photo(s) saved", "{detail} عکس بازیگر ذخیره شد"),
    "log.move": ("Moved: {detail}", "منتقل شد: {detail}"),
    "log.move_fail": ("Could not move: {detail}", "انتقال ناموفق: {detail}"),
    "log.season_poster": ("Season poster set: {detail}", "پوستر فصل تنظیم شد: {detail}"),
    "log.summary": ("Finished — {detail}", "پایان — {detail}"),
    "log.cancelled": ("Cancelled by user", "به درخواست شما لغو شد"),
    "log.error": ("Error: {detail}", "خطا: {detail}"),
    "log.proxy_error": ("Network blocked — a system proxy didn't respond. Trying direct connection next time. Check your VPN/proxy software.",
                        "شبکه مسدود بود — پروکسی سیستم پاسخ نداد. دفعهٔ بعد مستقیم وصل می‌شود. نرم‌افزار VPN/پروکسی خود را بررسی کنید."),
    "log.path_invalid": ("Path does not exist: {detail}", "مسیر وجود ندارد: {detail}"),
    "log.testing": ("Testing API keys…", "در حال آزمودن کلیدها…"),
    "log.testing_omdb": ("Checking OMDB API Key…", "بررسی کلید OMDB API…"),
    "log.testing_tmdb": ("Checking TMDB API Key & Token…", "بررسی کلید و توکن TMDB…"),
    "log.omdb_ok": ("OMDB API: Connected successfully ({detail})", "OMDB API: اتصال موفق ({detail})"),
    "log.omdb_err": ("OMDB API: Connection failed ({detail})", "OMDB API: اتصال ناموفق ({detail})"),
    "log.tmdb_ok": ("TMDB API: Connected successfully ({detail})", "TMDB API: اتصال موفق ({detail})"),
    "log.tmdb_err": ("TMDB API: Connection failed ({detail})", "TMDB API: اتصال ناموفق ({detail})"),
    "log.token_ok": ("TMDB Token: Read access confirmed", "توکن TMDB: دسترسی تأیید شد"),
    "log.token_err": ("TMDB Token: Invalid or unauthorized ({detail})", "توکن TMDB: نامعتبر یا غیرمجاز ({detail})"),
    "log.saved": ("API keys saved", "کلیدها ذخیره شد"),
    "log.test_result": ("Summary: OMDB [{om}] · TMDB [{tm}]", "نتیجه نهایی: OMDB [{om}] · TMDB [{tm}]"),
    "ok": ("valid", "معتبر"),
    "invalid": ("invalid", "نامعتبر"),

    # message boxes
    "msg.need_path_t": ("Missing path", "مسیر لازم است"),
    "msg.need_path": ("Choose a file or folder first.", "ابتدا یک فایل یا پوشه انتخاب کنید."),
    "msg.wrong_folder_t": ("Folder mode", "حالت پوشه"),
    "msg.wrong_folder": ("Folder mode needs a folder path.", "حالت پوشه به مسیر یک پوشه نیاز دارد."),
    "msg.wrong_file_t": ("File mode", "حالت فایل"),
    "msg.wrong_file": ("File mode needs a video file.", "حالت فایل به یک فایل ویدیویی نیاز دارد."),
    "msg.series_dir_t": ("Folder required", "پوشه لازم است"),
    "msg.series_dir": ("Choose the folder that contains the episodes.", "پوشهٔ حاوی قسمت‌های سریال را انتخاب کنید."),

    # language switcher
    "lang.label": ("Language", "زبان"),

    # ui size restart dialog
    "msg.restart_t": ("Restart needed", "ری‌استارت لازم است"),
    "msg.restart": ("The new size takes effect after a restart. Restart now?", "اندازهٔ جدید پس از ری‌استارت اعمال می‌شود. همین حالا ری‌استارت شود؟"),
    "msg.restart_btn": ("Restart", "ری‌استارت"),

    # about page
    "about.body": (
        "Cover Movies tidies your movie & TV collection: it creates a folder per title, sets the poster as the folder icon, saves cast photos and film information, and sorts series episodes into season folders.",
        "کاور موویز مجموعهٔ فیلم و سریال شما را مرتب می‌کند: برای هر اثر پوشه‌ای می‌سازد، پوستر را به‌عنوان آیکون پوشه تنظیم می‌کند، عکس بازیگران و اطلاعات اثر را ذخیره می‌کند و قسمت‌های سریال را در پوشه‌های فصل می‌چیند.",
    ),
    "about.attr": (
        "This product uses the TMDB API but is not endorsed or certified by TMDB. Movie data is also provided by OMDB.",
        "این برنامه از TMDB API استفاده می‌کند ولی مورد تأیید رسمی TMDB نیست. بخشی از داده‌ها توسط OMDB ارائه می‌شود.",
    ),
    "about.version": ("Version {detail}", "نسخهٔ {detail}"),
}


def t(lang, key, **kw):
    entry = TEXTS.get(key)
    if entry is None:
        return key
    text = entry[0 if lang == "en" else 1]
    if kw:
        try:
            text = text.format(**kw)
        except (KeyError, IndexError):
            pass
    return text
