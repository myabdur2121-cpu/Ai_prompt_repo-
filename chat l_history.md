prompt as p 
answer as s 

p1 = 
no end of sassion means sation is not stop automaticaly it work in background . and make a shortcurt to start it "background
a1 = 
ঠিক আছে ভাই। আপনি বলতে চাচ্ছেন:

> Termux session যেন নিজে নিজে বন্ধ না হয়, background-এ কাজ চালাতে পারে, আর shortcut command হবে `background`

এর জন্য আমরা `tmux` + `wake-lock` ব্যবহার করব।

---

## Step 1 — update

```bash
pkg update -y
```

---

## Step 2 — tmux install

```bash
pkg install -y tmux
```

---

## Step 3 — check wake-lock command আছে কিনা

```bash
which termux-wake-lock
```

যদি path দেখায়, ভালো। যদি কিছু না দেখায়, এটা চালান:

```bash
pkg install -y termux-tools
```

---

## Step 4 — `background` shortcut বানান

```bash
cat > $PREFIX/bin/background <<'EOF'
#!/data/data/com.termux/files/usr/bin/bash

SESSION_NAME="background-session"

termux-wake-lock 2>/dev/null || true

if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    echo "🔄 Resuming background session..."
    tmux attach-session -t "$SESSION_NAME"
else
    echo "🚀 Starting new background session..."
    tmux new-session -s "$SESSION_NAME"
fi
EOF
```

---

## Step 5 — executable করুন

```bash
chmod +x $PREFIX/bin/background
```

---

## Step 6 — test করুন

```bash
background
```

এতে নতুন tmux session খুলবে।

---

## কীভাবে background-এ রেখে বের হবেন

tmux session-এর ভিতরে থাকলে চাপুন:

```text
Ctrl + b
```

তারপর:

```text
d
```

মানে আগে `Ctrl+b`, তারপর `d`।

এতে session background-এ চলবে।

---

## আবার background session খুলতে

```bash
background
```

---

## session বন্ধ করতে চাইলে

tmux session-এর ভিতরে:

```bash
exit
```

অথবা বাইরে থেকে:

```bash
tmux kill-session -t background-session
```

তারপর wake-lock ছাড়তে:

```bash
termux-wake-unlock
```

---

## খুব গুরুত্বপূর্ণ

Android যেন Termux-কে kill না করে, তাই ফোনে করুন:

```text
Settings → Apps → Termux → Battery → Unrestricted / Don't optimize
```

এটা না করলে Android background process kill করতে পারে।

p2=ok after that i open a newsation and first command is "background " then one by one give me command 
a2 = ঠিক আছে ভাই। নতুন Termux session খুলে **প্রথমে** চালান:

```bash
background
```

এটার পর আপনি tmux background session-এর ভিতরে চলে যাবেন। এখন আমরা একদম এক এক করে setup করব।

---

## Command 1 — package list update

```bash
pkg update -y
```

শেষ হলে আমাকে শুধু লিখবেন:

```text
done 1
```

তারপর আমি Command 2 দেব।

p3 = done 
a3 =
ভালো।

## Command 2 — basic tools install

```bash
pkg install -y git curl wget nano jq
```

শেষ হলে লিখবেন:

```text
done 2
```

P4 = done 
a4 = 
ভালো।

## Command 3 — Python install

```bash
pkg install -y python
```

শেষ হলে লিখবেন:

```text
done 3
```
p5 = 
If you plan to use the 'ssh-agent'                      it is recommended to run it as a service.               Run 'pkg i termux-services'                             to install the ('runit') service manager                                                                        You can enable the ssh-agent service                    using 'sv-enable ssh-agent'                             You can also enable sshd to autostart                   using 'sv-enable sshd'                                  ~ $ pkg install -y python                               No mirror or mirror group selected. You might want to select one by running 'termux-change-repo'                CANNOT LINK EXECUTABLE "curl": cannot locate symbol "SSL_set_quic_tls_transport_params" referenced by "/data/data/com.termux/files/usr/lib/libngtcp2_crypto_ossl.so"... Failed to run the 'curl' command.                       To fix the 'curl' command, manually upgrade all packages by running: `apt update &amp;&amp; apt full-upgrade`           ~ $                                                     [backgroun0:bash*            "localhost"

a5 = 
এটা Termux-এর **package mismatch** সমস্যা। `curl` আর OpenSSL/ngtcp2 library version match করছে না। আগে mirror select + full upgrade করতে হবে।

এখন একটাই command চালান:

## Fix Command 1 — mirror select

```bash
termux-change-repo
```

এখানে menu আসলে:

1. **Main repository** select করুন  
2. তারপর **Mirror group** বা **Cloudflare / packages-cf.termux.dev** থাকলে সেটা select করুন  
3. OK/Enter দিন

শেষ হলে আমাকে লিখবেন:

```text
done fix 1
```

p6 = 
───────────────termux-change-repo──────────────────┐  │ Do you want to choose a mirror group or a single   │  │ mirror? Select with space.                         │  │ ┌────────────────────────────────────────────────┐ │  │ │(*) Mirror groupRotate between several mirrors (│ │  │ │( ) Single mirroChoose a single mirror to use   │ │  │ │                                                │ │  │ │

a6 = 
এখানে **Mirror group**-ই রাখুন।

এখন শুধু:

```text
Enter
```

চাপুন।

তারপর যদি mirror group list আসে, **Default / Cloudflare / Grimler** টাইপের stable option select করবেন।  
স্ক্রিনে পরের menu আসলে screenshot/text পাঠান।

p7 = 
প্রশ্ন হচ্ছে এর আগেও তো কাজ করেছি এরকম জিনিস তো আসেনি তো কেন আসিনি ?? এটা বাদেও কি কলা যেত না নাকি ??

a7 = 
ভাই, ভালো প্রশ্ন। আগে না আসার কারণ সাধারণত এইগুলোর মধ্যে একটা:

1. **আগে Termux fresh clear করেননি** — পুরোনো repo/mirror config ঠিক ছিল।  
2. **package upgrade মাঝপথে থেমেছিল** — এখন `curl` নতুন/পুরোনো library-এর সাথে mismatch হয়েছে।  
3. **Termux mirror selected নেই** — আপনি storage/cache clear করার পর repo config reset হয়ে গেছে।  
4. **partial update problem** — কিছু package নতুন, কিছু পুরোনো; তাই `curl` এই error দিচ্ছে:

```text
cannot locate symbol SSL_set_quic_tls_transport_params
```

এটা basically OpenSSL / ngtcp2 / curl version mismatch।

---

## এটা বাদ দিয়ে চালানো যেত?

**না, reliable ভাবে না।**

কারণ ManimGL setup করতে পরে লাগবে:

- `pkg install`
- `pip install`
- `git clone`
- `curl/wget`
- native libraries

এখন package manager/curl ভাঙা থাকলে পরে install মাঝপথে fail করবে।

তাই আগে repo + full-upgrade fix করা জরুরি।

---

## আপনি এখন যা করবেন

আপনার screen-এ আছে:

```text
(*) Mirror group
( ) Single mirror
```

এখানে **Mirror group** রেখে শুধু:

```text
Enter
```
চাপুন।

তারপর next screen এলে আমাকে পাঠান।

p8 = 
Which group of mirrors do you want to use? Select  │  │ with space.                                        │  │ ┌────────────────────────────────────────────────┐ │  │ │(*) All mirrors      All in the entire world    │ │  │ │( ) Mirrors in Asia  All in Asia (excl. Chinese │ │  │ │( ) Mirrors in ChinesAll in Chinese Mainland    │ │  │ │( ) Mirrors in EuropeAll in Europe              │ │  │ │( ) Mirrors in North All in North America       │ │  │ │( ) Mirrors in OceaniAll in Oceania             │ │  │ │( ) Mirrors in RussiaAll in Russia              │ │  │ │                                                │ │

│ │

a8 = এখানে **Mirrors in Asia** select করুন — বাংলাদেশ থেকে সাধারণত fastest/stable হবে।

### কী করবেন:
1. Arrow down দিয়ে যান:

```text
Mirrors in Asia
```

2. Space চাপুন, যেন `(*)` হয়।
3. তারপর Enter চাপুন।

এরপর menu শেষ হলে আমাকে লিখবেন:

```text
done mirror
```

p9 = ok 
a10 = 
ভালো।

এখন package mismatch fix করি।

## Fix Command 2 — full upgrade

```bash
apt update && apt full-upgrade -y
```

শেষ হলে লিখবেন:

```text
done upgrade
```

যদি কোনো prompt আসে:

- `Y/n` হলে `y`
- config file replace/keep জিজ্ঞেস করলে সাধারণত **default** রাখার জন্য Enter চাপুন. 


p10 = ok 
p10 = 
এখন চালান:

```bash
apt update && apt full-upgrade -y
```

শেষ হলে লিখবেন:

```text
done upgrade
```

p11 = done 
a11 = 
ভালো। এখন Python install আবার try করি।

## Command 3 — Python install

```bash
pkg install -y python
```

শেষ হলে লিখবেন:

```text
done 3
``` 


p12 = done 
a12 = 
ভালো।

## Command 4 — Python version check

```bash
python -V
```

Output পাঠান বা লিখুন:

```text
done 4
``` 

p12 = 
3.14.6 

a12 = 
ভালো। আপনার fresh Termux-এ এখন Python:

```text
Python 3.14.6
```

এখন build tools এক এক করে install করব।

## Command 5 — clang install

```bash
pkg install -y clang
```

শেষ হলে লিখবেন:

```text
done 5
```

p13 = 
ok done 

a13 = 
ভালো।

## Command 6 — make + pkg-config install

```bash
pkg install -y make pkg-config
```

শেষ হলে লিখবেন:

```text
done 6
```

p14 = 
done 

a14 = 
ভালো।

## Command 7 — cmake + ninja install

```bash
pkg install -y cmake ninja
```

শেষ হলে লিখবেন:

```text
done 7
``` 

p15 = 
done 

a15 = 
ভালো।

## Command 8 — patchelf + binutils install

```bash
pkg install -y patchelf binutils
```

শেষ হলে লিখবেন:

```text
done 8
```

p16 = done 
a16 = 
ভালো।

## Command 9 — FFmpeg install

```bash
pkg install -y ffmpeg
```

শেষ হলে লিখবেন:

```text
done 9
```

p17 = 
done 

a17 = 
ভালো।

এখন graphics/Mesa related repo enable করব।

## Command 10 — x11 repo install

```bash
pkg install -y x11-repo
```

শেষ হলে লিখবেন:

```text
done 10
``` 

p18 = done 
a18 = 
ভালো।

## Command 11 — update after x11 repo

```bash
pkg update -y
```

শেষ হলে লিখবেন:

```text
done 11
```

p19 = done 
a19 = 
ভালো।

## Command 12 — Mesa/OpenGL packages install

```bash
pkg install -y mesa mesa-demos libglvnd
```

শেষ হলে লিখবেন:

```text
done 12
``` 


p19 = done 
a19 = 
ভালো।

## Command 13 — graphics/native libraries install

```bash
pkg install -y freetype fontconfig harfbuzz fribidi libpng libjpeg-turbo zlib libxml2 libxslt glib libffi cairo pango xorgproto
```

শেষ হলে লিখবেন:

```text
done 13
``` 

p20 = 
Checking availability of current mirror:                [*] https://packages-cf.termux.dev/apt/termux-main/: ok Reading package lists... Done                           Building dependency tree... Done                        Reading state information... Done                       E: Unable to locate package cairo                       ~ $                                                     [backgroun0:bash* 



bro you downlod cario . but i want to use GPU

a20 = ভাই, বুঝেছি। কিন্তু একটা জিনিস পরিষ্কার করি:

**`cairo` GPU render করার জন্য না।**  
ManimGL-এর মূল render path GPU দিয়ে হয়:

```text
ManimGL → ModernGL → OpenGL/EGL → Zink/Turnip → Adreno GPU
```

`cairo / pango / harfbuzz` লাগে মূলত:

```text
text, font, SVG, LaTeX-like objects, manimpango
```

মানে `cairo` install করা মানে CPU renderer use করা না। কিন্তু Termux-এ package name `cairo` না, সম্ভবত `libcairo`।

তবে আপনার কথা ঠিক — আগে আমরা GPU path setup করি।

---

## এখন Command 13 — GPU/Vulkan loader install

এইটা চালান:

```bash
pkg install -y vulkan-loader-android
```

শেষ হলে লিখবেন:

```text
done 13
``` 

p21 = 
The following packages have unmet dependencies:          vulkan-icd : Depends: mesa-vulkan-icd-swrast but it is not going to be installed or                                                   mesa-vulkan-icd-freedreno but it is not going to be installed or                                                mesa-vulkan-icd-virtio but it is not going to be installed or                                                   swiftshader but it is not going to be installed                                          E: Error, pkgProblemResolver::Resolve generated breaks, this may be caused by held packages.                    ~ $                                                     [backgroun0:bash*

a21 = 
ভাই, এটা error না — এটা বলছে **Vulkan loader install করতে হলে একটা Vulkan driver/ICD বেছে দিতে হবে**।

আপনার GPU Adreno 615, তাই আমাদের দরকার:

```text
mesa-vulkan-icd-freedreno
```

এটা Termux-এর Turnip/Freedreno driver path।

## Command 14 — Adreno/Turnip Vulkan driver install

এইটা চালান:

```bash
pkg install -y mesa-vulkan-icd-freedreno vulkan-loader-android
```

শেষ হলে লিখবেন:

```text
done 14
```

যদি আবার error আসে, পুরো শেষ 15-20 লাইন পাঠাবেন। 

p22 = 
requested an impossible situation or if you are using the unstable                                              distribution that some required packages have not yet been created                                              or been moved out of Incoming.                          The following information may help to resolve the situation:                                                                                                            The following packages have unmet dependencies:

 vulkan-loader-generic : Conflicts: vulkan-loader-android                                                       E: Unable to correct problems, you have held broken packages.                                                   ~ $                                                     [backgroun0:bash*

a22 = 
ভাই, এটা normal conflict। এখানে দুইটা আলাদা Vulkan loader আছে:

```text
vulkan-loader-android  = Android system Vulkan driver path
vulkan-loader-generic  = Mesa/Turnip/Freedreno path
```

আপনার জন্য যেহেতু **Adreno 615 + Turnip/Freedreno GPU path** চাই, তাই `vulkan-loader-android` লাগবে না।  
আমরা ব্যবহার করব:

```text
mesa-vulkan-icd-freedreno
```

এটা নিজে `vulkan-loader-generic` নেবে।

---

## Command 14 fixed — Android loader বাদ, Freedreno install

```bash
pkg remove -y vulkan-loader-android
```

শেষ হলে এইটা চালান:

```bash
pkg install -y mesa-vulkan-icd-freedreno
```

শেষ হলে লিখবেন:

```text
done 14
```

যদি error আসে, শেষ 20 লাইন পাঠাবেন। 

p23 = 
Preparing to unpack .../mesa-vulkan-icd-freedreno_26.2.4_aarch64.deb ...                                        Unpacking mesa-vulkan-icd-freedreno (26.2.4) ...        Setting up mesa-vulkan-icd-freedreno (26.2.4) ...       ~ $ 

a23 = 
দারুণ ভাই ✅  
আপনার **Adreno/Turnip/Freedreno Vulkan driver installed** হয়েছে।

এখন GPU info check করার tool লাগবে।

## Command 15 — Vulkan tools install

```bash
pkg install -y vulkan-tools
```

শেষ হলে লিখবেন:

```text
done 15
``` 

p24 = ok 
a24 = 
এখন verify করি GPU detect হচ্ছে কিনা।

## Command 16 — Vulkan GPU info check

```bash
vulkaninfo --summary
```

Output-এ `GPU id`, `deviceName`, `driverName`, `Adreno`, `Turnip`, `freedreno` টাইপ কিছু দেখালে GPU path ভালো।

শেষের output পাঠান।

p25 = 
Unpacking vulkan-tools (1.4.365) ...

Setting up vulkan-tools (1.4.365) ...

~ $ vulkaninfo --summary

CANNOT LINK EXECUTABLE "vulkaninfo": cannot locate symbol "_ZNSt6__ndk113__hash_memoryEPKvm" referenced by "/data/data/com.termux/files/usr/bin/vulkaninfo"...          ~ $                                                     [backgroun0:bash* 

a25 = 
ভাই, এটা GPU problem না — এটা **Termux C++ runtime mismatch**।

`vulkaninfo` binary নতুন, কিন্তু `libc++` runtime পুরোনো/মিসম্যাচড। আগে C++ runtime ঠিক করি।

## Command 16A — libc++ fix

```bash
pkg install -y libc++
```

শেষ হলে লিখবেন:

```text
done 16A
``` 

p26 = 
database ... 28086 files and directories currently installed.)                                         Preparing to unpack .../archives/libc++_30_aarch64.deb ...                                                      Unpacking libc++ (30) over (29) ...

Setting up libc++ (30) ...

~ $

[backgroun0:bash*            " 


a26 = 
ভালো। এখন আবার GPU check করুন।

## Command 16B — Vulkan info retry

```bash
vulkaninfo --summary
```

Output পাঠান। 

p27 = 
database ... 28086 files and directories currently installed.)                                         Preparing to unpack .../archives/libc++_30_aarch64.deb ...                                                      Unpacking libc++ (30) over (29) ...



Setting up libc++ (30) ...



~ $



[backgroun0:bash*            " 

a27 = 
ভাই, আপনি শুধু `libc++` install-এর output পাঠিয়েছেন। এখন **আবার Vulkan check command** চালাতে হবে।

## Command 16B — GPU/Vulkan retry

```bash
vulkaninfo --summary
```

যদি output অনেক বড় হয়, তাহলে এইটা চালান:

```bash
vulkaninfo --summary 2>&1 | head -80
```

এর output পাঠান। 

p28 = 
get 342 kB of archives.

After this operation, 49.2 kB of additional disk space w

ill be used.                                            Get:1 https://packages-cf.termux.dev/apt/termux-main stable/main aarch64 libc++ aarch64 30 [342 kB]             Fetched 342 kB in 1s (383 kB/s)                         (Reading database ... 28086 files and directories currently installed.)                                         Preparing to unpack .../archives/libc++_30_aarch64.deb ...                                                      Unpacking libc++ (30) over (29) ...                     Setting up libc++ (30) ...

~ $ vulkaninfo --summary

'DISPLAY' environment variable not set... skipping surfa

ce info

==========

VULKANINFO

==========



Vulkan Instance Version: 1.4.365



 

Instance Extensions: count = 25

-------------------------------

VK_EXT_acquire_drm_display             : extension revis

ion 1

VK_EXT_acquire_xlib_display            : extension revis

ion 1

VK_EXT_debug_report                    : extension revis

ion 10

VK_EXT_debug_utils                     : extension revis

ion 2

VK_EXT_direct_mode_display             : extension revis

ion 1

VK_EXT_display_surface_counter

VK_EXT_acquire_drm_display             : 14:40 [45/1820]ion 1                                                   VK_EXT_acquire_xlib_display            : extension revision 1                                                   VK_EXT_debug_report                    : extension revision 10                                                  VK_EXT_debug_utils                     : extension revision 2                                                   VK_EXT_direct_mode_display             : extension revision 1                                                   VK_EXT_display_surface_counter         : extension revision 1                                                   VK_EXT_headless_surface                : extension revision 1                                                   VK_EXT_surface_maintenance1            : extension revision 1                                                   VK_EXT_swapchain_colorspace            : extension revision 5                                                   VK_KHR_device_group_creation           : extension revision 1                                                   VK_KHR_display                         : extension revis

ion 23

VK_KHR_external_fence_capabilities     : extension revis

ion 1                                                   VK_KHR_external_memory_capabilities    : extension revis

ion 1                                                   VK_KHR_external_semaphore_capabilities : extension revis

ion 1

VK_KHR_get_display_properties2         : extension revis

ion 1

VK_KHR_get_physical_device_properties2 : extension revis

ion 2

VK_KHR_get_surface_capabilities2       : extension revis

ion 1                                                   VK_KHR_portability_enumeration         : extension revis

ion 1

VK_KHR_surface                         : extension revis

ion 25

VK_KHR_surface_maintenance1            : extension revis

ion 1                                                   VK_KHR_surface_protected_capabilities  : extension revis

ion 1                                                   VK_KHR_wayland_surface                 : extension revis

ion 6

[backgroun0:[tmux]*

                                               VK_KHR_xlib_surface                    : extension revision 6                                                   VK_LUNARG_direct_driver_loading        : extension revision 1                                                                                                           Instance Layers:                                        ----------------                                                                                                Devices:                                                ========                                                GPU0:                                                           apiVersion         = 1.3.354                            driverVersion      = 26.2.4                             vendorID           = 0x5143                             deviceID           = 0x6030001                          deviceType         = PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU                                                        deviceName         = Turnip Adreno (TM) 630

        driverID           = DRIVER_ID_MESA_TURNIP              driverName         = turnip Mesa driver

        driverInfo         = Mesa 26.2.4

        conformanceVersion = 1.2.7.1

        deviceUUID         = 7900ee64-e98f-fdc8-f212-02dfadc8aa03

        driverUUID         = ca280d64-7b4b-f58c-e0a4-470865f38e17

GPU1:

        apiVersion         = 1.4.354

        driverVersion      = 26.2.4

        vendorID           = 0x10005

        deviceID           = 0x0000

        deviceType         = PHYSICAL_DEVICE_TYPE_CPU

        deviceName         = llvmpipe (LLVM 21.1.8, 128 bits)

        driverID           = DRIVER_ID_MESA_LLVMPIPE

        driverName         = llvmpipe

        driverInfo         = Mesa 26.2.4 (LLVM 21.1.8)

        conformanceVersion = 1.3.1.1

        deviceUUID         = 6d657361-3236-2e32-2e34-000000000000

        driverUUID         = 6c6c766d-7069-7065-5555-494400000000

~ $ 
a28 = 
দারুণ ভাই! ✅  
এটা **খুব ভালো news**।

আপনার output-এ GPU detect হয়েছে:

```text
GPU0:
deviceName = Turnip Adreno (TM) 630
driverName = turnip Mesa driver
driverInfo = Mesa 26.2.4
```

মানে Termux এখন **Turnip/Freedreno Vulkan GPU driver** দেখতে পাচ্ছে।  
`GPU1 llvmpipe` আছে, কিন্তু সেটা CPU fallback। আমাদের লক্ষ্য হবে **GPU0 Turnip** ব্যবহার করা।

এখন ManimGL-এর জন্য OpenGL → Vulkan bridge দরকার, সেটা হলো **Zink**।

---

## Command 17 — Zink install

```bash
pkg install -y mesa-zink
```

শেষ হলে লিখবেন:

```text
done 17
```

যদি `Unable to locate package` আসে, output পাঠাবেন। 

p29 = ok 
a29 = 
জি ভাই, আছি।  
আপনি এখন কোন অবস্থায় আছেন?

আমাদের current status:

✅ `mesa-vulkan-icd-freedreno` installed  
✅ `vulkaninfo` GPU detect করেছে  
✅ Turnip GPU path আছে:

```text
Turnip Adreno
driverName = turnip Mesa driver
```

এখন next step ছিল:

```bash
pkg install -y mesa-zink
```

কারণ ManimGL OpenGL চায়, আর Zink OpenGL → Vulkan → Adreno GPU path দেয়।

আপনি কি `mesa-zink` command চালিয়েছেন?  
না চালালে এখন চালান:

```bash
pkg install -y mesa-zink
```

তারপর output পাঠান। 

p30 = 
Reading state information... Done

E: Unable to locate package mesa-zink

~ $ pkg install -y mesa-zink                            Checking availability of current mirror:                [*] https://packages-cf.termux.dev/apt/termux-main/: ok Reading package lists... Done                           Building dependency tree... Done                        Reading state information... Done                       E: Unable to locate package mesa-zink                   ~ $                                                     [backgroun0:bash*

a30 = 
ঠিক আছে ভাই — `mesa-zink` main repo-তে নেই, এটা সাধারণত **TUR repo** থেকে আসে। তাই আগে TUR repo enable করতে হবে। এই fix commonly used for `mesa-zink` on Termux [1](https://www.reddit.com/r/termux/comments/1fv4c8n/unable_to_locate_package_mesazink/)।

## Command 17A — TUR repo enable

```bash
pkg install -y tur-repo
```

শেষ হলে লিখবেন:

```text
done 17A
``` 

p31 = 
next 

a31 = 
## Command 17B — update after TUR repo

```bash
pkg update -y
```

শেষ হলে লিখবেন:

```text
done 17B
``` 

p32 = 
next 
a32 = 
## Command 17C — install Zink

```bash
pkg install -y mesa-zink
```

শেষ হলে output দেখে লিখবেন:

```text
done 17C
```

যদি error আসে, শেষের 15–20 লাইন পাঠাবেন। 

p33 = 
next 

a33 = 
## Command 18 — Zink driver file আছে কিনা check

```bash
ls $PREFIX/lib/dri | grep -E "zink|freedreno|swrast"
```

Output পাঠান।  
বিশেষ করে `zink_dri.so` দেখা গেলে ভালো। 

p34 = (Reading database ... 28036 files and directories currently installed.)                                         Preparing to unpack .../mesa-zink_22.0.5-5_aarch64.deb ...

Unpacking mesa-zink (22.0.5-5) ...                      Setting up xorg-xrandr (1.5.4) ...

Setting up mesa-zink (22.0.5-5) ...

~ $

[backgroun0:bash*            "log 


a34 = 
দারুণ ভাই ✅ `mesa-zink` install হয়ে গেছে।

এখন verify করি Zink driver file আছে কিনা।

## Command 18 — Zink/Freedreno driver files check

```bash
ls $PREFIX/lib/dri | grep -E "zink|freedreno|swrast"
```

Output পাঠান। 

p35 = 
Setting up mesa-zink (22.0.5-5) ...                     ~ $ ls $PREFIX/lib/dri | grep -E "zink|freedreno|swrast"kms_swrast_dri.so

swrast_dri.so                                           zink_dri.so                                             ~ $

[backgroun0:bash*



আসলে আমাদের কথোপকথন একটু আর আগ পিছ হয়ে গেছে অর্থাৎ আমি এখন যেটা দিচ্ছি সেটা দুইটা চ্যাট পড়ে এসে দেখা যাবে মানে একটু অন্যরকম হয়ে গেল 

a35 = 
কোনো সমস্যা নেই ভাই। কথোপকথন একটু আগ-পিছ হলেও current status আমি ঠিক ধরেছি।

আপনার current result:

```text
zink_dri.so
kms_swrast_dri.so
swrast_dri.so
```

মানে **Zink installed আছে** ✅  
এখন আমরা test করব Zink দিয়ে OpenGL context ওঠে কিনা।

---

## Command 19 — EGL/Zink info test

```bash
MESA_LOADER_DRIVER_OVERRIDE=zink GALLIUM_DRIVER=zink TU_DEBUG=noconform eglinfo -B
```

যদি output বড় হয়, শেষের অংশ পাঠাবেন।  
বিশেষ করে এইগুলো খুঁজব:

```text
EGL vendor
OpenGL vendor
OpenGL renderer
zink
Turnip
Adreno
```

Command চালিয়ে output পাঠান। 

p36 = 
next 

a26 = 
ঠিক আছে ভাই। এখন `eglinfo` output বড় হলে compact করে দেখি।

## Command 20 — compact GPU/OpenGL renderer check

```bash
MESA_LOADER_DRIVER_OVERRIDE=zink GALLIUM_DRIVER=zink TU_DEBUG=noconform eglinfo -B 2>&1 | grep -Ei "vendor|renderer|version|zink|turnip|adreno|llvmpipe|software"
```

Output পাঠান।  
আমরা দেখতে চাই `zink` / `Turnip` / `Adreno` আসে কিনা। 

p37 = 

penGL core profile shading language version: 1.50      OpenGL compatibility profile vendor: Collabora Ltd      OpenGL compatibility profile renderer: zink (Turnip Adreno (TM) 630)                                            OpenGL compatibility profile version: 3.2 (Compatibility Profile) Mesa 22.0.5                                   OpenGL compatibility profile shading language version: 1.50                                                     OpenGL ES profile vendor: Collabora Ltd                 OpenGL ES profile renderer: zink (Turnip Adreno (TM) 630)                                                       OpenGL ES profile version: OpenGL ES 3.2 Mesa 22.0.5    OpenGL ES profile shading language version: OpenGL ES GLSL ES 3.20                                                                                                      Device platform:                                        Device #0:                                                                                                      Platform Device platform:                               EGL API version: 1.4                                    EGL vendor string: Mesa Project

EGL version string: 1.4

EGL client APIs: OpenGL OpenGL_ES

OpenGL core profile vendor: Collabora Ltd

OpenGL core profile renderer: zink (Turnip Adreno (TM) 630)

OpenGL core profile version: 3.2 (Core Profile) Mesa 22.0.5

OpenGL core profile shading language version: 1.50

OpenGL compatibility profile vendor: Collabora Ltd

OpenGL compatibility profile renderer: zink (Turnip Adreno (TM) 630)

OpenGL compatibility profile version: 3.2 (Compatibility Profile) Mesa 22.0.5

OpenGL compatibility profile shading language version: 1.50

OpenGL ES profile vendor: Collabora Ltd

OpenGL ES profile renderer: zink (Turnip Adreno (TM) 630)

OpenGL ES profile version: OpenGL ES 3.2 Mesa 22.0.5

OpenGL ES profile shading language version: OpenGL ES GLSL ES 

a37 = 
দারুণ ভাই ✅  
এটা confirm হয়ে গেছে:

```text
OpenGL renderer: zink (Turnip Adreno)
```

মানে **GPU path active**:

```text
OpenGL → Zink → Turnip → Adreno GPU
```

এখন ছোট একটা গুরুত্বপূর্ণ test করব: ManimGL/ModernGL সাধারণত **OpenGL 3.3** চায়। আপনার output-এ 3.2 দেখাচ্ছে। তাই override দিয়ে 3.3 পাওয়া যায় কিনা দেখি।

## Command 21 — OpenGL 3.3 override test

```bash
MESA_LOADER_DRIVER_OVERRIDE=zink GALLIUM_DRIVER=zink TU_DEBUG=noconform MESA_GL_VERSION_OVERRIDE=3.3 MESA_GLSL_VERSION_OVERRIDE=330 eglinfo -B 2>&1 | grep -Ei "OpenGL core profile vendor|OpenGL core profile renderer|OpenGL core profile version|shading language"
```

Output পাঠান। 


p38 = 
next 

a38 = 
ভাই, আগে Command 21-এর output দেখা দরকার ছিল। আপনি যদি চালিয়ে থাকেন, output পাঠান।

যদি না চালিয়ে থাকেন, এখন চালান:

```bash
MESA_LOADER_DRIVER_OVERRIDE=zink GALLIUM_DRIVER=zink TU_DEBUG=noconform MESA_GL_VERSION_OVERRIDE=3.3 MESA_GLSL_VERSION_OVERRIDE=330 eglinfo -B 2>&1 | grep -Ei "OpenGL core profile vendor|OpenGL core profile renderer|OpenGL core profile version|shading language"
```

তারপর output দিন।  
এরপর আমরা Python ModernGL GPU context test করব। 


p39 = 
14:54 [55/1910]~ $ MESA_LOADER_DRIVER_OVERRIDE=zink GALLIUM_DRIVER=zink TU_DEBUG=noconform eglinfo -B 2&gt;&amp;1 | grep -Ei "vendor|renderer|version|zink|turnip|adreno|llvmpipe|software"   EGL API version: 1.4                                    EGL vendor string: Mesa Project                         EGL version string: 1.4                                 OpenGL core profile vendor: Collabora Ltd               OpenGL core profile renderer: zink (Turnip Adreno (TM) 630)                                                     OpenGL core profile version: 3.2 (Core Profile) Mesa 22.0.5                                                     OpenGL core profile shading language version: 1.50      OpenGL compatibility profile vendor: Collabora Ltd      OpenGL compatibility profile renderer: zink (Turnip Adreno (TM) 630)                                            OpenGL compatibility profile version: 3.2 (Compatibility Profile) Mesa 22.0.5                                   OpenGL compatibility profile shading language version: 1.50                                                     OpenGL ES profile vendor: Collabora Ltd                 OpenGL ES profile renderer: zink (Turnip Adreno (TM) 630)

OpenGL ES profile version: OpenGL ES 3.2 Mesa 22.0.5

OpenGL ES profile shading language version: OpenGL ES GLSL ES 3.20

EGL API version: 1.4                                    EGL vendor string: Mesa Project

EGL version string: 1.4

OpenGL core profile vendor: Collabora Ltd               OpenGL core profile renderer: zink (Turnip Adreno (TM) 6

30)                                                     OpenGL core profile version: 3.2 (Core Profile) Mesa 22.

0.5

OpenGL core profile shading language version: 1.50      OpenGL compatibility profile vendor: Collabora Ltd

OpenGL compatibility profile renderer: zink (Turnip Adreno (TM) 630)

OpenGL compatibility profile version: 3.2 (Compatibility

 Profile)

)                                                     OpenGL core profile version: 3.3 (Core Profile) Mesa 22.0.5                                                     OpenGL core profile shading language version: 3.30      OpenGL compatibility profile shading language version: 3.30                                                     OpenGL ES profile shading language version: OpenGL ES GLSL ES 3.20                                              OpenGL core profile vendor: Collabora Ltd               OpenGL core profile renderer: zink (Turnip Adreno (TM) 630)                                                     OpenGL core profile version: 3.3 (Core Profile) Mesa 22.0.5                                                     OpenGL core profile shading language version: 3.30      OpenGL compatibility profile shading language version: 3.30                                                     OpenGL ES profile shading language version: OpenGL ES GLSL ES 3.20                                              ~ $ MESA_LOADER_DRIVER_OVERRIDE=zink GALLIUM_DRIVER=zink TU_DEBUG=noconform MESA_GL_VERSION_OVERRIDE=3.3 MESA_GLSL_VERSION_OVERRIDE=330 eglinfo -B 2&gt;&amp;1 | grep -Ei "OpenGL core profile vendor|OpenGL core profile renderer|OpenGL core profile version|shading language"

OpenGL core profile vendor: Collabora Ltd

OpenGL core profile renderer: zink (Turnip Adreno (TM) 630)

OpenGL core profile version: 3.3 (Core Profile) Mesa 22.0.5

OpenGL core profile shading language version: 3.30

OpenGL compatibility profile shading language version: 3.30

OpenGL ES profile shading language version: OpenGL ES GLSL ES 3.20

OpenGL core profile vendor: Collabora Ltd

OpenGL core profile renderer: zink (Turnip Adreno (TM) 630)

OpenGL core profile version: 3.3 (Core Profile) Mesa 22.0.5

OpenGL core profile shading language version: 3.30

OpenGL compatibility profile shading language version: 3.30

OpenGL ES profile shading language version: OpenGL ES GLSL ES 3.20 

a39 = দারুণ ভাই ✅ GPU path এখন confirmed:

```text
OpenGL 3.3 → zink → Turnip Adreno GPU
```

এখন ManimGL-এর text/font dependency install করব। আগের `cairo` ভুল package name ছিল; Termux-এ সঠিক নাম হলো **`libcairo`**। এটা GPU না, শুধু text/SVG/font support-এর জন্য লাগে।

## Command 22 — Cairo/Pango text libs

```bash
pkg install -y libcairo pango
```

শেষ হলে লিখবেন:

```text
done 22
```

Error হলে শেষের output পাঠাবেন।

p40 = 
can you see it. 

a40 = 
হ্যাঁ ভাই, আমি **আপনি যে output paste করেছেন সেটা দেখতে পাচ্ছি**।  
তবে আমি আপনার Termux screen **live দেখতে পাই না**—আপনি যা এখানে paste/upload করেন, শুধু সেটাই দেখি।

আমি দেখেছি:

```text
OpenGL core profile renderer: zink (Turnip Adreno)
OpenGL core profile version: 3.3
```

মানে GPU path ঠিক আছে ✅

এখন next command চালান:

```bash
pkg install -y libcairo pango
```

শেষ হলে লিখবেন:

```text
done 22
```

p41 = 
done pkg install -y libcairo pango 

a41 = 
ভালো ✅

এখন ManimGL-এর Python heavy dependencies install করব Termux repo থেকে — এতে pip build কম হবে।

## Command 23 — Python scientific/text packages

```bash
pkg install -y python-numpy python-scipy python-pillow python-matplotlib python-manimpango
```

শেষ হলে লিখবেন:

```text
done 23
```

যদি কোনো package unavailable হয়, শেষের output পাঠাবেন। 

p42 = done pkg install -y libcairo pango

a42 = 
ঠিক আছে ভাই, Command 22 complete ✅

এখন next command চালান।

## Command 23 — Python scientific packages

```bash
pkg install -y python-numpy python-scipy python-pillow python-matplotlib python-manimpango
```

শেষ হলে লিখবেন:

```text
done 23
```

যদি error আসে, শেষের 15–20 লাইন পাঠাবেন। 


p43 = 

Building dependency tree... Done                        Reading state information... Done                       E: Unable to locate package python-matplotlib           ~ $                                                     [backgroun0:bash* 

a43 = 
ঠিক আছে ভাই। `python-matplotlib` package আপনার repo-তে নেই। সমস্যা নেই — আগে বাকি important packages install করি।

## Command 23A — install available Python packages

```bash
pkg install -y python-numpy python-scipy python-pillow python-manimpango
```

শেষ হলে লিখবেন:

```text
done 23A
```

যদি error আসে, output পাঠাবেন। 

p44 = 
Preparing to unpack .../pango_1.58.2_aarch64.deb ...    Unpacking pango (1.58.2) ...

Setting up libxft (2.3.9-1) ...

Setting up pango (1.58.2) ...

~ $ pkg install -y python-numpy python-scipy python-pillow python-matplotlib python-manimpango                  Checking availability of current mirror:                [*] https://packages-cf.termux.dev/apt/termux-main/: ok Reading package lists... Done                           Building dependency tree... Done                        Reading state information... Done                       E: Unable to locate package python-matplotlib           ~ $                                                     [backgroun0:bash* 

a44 = 
হ্যাঁ ভাই, আমি দেখছি — `python-matplotlib` নেই, তাই পুরো command থেমে গেছে। এখন matplotlib বাদ দিয়ে চালান।

## Command 23A

```bash
pkg install -y python-numpy python-scipy python-pillow python-manimpango
```

শেষ হলে লিখবেন:

```text
done 23A
``` 

p45 = 
done 23 Setting up python-pillow (12.3.0) ...                   Installing dependencies for python-pillow through pip...Requirement already satisfied: pillow in ./data/data/com.termux/files/usr/lib/python3.14/site-packages (12.3.0) Setting up python-scipy (1:1.18.1) ...                  Installing dependencies for python-scipy through pip... Requirement already satisfied: scipy in ./data/data/com.termux/files/usr/lib/python3.14/site-packages (1.18.1)  Requirement already satisfied: numpy&lt;2.8,&gt;=2.0.0 in ./data/data/com.termux/files/usr/lib/python3.14/site-packages (from scipy) (2.4.4)                                  ~ $

a45 = 
দারুণ ✅

এখন pip build tools install করব, কিন্তু `maturin` দেব না।

## Command 24 — pip build tools

```bash
python -m pip install -U pip setuptools wheel cython pybind11 meson
```

শেষ হলে লিখবেন:

```text
done 24
``` 

p46 = 
done 

a46 = 
ভালো, Command 23A complete ✅

এখন Command 24 চালান।

## Command 24 — pip build tools

```bash
python -m pip install -U pip setuptools wheel cython pybind11 meson
```

শেষ হলে লিখবেন:

```text
done 24
``` 

P47 = 
kaging, meson, cython, wheel              15:09 [5/1955]ERROR: Exception:                                       Traceback (most recent call last):                        File "/data/data/com.termux/files/usr/lib/python3.14/site-packages/pip/_internal/cli/base_command.py", line 109, in _run_wrapper                                          status = _inner_run()                                 File "/data/data/com.termux/files/usr/lib/python3.14/site-packages/pip/_internal/cli/base_command.py", line 102, in _inner_run                                            return self.run(options, args)                                 ~~~~~~~~^^^^^^^^^^^^^^^                        File "/data/data/com.termux/files/usr/lib/python3.14/site-packages/pip/_internal/cli/req_command.py", line 106, in wrapper                                                return func(self, options, args)                      File "/data/data/com.termux/files/usr/lib/python3.14/site-packages/pip/_internal/commands/install.py", line 570, in run                                                   installed = install_given_reqs(                             to_install,                                         ...&lt;6 lines&gt;...

        progress_bar=options.progress_bar,

    )

  File "/data/data/com.termux/files/usr/lib/python3.14/s

ite-packages/pip/_internal/req/__init__.py", line 85, in

 install_given_reqs

    requirement.install(

    ~~~~~~~~~~~~~~~~~~~^

        root=root,

        ^^^^^^^^^^

    ...&lt;5 lines&gt;...                                             script_executable=script_executable,                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    )                                                       ^

  File "/data/data/com.termux/files/usr/lib/python3.14/site-packages/pip/_internal/req/req_install.py", line 779, in install

    from pip._internal.operations.install.wheel import i

nstall_wheel                                              File "/data/data/com.termux/files/usr/lib/python3.14/s

ite-packages/pip/_internal/commands/install.py", line 9$

, in _prevent_import_hook

[backgroun0:[tmux]* 

a47 = 
ঠিক আছে ভাই, এটা বড় সমস্যা না।  
`pip` নিজেকেই upgrade করতে গিয়ে Termux Python 3.14-এর সাথে conflict করেছে। ManimGL-এর জন্য **pip upgrade দরকার নেই**।

আগে দেখি `pip` এখনও ঠিক আছে কিনা।

## Command 24A — pip check

```bash
python -m pip --version
```

Output পাঠান। 

p48 = 
```
kaging, meson, cython, wheel              15:09 [5/1955]ERROR: Exception:                                       Traceback (most recent call last):                        File "/data/data/com.termux/files/usr/lib/python3.14/site-packages/pip/_internal/cli/base_command.py", line 109, in _run_wrapper                                          status = _inner_run()                                 File "/data/data/com.termux/files/usr/lib/python3.14/site-packages/pip/_internal/cli/base_command.py", line 102, in _inner_run                                            return self.run(options, args)                                 ~~~~~~~~^^^^^^^^^^^^^^^                        File "/data/data/com.termux/files/usr/lib/python3.14/site-packages/pip/_internal/cli/req_command.py", line 106, in wrapper                                                return func(self, options, args)                      File "/data/data/com.termux/files/usr/lib/python3.14/site-packages/pip/_internal/commands/install.py", line 570, in run                                                   installed = install_given_reqs(                             to_install,                                         ...<6 lines>...
        progress_bar=options.progress_bar,
    )
  File "/data/data/com.termux/files/usr/lib/python3.14/s
ite-packages/pip/_internal/req/__init__.py", line 85, in
 install_given_reqs
    requirement.install(
    ~~~~~~~~~~~~~~~~~~~^
        root=root,
        ^^^^^^^^^^
    ...<5 lines>...                                             script_executable=script_executable,                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )                                                       ^
  File "/data/data/com.termux/files/usr/lib/python3.14/site-packages/pip/_internal/req/req_install.py", line 779, in install
    from pip._internal.operations.install.wheel import i
nstall_wheel                                              File "/data/data/com.termux/files/usr/lib/python3.14/s
ite-packages/pip/_internal/commands/install.py", line 9$
, in _prevent_import_hook
[backgroun0:[tmux]*
```

a48 = 
ভাই, আপনি আবার আগের error-টাই paste করেছেন। সমস্যা নেই।

এখন আমাদের শুধু check করতে হবে `pip` এখনো কাজ করছে কিনা।

## Command 24A — pip check

Termux prompt-এ এই একটাই command চালান:

```bash
python -m pip --version
```

যদি version দেখায়, তাহলে লিখবেন:

```text
pip ok
```

যদি আবার error দেখায়, তাহলে লিখবেন:

```text
pip broken
```

এবং শেষের 20 লাইন পাঠাবেন। 

p49 = 

python -m pip --version

pip 26.2.1 from /data/data/com.termux/files/usr/lib/python3.14/site-packages/pip (python 3.14)

~ $ 

a50 = 
ভালো ✅ `pip` ঠিক আছে।

এখন pip upgrade না করে শুধু missing build tools install করব।

## Command 24B — build tools without pip upgrade

```bash
python -m pip install setuptools wheel cython pybind11 meson
```

শেষ হলে লিখবেন:

```text
done 24B
``` 

p51 = 
python -m pip --version



pip 26.2.1 from /data/data/com.termux/files/usr/lib/python3.14/site-packages/pip (python 3.14)



~ $ 

a51 = 
ভালো। এখন এই command চালান:

```bash
python -m pip install setuptools wheel cython pybind11 meson
```

শেষ হলে লিখবেন:

```text
done 24B
``` 

p52 = 
Collecting packaging&gt;=24.0 (from wheel)

  Using cached packaging-26.3-py3-none-any.whl.metadata (3.5 kB)

Using cached setuptools-84.0.0-py3-none-any.whl (818 kB)

Using cached wheel-0.48.0-py3-none-any.whl (33 kB)

Using cached cython-3.3.0-py3-none-any.whl (1.3 MB)

Using cached pybind11-3.1.0-py3-none-any.whl (319 kB)

Using cached meson-1.12.1-py3-none-any.whl (1.1 MB)

Using cached packaging-26.3-py3-none-any.whl (129 kB)

Installing collected packages: setuptools, pybind11, packaging, meson, cython, wheel

ERROR: Exception:

Traceback (most recent call last):

  File "/data/data/com.termux/files/usr/lib/python3.14/site-packages/pip/_internal/cli/base_command.py", line 109, in _run_wrapper

    status = _inner_run()

  File "/data/data/com.termux/files/usr/lib/python3.14/site-packages/pip/_internal/cli/base_command.py", line 102, in _inner_run

    return self.run(options, args)

           ~~~~~~~~^^^^^^^^^^^^^^^

  File "/data/data/com.termux/files/usr/lib/python3.14/site-packages/pip/_internal/cli/req_command.py", line 106, in wrapper

    return func(self, options, args)

  File "/data/data/com.termux/files/usr/lib/python3.14/site-packages/pip/_internal/commands/install.py", line 570, in run

    installed = install_given_reqs(

        to_install,

    ...&lt;6 lines&gt;...

        progress_bar=options.progress_bar,

    )

  File "/data/data/com.termux/files/usr/lib/python3.14/site-packages/pip/_internal/req/__init__.py", line 85, in install_given_reqs

    requirement.install(

    ~~~~~~~~~~~~~~~~~~~^

        root=root,

        ^^^^^^^^^^

    ...&lt;5 lines&gt;...

        script_executable=script_executable,

        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    )

    ^

  File "/data/data/com.termux/files/usr/lib/python3.14/site-packages/pip/_internal/req/req_install.py", line 779, in install

    from pip._internal.operations.install.wheel import install_wheel

  File "/data/data/com.termux/files/usr/lib/python3.14/site-packages/pip/_internal/commands/install.py", line 97, in _prevent_import_hook

    raise ImportError(f"No module named {module!r}")

ImportError: No module named 'pip._internal.operations.install.wheel'

~ $

a51 = 
ভাই, `pip` এখন **partially broken** হয়েছে, কারণ Termux-এ `pip` নিজে দিয়ে `setuptools/wheel` install করতে গিয়ে internal wheel installer miss করছে।

এটা ঠিক করতে Termux-এর official pip package install করি।

## Command 24C — repair pip

```bash
pkg install -y python-pip
```

শেষ হলে লিখবেন:

```text
done 24C
```

যদি বলে already installed, তবুও output পাঠাবেন। 

p52 = 
ImportError: No module named 'pip._internal.operations.install.wheel'

~ $ pkg install -y python-pip

Checking availability of current mirror:

[*] https://packages-cf.termux.dev/apt/termux-main/: ok

Reading package lists... Done

Building dependency tree... Done

Reading state information... Done

python-pip is already the newest version (26.2.1).

python-pip set to manually installed.

0 upgraded, 0 newly installed, 0 to remove and 64 not upgraded.

~ $
a52 = 
ভাই, `python-pip` already installed, কিন্তু pip-এর internal files mismatch/partial broken হয়েছে। তাই এখন **reinstall** করতে হবে।

## Command 24D — force reinstall pip

```bash
apt install --reinstall -y python-pip
```

শেষ হলে এই check চালান:

```bash
python -m pip --version
```

তারপর এই check চালান:

```bash
python - <<'PY'
import pip._internal.operations.install.wheel
print("PIP_WHEEL_INTERNAL_OK")
PY
```

Output পাঠান। 

p53 = 

(Reading database ... 31016 files and directories currently installed.)

Preparing to unpack .../python-pip_26.2.1_all.deb ...

Unpacking python-pip (26.2.1) over (26.2.1) ...

Setting up python-pip (26.2.1) ...

pip setup...

Writing to /data/data/com.termux/files/usr/etc/pip.conf

~ $ python -m pip --version

pip 26.2.1 from /data/data/com.termux/files/usr/lib/python3.14/site-packages/pip (python 3.14)

~ $ python - &lt;&lt;'PY'

import pip._internal.operations.install.wheel

print("PIP_WHEEL_INTERNAL_OK")

PY

Traceback (most recent call last):

  File "&lt;stdin&gt;", line 1, in &lt;module&gt;

  File "/data/data/com.termux/files/usr/lib/python3.14/site-packages/pip/_internal/operations/install/wheel.py", line 32, in &lt;module&gt;

    from pip._vendor.distlib.scripts import ScriptMaker

  File "/data/data/com.termux/files/usr/lib/python3.14/site-packages/pip/_vendor/distlib/scripts.py", line 17, in &lt;module&gt;

    from .compat import sysconfig, detect_encoding, ZipFile

  File "/data/data/com.termux/files/usr/lib/python3.14/site-packages/pip/_vendor/distlib/compat.py", line 77, in &lt;module&gt;

    import xmlrpc.client as xmlrpclib

  File "/data/data/com.termux/files/usr/lib/python3.14/xmlrpc/client.py", line 138, in &lt;module&gt;

    from xml.parsers import expat

  File "/data/data/com.termux/files/usr/lib/python3.14/xml/parsers/expat.py", line 4, in &lt;module&gt;

    from pyexpat import *

ImportError: dlopen failed: cannot locate symbol "XML_SetHashSalt16Bytes" referenced by "/data/data/com.termux/files/usr/lib/python3.14/lib-dynload/pyexpat.cpython-314-aarch64-linux-android.so"...

~ $ 


a53 = 
ভাই, এখন যে error এসেছে এটা **pip problem না** — এটা আসলে **libexpat / Python mismatch**।

Error:

```text
XML_SetHashSalt16Bytes
```

মানে Python 3.14-এর `pyexpat` নতুন `libexpat` চাচ্ছে, কিন্তু আপনার Termux-এ পুরোনো/মিসম্যাচড `libexpat` load হচ্ছে।

আপনার output-এ আগে দেখা গেছে:

```text
64 not upgraded
```

তাই আগে সব package align করতে হবে।

## Command 24E — full system upgrade

```bash
apt update && apt full-upgrade -y
```

যদি prompt আসে:

- `Y/n` → `y`
- config file keep/replace → default রাখতে Enter

শেষ হলে লিখবেন:

```text
done 24E
```

তারপর আমরা `pyexpat` check করব। 


p54 = 
done 

a54 =
ভালো। এখন `pyexpat` ঠিক হয়েছে কিনা check করি।

## Command 24F — pyexpat check

```bash
python - <<'PY'
from xml.parsers import expat
print("PYEXPAT_OK")
print(expat.EXPAT_VERSION)
PY
```

Output পাঠান। 

p55 = 
using 'sv-enable ssh-agent'

You can also enable sshd to autostart

using 'sv-enable sshd'

~ $ python - &lt;&lt;'PY'

from xml.parsers import expat

print("PYEXPAT_OK")

print(expat.EXPAT_VERSION)

PY

PYEXPAT_OK

expat_2.8.5

~ $ 


a55 = 
দারুণ ভাই ✅  
এখন Python XML/expat problem fixed:

```text
PYEXPAT_OK
expat_2.8.5
```

এখন pip আবার ঠিকমতো install করতে পারে কিনা check করি।

## Command 24G — pip internal wheel check

```bash
python - <<'PY'
import pip._internal.operations.install.wheel
print("PIP_INTERNAL_WHEEL_OK")
PY
```

Output পাঠান।

p56 = print(expat.EXPAT_VERSION)

PY

PYEXPAT_OK

expat_2.8.5

~ $ python - &lt;&lt;'PY'

import pip._internal.operations.install.wheel

print("PIP_INTERNAL_WHEEL_OK")

PY

PIP_INTERNAL_WHEEL_OK

~ $ 

a56 = 
দারুণ ✅ pip এখন ঠিক হয়েছে।

এখন আবার build tools install করি।

## Command 25 — pip build tools install

```bash
python -m pip install setuptools wheel cython pybind11 meson
```

শেষ হলে লিখবেন:

```text
done 25
``` 


p57 = 
Using cached setuptools-84.0.0-py3-none-any.whl (818 kB)

Using cached wheel-0.48.0-py3-none-any.whl (33 kB)

Using cached cython-3.3.0-py3-none-any.whl (1.3 MB)

Using cached pybind11-3.1.0-py3-none-any.whl (319 kB)

Using cached meson-1.12.1-py3-none-any.whl (1.1 MB)

Using cached packaging-26.3-py3-none-any.whl (129 kB)

Installing collected packages: setuptools, pybind11, packaging, meson, cython, wheel

Successfully installed cython-3.3.0 meson-1.12.1 packaging-26.3 pybind11-3.1.0 setuptools-84.0.0 wheel-0.48.0

~ $ 


a57 = 
দারুণ ভাই ✅ Build tools install হয়ে গেছে।

এখন ManimGL-এর **pure Python dependencies** install করি। এগুলো সাধারণত compile করে না, তাই safe.

## Command 26 — Pure Python dependencies

```bash
python -m pip install addict appdirs colour diskcache fonttools ipython pydub pygments PyOpenGL pyperclip pyyaml rich screeninfo svgelements sympy tqdm validators audioop-lts
```

শেষ হলে লিখবেন:

```text
done 26
``` 

p58 = 
ollecting prompt_toolkit&lt;3.1.0,&gt;=3.0.41 (from ipython)

  Downloading prompt_toolkit-3.0.53-py3-none-any.whl.metadata (6.4 kB)

Collecting psutil&gt;=7 (from ipython)

  Downloading psutil-7.2.2.tar.gz (493 kB)

  Installing build dependencies ... done

  Getting requirements to build wheel ... error

  error: subprocess-exited-with-error



  × Getting requirements to build wheel did not run successfully.

  │ exit code: 1

  ╰─&gt; [1 lines of output]

      platform android is not supported

      [end of output]



  note: This error originates from a subprocess, and is likely not a problem with pip.

ERROR: Failed to build 'psutil' when getting requirements to build wheel

~ $ 


a58 = 
ভাই, errorটা `ipython` latest version-এর কারণে হয়েছে। Latest `ipython` → `psutil>=7` টানে, আর PyPI `psutil` Android support করে না।

আমরা `ipython`-এর stable older version pin করব, যেটা ManimGL-এর requirement পূরণ করে কিন্তু `psutil` টানে না।

## Command 26A — pure dependencies with pinned IPython

```bash
python -m pip install addict appdirs colour diskcache fonttools "ipython==8.37.0" pydub pygments PyOpenGL pyperclip pyyaml rich screeninfo svgelements sympy tqdm validators audioop-lts
```

শেষ হলে লিখবেন:

```text
done 26A
```

যদি error আসে, শেষের 20 লাইন পাঠাবেন। 


p59 = 
Building wheel for audioop-lts (pyproject.toml) ... done

  Created wheel for audioop-lts: filename=audioop_lts-0.2.2-cp313-abi3-android_24_arm64_v8a.whl size=66761 sha256=b4c397a56a8fd0e4fad9092b1fc35f1ce97bd15ba1dbef2e1cc37f7c717b31dc

  Stored in directory: /data/data/com.termux/files/home/.cache/pip/wheels/18/aa/af/9a81da45c94fe57529c31c753fecf810b8380ba58b6272766a

Successfully built pyyaml audioop-lts

Installing collected packages: svgelements, pyperclip, PyOpenGL, pydub, pure-eval, ptyprocess, mpmath, colour, appdirs, addict, wcwidth, validators, traitlets, tqdm, sympy, screeninfo, pyyaml, pygments, pexpect, parso, mdurl, fonttools, executing, diskcache, decorator, audioop-lts, asttokens, stack_data, prompt_toolkit, matplotlib-inline, markdown-it-py, jedi, rich, ipython

Successfully installed PyOpenGL-3.1.10 addict-2.4.0 appdirs-1.4.4 asttokens-3.0.2 audioop-lts-0.2.2 colour-0.1.5 decorator-5.3.1 diskcache-5.6.3 executing-2.2.1 fonttools-4.66.1 ipython-8.37.0 jedi-0.20.0 markdown-it-py-4.2.0 matplotlib-inline-0.2.2 mdurl-0.1.2 mpmath-1.3.0 parso-0.8.7 pexpect-4.9.0 prompt_toolkit-3.0.53 ptyprocess-0.7.0 pure-eval-0.2.4 pydub-0.25.1 pygments-2.21.0 pyperclip-1.11.0 pyyaml-6.0.3 rich-15.0.0 screeninfo-0.8.1 stack_data-0.6.3 svgelements-1.9.6 sympy-1.14.0 tqdm-4.70.1 traitlets-5.16.1 validators-0.35.0 wcwidth-0.9.1

~ $ 


a59 = 
দারুণ ভাই ✅ Pure Python dependencies install হয়ে গেছে।

এখন ManimGL-এর OpenGL/ModernGL dependency install করব।

## Command 27 — ModernGL + Pyglet dependencies

```bash
python -m pip install moderngl glcontext moderngl-window pyglet mapbox-earcut isosurfaces
```

শেষ হলে লিখবেন:

```text
done 27
```

যদি error আসে, শেষের 20 লাইন পাঠাবেন। 


p60 = 
━━━━━━━━━━━━━━━━━━━━━━━━ 1.0/1.0 MB 5.0 MB/s  0:00:00

Downloading isosurfaces-0.1.2-py3-none-any.whl (11 kB)

Building wheels for collected packages: moderngl, glcontext, pyglm, mapbox-earcut

  Building wheel for moderngl (pyproject.toml) ... done

  Created wheel for moderngl: filename=moderngl-5.12.0-cp314-cp314-android_24_arm64_v8a.whl size=273602 sha256=0247fca72050138e0a7dddb473dd9046e754e5856b2dee0f5b08c261934f448c

  Stored in directory: /data/data/com.termux/files/home/.cache/pip/wheels/ae/f7/05/d5828e23a0c31b14c40360bd98740b88e02f9042aca4320d99

  Building wheel for glcontext (pyproject.toml) ... done

  Created wheel for glcontext: filename=glcontext-3.0.0-cp314-cp314-android_24_arm64_v8a.whl size=35600 sha256=4ea5b08a9127c94977bd385428f7229e167aa59fd2f974b8bca088e7fd886878

  Stored in directory: /data/data/com.termux/files/home/.cache/pip/wheels/30/c2/09/a42f2605cc96193b38e494f4e05550ad395b3101fcd9254c94

  Building wheel for pyglm (pyproject.toml) ... /



time takes how much 


a60 =`pyglm` build হচ্ছে — এটা C++ extension, তাই Pixel 3a-তে একটু সময় নিতে পারে।

### কত সময় লাগতে পারে?
সাধারণত:

```text
5–20 মিনিট
```

কখনো বেশি হলেও 30 মিনিট পর্যন্ত যেতে পারে।

---

## এখন কী করবেন?

এখনই cancel করবেন না।  
আরও কিছুক্ষণ wait করুন।

যদি 20–30 মিনিটেও same জায়গায় থাকে, তখন `Ctrl+C` করবেন, তারপর আমরা `moderngl-window` বাদ দিয়ে minimal install করব। কারণ ManimGL headless render-এর জন্য অনেক সময় `moderngl-window/pyglm` strictly দরকার হয় না, কিন্তু package dependency হিসেবে টানছে।

---

## যদি আটকে যায়, fallback command হবে

এখন চালাবেন না — শুধু দরকার হলে:

```bash
python -m pip install moderngl glcontext pyglet mapbox-earcut isosurfaces
```

কিন্তু আগে current build শেষ হতে দিন। 






