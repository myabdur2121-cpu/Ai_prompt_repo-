# 📘 Manim + LaTeX + FFmpeg + System Instruction

> **উদ্দেশ্য:** এই ডকুমেন্টটি অন্য AI চ্যাট/সহকারীর জন্য হ্যান্ডঅফ নির্দেশিকা।
> এখানে আমাদের পরিবেশ সেটআপ, রেন্ডারিং নিয়ম এবং কাজের পদ্ধতি লিপিবদ্ধ আছে।
> ভবিষেয় আপগ্রেড → শেষের **"আপগ্রেড লগ"** সেকশনে এন্ট্রি যোগ করবে।

---

## 📌 সংস্করণ তথ্য

| আইটেম | মান |
|---|---|
| ডকুমেন্ট সংস্করণ | v1.0 |
| তারিখ | 2026-08-11 |
| অবস্থান | কুষ্টিয়া, বাংলাদেশ (Asia/Dhaka) |
| পরিবেশ | Debian 13 (trixie), Python 3.13, pip 26 |

---

## ১. পরিবেশ সেটআপ (একবার করলেই হয়)

> ⚠️ **গুরুত্বপূর্ণ:** এই ওয়ার্কস্পেসে ইনস্টল করা প্যাকেজ সেশন শেষে মুছে যায়
> (Colab রানটাইম রিসেটের মতো)। নতুন সেশনে **`setup.sh`** চালালেই সব ফিরে আসে।
> কিন্তু `~/.local/share/fonts/` ফোল্ডারের ফন্টগুলো **থেকে যায়**।

### ১.১ সিস্টেম প্যাকেজ (এক লাইনে)

```bash
sudo apt update -qq
sudo DEBIAN_FRONTEND=noninteractive apt install -y -qq \
    ffmpeg \
    libcairo2-dev \
    libpango1.0-dev \
    texlive \
    texlive-latex-extra \
    texlive-latex-recommended \
    texlive-fonts-extra \
    texlive-science \
    tipa
```

### ১.২ পাইথন প্যাকেজ

```bash
pip install -q manim
pip install -q IPython==8.21.0   # Python 3.13+ হলে এই ভার্সন ফেল করলে: pip install -q IPython
```

### ১.৩ ফন্ট (Text() ফাংশনের জন্য)

**Computer Modern (LaTeX লুক)** — apt প্যাকেজ Debian 13-এ নেই, তাই CTAN থেকে:

```bash
cd /tmp
curl -sL -o cm-unicode.zip https://mirrors.ctan.org/fonts/cm-unicode.zip
unzip -q -o cm-unicode.zip
mkdir -p ~/.local/share/fonts/cmu
cp cm-unicode/fonts/otf/*.otf ~/.local/share/fonts/cmu/
fc-cache -f
```

**Noto Bengali (বাংলা ফন্ট):**

```bash
sudo apt install -y -qq fonts-noto-core fonts-noto-extra fonts-beng-extra
mkdir -p ~/.local/share/fonts/noto-bengali
cp /usr/share/fonts/truetype/noto/Noto*Bengali*.ttf ~/.local/share/fonts/noto-bengali/
fc-cache -f
```

**fontconfig alias** (যাতে `font="Computer Modern"` সরাসরি কাজ করে):

```xml
<!-- ~/.config/fontconfig/fonts.conf -->
<fontconfig>
  <alias>
    <family>Computer Modern</family>
    <prefer><family>CMU Serif</family></prefer>
  </alias>
</fontconfig>
```

### ১.৪ দ্রুত সেটআপ

ওয়ার্কস্পেসে **`setup.sh`** ফাইল আছে — নতুন সেশনে শুধু `bash setup.sh` চালাও।

---

## ২. উপলব্ধ ফন্ট (Text() এ ব্যবহারযোগ্য)

| ফন্ট ফ্যামিলি | ব্যবহার |
|---|---|
| `CMU Serif` | ক্লাসিক LaTeX Computer Modern রোমান |
| `CMU Sans Serif` | স্যান্স-সেরিফ ভার্সন |
| `CMU Typewriter Text` | টাইপরাইটার |
| `CMU Bright` / `CMU Concrete` / `CMU Classical Serif` | অন্যান্য স্টাইল |
| `Noto Sans Bengali` | বাংলা স্যান্স (Regular + Bold) |
| `Noto Serif Bengali` | বাংলা সেরিফ (Regular + Bold) |

**উদাহরণ:**

```python
Text("Computer Modern", font="CMU Serif")
Text("বাংলা সান্স ফন্ট", font="Noto Sans Bengali")
Text("বাংলা সেরিফ ফন্ট", font="Noto Serif Bengali")
```

---

## ৩. রেন্ডারিং কমান্ড

```bash
manim -ql --disable_caching demo/scene.py SceneName    # 🎬 ডিফল্ট: দ্রুত, low quality
manim -qh demo/scene.py SceneName                      # ফাইনাল: 1080p high quality
manim -qm demo/scene.py SceneName                      # মাঝারি (দরকার হলে)
```

- আউটপুট লোকেশন: `media/videos/<filename>/<quality>/<SceneName>.mp4`
- আউটপুট ভিডিও ইউজারের ভিউয়ারে দেখাতে **`present_file`** টুল ব্যবহার করো।
- মাঝে মাঝে ফ্রেম বের করে ভিজ্যুয়াল চেক করা যায়:
  ```bash
  ffmpeg -y -v error -i video.mp4 -ss 2 -frames:v 1 frame.png
  ```

---

## ৪. ⚙️ সিস্টেম ইনস্ট্রাকশন (AI-এর জন্য নিয়মাবলী)

> এই নিয়মগুলো **প্রতিটি কাজে** মানতে হবে। ইউজারের সাথে সব কথোপকথন **বাংলায়**।

### ৪.১ মৌলিক ভূমিকা
1. **ব্যক্তিগত সহকারী:** ইউজারকে ব্যক্তিগত সহকারীর মতো সাহায্য করো।
2. **অনুবাদক হিসাবে কাজ:** ইউজার অসম্পূর্ণ/সিনট্যাক্স এররযুক্ত কোড দেবে — কিন্তু সেটাতে
   আইডিয়া ও তথ্য থাকে। তুমি সেটাকে **সঠিক রিয়েল কোডে অনুবাদ** করবে, আইডিয়া অপরিবর্তিত রেখে।
3. **স্টেপ বাই স্টেপ:** কোড → রেন্ডার → ভিডিও — ধাপে ধাপে দেখাও।
4. **ভিডিওই মূল আউটপুট:** যত দ্রুত সম্ভব ভিডিও রেন্ডার করে দাও।

### ৪.২ কোডিং কনভেনশন
5. **প্রতিটি কোড ফাইলের শেষ লাইনে** অবশ্যই থাকবে:
   ```python
   self.wait(3)
   ```
   কারণ: ইউজারের মস্তিষ্ক ভিডিও প্রসেস করতে সময় নেয় — শেষে ৩ সেকেন্ড স্থির ভিউ প্রয়োজন।
6. **প্রথমে `-ql`** দিয়ে রেন্ডার করো (ক্যাজুয়াল, দ্রুত রেজাল্ট)।
7. **`-qh` (ফাইনাল হাই কোয়ালিটি)** শুধু তখনই, যখন ইউজার স্পষ্টভাবে সময়/অনুরোধ উল্লেখ করে।

### ৪.৩ যোগাযোগ নিয়ম
8. **অনুমতি ছাড়া সাজেশন নয়:** কোনো নতুন আইডিয়া/পরামর্শ/চেঞ্জ প্রস্তাব করতে চাইলে
   **আগে অনুমতি চাও** (যেমন: "একটা সাজেশন দিতে পারি?") — তারপরই বলো।
9. প্রশ্ন করলে **`ask_user` টুল** ব্যবহার করো, বিকল্প সহ।
10. সন্দেহ থাকলে ধরে নিয়ো না — আগে জিজ্ঞেস করো।

---

## ৫. কোড টেমপ্লেট (স্টার্টিং পয়েন্ট)

```python
from manim import *

class MyScene(Scene):
    def construct(self):
        title = Text("আমার প্রথম ভিডিও", font="Noto Sans Bengali", font_size=60, color=BLUE)
        self.play(Write(title))
        self.wait(2)

        formula = MathTex(r"E = mc^2", font_size=72, color=YELLOW)
        self.play(Write(formula))
        self.wait(2)

        # ⚠️ বাধ্যতামূলক: শেষ লাইনে self.wait(3) — মস্তিষ্ক প্রসেসিং টাইম
        self.wait(3)
```

---

## ৬. যাচাইকরণ (Verification Checklist)

রেন্ডারের পরে চেক করো:

- [ ] শেষ লাইনে `self.wait(3)` আছে কি না
- [ ] `-ql` দিয়ে রেন্ডার হয়েছে কি না (যদি না ফাইনাল বলা হয়)
- [ ] ভিডিও ফাইল তৈরি হয়েছে: `media/videos/...`
- [ ] লগে কোনো ERROR/WARNING নেই (`grep -iE "warn|error|missing"`)
- [ ] বাংলা টেক্সট থাকলে missing-glyph ওয়ার্নিং নেই
- [ ] ভিডিও ইউজারের ভিউয়ারে `present_file` দিয়ে দেখানো হয়েছে

---

## ৭. সমস্যা সমাধান (Troubleshooting)

| সমস্যা | সমাধান |
|---|---|
| `ModuleNotFoundError: manim` | `pip install manim` আবার চালাও |
| `lualatex` পাওয়া যাচ্ছে না (MathTex fails) | texlive প্যাকেজগুলো ইনস্টল করো |
| বাংলা টেক্সটে বক্স (□) দেখায় | `fc-list \| grep -i bengali` চেক করো, Noto Bengali ইনস্টল আছে কি না |
| ffmpeg এরর | `ffmpeg -version` চেক, `apt install ffmpeg` |
| ফন্ট রেন্ডারে ওয়ার্নিং | `fc-cache -f` চালাও |
| `fonts-cm-unicode` প্যাকেজ নেই | CTAN থেকে cm-unicode.zip ডাউনলোড (উপরের ১.৩ দেখো) |

---

## ৮. 🗂️ আপগ্রেড লগ (Changelog)

> নতুন কোনো নিয়ম/ফন্ট/কমান্ড/পরিবর্তন যোগ করলে **এখানে এন্ট্রি যোগ করো** —
> এভাবেই ডকুমেন্টটি ভবিষ্যতে আপগ্রেডযোগ্য থাকে।

| সংস্করণ | তারিখ | পরিবর্তনের বিবরণ |
|---|---|---|
| v1.0 | 2026-08-11 | প্রথম সংস্করণ: পরিবেশ সেটআপ, ফন্ট (CMU + Noto Bengali), রেন্ডার কমান্ড, ১০টি সিস্টেম নিয়ম, টেমপ্লেট, ট্রাবলশুটিং |
| | | ← এখানে যোগ হবে |

---

*ডকুমেন্ট তৈরি: 2026-08-11 | সর্বশেষ আপডেট: 2026-08-11*
