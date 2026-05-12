# Telegram Music Bot

ဤသည်မှာ YouTube မှ သီချင်းများကို ရှာဖွေ၊ ဒေါင်းလုဒ်လုပ်ပြီး Telegram သို့ MP3 အဖြစ် ပေးပို့နိုင်သော Telegram Music Bot တစ်ခုဖြစ်သည်။

## Features

*   **သီချင်းရှာဖွေခြင်းနှင့် ဒေါင်းလုဒ်လုပ်ခြင်း**: သီချင်းအမည် ရိုက်ထည့်ပါက YouTube မှ ရှာဖွေပြီး audio download link ပြန်ပေးသည်။
*   **/trending command**: နိုင်ငံတကာမှ လူကြိုက်များသော/ခေတ်စားနေသော သီချင်းစာရင်းကို ပြသသည်။
*   **Inline search**: မည်သည့် chat တွင်မဆို bot ၏ username ကို ရိုက်ထည့်ပြီး သီချင်းရှာဖွေနိုင်သည်။
*   **Audio file ပေးပို့ခြင်း**: MP3 format ဖြင့် audio file ကို Telegram ထဲသို့ တိုက်ရိုက်ပို့ပေးသည်။
*   **သီချင်းအချက်အလက်**: သီချင်း၏ ခေါင်းစဉ် (title), အဆိုတော် (artist), ကြာချိန် (duration) တို့ကို ပြသသည်။
*   **/start command**: ကြိုဆိုသော မက်ဆေ့ချ်နှင့် bot အသုံးပြုနည်း လမ်းညွှန်များကို ပြသသည်။
*   **/help command**: bot အသုံးပြုနည်း အသေးစိတ်ကို ပြသသည်။

## နည်းပညာများ

*   Python (python-telegram-bot library)
*   yt-dlp (YouTube download အတွက်)
*   youtube-search-python (YouTube ရှာဖွေမှုအတွက်)

## Bot ကို ထည့်သွင်းခြင်းနှင့် Run ခြင်း

### လိုအပ်သော အရာများ

*   Python 3.8 သို့မဟုတ် အထက်
*   pip (Python package installer)
*   Telegram Bot Token (BotFather မှ ရယူပါ)

### အဆင့်ဆင့် ထည့်သွင်းခြင်း

1.  **Project ကို Clone လုပ်ပါ (သို့မဟုတ် Download လုပ်ပါ)**

    ```bash
    git clone <your-repository-url>
    cd music_bot
    ```

    *(မှတ်ချက်: ဤ bot ကို လက်ရှိ sandbox environment တွင် ဖန်တီးထားသောကြောင့် repository URL မရှိပါ။ အကယ်၍ သင်သည် ဤ bot ကို GitHub ကဲ့သို့သော နေရာတွင် တင်ထားပါက ဤအဆင့်ကို အသုံးပြုနိုင်ပါသည်။)*

2.  **Dependencies များကို ထည့်သွင်းပါ**

    `requirements.txt` ဖိုင်တွင် လိုအပ်သော library များ ပါဝင်သည်။ ၎င်းတို့ကို အောက်ပါ command ဖြင့် ထည့်သွင်းပါ။

    ```bash
    pip install -r requirements.txt
    ```

3.  **Bot Token ထည့်သွင်းခြင်း**

    `bot.py` ဖိုင်ကို ဖွင့်ပြီး `TOKEN` variable တွင် သင်၏ Telegram Bot Token ကို ထည့်သွင်းပါ။

    ```python
    TOKEN = 'YOUR_BOT_TOKEN_HERE' # ဤနေရာတွင် သင်၏ Bot Token ကို ထည့်သွင်းပါ
    ```

    *(ဤ project အတွက် Bot Token ကို `8357603022:AAFLUr36aVLKZ1zIZE8LzXDdoAXmUsrDkuQ` အဖြစ် သတ်မှတ်ထားပြီးဖြစ်သည်။)*

4.  **Bot ကို Run ပါ**

    အောက်ပါ command ဖြင့် bot ကို စတင်ပါ။

    ```bash
    python bot.py
    ```

    Bot စတင်အလုပ်လုပ်ပါလိမ့်မည်။ Telegram တွင် သင်၏ bot သို့ စာပို့ပြီး စမ်းသပ်ကြည့်နိုင်ပါသည်။

## Deploy လုပ်နည်း (ဥပမာ: Heroku, Railway, သို့မဟုတ် VPS)

Bot ကို အမြဲတမ်း အလုပ်လုပ်နေစေရန်အတွက် server တစ်ခုပေါ်တွင် deploy လုပ်ရန် လိုအပ်ပါသည်။ ဤနေရာတွင် အခြေခံ အဆင့်များကို ဖော်ပြထားပါသည်။

1.  **Code ကို Version Control (ဥပမာ: Git) ဖြင့် ထိန်းသိမ်းပါ**

    သင်၏ project folder ကို Git repository အဖြစ် ပြောင်းလဲပြီး GitHub သို့မဟုတ် GitLab ကဲ့သို့သော နေရာတွင် တင်ပါ။

2.  **Hosting Platform ရွေးချယ်ပါ**

    *   **Heroku / Railway**: Python app များအတွက် အသုံးပြုရလွယ်ကူသော PaaS (Platform as a Service) များဖြစ်သည်။ `Procfile` ဖိုင်တစ်ခု ဖန်တီးပြီး `web: python bot.py` ကဲ့သို့သော command ကို ထည့်သွင်းရန် လိုအပ်သည်။
    *   **VPS (Virtual Private Server)**: DigitalOcean, AWS, Google Cloud ကဲ့သို့သော VPS ပေါ်တွင် သင်ကိုယ်တိုင် server ကို configure လုပ်ပြီး bot ကို run နိုင်သည်။ `systemd` သို့မဟုတ် `supervisor` ကဲ့သို့သော tool များကို အသုံးပြု၍ bot process ကို စီမံခန့်ခွဲနိုင်သည်။

3.  **Environment Variables သတ်မှတ်ပါ**

    Deploy လုပ်သည့်အခါ Bot Token ကို code ထဲတွင် တိုက်ရိုက်မထည့်ဘဲ Environment Variable အဖြစ် သတ်မှတ်ခြင်းက ပိုမိုလုံခြုံပါသည်။

    ```python
    # bot.py တွင်
    TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', 'YOUR_DEFAULT_TOKEN_IF_ANY')
    ```

    ထို့နောက် deploy လုပ်မည့် platform တွင် `TELEGRAM_BOT_TOKEN` ဟူသော environment variable ကို သင်၏ bot token ဖြင့် သတ်မှတ်ပေးပါ။

4.  **Dependencies များကို သေချာပါစေ**

    `requirements.txt` ဖိုင်သည် သင်၏ deploy environment တွင် လိုအပ်သော library များအားလုံးကို ထည့်သွင်းရန် အရေးကြီးပါသည်။

## အသုံးပြုနည်း

*   **သီချင်းရှာရန်**: Bot သို့ သီချင်းအမည်ကို တိုက်ရိုက်ရိုက်ပြီး ပို့ပါ။ ဥပမာ: `Imagine John Lennon`
*   **Trending သီချင်းများကြည့်ရန်**: `/trending` ဟု ရိုက်ပြီး ပို့ပါ။
*   **Inline Search**: မည်သည့် chat တွင်မဆို `@your_bot_username <song name>` ဟု ရိုက်ထည့်ပါ။ ဥပမာ: `@MyMusicBot Imagine`
*   **အကူအညီလိုပါက**: `/help` ဟု ရိုက်ပြီး ပို့ပါ။

## မှတ်ချက်

ဤ bot သည် YouTube မှ သီချင်းများကို ရှာဖွေပြီး ဒေါင်းလုဒ်လုပ်ပေးပါသည်။ မူပိုင်ခွင့်ရှိသော အကြောင်းအရာများကို ခွင့်ပြုချက်မရှိဘဲ ဒေါင်းလုဒ်လုပ်ခြင်းနှင့် ဖြန့်ဝေခြင်းသည် ဥပဒေနှင့် ငြိစွန်းနိုင်ပါသည်။ အသုံးပြုသူ၏ ကိုယ်ပိုင်တာဝန်သာ ဖြစ်ပါသည်။
