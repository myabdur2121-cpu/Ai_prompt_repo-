# 🤖 AI TASK FILE — এটি ডকুমেন্টেশন নয়, কাজের নির্দেশ

> **এই ফাইলটি `.md` কেন?**
> আমার টুল থেকে `.py` ফাইল সরাসরি আপলোড করা যায় না, তাই সব পাইথন কোড
> এই একটি Markdown ফাইলের ভেতরে ব্লক আকারে রাখা হয়েছে।
>
> **তোমার কাজ:** নিচের ব্লকগুলো আলাদা করে নির্দিষ্ট পথে নির্দিষ্ট নামে
> ফাইল তৈরি/সম্পাদনা করা, তারপর রিপোতে commit ও push করা।

**Repository:** `myabdur2121-cpu/castom_manimlib`

---

## ⚠️ আগে পড়ো — গুরুত্বপূর্ণ নিয়ম

1. **কোড হুবহু কপি করবে।** কোনো লাইন "উন্নত", রিফ্যাক্টর, ফরম্যাট বা
   সংক্ষিপ্ত করার চেষ্টা করবে না। কোডটি পরীক্ষিত ও চালু অবস্থায় আছে।
2. **এই `text.md` ফাইলটি রিপোতে push করবে না।** এটি শুধু বাহক।
3. **`blur.py` কে `shapes.py` এর *পাশে* রাখবে**, ভেতরে নয় — দুটি একই
   ডিরেক্টরিতে ভাইবোন ফাইল হবে।
4. **`__init__.py` দুটি সম্পূর্ণ মুছে ফেলবে না** — `SmoothPolygon` অক্ষত
   রেখে শুধু নতুন নামগুলো যোগ করবে।
5. কোড ব্লকের বাইরের বাংলা ব্যাখ্যা কোডে ঢোকাবে না।

---

## 🎯 লক্ষ্য কাঠামো

```text
castom_manimlib/
├── my_manim_lib/
│   ├── __init__.py                 ← কাজ ৩ (সম্পাদনা)
│   └── manim_util/
│       ├── __init__.py             ← কাজ ২ (সম্পাদনা)
│       ├── shapes.py               ← অপরিবর্তিত
│       └── blur.py                 ← কাজ ১ (নতুন) ✅ shapes.py এর পাশে
├── examples/
│   ├── smooth_polygon_example.py   ← অপরিবর্তিত
│   └── blur_example.py             ← কাজ ৪ (নতুন)
├── requirements.txt                ← কাজ ৫ (যাচাই)
└── README.md                       ← কাজ ৬ (তোমার বিবেচনায়)
```

---

## 📋 কাজের তালিকা

| # | ধরন | পথ |
|---|---|---|
| ১ | নতুন ফাইল | `my_manim_lib/manim_util/blur.py` |
| ২ | সম্পাদনা | `my_manim_lib/manim_util/__init__.py` |
| ৩ | সম্পাদনা | `my_manim_lib/__init__.py` |
| ৪ | নতুন ফাইল | `examples/blur_example.py` |
| ৫ | যাচাই | `requirements.txt` |
| ৬ | পুনর্গঠন | `README.md` |

---

## 🧩 নতুন কোডটি কী

Manim এর জন্য একটি **Gaussian blur layer** সিস্টেম। পাঁচটি শ্রেণি:

| শ্রেণি | কাজ |
|---|---|
| `Blur(shape)` | প্রতি ফ্রেমে ব্লার — সত্যিকারের ব্লার-গ্লাস |
| `IMGBlur(shape)` | প্রথম ফ্রেমের ছবি জমিয়ে রাখে — স্থির |
| `BlurCard(...)` | ওয়েবসাইট-স্টাইল ভাসমান কাচের কার্ড (লাইভ) |
| `IMGBlurCard(...)` | একই কার্ড, স্থির |
| `CameraBlur(...)` | পুরো ক্যামেরা ফ্রেম — সবসময় লাইভ |

যেকোনো `VMobject` (Circle, Star, Polygon, Bézier, ফাঁপা শেপ) কে ইনপুট
হিসেবে নিতে পারে। ব্লার z_index দিয়ে নিয়ন্ত্রিত: Blur এর চেয়ে কম
z_index = ব্লার হবে, বেশি = শার্প থাকবে।

---

## ✅ কাজ ১ — নতুন ফাইল তৈরি করো

**পথ:** `my_manim_lib/manim_util/blur.py`

> এটি `shapes.py` এর **পাশে** থাকবে (একই ডিরেক্টরিতে), ভেতরে নয়।
> নিচের সম্পূর্ণ কোডটি হুবহু এই ফাইলে বসাও।

````python
"""
blur.py — Blur / IMGBlur for Manim Community v0.20.x
====================================================

    from manim import *
    from blur import *

    rec = Rectangle(width=6, height=3)
    glass = Blur(rec)              # rec এর ভেতরটা ব্লার-গ্লাস হয়ে গেল
    glass.set_z_index(1)
    self.add(glass)

    circle = Circle().set_z_index(0)          # কাচের নিচে
    self.play(circle.animate.shift(LEFT*4))   # ঝাপসা হয়ে পার হবে

-------------------------------------------------------------------------------
পাঁচটা ক্লাস
-------------------------------------------------------------------------------
``Blur(shape)``        প্রতি ফ্রেমে ব্লার — সত্যিকারের ব্লার-গ্লাস
``IMGBlur(shape)``     প্রথম ফ্রেমের ছবি জমিয়ে রাখে — স্থির
``BlurCard(...)``      Blur এর উপর ওয়েবসাইট-স্টাইল কার্ড
``IMGBlurCard(...)``   IMGBlur এর উপর একই কার্ড
``CameraBlur(...)``    পুরো ক্যামেরা ফ্রেম (লাইভ শুধু)

-------------------------------------------------------------------------------
কীভাবে কাজ করে
-------------------------------------------------------------------------------
Manim এর ``Camera.capture_mobjects()`` mobject গুলোকে z_index অনুসারে সাজিয়ে
একটার পর একটা একই RGBA buffer এ আঁকে। আমরা সেখানে হুক বসিয়েছি — তাই
Blur এর পালা এলে সে "এখন পর্যন্ত যা আঁকা হয়েছে" সেটা ব্লার করে।

শেপের ভেতর কোনটুকু, সেটা ঠিক করা হয় Cairo দিয়ে শেপের Bézier path আঁকিয়ে
একটা anti-aliased মাস্ক বানিয়ে। তাই Circle, Square, Star, Bézier — এমনকি
ফাঁপা শেপ (Annulus, "O" অক্ষর) — সবই ঠিকঠাক কাজ করে।
"""

from __future__ import annotations

__all__ = [
    "Blur",
    "IMGBlur",
    "BlurCard",
    "IMGBlurCard",
    "CameraBlur",
    "blur_config",
    "gaussian_blur_rgba",
    # পুরোনো API (আগের কোড যেন না ভাঙে)
    "BlurScene",
    "BlurCamera",
    "BlurMovingCamera",
    "BlurMovingCameraScene",
    "blur",
]

import itertools as it
from typing import Any, Iterable, Sequence

import cairo
import numpy as np
from PIL import Image, ImageFilter

from manim import (
    BLACK,
    ORIGIN,
    WHITE,
    Animation,
    Camera,
    Mobject,
    MovingCamera,
    MovingCameraScene,
    Rectangle,
    RoundedRectangle,
    Scene,
    VMobject,
    config,
)
from manim.utils.color import ManimColor

try:
    from scipy.ndimage import gaussian_filter as _scipy_gaussian_filter

    _HAS_SCIPY = True
except Exception:  # pragma: no cover
    _HAS_SCIPY = False


# =============================================================================
# GLOBAL CONFIG
# =============================================================================
class _BlurConfig:
    """সব blur এর global default।

    >>> blur_config.fast()          # দ্রুত preview
    >>> blur_config.enabled = False # সব blur বন্ধ
    """

    def __init__(self) -> None:
        self.default_blur: float = 20.0
        self.quality: str = "high"  # "high" | "fast"
        self.fast_downscale: int = 4
        self.padding_factor: float = 3.0
        self.enabled: bool = True

    def fast(self) -> "_BlurConfig":
        self.quality = "fast"
        return self

    def high(self) -> "_BlurConfig":
        self.quality = "high"
        return self

    # পুরোনো নাম
    @property
    def default_c(self) -> float:
        return self.default_blur

    @default_c.setter
    def default_c(self, v: float) -> None:
        self.default_blur = float(v)


blur_config = _BlurConfig()


# =============================================================================
# PIXEL MATH
# =============================================================================
def _gaussian_high(arr: np.ndarray, sigma: float) -> np.ndarray:
    """Premultiplied-alpha সহ exact Gaussian।

    Premultiply না করলে স্বচ্ছ পিক্সেলের অর্থহীন রঙ পাশের দৃশ্যমান পিক্সেলে
    চুইয়ে পড়ে কালো প্রান্ত তৈরি করে।
    """
    f = arr.astype(np.float32)
    rgb, alpha = f[..., :3], f[..., 3:4] / 255.0
    pre_b = _scipy_gaussian_filter(rgb * alpha, sigma=(sigma, sigma, 0), mode="nearest")
    a_b = _scipy_gaussian_filter(alpha, sigma=(sigma, sigma, 0), mode="nearest")
    out_rgb = np.where(a_b > 1e-6, pre_b / np.maximum(a_b, 1e-6), 0.0)
    out = np.concatenate([out_rgb, a_b * 255.0], axis=-1)
    return np.clip(out, 0, 255).astype(arr.dtype)


def _gaussian_fast(arr: np.ndarray, sigma: float, downscale: int) -> np.ndarray:
    """Downscale → blur → upscale. প্রায় একই দেখতে, অনেক দ্রুত।"""
    h, w = arr.shape[:2]
    d = max(1, int(downscale))
    sw, sh = max(1, w // d), max(1, h // d)
    small = Image.fromarray(arr, mode="RGBA").resize((sw, sh), Image.BILINEAR)
    small = small.filter(ImageFilter.GaussianBlur(radius=max(sigma / d, 0.1)))
    return np.asarray(small.resize((w, h), Image.BILINEAR), dtype=arr.dtype)


def gaussian_blur_rgba(
    arr: np.ndarray,
    sigma: float,
    quality: str | None = None,
    downscale: int | None = None,
) -> np.ndarray:
    """(H, W, 4) uint8 RGBA array কে Gaussian blur করে ফেরত দেয়।"""
    if sigma is None or sigma <= 0 or arr.size == 0:
        return arr
    quality = quality or blur_config.quality
    downscale = blur_config.fast_downscale if downscale is None else downscale
    if quality == "high" and _HAS_SCIPY:
        return _gaussian_high(arr, sigma)
    return _gaussian_fast(arr, sigma, downscale)


# =============================================================================
# SHAPE → PIXEL MASK  (এটাই পুরো সিস্টেমের ভিত্তি)
# =============================================================================
def _shape_mask(
    vmob: VMobject,
    camera: Camera,
    box: tuple[int, int, int, int],
    even_odd: bool = True,
) -> np.ndarray:
    """শেপের ভেতরটা কোথায়, তার (h, w, 1) float মাস্ক বানায়।

    Cairo দিয়ে শেপের Bézier path আঁকা হয়, তাই যেকোনো আকৃতি — বৃত্ত,
    তারা, হাতে বানানো Bézier, এমনকি ফাঁপা শেপ (Annulus, "O") — সবই
    নিখুঁত ও anti-aliased হয়।

    Parameters
    ----------
    box
        (x0, y0, x1, y1) পিক্সেল bounding box. শুধু ততটুকুই আঁকা হয়।
    even_odd
        ফাঁপা শেপ (ডোনাট, অক্ষরের ফুটো) ঠিকঠাক দেখাতে even-odd rule।
    """
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    if w <= 0 or h <= 0:
        return np.zeros((max(h, 0), max(w, 0), 1), dtype=np.float32)

    surface = cairo.ImageSurface(cairo.FORMAT_A8, w, h)
    ctx = cairo.Context(surface)

    drew = False
    for sub in vmob.family_members_with_points():
        if not isinstance(sub, VMobject):
            continue
        for subpath in sub.get_subpaths():
            quads = sub.gen_cubic_bezier_tuples_from_points(subpath)
            if len(quads) == 0:
                continue
            start = camera.points_to_subpixel_coords(sub, quads[0][0].reshape(1, 3))[0]
            ctx.new_sub_path()
            ctx.move_to(start[0] - x0, start[1] - y0)
            for _a, b, c, d in quads:
                p = camera.points_to_subpixel_coords(sub, np.array([b, c, d]))
                ctx.curve_to(
                    p[0][0] - x0, p[0][1] - y0,
                    p[1][0] - x0, p[1][1] - y0,
                    p[2][0] - x0, p[2][1] - y0,
                )
            ctx.close_path()
            drew = True

    if not drew:
        return np.zeros((h, w, 1), dtype=np.float32)

    ctx.set_fill_rule(
        cairo.FILL_RULE_EVEN_ODD if even_odd else cairo.FILL_RULE_WINDING
    )
    ctx.fill()
    surface.flush()

    buf = np.ndarray(
        shape=(h, surface.get_stride()), dtype=np.uint8, buffer=surface.get_data()
    )
    return (buf[:, :w].astype(np.float32) / 255.0)[..., None]


def _soften(mask: np.ndarray, feather: float) -> np.ndarray:
    """মাস্কের প্রান্ত আরও নরম করে (ঐচ্ছিক)।"""
    if feather <= 0:
        return mask
    if _HAS_SCIPY:
        return _scipy_gaussian_filter(mask, sigma=(feather, feather, 0), mode="nearest")
    img = Image.fromarray((mask[..., 0] * 255).astype(np.uint8), mode="L")
    img = img.filter(ImageFilter.GaussianBlur(radius=feather))
    return (np.asarray(img, dtype=np.float32) / 255.0)[..., None]


# =============================================================================
# BASE CLASS
# =============================================================================
class _BlurBase(VMobject):
    """``Blur`` ও ``IMGBlur`` এর সাধারণ ভিত্তি।

    এটা একটা সত্যিকারের ``VMobject`` — তাই ইনপুট শেপের stroke, fill, কোণা,
    সবকিছু কপি হয় এবং স্বাভাবিকভাবেই আঁকা হয়। শুধু বাড়তি কাজ: আঁকার আগে
    শেপের ভেতরের পিক্সেলগুলো ব্লার করে দেয়।

    সাবক্লাস শুধু :meth:`_source_pixels` বদলায়:

    * :class:`Blur`    → এই ফ্রেমের বর্তমান pixel_array
    * :class:`IMGBlur` → প্রথমবার জমানো স্ন্যাপশট
    """

    def __init__(
        self,
        shape: VMobject | float | None = None,
        blur: float | None = None,
        *,
        c: float | None = None,
        amount: float | None = None,
        intensity: float = 1.0,
        feather: float = 0.0,
        tint: Any = None,
        tint_opacity: float = 0.0,
        copy_style: bool = True,
        quality: str | None = None,
        downscale: int | None = None,
        even_odd: bool = True,
        z_index: float | None = None,
        **kwargs: Any,
    ) -> None:
        # ---- পুরোনো API: Blur(25) মানে সংখ্যা প্রথমে ----
        if isinstance(shape, (int, float)) and shape is not None:
            blur = float(shape) if blur is None else blur
            shape = None

        # blur / c / amount — তিনটাই চলে
        for alt in (c, amount):
            if blur is None and alt is not None:
                blur = alt
        self.blur_amount = blur if blur is not None else blur_config.default_blur

        self.intensity = float(intensity)
        self.mask_feather = float(feather)
        self.tint = ManimColor(tint) if tint is not None else None
        self.tint_opacity = float(tint_opacity)
        self.quality = quality
        self.downscale = downscale
        self.even_odd = bool(even_odd)
        self.enabled = True
        self._mask_cache: tuple[Any, np.ndarray] | None = None

        # ---- শেপ ----
        style_kwargs: dict[str, Any] = {}
        if shape is None:
            shape = self._default_shape(**kwargs)
        elif copy_style:
            # ইনপুট শেপের stroke কপি করি।
            # fill ইচ্ছাকৃতভাবে বাদ: কাচের ভেতরটা ভরাট থাকলে ব্লারই ঢেকে যায়।
            # ভরাট চাইলে fill_opacity=... স্পষ্ট করে দিতে হবে।
            src = shape
            style_kwargs = dict(
                stroke_color=src.get_stroke_color(),
                stroke_width=src.get_stroke_width(),
                stroke_opacity=src.get_stroke_opacity(),
                fill_color=src.get_fill_color(),
                fill_opacity=0.0,
            )

        vm_kwargs = {k: v for k, v in kwargs.items() if k not in _SHAPE_ONLY_KEYS}
        super().__init__(**{**style_kwargs, **vm_kwargs})

        # শেপের জ্যামিতি কপি করি (ইনপুট mobject অক্ষত থাকে)
        self.match_shape(shape)

        # fade হিসাবের জন্য মূল opacity মনে রাখি
        try:
            self._base_stroke_opacity = float(self.get_stroke_opacity())
            self._base_fill_opacity = float(self.get_fill_opacity())
        except Exception:
            self._base_stroke_opacity = None
            self._base_fill_opacity = None

        if z_index is not None:
            self.set_z_index(z_index)

    # ------------------------------------------------------------------
    def _default_shape(self, **kwargs: Any) -> VMobject:
        """শেপ না দিলে কী হবে — সাবক্লাস override করে।"""
        return Rectangle(
            width=kwargs.pop("width", config.frame_width),
            height=kwargs.pop("height", config.frame_height),
            stroke_width=0,
        )

    def match_shape(self, shape: VMobject) -> "_BlurBase":
        """অন্য একটা শেপের জ্যামিতি নিয়ে নেয় (স্টাইল বদলায় না)।"""
        self.set_points(shape.get_points().copy())
        self.submobjects = [s.copy() for s in shape.submobjects]
        for s in self.submobjects:
            s.set_opacity(0)  # সাবশেপগুলো শুধু মাস্কের জন্য, আঁকা হবে না
        self._mask_cache = None
        return self

    # =====================================================================
    # প্যারামিটার
    # =====================================================================
    def set_blur(self, v: float) -> "_BlurBase":
        self.blur_amount = float(v)
        return self

    def get_blur(self) -> float:
        return self.blur_amount

    set_c = set_blur
    get_c = get_blur

    def set_intensity(self, v: float) -> "_BlurBase":
        self.intensity = float(np.clip(v, 0.0, 1.0))
        return self

    def set_tint(self, color: Any, opacity: float | None = None) -> "_BlurBase":
        self.tint = ManimColor(color) if color is not None else None
        if opacity is not None:
            self.tint_opacity = float(opacity)
        return self

    def set_tint_opacity(self, v: float) -> "_BlurBase":
        self.tint_opacity = float(v)
        return self

    def set_feather(self, v: float) -> "_BlurBase":
        self.mask_feather = float(v)
        return self

    def enable(self) -> "_BlurBase":
        self.enabled = True
        return self

    def disable(self) -> "_BlurBase":
        self.enabled = False
        return self

    # ------------------------------------------------- অ্যানিমেশন হেল্পার
    def fade_in(self, run_time: float = 1.2, **kw: Any) -> Animation:
        """0 → বর্তমান মান পর্যন্ত ব্লার আনে।"""
        target = self.blur_amount
        self.set_blur(0)
        return self.animate(run_time=run_time, **kw).set_blur(target).build()

    def fade_out(self, run_time: float = 1.2, **kw: Any) -> Animation:
        return self.animate(run_time=run_time, **kw).set_blur(0).build()

    def to(self, v: float, run_time: float = 1.2, **kw: Any) -> Animation:
        return self.animate(run_time=run_time, **kw).set_blur(v).build()

    # ------------------------------------------- Transform / .animate
    def interpolate_color(self, m1: "_BlurBase", m2: "_BlurBase", alpha: float):
        super().interpolate_color(m1, m2, alpha)
        lerp = lambda a, b: float(a + (b - a) * alpha)
        self.blur_amount = lerp(m1.blur_amount, m2.blur_amount)
        self.intensity = lerp(m1.intensity, m2.intensity)
        self.mask_feather = lerp(m1.mask_feather, m2.mask_feather)
        self.tint_opacity = lerp(m1.tint_opacity, m2.tint_opacity)
        self.tint = m2.tint if alpha > 0.5 else m1.tint
        self.enabled = m2.enabled if alpha > 0.5 else m1.enabled
        return self

    # =====================================================================
    # রেন্ডারিং
    # =====================================================================
    def _source_pixels(self, camera: Camera, pixel_array: np.ndarray) -> np.ndarray:
        """কোন পিক্সেলগুলো ব্লার করা হবে — সাবক্লাস ঠিক করে।"""
        raise NotImplementedError

    def apply_to_pixel_array(self, camera: Camera, pixel_array: np.ndarray) -> None:
        """Camera এটা ডাকে, ঠিক এই mobject এর z_index এর সময়।"""
        if not (self.enabled and blur_config.enabled):
            return

        # FadeIn / FadeOut কাজ করানোর জন্য: mobject এর opacity কমলে
        # ব্লারের জোরও সেই অনুপাতে কমে। (fade_alpha = 1 হলে কোনো প্রভাব নেই)
        fade = self._fade_alpha()
        if fade <= 0.0:
            return

        sigma = max(0.0, self.blur_amount * camera.pixel_width / 1920.0)
        if sigma <= 0 and self.tint_opacity <= 0:
            return

        H, W = pixel_array.shape[:2]
        box = self._pixel_box(camera, W, H)
        if box is None:
            return
        x0, y0, x1, y1 = box

        source = self._source_pixels(camera, pixel_array)
        if source is None or source.shape[:2] != pixel_array.shape[:2]:
            source = pixel_array

        # region এর বাইরে থেকে কিছু পিক্সেল "ধার" নিই, নাহলে প্রান্তে halo
        pad = int(np.ceil(sigma * blur_config.padding_factor)) + 1
        px0, py0 = max(0, x0 - pad), max(0, y0 - pad)
        px1, py1 = min(W, x1 + pad), min(H, y1 + pad)

        blurred = gaussian_blur_rgba(
            source[py0:py1, px0:px1], sigma, self.quality, self.downscale
        )

        if self.tint is not None and self.tint_opacity > 0:
            t = np.array(self.tint.to_rgb(), dtype=np.float32) * 255.0
            k = float(np.clip(self.tint_opacity, 0.0, 1.0))
            b = blurred.astype(np.float32)
            b[..., :3] = b[..., :3] * (1 - k) + t[None, None, :] * k
            blurred = np.clip(b, 0, 255).astype(pixel_array.dtype)

        ox0, oy0 = x0 - px0, y0 - py0
        src = blurred[oy0 : oy0 + (y1 - y0), ox0 : ox0 + (x1 - x0)].astype(np.float32)
        dst = pixel_array[y0:y1, x0:x1].astype(np.float32)
        if src.shape != dst.shape:
            return

        mask = self._get_mask(camera, (x0, y0, x1, y1))
        if mask.shape[:2] != dst.shape[:2]:
            return
        mask = mask * float(np.clip(self.intensity, 0.0, 1.0)) * fade

        pixel_array[y0:y1, x0:x1] = np.clip(
            dst * (1.0 - mask) + src * mask, 0, 255
        ).astype(pixel_array.dtype)

    # ------------------------------------------------------------ helpers
    def _fade_alpha(self) -> float:
        """``FadeIn``/``FadeOut`` এর সময় ব্লারও যেন মিলিয়ে যায়।

        Manim এর fade animation গুলো stroke/fill opacity বদলায়। আমরা
        সেটাকে ব্লারের জোরের গুণক হিসেবে ব্যবহার করি। শেপে stroke বা fill
        কিছুই না থাকলে (খালি কাচ) fade ধরা যায় না, তাই 1.0 ফেরত দিই।
        """
        a = getattr(self, "_blur_fade", None)
        if a is not None:
            return float(np.clip(a, 0.0, 1.0))
        try:
            so = float(self.get_stroke_opacity())
            fo = float(self.get_fill_opacity())
        except Exception:
            return 1.0
        base_s = getattr(self, "_base_stroke_opacity", None)
        base_f = getattr(self, "_base_fill_opacity", None)
        if base_s is None and base_f is None:
            return 1.0
        vals = []
        if base_s:
            vals.append(so / base_s)
        if base_f:
            vals.append(fo / base_f)
        return float(np.clip(max(vals) if vals else 1.0, 0.0, 1.0))

    def set_blur_fade(self, a: float) -> "_BlurBase":
        """ব্লারের দৃশ্যমানতা সরাসরি 0..1 এ সেট করে।"""
        self._blur_fade = float(np.clip(a, 0.0, 1.0))
        return self

    def _get_mask(self, camera: Camera, box: tuple[int, int, int, int]) -> np.ndarray:
        """শেপের মাস্ক (একই অবস্থানে থাকলে ক্যাশ থেকে)।"""
        key = (box, self.mask_feather, self.even_odd,
               round(float(np.sum(self.get_points())), 4))
        if self._mask_cache is not None and self._mask_cache[0] == key:
            return self._mask_cache[1]
        mask = _shape_mask(self, camera, box, self.even_odd)
        mask = _soften(mask, self.mask_feather)
        self._mask_cache = (key, mask)
        return mask

    def _pixel_box(
        self, camera: Camera, W: int, H: int
    ) -> tuple[int, int, int, int] | None:
        pts = self.get_all_points()
        if len(pts) == 0:
            return None
        p = camera.points_to_pixel_coords(self, pts)
        x0 = max(0, int(np.floor(p[:, 0].min())) - 1)
        y0 = max(0, int(np.floor(p[:, 1].min())) - 1)
        x1 = min(W, int(np.ceil(p[:, 0].max())) + 1)
        y1 = min(H, int(np.ceil(p[:, 1].max())) + 1)
        if x1 <= x0 or y1 <= y0:
            return None
        return x0, y0, x1, y1


_SHAPE_ONLY_KEYS = {"width", "height", "corner_radius", "side_length", "radius"}


# =============================================================================
# ১. Blur — প্রতি ফ্রেমে (সত্যিকারের ব্লার-গ্লাস)
# =============================================================================
class Blur(_BlurBase):
    """প্রতিটা ফ্রেমে শেপের ভেতরটা ব্লার করে — সত্যিকারের ব্লার-গ্লাস।

    Parameters
    ----------
    shape
        যেকোনো ``VMobject`` — Circle, Square, Rectangle, Star, Polygon,
        হাতে বানানো Bézier, এমনকি ফাঁপা শেপ। শুধু জ্যামিতি ও স্টাইল কপি
        হয়; **ইনপুট mobject অক্ষত থাকে এবং তার z_index আলাদা**।
        কিছু না দিলে পুরো ফ্রেম।
    blur
        ব্লারের পরিমাণ। ``c=`` বা ``amount=`` নামেও দেওয়া যায়।
        1920px ফ্রেমের সাপেক্ষে normalize করা, তাই ``-ql`` আর ``-qh``
        তে একই রকম দেখায়।
    intensity
        0..1 — ব্লার আর আসল ছবির মিশ্রণ।
    feather
        মাস্কের প্রান্ত কত পিক্সেল নরম হবে।
    tint, tint_opacity
        ব্লারের উপর রঙের প্রলেপ।
    copy_style
        ইনপুট শেপের stroke/fill কপি হবে কিনা (ডিফল্ট ``True``)।

    Examples
    --------
    ::

        rec = Rectangle(width=6, height=3)
        glass = Blur(rec)
        glass.set_z_index(1)
        self.add(glass)

        circle = Circle().set_z_index(0)
        self.play(circle.animate.shift(LEFT * 4))   # ঝাপসা হয়ে পার হবে
        self.play(glass.animate.shift(UP))          # কাচ নিজেও নড়ে
    """

    def _source_pixels(self, camera: Camera, pixel_array: np.ndarray) -> np.ndarray:
        return pixel_array  # এখনকার ফ্রেম — তাই লাইভ


# =============================================================================
# ২. IMGBlur — স্ন্যাপশট (স্থির)
# =============================================================================
class IMGBlur(_BlurBase):
    """প্রথম ফ্রেমের ছবি জমিয়ে রাখে — কাচ নড়লেও ভেতরের ছবি বদলায় না।

    ``Blur`` এর সাথে পার্থক্য একটাই: এটা প্রতি ফ্রেমে নতুন করে ব্লার হিসাব
    করে না। প্রথমবার রেন্ডার হওয়ার মুহূর্তে পর্দার ছবিটা ভেতরে সংরক্ষণ করে,
    তারপর সবসময় সেটাই ব্যবহার করে।

    ফলে নিচের জিনিস নড়াচড়া করলেও ভেতরের ছবি স্থির থাকে — তুমি যেমন
    বলেছিলে, *"এর নির্দেশে কী হচ্ছে এটা জানে না।"*

    ছবিটা **পর্দার সাপেক্ষে স্থির** থাকে (দেয়ালে আঁকা ছবির উপর জানালা
    সরানোর মতো)। কাচের সাথে ছবিও নড়াতে চাইলে ``frozen_content=True``।

    Parameters
    ----------
    frozen_content
        ``False`` (ডিফল্ট) → ছবি পর্দায় স্থির।
        ``True`` → ছবিটা কাচের সাথে সরে (ফটোফ্রেমের মতো)।

    Examples
    --------
    ::

        glass = IMGBlur(rec)
        self.add(glass)
        self.play(glass.animate.shift(LEFT * 3))   # ভেতরের ছবি বদলাবে না
        glass.recapture()                          # নতুন করে ছবি নাও
    """

    def __init__(self, *args: Any, frozen_content: bool = False, **kwargs: Any) -> None:
        self._snapshot: np.ndarray | None = None
        self._snapshot_center: np.ndarray | None = None
        self.frozen_content = bool(frozen_content)
        super().__init__(*args, **kwargs)

    # ------------------------------------------------------------------
    def recapture(self) -> "IMGBlur":
        """পরের ফ্রেমে নতুন করে স্ন্যাপশট নেবে।"""
        self._snapshot = None
        self._snapshot_center = None
        return self

    capture = recapture

    def has_snapshot(self) -> bool:
        return self._snapshot is not None

    # ------------------------------------------------------------------
    def _source_pixels(self, camera: Camera, pixel_array: np.ndarray) -> np.ndarray:
        if self._snapshot is None or self._snapshot.shape != pixel_array.shape:
            # প্রথমবার — এখনকার পর্দাটা জমিয়ে রাখি
            self._snapshot = pixel_array.copy()
            self._snapshot_center = self.get_center().copy()

        if not self.frozen_content:
            return self._snapshot  # পর্দায় স্থির

        # frozen_content: কাচ যতটা সরেছে, ছবিটাও ততটা সরাই
        shift = self.get_center() - self._snapshot_center
        if np.allclose(shift, 0):
            return self._snapshot
        dx = int(round(shift[0] * camera.pixel_width / camera.frame_width))
        dy = int(round(-shift[1] * camera.pixel_height / camera.frame_height))
        return np.roll(self._snapshot, (dy, dx), axis=(0, 1))


# =============================================================================
# ৩. CameraBlur — পুরো ফ্রেম (লাইভ শুধু)
# =============================================================================
class CameraBlur(Blur):
    """ক্যামেরা যতটুকু দেখছে, ঠিক ততটুকু ব্লার করে।

    ক্যামেরা zoom বা pan করলে নিজে থেকে মানিয়ে নেয়।
    তোমার নির্দেশ মতো এর কোনো ``IMG`` সংস্করণ নেই — সবসময় লাইভ।

    Examples
    --------
    ::

        self.add(CameraBlur(30))
        self.add(title)              # এটা শার্প থাকবে
    """

    def __init__(self, blur: float | None = None, **kwargs: Any) -> None:
        kwargs.setdefault("stroke_width", 0)
        kwargs.setdefault("fill_opacity", 0)
        super().__init__(None, blur, **kwargs)
        self._follow_camera = True

    def _pixel_box(self, camera: Camera, W: int, H: int):
        return 0, 0, W, H

    def _get_mask(self, camera: Camera, box: tuple[int, int, int, int]) -> np.ndarray:
        # পুরো ফ্রেম — মাস্ক আঁকার দরকারই নেই
        h, w = box[3] - box[1], box[2] - box[0]
        return np.ones((h, w, 1), dtype=np.float32)


# =============================================================================
# ৪ ও ৫. কার্ড — ওয়েবসাইটের floating glass board
# =============================================================================
def _card_shape(
    width: float, height: float, corner_radius: float, **style: Any
) -> VMobject:
    if corner_radius and corner_radius > 0:
        return RoundedRectangle(
            corner_radius=corner_radius, width=width, height=height, **style
        )
    return Rectangle(width=width, height=height, **style)


class _CardMixin:
    """``BlurCard`` ও ``IMGBlurCard`` এর সাধারণ চেহারা।"""

    def __init__(
        self,
        shape: VMobject | float | None = None,
        blur: float | None = None,
        *,
        width: float = 8.0,
        height: float = 4.5,
        corner_radius: float = 0.45,
        tint: Any = WHITE,
        tint_opacity: float = 0.18,
        border_color: Any = WHITE,
        border_width: float = 2.5,
        border_opacity: float = 0.55,
        match_size: bool = False,
        **kwargs: Any,
    ) -> None:
        """কার্ড — ডিফল্টে গোল-কোণা আয়তক্ষেত্র, তবে যেকোনো আকৃতি দেওয়া যায়।

        Parameters
        ----------
        shape
            ঐচ্ছিক ``VMobject`` — Star, Circle, Polygon, Bézier যা খুশি।
            কিছু না দিলে ``width``/``height``/``corner_radius`` দিয়ে
            গোল-কোণা আয়তক্ষেত্র বানানো হয়।
            সংখ্যা দিলে সেটাকে ``blur`` ধরা হয় (যেমন ``BlurCard(35)``)।
        match_size
            ``True`` দিলে দেওয়া শেপটাকে ``width``×``height`` মাপে
            টেনে বসানো হয়। ডিফল্ট ``False`` — শেপের নিজের মাপ থাকে।
        """
        # BlurCard(35) — সংখ্যা প্রথমে দিলে সেটা blur
        if isinstance(shape, (int, float)):
            blur = float(shape) if blur is None else blur
            shape = None

        if shape is None:
            shape = _card_shape(width, height, corner_radius)
        else:
            shape = shape.copy()
            if match_size:
                shape.stretch_to_fit_width(width).stretch_to_fit_height(height)

        # কার্ডের নিজস্ব বর্ডার-স্টাইল সব সময় প্রয়োগ হয়
        shape.set_stroke(
            color=ManimColor(border_color),
            width=border_width,
            opacity=border_opacity,
        )
        shape.set_fill(opacity=0)

        kwargs.setdefault("feather", 1.2)  # প্রান্ত একটু নরম
        super().__init__(
            shape,
            blur if blur is not None else 30.0,
            tint=tint,
            tint_opacity=tint_opacity,
            **kwargs,
        )

    # সুবিধার জন্য
    def set_border(
        self, color: Any = None, width: float | None = None,
        opacity: float | None = None,
    ):
        if color is not None:
            self.set_stroke(color=ManimColor(color))
        if width is not None:
            self.set_stroke(width=width)
        if opacity is not None:
            self.set_stroke(opacity=opacity)
        return self


class BlurCard(_CardMixin, Blur):
    """ওয়েবসাইট-স্টাইল ভাসমান কাচের কার্ড — **লাইভ** ব্লার।

    Examples
    --------
    ::

        card = BlurCard(width=8, height=4.5)
        card.set_z_index(1)
        self.add(card)
        self.add(Text("Hello").set_z_index(2))
    """


class IMGBlurCard(_CardMixin, IMGBlur):
    """একই কার্ড, কিন্তু **স্থির** (স্ন্যাপশট) ব্লার।"""


# =============================================================================
# CAMERA HOOK — একবার patch, সব Scene এ কাজ করে
# =============================================================================
def _install() -> None:
    """``Camera.capture_mobjects`` কে blur-সচেতন করে।

    সব Camera সাবক্লাস শেষমেশ ``Camera.capture_mobjects`` ডাকে, তাই
    একবার patch করলেই ``Scene``, ``MovingCameraScene``, ``ThreeDScene``
    সবখানে কাজ করে।
    """
    if getattr(Camera, "_blur_installed", False):
        return

    original = Camera.capture_mobjects

    def capture_mobjects(self, mobjects: Iterable[Mobject], **kwargs: Any) -> None:
        mobs = self.get_mobjects_to_display(mobjects, **kwargs)
        if not any(isinstance(m, _BlurBase) for m in mobs):
            return original(self, mobjects, **kwargs)

        def kind(m: Mobject) -> Any:
            return "blur" if isinstance(m, _BlurBase) else self.type_or_raise(m)

        for group_type, group in it.groupby(mobs, kind):
            batch = list(group)
            if group_type == "blur":
                for b in batch:
                    # ১) আগে ভেতরটা ব্লার করি
                    b.apply_to_pixel_array(self, self.pixel_array)
                    # ২) তারপর শেপের নিজের stroke/fill আঁকি
                    if b.get_stroke_width() > 0 or b.get_fill_opacity() > 0:
                        self.display_multiple_vectorized_mobjects(
                            [b], self.pixel_array
                        )
            else:
                self.display_funcs[group_type](batch, self.pixel_array)

    Camera.capture_mobjects = capture_mobjects
    Camera._blur_installed = True


_install()


# =============================================================================
# পুরোনো API (আগের কোড যেন না ভাঙে)
# =============================================================================
def blur(c: float | None = None, **kw: Any) -> Blur:
    """পুরোনো সংক্ষিপ্ত রূপ: ``blur(25)``।"""
    return Blur(None, c, **kw)


def _legacy_on(cls):
    """পুরোনো ``Blur(25, on=card)`` সমর্থন।"""
    orig_init = cls.__init__

    def __init__(self, *args: Any, on: Mobject | None = None,
                 buff: float = 0.0, at: Sequence[float] | None = None,
                 width: float | None = None, height: float | None = None,
                 radius: float | None = None, **kw: Any) -> None:
        shape = None
        if on is not None:
            shape = _card_shape(
                on.width + 2 * buff, on.height + 2 * buff,
                (radius or 0) / 100.0, stroke_width=0, fill_opacity=0,
            )
            shape.move_to(on.get_center())
        elif width is not None or height is not None:
            shape = _card_shape(
                width if width is not None else config.frame_width,
                height if height is not None else config.frame_height,
                (radius or 0) / 100.0, stroke_width=0, fill_opacity=0,
            )
        if shape is not None:
            if at is not None:
                shape.move_to(at)
            args = (shape,) + args[1:] if args and not isinstance(
                args[0], VMobject
            ) else (shape,) + args
            if len(args) > 1 and isinstance(args[1], VMobject):
                args = (shape,) + args[2:]
        orig_init(self, *args, **kw)
        if on is not None:
            self._legacy_target = on
            self._legacy_buff = buff

    cls.__init__ = __init__
    return cls


# পুরোনো প্রিসেট
def _preset(cls):
    @classmethod
    def glass(c, blur_amount: float = 30, **kw: Any):
        kw.setdefault("tint", WHITE)
        kw.setdefault("tint_opacity", 0.22)
        kw.setdefault("feather", 1.2)
        return c(kw.pop("shape", None), blur_amount, **kw)

    @classmethod
    def dark(c, blur_amount: float = 25, **kw: Any):
        kw.setdefault("tint", BLACK)
        kw.setdefault("tint_opacity", 0.45)
        return c(kw.pop("shape", None), blur_amount, **kw)

    @classmethod
    def subtle(c, blur_amount: float = 8, **kw: Any):
        return c(kw.pop("shape", None), blur_amount, **kw)

    @classmethod
    def heavy(c, blur_amount: float = 55, **kw: Any):
        return c(kw.pop("shape", None), blur_amount, **kw)

    cls.glass = glass
    cls.dark = dark
    cls.subtle = subtle
    cls.heavy = heavy
    return cls


_preset(Blur)
_preset(IMGBlur)



BlurCamera = Camera
BlurMovingCamera = MovingCamera


class BlurScene(Scene):
    """আর দরকার নেই — সাধারণ ``Scene`` এ blur কাজ করে।"""


class BlurMovingCameraScene(MovingCameraScene):
    """আর দরকার নেই — সাধারণ ``MovingCameraScene`` ই যথেষ্ট।"""
````

---

## ✅ কাজ ২ — সম্পাদনা করো

**পথ:** `my_manim_lib/manim_util/__init__.py`

**বর্তমান অবস্থা:**

```python
from .shapes import SmoothPolygon

__all__ = ["SmoothPolygon"]
```

**করণীয়:** `SmoothPolygon` রেখে দিয়ে নতুন নামগুলো যোগ করো। ফলাফল হবে:

````python
from .shapes import SmoothPolygon
from .blur import (
    Blur,
    IMGBlur,
    BlurCard,
    IMGBlurCard,
    CameraBlur,
    blur_config,
    gaussian_blur_rgba,
)

__all__ = [
    "SmoothPolygon",
    "Blur",
    "IMGBlur",
    "BlurCard",
    "IMGBlurCard",
    "CameraBlur",
    "blur_config",
    "gaussian_blur_rgba",
]
````

---

## ✅ কাজ ৩ — সম্পাদনা করো

**পথ:** `my_manim_lib/__init__.py`

**বর্তমান অবস্থা:**

```python
from .manim_util import SmoothPolygon

__all__ = ["SmoothPolygon"]
```

**করণীয়:** এখানেও `SmoothPolygon` রেখে নতুন নামগুলো যোগ করো:

````python
from .manim_util import (
    SmoothPolygon,
    Blur,
    IMGBlur,
    BlurCard,
    IMGBlurCard,
    CameraBlur,
    blur_config,
    gaussian_blur_rgba,
)

__all__ = [
    "SmoothPolygon",
    "Blur",
    "IMGBlur",
    "BlurCard",
    "IMGBlurCard",
    "CameraBlur",
    "blur_config",
    "gaussian_blur_rgba",
]
````

> এরপর ব্যবহারকারী লিখতে পারবে:
> `from my_manim_lib import Blur, IMGBlur, BlurCard, CameraBlur`

---

## ✅ কাজ ৪ — নতুন ফাইল তৈরি করো

**পথ:** `examples/blur_example.py`

````python
"""
blur_example.py — Blur / IMGBlur ব্যবহারের ছোট উদাহরণ।

Run::

    manim -pql examples/blur_example.py GlassDoor
    manim -pql examples/blur_example.py Snapshot
    manim -pql examples/blur_example.py ShapeCards
"""

from manim import *

from my_manim_lib import Blur, BlurCard, CameraBlur, IMGBlur


def scenery():
    """রঙিন পটভূমি — ব্লার কতটা হচ্ছে চোখে দেখার জন্য।"""
    return VGroup(*[
        Circle(radius=1.4, fill_opacity=1, stroke_width=0, color=c).shift(RIGHT * x)
        for x, c in zip([-5, -2.5, 0, 2.5, 5], [RED, GREEN, BLUE, YELLOW, PURPLE])
    ])


class GlassDoor(Scene):
    """ব্লার-গ্লাসের দরজার পাশ দিয়ে কেউ হেঁটে যাচ্ছে।"""

    def construct(self):
        rec = Rectangle(width=5, height=5.4, stroke_color=WHITE, stroke_width=4)
        glass = Blur(rec, 30)          # প্রতি ফ্রেমে ব্লার
        glass.set_z_index(1)
        self.add(glass)

        person = VGroup(
            Circle(radius=0.42, fill_opacity=1, stroke_width=0, color=RED),
            RoundedRectangle(corner_radius=0.25, width=1.1, height=2.0,
                             fill_opacity=1, stroke_width=0, color=RED),
        ).arrange(DOWN, buff=0.08).move_to(LEFT * 7).set_z_index(0)
        self.add(person)

        self.play(person.animate.move_to(RIGHT * 7), run_time=3.5, rate_func=linear)


class Snapshot(Scene):
    """IMGBlur — কাচ কিছুই টের পায় না।"""

    def construct(self):
        mover = Circle(radius=1.1, fill_opacity=1, stroke_width=0,
                       color=RED).shift(LEFT * 6).set_z_index(0)
        self.add(mover)

        rec = Rectangle(width=5, height=3.4, stroke_color=WHITE, stroke_width=4)
        self.add(IMGBlur(rec, 28).set_z_index(1))

        self.play(mover.animate.shift(RIGHT * 12), run_time=3, rate_func=linear)


class AnyShape(Scene):
    """যেকোনো আকৃতি — ফাঁপা শেপ সহ।"""

    def construct(self):
        self.add(scenery())
        shapes = [
            Circle(radius=1.4, stroke_color=WHITE, stroke_width=4),
            Star(7, outer_radius=1.7, stroke_color=YELLOW, stroke_width=4),
            Annulus(inner_radius=0.7, outer_radius=1.6, stroke_width=0),
        ]
        for i, sh in enumerate(shapes):
            self.add(Blur(sh, 28).move_to([-4.4 + i * 4.4, 0, 0]).set_z_index(1))
        self.wait(2)


class ShapeCards(Scene):
    """যেকোনো আকৃতির রঙিন কার্ড।"""

    def construct(self):
        self.add(scenery())

        cards = [
            BlurCard(Star(7, outer_radius=1.7), tint=GREEN, tint_opacity=0.35,
                     border_color=GREEN, border_width=5).shift(LEFT * 4.6 + UP * 1.5),
            BlurCard(Circle(radius=1.6), tint=BLUE, tint_opacity=0.4,
                     border_color=WHITE, border_width=5).shift(UP * 1.5),
            BlurCard(RegularPolygon(6).scale(1.7), tint=ORANGE, tint_opacity=0.4,
                     border_color=ORANGE, border_width=5).shift(RIGHT * 4.6 + UP * 1.5),
            BlurCard(width=4.2, height=2.4, tint=PURPLE, tint_opacity=0.4,
                     border_color=PURPLE, border_width=5).shift(LEFT * 3.4 + DOWN * 1.9),
            BlurCard(Triangle().scale(1.9), tint=RED, tint_opacity=0.35,
                     border_color=RED, border_width=5).shift(RIGHT * 3.4 + DOWN * 1.9),
        ]
        for c in cards:
            c.set_z_index(1)
            self.add(c)
        self.wait(2)


class WholeScreen(Scene):
    """পুরো ফ্রেম ব্লার।"""

    def construct(self):
        self.add(scenery())
        veil = CameraBlur(0)
        veil.set_z_index(1)
        self.add(veil)
        self.add(Text("Sharp Title", font_size=52, weight=BOLD).set_z_index(2))
        self.play(veil.to(32), run_time=2)
        self.wait(1)
````

---

## ✅ কাজ ৫ — `requirements.txt` যাচাই করো

`blur.py` এর জন্য দরকার:

- `manim` (আগে থেকেই আছে)
- `numpy` (manim এর সাথে আসে)
- `pillow` (manim এর সাথে আসে)
- `pycairo` (manim এর সাথে আসে — শেপ মাস্ক আঁকতে ব্যবহৃত)
- **`scipy`** — উচ্চ মানের Gaussian blur এর জন্য

**করণীয়:** `requirements.txt` এ `scipy` না থাকলে যোগ করো।

> নোট: `scipy` না থাকলেও কোড চলবে (Pillow দিয়ে fallback আছে), তবে
> ব্লারের মান কিছুটা কম হবে। তাই এটি যোগ করা বাঞ্ছনীয়।

---

## ✅ কাজ ৬ — `README.md` পুনর্গঠন করো (তোমার বিবেচনায়)

**পরিস্থিতি:** বর্তমান README পুরোটাই একটিমাত্র শ্রেণি `SmoothPolygon`
ধরে সাজানো — Features, Usage, Project Structure, Run an example, সবই।
তখন রিপোতে একটিই জিনিস ছিল বলে সেটাই যুক্তিসঙ্গত ছিল।

**এখন** রিপোতে দুটি আলাদা মডিউল হলো: `shapes.py` (SmoothPolygon) এবং
`blur.py` (পাঁচটি blur শ্রেণি)। ভবিষ্যতে আরও যোগ হবে।

**করণীয়:** README কে এমনভাবে পুনর্গঠন করো যাতে এটি **একাধিক মডিউল**
ধরতে পারে। কী রাখবে, কী মুছবে, কীভাবে সাজাবে — **সিদ্ধান্ত তোমার**।
এক শ্রেণির জন্য যেসব অংশ অতিরিক্ত বিস্তারিত মনে হয়, সংক্ষিপ্ত করতে পারো।

**শুধু দুটি শর্ত:**

1. `SmoothPolygon` সম্পর্কিত তথ্য হারিয়ে যাবে না।
2. Project Structure অংশে নতুন `blur.py` ও `blur_example.py` দেখাবে।

সহায়ক তথ্য (তোমার প্রয়োজনমতো ব্যবহার করো):

- **কী:** Manim এর জন্য z_index-সচেতন Gaussian blur layer
- **শ্রেণি:** `Blur`, `IMGBlur`, `BlurCard`, `IMGBlurCard`, `CameraBlur`
- **সহায়ক:** `blur_config` (global সেটিংস), `gaussian_blur_rgba`
- **মূল ধারণা:** `Blur` = প্রতি ফ্রেমে লাইভ ব্লার · `IMGBlur` = প্রথম
  ফ্রেমের স্ন্যাপশট ধরে রাখে
- **ইনপুট:** যেকোনো `VMobject` — Circle, Star, Polygon, Bézier, ফাঁপা শেপ
- **নিয়ন্ত্রণ:** z_index — Blur এর চেয়ে কম = ব্লার, বেশি = শার্প
- **উদাহরণ চালানো:** `manim -pql examples/blur_example.py GlassDoor`

ন্যূনতম ব্যবহারের নমুনা:

```python
from manim import *
from my_manim_lib import Blur

class GlassDoorScene(Scene):
    def construct(self):
        rec = Rectangle(width=5, height=5, stroke_color=WHITE, stroke_width=4)
        glass = Blur(rec, 30)
        glass.set_z_index(1)
        self.add(glass)

        person = Circle(radius=0.6, fill_opacity=1, color=RED)
        person.move_to(LEFT * 6).set_z_index(0)
        self.add(person)

        self.play(person.animate.move_to(RIGHT * 6), run_time=3)
```

---

## 🔍 শেষ ধাপ — push করার আগে যাচাই করো

- [ ] `blur.py` আছে `my_manim_lib/manim_util/` এ, `shapes.py` এর পাশে
- [ ] `shapes.py` অপরিবর্তিত
- [ ] দুটি `__init__.py` তেই `SmoothPolygon` এখনও আছে
- [ ] `from my_manim_lib import Blur` কাজ করে
- [ ] `examples/blur_example.py` তৈরি হয়েছে
- [ ] `requirements.txt` এ `scipy` আছে
- [ ] README একাধিক মডিউল ধরে সাজানো
- [ ] **`text.md` push করা হয়নি**

**Commit message এর প্রস্তাব:**

```text
feat: add Blur/IMGBlur glass-blur module

- add my_manim_lib/manim_util/blur.py (Blur, IMGBlur, BlurCard,
  IMGBlurCard, CameraBlur)
- export new classes from both __init__.py files
- add examples/blur_example.py
- add scipy to requirements
- restructure README for multiple modules
```

