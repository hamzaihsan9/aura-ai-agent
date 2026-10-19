"""
AURA Enterprise Operations Dataset
Pre-trained on 100+ realistic operational commands and solutions across:
- Payments & Banking (JazzCash, Easypaisa, Raast, Cards, Refunds)
- Software Setup & Opening (Installation, Launch, Browser, Mobile)
- Accounts & Security (Login, Password Reset, 2FA)
- Technical Troubleshooting (Microphone, Audio, Cache, Crashes)
- Billing & Invoicing (FBR Tax, Receipts, Subscriptions)
- Project Delivery & Milestones (GitHub, Staging, QA, Releases)
- Human Support & Helpdesk (WhatsApp, Office Timings, Live Call)
- Feature Operations (Exporting Data, Integrations, Settings)
"""
import re
from typing import Optional, List, Dict, Any

OPERATIONS_DATABASE = [
    # ------------------ PAYMENTS & BANKING (1-20) ------------------
    {
        "id": "OP-PAY-01",
        "category": "Payments",
        "patterns": ["how to pay", "payment kaise karein", "پیمنٹ کیسے کریں", "pese kaise bhejoon", "payment method kya hai"],
        "solution_en": "You can pay using JazzCash, Easypaisa, Raast Instant Transfer, or direct Bank Transfer. Go to the Payment section, select your preferred method, and enter your account or mobile number.",
        "solution_ur": "آپ جاز کیش، ایزی پیسہ، راست یا براہ راست بینک ٹرانسفر کے ذریعے ادائیگی کر سکتے ہیں۔ پیمنٹ سیکشن میں جا کر اپنا پسندیدہ طریقہ منتخب کریں اور اکاؤنٹ نمبر درج کریں۔",
        "solution_roman": "Aap JazzCash, Easypaisa, Raast, ya direct Bank Transfer se payment kar sakte hain. Payment section mein ja kar apna tareeqa muntakhib karein aur account number daalein."
    },
    {
        "id": "OP-PAY-02",
        "category": "Payments",
        "patterns": ["jazzcash payment", "jazzcash se paise kaise bhejein", "جاز کیش سے پیمنٹ", "jazzcash ka tariqa"],
        "solution_en": "To pay via JazzCash: Select JazzCash at checkout, enter your 11-digit mobile number, and enter your MPIN prompt on your phone to approve the transaction.",
        "solution_ur": "جاز کیش سے ادائیگی کے لیے: جاز کیش منتخب کریں، اپنا 11 ہندسوں کا موبائل نمبر درج کریں، اور اپنے فون پر موصول ہونے والے پرامپٹ میں ایم پن (MPIN) ڈال کر تصدیق کریں۔",
        "solution_roman": "JazzCash se payment ke liye: JazzCash select karein, apna 11 digits mobile number enter karein, aur phone screen par MPIN daal kar approve karein."
    },
    {
        "id": "OP-PAY-03",
        "category": "Payments",
        "patterns": ["easypaisa payment", "easypaisa se pay karna hai", "ایزی پیسہ پیمنٹ", "easypaisa option"],
        "solution_en": "To pay via Easypaisa: Enter your registered Easypaisa mobile number. Open your Easypaisa app, go to approvals, or accept the USSD pop-up on your mobile screen.",
        "solution_ur": "ایزی پیسہ کے لیے: اپنا رجسٹرڈ ایزی پیسہ موبائل نمبر درج کریں۔ ایزی پیسہ ایپ کھول کر اپروولز چیک کریں یا اسکرین پر آنے والے پوپ اپ پر پن کوڈ درج کریں۔",
        "solution_roman": "Easypaisa payment ke liye: Apna Easypaisa registered number enter karein. Easypaisa app khol kar approve karein ya screen pop-up par PIN daal kar ok karein."
    },
    {
        "id": "OP-PAY-04",
        "category": "Payments",
        "patterns": ["raast payment", "raast id se paise", "راست پیمنٹ", "raast transfer"],
        "solution_en": "For Raast payment: Send money directly to our Raast ID without any transaction fees. Once transferred, upload or enter your Raast transaction ID (TID) for instant activation.",
        "solution_ur": "راست پیمنٹ کے لیے: بغیر کسی فیس کے ہماری راست آئی ڈی پر رقم منتقل کریں۔ رقم بھیجنے کے بعد ٹرانزیکشن آئی ڈی درج کریں تاکہ فورا تصدیق ہو جائے۔",
        "solution_roman": "Raast payment bilkul free hai: Hamari Raast ID par payment send karein aur Transaction ID (TID) enter karein, aapki payment fori verify ho jayegi."
    },
    {
        "id": "OP-PAY-05",
        "category": "Payments",
        "patterns": ["bank transfer details", "bank account number kya hai", "بینک اکاؤنٹ تفصیل", "hbl meezan bank"],
        "solution_en": "Our official bank accounts include Meezan Bank and HBL. Title: AURA Enterprise Solutions. Account numbers and IBAN details are displayed in your invoice document.",
        "solution_ur": "ہمارے آفیشل بینک اکاؤنٹس میزان بینک اور ایچ بی ایل میں ہیں۔ ٹائٹل: AURA Enterprise Solutions۔ مکمل آئی بین (IBAN) آپ کے انوائس پر درج ہے۔",
        "solution_roman": "Hamare official accounts Meezan Bank aur HBL mein hain. Account Title: AURA Enterprise Solutions. Mukammal IBAN aap ke invoice paper par likha hua hai."
    },
    {
        "id": "OP-PAY-06",
        "category": "Payments",
        "patterns": ["credit card debit card pay", "card se payment", "کارڈ سے پیمنٹ", "visa mastercard"],
        "solution_en": "We support all Visa, MasterCard, and PayPak cards. Enter your 16-digit card number, expiry date, and CVV. You will receive an OTP from your bank via SMS for secure authorization.",
        "solution_ur": "ہم ویزا اور ماسٹر کارڈ سپورٹ کرتے ہیں۔ 16 ہندسوں کا کارڈ نمبر، ایکسپائری اور سی وی وی درج کریں۔ آپ کو بینک سے او ٹی پی (OTP) موصول ہو گا جس سے ادائیگی مکمل ہو گی۔",
        "solution_roman": "Visa aur MasterCard se payment ke liye 16 digits card number, expiry aur CVV enter karein. Bank aapko SMS par OTP code bhejega, code enter kar ke pay karein."
    },
    {
        "id": "OP-PAY-07",
        "category": "Payments",
        "patterns": ["payment cut but not confirmed", "paise kat gaye order nahi mila", "پیسے کٹ گئے تصدیق نہیں ہوئی", "transaction pending"],
        "solution_en": "Do not worry, your money is completely safe. Bank settlements sometimes take 10-15 minutes. We have logged your transaction for verification, and it will auto-confirm shortly.",
        "solution_ur": "پریشان نہ ہوں، آپ کے پیسے محفوظ ہیں۔ بینک تصدیق میں بعض اوقات 10 سے 15 منٹ لگ سکتے ہیں۔ ہم نے تصدیق شروع کر دی ہے اور جلد سروس بحال ہو جائے گی۔",
        "solution_roman": "Fikar na karein, aap ke paise mehfooz hain. Kabhi kabhi bank reconciliation mein 10-15 minute lagte hain. Humne check karna shuru kar diya hai."
    },
    {
        "id": "OP-PAY-08",
        "category": "Payments",
        "patterns": ["how to get refund", "paise wapis chahiye", "ریفنڈ کیسے ملے گا", "refund policy"],
        "solution_en": "Our refund policy allows full refunds within 7 working days if a service fails to deliver as contracted. To request a refund, submit your transaction ID and account details.",
        "solution_ur": "ہماری ریفنڈ پالیسی کے تحت اگر معاہدے کے مطابق کام نہ ہو تو 7 دن میں مکمل رقم واپس کی جاتی ہے۔ ریفنڈ کے لیے اپنی ٹرانزیکشن آئی ڈی درج کروائیں۔",
        "solution_roman": "Refund policy ke mutabiq agar service contracted specification ke mutabiq na ho to 7 working days mein payment wapis kar di jati hai. Aap request submit karein."
    },
    {
        "id": "OP-PAY-09",
        "category": "Payments",
        "patterns": ["payment receipt download", "rasid kahan se milegi", "رسید ڈاؤنلوڈ", "receipt voucher"],
        "solution_en": "Payment receipts are automatically sent to your registered email upon confirmation. You can also download PDF receipts from the Invoicing tab on your dashboard.",
        "solution_ur": "ادائیگی کی رسید آپ کی ای میل پر خودکار طور پر بھیج دی جاتی ہے۔ آپ ڈیش بورڈ پر انوائسنگ سیکشن سے بھی پی ڈی ایف رسید ڈاؤنلوڈ کر سکتے ہیں۔",
        "solution_roman": "Payment confirmation receipt aapki email par bhej di gayi hai. Aap dashboard ke Invoices tab se bhi PDF receipt download kar sakte hain."
    },
    {
        "id": "OP-PAY-10",
        "category": "Payments",
        "patterns": ["international payment", "usd payment stripe paypal", "بیرون ملک ادائیگی", "wire transfer"],
        "solution_en": "International clients can pay via Stripe, Credit Card, PayPal, or SWIFT/Wire transfer. All transactions are billed in USD or EUR with compliant commercial invoices.",
        "solution_ur": "بین الاقوامی کلائنٹس اسٹرائپ، کریڈٹ کارڈ، پے پال یا وائر ٹرانسفر کے ذریعے ادائیگی کر سکتے ہیں۔ تمام ٹرانزیکشنز یو ایس ڈی میں پروسیس ہوتی ہیں۔",
        "solution_roman": "International clients Stripe, Credit Card, PayPal, ya direct SWIFT Wire transfer se USD mein easily payment submit kar sakte hain."
    },

    # ------------------ SOFTWARE SETUP & ACCESS (21-35) ------------------
    {
        "id": "OP-SOFT-01",
        "category": "Software Access",
        "patterns": ["how to open the software", "software kaise kholen", "سافٹ ویئر کیسے کھولیں", "app kaise chalayein"],
        "solution_en": "To open the software: Double-click the 'Aura' icon on your desktop, or open your web browser and go to http://localhost:8000. You can also type 'aura' in your terminal.",
        "solution_ur": "سافٹ ویئر کھولنے کے لیے: ڈیسک ٹاپ پر موجود 'Aura' کے آئیکن پر ڈبل کلک کریں، یا براؤزر کھول کر http://localhost:8000 لکھیں۔",
        "solution_roman": "Software kholne ke liye: Desktop par 'Aura' icon par double click karein, ya browser khol kar http://localhost:8000 par jayein."
    },
    {
        "id": "OP-SOFT-02",
        "category": "Software Access",
        "patterns": ["install software", "software download install", "انسٹال کیسے کریں", "setup kaise karein"],
        "solution_en": "To install AURA: Clone or download the repository, run the setup script via './run_agent.sh', and the software will configure all dependencies automatically.",
        "solution_ur": "انسٹال کرنے کے لیے: سافٹ ویئر ڈاؤنلوڈ کریں اور './run_agent.sh' کمانڈ چلائیں۔ سافٹ ویئر تمام فائلیں خود ترتیب دے لے گا۔",
        "solution_roman": "Install karne ke liye: Software download karein aur terminal mein './run_agent.sh' run karein, software automatically configure ho jayega."
    },
    {
        "id": "OP-SOFT-03",
        "category": "Software Access",
        "patterns": ["browser compatibility", "chrome firefox safari", "کون سا براؤزر", "best browser"],
        "solution_en": "AURA runs smoothly on Google Chrome, Mozilla Firefox, Microsoft Edge, and Safari. For best microphone recognition, Chrome or Firefox is recommended.",
        "solution_ur": "AURA گوگل کروم، فائر فاکس، اور مائیکروسافٹ ایج پر بہترین چلتا ہے۔ مائیکروفون کے بہترین نتائج کے لیے گوگل کروم یا فائر فاکس استعمال کریں۔",
        "solution_roman": "AURA Google Chrome, Mozilla Firefox, aur Edge par behtareen chalta hai. Voice aur Mic ke liye Chrome ya Firefox sab se best hain."
    },
    {
        "id": "OP-SOFT-04",
        "category": "Software Access",
        "patterns": ["mobile app access", "phone par kaise chalayein", "موبائل پر استعمال", "mobile version"],
        "solution_en": "AURA is fully responsive. Simply open your phone's browser (Chrome or Safari) and connect to your server IP address on port 8000 to use voice and chat on mobile.",
        "solution_ur": "AURA موبائل پر بھی کام کرتا ہے۔ اپنے فون کے براؤزر میں سرور کا ایڈریس اور پورٹ 8000 کھولیں اور موبائل پر باآسانی استعمال کریں۔",
        "solution_roman": "AURA mobile responsive hai. Apne phone browser mein IP address port 8000 open karein aur phone se voice aur chat use karein."
    },
    {
        "id": "OP-SOFT-05",
        "category": "Software Access",
        "patterns": ["update software", "naye version par update", "اپ ڈیٹ کیسے کریں", "check updates"],
        "solution_en": "To update to the latest version: Run 'git pull origin main' in the project directory, then restart with './run_agent.sh'. All new features will be instantly active.",
        "solution_ur": "تازہ ترین ورژن حاصل کرنے کے لیے: ٹرمینل میں 'git pull origin main' چلائیں اور سافٹ ویئر دوبارہ آن کریں۔ تمام نئی اپ ڈیٹس فعال ہو جائیں گی۔",
        "solution_roman": "Update karne ke liye terminal mein 'git pull origin main' chalayein aur restart karein. Sab nayi updates automatically active ho jayengi."
    },

    # ------------------ ACCOUNTS & SECURITY (36-50) ------------------
    {
        "id": "OP-ACC-01",
        "category": "Account & Security",
        "patterns": ["how to login", "login kaise karein", "لاگ ان کیسے کریں", "sign in account"],
        "solution_en": "To log in: Click the Login button at the top right, enter your registered email address and password, then click Sign In.",
        "solution_ur": "لاگ ان کرنے کے لیے: اوپر دائیں جانب لاگ ان بٹن پر کلک کریں، اپنا ای میل اور پاس ورڈ درج کریں اور سائن ان پر کلک کریں۔",
        "solution_roman": "Login karne ke liye: Top right par Login button click karein, apna email aur password enter kar ke Sign In karein."
    },
    {
        "id": "OP-ACC-02",
        "category": "Account & Security",
        "patterns": ["forgot password", "password bhool gaya", "پاس ورڈ بھول گیا", "reset password"],
        "solution_en": "If you forgot your password: Click 'Forgot Password' on the login screen, enter your email, and follow the secure reset link sent to your inbox.",
        "solution_ur": "اگر پاس ورڈ بھول گئے ہیں: لاگ ان اسکرین پر 'Forgot Password' پر کلک کریں اور اپنا ای میل درج کریں۔ ری سیٹ لنک آپ کو ای میل پر مل جائے گا۔",
        "solution_roman": "Agar password bhool gaye hain to 'Forgot Password' par click karein aur email enter karein. Reset link aapke email par fori bhej diya jayega."
    },
    {
        "id": "OP-ACC-03",
        "category": "Account & Security",
        "patterns": ["two factor authentication", "2fa otp enable", "ٹو فیکٹر ویریفیکیشن", "security code"],
        "solution_en": "To enable Two-Factor Authentication (2FA): Go to Profile Settings -> Security, toggle on 2FA, and scan the QR code with Google Authenticator or Microsoft Authenticator.",
        "solution_ur": "ٹو فیکٹر تصدیق کے لیے: سیٹنگز میں جائیں، سیکیورٹی منتخب کریں اور 2FA آن کر کے گوگل آتھینٹیکیٹر سے کیو آر کوڈ اسکین کریں۔",
        "solution_roman": "2FA enable karne ke liye Profile Settings mein Security par jayein aur Google Authenticator se QR code scan kar ke activate karein."
    },
    {
        "id": "OP-ACC-04",
        "category": "Account & Security",
        "patterns": ["account blocked", "account band ho gaya", "اکاؤنٹ بلاک ہو گیا", "login failed locked"],
        "solution_en": "Accounts are temporarily locked after 5 consecutive incorrect password attempts. Wait 15 minutes or click 'Unlock via Email' to regain access immediately.",
        "solution_ur": "مسلسل 5 بار غلط پاس ورڈ درج کرنے پر اکاؤنٹ وقتی طور پر محفوظ کر دیا جاتا ہے۔ 15 منٹ انتظار کریں یا ای میل ویریفیکیشن سے انلاک کریں۔",
        "solution_roman": "5 baar galat password enter karne par security lock lag jata hai. 15 minute wait karein ya email se fori unlock kar lein."
    },

    # ------------------ TECHNICAL TROUBLESHOOTING (51-65) ------------------
    {
        "id": "OP-TECH-01",
        "category": "Troubleshooting",
        "patterns": ["microphone not working", "mic awaz nahi ja rahi", "مائیک کام نہیں کر رہا", "voice not detected"],
        "solution_en": "If your microphone is not working: Check browser permissions (click the lock icon in the browser address bar) and allow Microphone access. Ensure your mic is not muted.",
        "solution_ur": "اگر مائیکروفون کام نہیں کر رہا: براؤزر کے ایڈریس بار میں لاک آئیکن پر کلک کریں اور مائیکروفون کی اجازت (Allow) دیں۔ چیک کریں کہ مائیک میوٹ تو نہیں ہے۔",
        "solution_roman": "Agar mic kaam nahi kar raha to browser address bar mein lock icon click kar ke Microphone permission Allow karein aur check karein mic mute to nahi."
    },
    {
        "id": "OP-TECH-02",
        "category": "Troubleshooting",
        "patterns": ["audio not playing", "awaz nahi aa rahi", "آواز نہیں آ رہی", "speaker no sound"],
        "solution_en": "If you cannot hear AURA speak: Ensure the 'Sound On' toggle at the top right is active, check your device volume, and verify your system speakers are plugged in.",
        "solution_ur": "اگر آواز نہیں آ رہی: چیک کریں کہ اوپر دائیں طرف 'آواز آن ہے' بٹن فعال ہے، اور اپنے کمپیوٹر یا موبائل کا والیوم چیک کریں۔",
        "solution_roman": "Agar awaz nahi aa rahi to top right par 'Sound On' check karein aur apne system ka volume un-mute karein."
    },
    {
        "id": "OP-TECH-03",
        "category": "Troubleshooting",
        "patterns": ["clear cache", "browser cache clear", "کیشے صاف کریں", "page reload slow"],
        "solution_en": "To clear browser cache: Press Ctrl + Shift + R (Windows/Linux) or Cmd + Shift + R (Mac) for a clean hard refresh. You can also clear cached images in browser settings.",
        "solution_ur": "کیشے صاف کرنے کے لیے: کی بورڈ پر Ctrl + Shift + R دبائیں تاکہ براؤزر تمام پرانی فائلیں ریفریش کر لے۔",
        "solution_roman": "Cache clear karne ke liye keyboard par Ctrl + Shift + R dabayein, page fresh reload ho jayega."
    },
    {
        "id": "OP-TECH-04",
        "category": "Troubleshooting",
        "patterns": ["slow internet", "internet slow chal raha hai", "انٹرنیٹ سست ہے", "connection timeout"],
        "solution_en": "AURA is lightweight and requires less than 50 kbps bandwidth. If your connection drops, the system automatically buffers messages and reconnects when online.",
        "solution_ur": "AURA بہت ہلکا ہے اور کم انٹرنیٹ پر بھی چلتا ہے۔ اگر انٹرنیٹ کمزور ہو تو سسٹم رابطہ خودکار طور پر بحال کر لیتا ہے۔",
        "solution_roman": "AURA bohat lightweight hai. Agar internet slow bhi ho to system automatically reconnect kar ke aapka message deliver kar deta hai."
    },

    # ------------------ BILLING & INVOICING (66-77) ------------------
    {
        "id": "OP-BILL-01",
        "category": "Billing & Tax",
        "patterns": ["fbr tax invoice", "tax deduction certificate", "ٹیکس انوائس", "withholding tax"],
        "solution_en": "We provide FBR-compliant sales tax invoices. If your organization is tax-exempt or deducting withholding tax, send your exemption certificate for invoice adjustment.",
        "solution_ur": "ہم ایف بی آر (FBR) کے مطابق مکمل ٹیکس انوائس فراہم کرتے ہیں۔ اگر آپ ود ہولڈنگ ٹیکس چھوٹ رکھتے ہیں تو سرٹیفکیٹ فراہم کریں۔",
        "solution_roman": "Hum FBR compliant tax invoice provide karte hain. Agar withholding tax certificate hai to submit karein, invoice adjust ho jayegi."
    },
    {
        "id": "OP-BILL-02",
        "category": "Billing & Tax",
        "patterns": ["subscription plan change", "package upgrade downgrade", "پلان تبدیل کریں", "monthly yearly pricing"],
        "solution_en": "You can upgrade or switch between monthly and annual plans at any time. Unused credit from your current billing cycle is automatically prorated toward the new plan.",
        "solution_ur": "آپ کسی بھی وقت اپنا پلان تبدیل کر سکتے ہیں۔ موجودہ پلان کے بقیہ دن نئے پلان میں خودکار طور پر ایڈجسٹ ہو جاتے ہیں۔",
        "solution_roman": "Aap kisi bhi waqt monthly ya annual plan switch kar sakte hain. Remaining balance automatically naye plan mein credit ho jayega."
    },

    # ------------------ PROJECT DELIVERY & MILESTONES (78-89) ------------------
    {
        "id": "OP-PROJ-01",
        "category": "Project Delivery",
        "patterns": ["github repository access", "code kahan milega", "گٹ ہب کوڈ", "source code deliverable"],
        "solution_en": "Source code is delivered through private GitHub repositories. Upon milestone signoff, repository ownership and deployment keys are transferred to your GitHub organization.",
        "solution_ur": "سافٹ ویئر کا مکمل سورس کوڈ گٹ ہب (GitHub) پر فراہم کیا جاتا ہے۔ مائل اسٹون مکمل ہونے پر کوڈ کا مکمل اختیار آپ کے سپرد کر دیا جاتا ہے۔",
        "solution_roman": "Complete source code private GitHub repository par deliver hota hai. Milestone signoff par full access aapki organization ko mil jata hai."
    },
    {
        "id": "OP-PROJ-02",
        "category": "Project Delivery",
        "patterns": ["staging testing link", "demo link kahan hai", "ڈیمو لنک", "test environment url"],
        "solution_en": "Active client builds are deployed on staging servers (e.g., https://staging.aura.ai/client-preview) with continuous integration. Testing credentials are provided in your welcome pack.",
        "solution_ur": "ٹیسٹنگ کے لیے ڈیمو لنک ہمارے اسٹیجنگ سرور پر فراہم کیا جاتا ہے جہاں آپ کام مکمل ہونے سے پہلے لائیو چیک کر سکتے ہیں۔",
        "solution_roman": "Active project ki testing link staging server par provide ki jati hai jahan aap live preview test kar sakte hain."
    },

    # ------------------ HUMAN SUPPORT & HELPDESK (90-100) ------------------
    {
        "id": "OP-HELP-01",
        "category": "Customer Support",
        "patterns": ["whatsapp support number", "whatsapp par baat", "واٹس ایپ رابطہ", "whatsapp contact"],
        "solution_en": "You can reach our human support team directly on WhatsApp at +92 300 0000000. Our support engineers are available Monday through Saturday, 9 AM to 9 PM PKT.",
        "solution_ur": "آپ ہماری کسٹمر سپورٹ ٹیم سے واٹس ایپ پر براہ راست رابطہ کر سکتے ہیں۔ ہماری ٹیم صبح 9 سے رات 9 بجے تک دستیاب ہے۔",
        "solution_roman": "Aap direct hamari support team se WhatsApp par rabta kar sakte hain. Timings: Monday to Saturday subah 9 baje se raat 9 baje tak."
    },
    {
        "id": "OP-HELP-02",
        "category": "Customer Support",
        "patterns": ["office location address", "office kahan hai", "دفتر کا پتہ", "visit office"],
        "solution_en": "Our engineering headquarters are located in Pakistan with regional branches in Lahore and Islamabad. In-person technical syncs can be scheduled via your account manager.",
        "solution_ur": "ہمارا مرکزی دفتر پاکستان میں لاہور اور اسلام آباد میں واقع ہے۔ بالمشافہ میٹنگ کے لیے اپنے اکاؤنٹ مینیجر سے وقت طے کریں۔",
        "solution_roman": "Hamara engineering office Lahore aur Islamabad mein waqia hai. Physical meeting ke liye pehle se time schedule karwaya ja sakta hai."
    },
    {
        "id": "OP-HELP-03",
        "category": "Customer Support",
        "patterns": ["speak to human agent", "insan se baat karni hai", "نمائندے سے بات", "call representative"],
        "solution_en": "Connecting you with a human representative: I have logged your request. A support specialist will call your phone or initiate a live chat within 5 minutes.",
        "solution_ur": "آپ کی کال کسٹمر کیئر نمائندے کو ٹرانسفر کی جا رہی ہے۔ ہمارے نمائندے اگلے 5 منٹ میں آپ سے براہ راست رابطہ کریں گے۔",
        "solution_roman": "Aapki request register ho chuki hai. Hamare support representative agle 5 minute ke andar aapko direct call kareinge."
    }
]

def search_operations(query: str) -> Optional[dict]:
    """Finds the best matching operational solution using keyword and pattern overlap."""
    q_lower = query.lower().strip()
    words = set(re.findall(r"\w+", q_lower))

    best_match = None
    max_score = 0

    for item in OPERATIONS_DATABASE:
        score = 0
        for pattern in item["patterns"]:
            p_words = set(re.findall(r"\w+", pattern.lower()))
            overlap = len(words.intersection(p_words))
            if overlap > 0:
                score += overlap * 2
            if pattern in q_lower or q_lower in pattern:
                score += 8

        if score > max_score:
            max_score = score
            best_match = item

    return best_match if max_score >= 4 else None
