"""Glowing dots for Manim Community — single-file implementation.

Drop-in replacement for ``manim_extras/mobjects/glow_dot.py``: everything the
older version had (``core_color`` hot centre, ``render_mode="raster"``, custom
``falloff``, per-dot colours, ``to_grid``, ``scale`` that scales radii) **plus**
GPU shader classes for the OpenGL renderer (``OpenGLGlowDot`` and friends).

Everything lives in this one file — the GLSL shader is embedded below as plain
strings and written to a temp directory at import time, so no extra ``.glsl``
files are needed.

The manimGL API is kept: ``DotCloud``, ``GlowDots``, ``GlowDot``, ``TrueDot``
with ``set_radius``, ``set_radii``, ``scale_radii``, ``set_glow_factor``,
``to_grid``, ``make_3d`` and a ``scale`` that also scales the radii.

Use the Cairo classes on the default renderer::

    from manim_extras.mobjects.glow_dot import GlowDot

Use the OpenGL classes with ``--renderer=opengl``::

    from manim_extras.mobjects.glow_dot import OpenGLGlowDot
"""

from __future__ import annotations

import inspect
import tempfile
from collections.abc import Callable, Sequence
from pathlib import Path

import numpy as np
from manim import (
    GREY_C,
    ORIGIN,
    YELLOW,
    Circle,
    Group,
    ImageMobject,
    Mobject,
    VGroup,
)
from manim.mobject.opengl.opengl_point_cloud_mobject import OpenGLPMobject
from manim.utils.color import ManimColor, color_to_rgba

__all__ = [
    "DEFAULT_DOT_RADIUS",
    "DEFAULT_GLOW_DOT_RADIUS",
    "DEFAULT_GRID_HEIGHT",
    "DEFAULT_BUFF_RATIO",
    "RENDER_MODES",
    "DotCloud",
    "GlowDot",
    "GlowDots",
    "TrueDot",
    "OpenGLDotCloud",
    "OpenGLGlowDot",
    "OpenGLGlowDots",
    "OpenGLTrueDot",
]

# Matching manimlib/mobject/types/dot_cloud.py
DEFAULT_DOT_RADIUS = 0.05
DEFAULT_GLOW_DOT_RADIUS = 0.2
DEFAULT_GRID_HEIGHT = 6.0
DEFAULT_BUFF_RATIO = 0.5

DEFAULT_GLOW_FACTOR = 2.0
DEFAULT_NUM_LAYERS = 24

RENDER_MODES = ("raster", "vector")

DEFAULT_CANVAS_SIZE = 512
MAX_CANVAS_PIXELS = 2048
RASTER_SIZE_STEP = 128

NULL_POINTS = np.zeros((0, 3), dtype=float)


# ============================================================================
# Glow math
# ============================================================================

def default_falloff(r: float, glow_factor: float = DEFAULT_GLOW_FACTOR) -> float:
    """3Blue1Brown's ``true_dot`` shader falloff: ``alpha = (1 - r)^glow_factor``."""
    return (1.0 - r) ** glow_factor


def _positional_arity(func) -> int:
    try:
        sig = inspect.signature(func)
    except (TypeError, ValueError):
        return 2
    return sum(
        1
        for p in sig.parameters.values()
        if p.kind
        in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
    )


def evaluate_falloff(falloff: Callable, r: float, glow_factor: float = DEFAULT_GLOW_FACTOR) -> float:
    """Evaluate ``falloff`` at normalized radius ``r``.

    Both signatures are supported: ``falloff(r)`` or ``falloff(r, glow_factor)``.
    """
    if _positional_arity(falloff) >= 2:
        return falloff(r, glow_factor)
    return falloff(r)


def layer_alphas(
    falloff: Callable,
    num_layers: int = DEFAULT_NUM_LAYERS,
    opacity: float = 1.0,
    glow_factor: float = DEFAULT_GLOW_FACTOR,
) -> tuple[np.ndarray, np.ndarray]:
    """Concentric-disc alphas that reproduce the opacity profile exactly.

    A pixel at radius ``r`` is covered by every disc whose radius is >= ``r``.
    Choosing ``a_i = 1 - h(x_i)/h(x_{i+1})`` (with ``h = 1 - opacity*profile``)
    makes the source-over composite telescope, so the composited alpha *exactly
    equals* ``opacity * clamp01(falloff(x_i))`` at every disc boundary.
    """
    xs = np.linspace(1.0 / num_layers, 1.0, num_layers)
    h = np.array(
        [
            1.0 - opacity * min(max(float(evaluate_falloff(falloff, x, glow_factor)), 0.0), 1.0)
            for x in xs
        ],
        dtype=float,
    )
    h = np.maximum(h, 1e-6)
    alphas = np.empty(num_layers, dtype=float)
    alphas[:-1] = 1.0 - h[:-1] / h[1:]
    alphas[-1] = 1.0 - h[-1]
    return xs, np.clip(alphas, 0.0, 1.0)


# ============================================================================
# Embedded GLSL shader (written to a temp dir at import time)
# ============================================================================

_GLSL_VERT = """\
#version 330

uniform vec2 frame_shape;
uniform float anti_alias_width;
uniform vec3 camera_center;
uniform mat3 camera_rotation;
uniform float is_fixed_in_frame;
uniform float is_fixed_orientation;
uniform vec3 fixed_orientation_center;
uniform float focal_distance;

in vec3 point;
in float radius;
in vec4 color;

out vec3 v_point;
out float v_point_radius;
out vec4 v_color;

vec3 rotate_point_into_frame(vec3 point){
    if(bool(is_fixed_in_frame)){ return point; }
    return camera_rotation * point;
}
vec3 position_point_into_frame(vec3 point){
    if(bool(is_fixed_in_frame)){ return point; }
    if(bool(is_fixed_orientation)){
        vec3 new_center = rotate_point_into_frame(fixed_orientation_center);
        return point + (new_center - fixed_orientation_center);
    }
    return rotate_point_into_frame(point - camera_center);
}

void main(){
    v_point = position_point_into_frame(point);
    v_point_radius = radius;
    v_color = color;
}
"""

_GLSL_GEOM = """\
#version 330

layout (points) in;
layout (triangle_strip, max_vertices = 4) out;

uniform vec2 frame_shape;
uniform float focal_distance;
uniform float is_fixed_in_frame;
uniform float is_fixed_orientation;
uniform vec3 fixed_orientation_center;
uniform float anti_alias_width;

in vec3 v_point[1];
in float v_point_radius[1];
in vec4 v_color[1];

out vec4 color;
out float point_radius;
out vec2 center;
out vec2 point;

const vec2 DEFAULT_FRAME_SHAPE = vec2(8.0 * 16.0 / 9.0, 8.0);
float perspective_scale_factor(float z, float focal_distance){
    return max(0.0, focal_distance / (focal_distance - z));
}
vec4 get_gl_Position(vec3 point){
    vec4 result = vec4(point, 1.0);
    if(!bool(is_fixed_in_frame)){
        result.x *= 2.0 / frame_shape.x;
        result.y *= 2.0 / frame_shape.y;
        float psf = perspective_scale_factor(result.z, focal_distance);
        if (psf > 0){
            result.xy *= psf;
            result.z *= 0.01;
        }
    } else {
        if (!bool(is_fixed_orientation)){
            result.x *= 2.0 / DEFAULT_FRAME_SHAPE.x;
            result.y *= 2.0 / DEFAULT_FRAME_SHAPE.y;
        } else {
            result.x *= 2.0 / frame_shape.x;
            result.y *= 2.0 / frame_shape.y;
        }
    }
    result.z *= -1;
    return result;
}

void main() {
    color = v_color[0];
    point_radius = v_point_radius[0];
    center = v_point[0].xy;
    point_radius = v_point_radius[0] / max(1.0 - v_point[0].z / focal_distance / frame_shape.y, 0.0);
    float rpa = point_radius + anti_alias_width;
    for(int i = 0; i < 4; i++){
        int x_index = 2 * (i % 2) - 1;
        int y_index = 2 * (i / 2) - 1;
        vec3 corner = v_point[0] + vec3(x_index * rpa, y_index * rpa, 0.0);
        gl_Position = get_gl_Position(corner);
        point = corner.xy;
        EmitVertex();
    }
    EndPrimitive();
}
"""

_GLSL_FRAG = """\
#version 330

uniform vec3 light_source_position;
uniform float gloss;
uniform float shadow;
uniform float anti_alias_width;
uniform float glow_factor;

in vec4 color;
in float point_radius;
in vec2 center;
in vec2 point;

out vec4 frag_color;

vec4 add_light(vec4 color, vec3 point, vec3 unit_normal, vec3 light_coords, float gloss, float shadow){
    if(gloss == 0.0 && shadow == 0.0) return color;
    if(unit_normal.z < 0){ unit_normal *= -1; }
    float camera_distance = 6;
    vec3 to_camera = vec3(0, 0, camera_distance) - point;
    vec3 to_light = light_coords - point;
    vec3 light_reflection = -to_light + 2 * unit_normal * dot(to_light, unit_normal);
    float dot_prod = dot(normalize(light_reflection), normalize(to_camera));
    float shine = gloss * exp(-3 * pow(1 - dot_prod, 2));
    float dp2 = dot(normalize(to_light), unit_normal);
    float darkening = mix(1, max(dp2, 0), shadow);
    return vec4(darkening * mix(color.rgb, vec3(1.0), shine), color.a);
}
vec4 finalize_color(vec4 color, vec3 point, vec3 unit_normal, vec3 light_coords, float gloss, float shadow){
    return add_light(color, point, unit_normal, light_coords, gloss, shadow);
}

void main() {
    vec2 diff = point - center;
    float dist = length(diff);
    float r = dist / max(point_radius, 1e-4);
    if (r > 1.0) discard;

    vec3 normal = vec3(diff / max(point_radius, 1e-4), sqrt(1.0 - r * r));
    frag_color = finalize_color(
        color,
        vec3(point.xy, 0.0),
        normal,
        light_source_position,
        gloss,
        shadow
    );

    // 3Blue1Brown glow falloff — per pixel on the GPU
    if (glow_factor > 0.0) {
        frag_color.a *= pow(1.0 - r, glow_factor);
    }

    float rim = smoothstep(1.0, 1.0 - 0.5 * anti_alias_width / max(point_radius, 1e-4), r);
    frag_color.a *= rim;
}
"""

_SHADER_DIR: Path | None = None


def _get_shader_dir() -> Path:
    """Write the embedded GLSL to a temp dir once, return its path."""
    global _SHADER_DIR
    if _SHADER_DIR is None:
        d = Path(tempfile.mkdtemp(prefix="manim_extras_glow_"))
        (d / "vert.glsl").write_text(_GLSL_VERT)
        (d / "geom.glsl").write_text(_GLSL_GEOM)
        (d / "frag.glsl").write_text(_GLSL_FRAG)
        _SHADER_DIR = d
    return _SHADER_DIR


# ============================================================================
# Cairo implementation (default renderer)
# ============================================================================

def _as_rgb(color) -> np.ndarray:
    return np.array(ManimColor(color).to_rgb(), dtype=float)


def _resize_rgba(array: np.ndarray, shape: tuple[int, int]) -> np.ndarray:
    rows = np.linspace(0, array.shape[0] - 1, shape[0]).round().astype(int)
    cols = np.linspace(0, array.shape[1] - 1, shape[1]).round().astype(int)
    return array[np.ix_(rows, cols)]


class DotCloud(Group):
    """A cloud of glowing (or crisp) dots.

    Parameters
    ----------
    points
        Dot centres, shape ``(n, 2)`` or ``(n, 3)``.  Defaults to one dot at the
        origin.
    color
        Dot colour — a single colour, or one per dot (cycled if shorter).
    opacity
        Peak opacity at the centre of each dot.
    radius
        Dot radius in scene units.  Use :meth:`set_radii` for per-dot radii.
    glow_factor
        Sharpness of the falloff.  ``0`` is a solid disc; larger values
        concentrate the light.  ``GlowDot`` uses ``2``.
    render_mode
        ``"vector"`` (default) — concentric discs, transmission-matched (exact);
        ``"raster"`` — one per-pixel RGBA image.
    falloff
        Optional custom falloff ``f(r)`` or ``f(r, glow_factor)`` replacing
        ``(1-r)**glow_factor``.
    distribution_equation
        Alias for ``falloff``.
    core_color
        Optional colour at the very centre, blending out to ``color`` at the
        rim.  ``None`` keeps a single flat colour.
    core_size
        How far the core colour reaches, 0-1 of the radius.
    canvas_size
        Raster resolution along the longest side (raster mode only).
    num_layers
        Discs per dot in vector mode.
    anti_alias_width
        Edge-fade width in pixels (raster mode).
    """

    def __init__(
        self,
        points: Sequence | np.ndarray | None = None,
        color=GREY_C,
        opacity: float = 1.0,
        radius: float = DEFAULT_DOT_RADIUS,
        glow_factor: float = 0.0,
        render_mode: str = "vector",
        falloff: Callable | None = None,
        distribution_equation: Callable | None = None,
        core_color=None,
        core_size: float = 0.35,
        canvas_size: int = DEFAULT_CANVAS_SIZE,
        num_layers: int = DEFAULT_NUM_LAYERS,
        anti_alias_width: float = 2.0,
        **kwargs,
    ) -> None:
        if distribution_equation is not None and falloff is None:
            falloff = distribution_equation
        if render_mode not in RENDER_MODES:
            raise ValueError(f"render_mode must be one of {RENDER_MODES}, got {render_mode!r}.")
        if radius < 0:
            raise ValueError(f"radius must be non-negative, got {radius}.")
        if not 0.0 <= opacity <= 1.0:
            raise ValueError(f"opacity must lie in [0, 1], got {opacity}.")
        if glow_factor < 0:
            raise ValueError(f"glow_factor must be non-negative, got {glow_factor}.")
        if not 0.0 <= core_size <= 1.0:
            raise ValueError(f"core_size must lie in [0, 1], got {core_size}.")
        if num_layers < 1:
            raise ValueError(f"num_layers must be at least 1, got {num_layers}.")

        super().__init__(**kwargs)
        self.render_mode = render_mode
        self.falloff = falloff
        self.core_color = core_color
        self.core_size = core_size
        self.canvas_size = canvas_size
        self.num_layers = num_layers
        self.anti_alias_width = anti_alias_width
        self.glow_factor = glow_factor
        self.opacity = opacity

        self.points = self._clean_points(points)
        n = len(self.points)
        self.radii = np.full(n, float(radius))
        self.colors = self._clean_colors(color, n)

        self._rebuild()

    # ------------------------------------------------------------------
    # input handling
    # ------------------------------------------------------------------
    @staticmethod
    def _clean_points(points) -> np.ndarray:
        if points is None:
            return np.array([ORIGIN], dtype=float)
        array = np.asarray(points, dtype=float)
        if array.ndim == 1:
            array = array.reshape(1, -1)
        if array.ndim != 2 or array.shape[1] not in (2, 3):
            raise ValueError(f"points must have shape (n, 2) or (n, 3), got {array.shape}.")
        if array.shape[1] == 2:
            array = np.column_stack([array, np.zeros(len(array))])
        if len(array) == 0:
            raise ValueError("points cannot be empty.")
        return array

    @staticmethod
    def _clean_colors(color, n: int) -> list:
        if isinstance(color, (list, tuple, np.ndarray)) and not isinstance(color, str):
            colors = list(color)
            if not colors:
                raise ValueError("color cannot be an empty sequence.")
            return [colors[i % len(colors)] for i in range(n)]
        return [color] * n

    # ------------------------------------------------------------------
    # building
    # ------------------------------------------------------------------
    def _alpha_at(self, r: np.ndarray) -> np.ndarray:
        """Alpha profile over normalised radius ``r``, clipped to the disc."""
        rr = np.asarray(r, dtype=float)
        if self.falloff is not None:
            alpha = np.asarray(
                [evaluate_falloff(self.falloff, float(x), self.glow_factor) for x in rr.ravel()],
                dtype=float,
            ).reshape(rr.shape)
        else:
            alpha = np.power(np.clip(1.0 - rr, 0.0, 1.0), self.glow_factor)
        return np.clip(np.where(rr > 1.0, 0.0, alpha), 0.0, 1.0) * self.opacity

    def _rgb_at(self, r: np.ndarray, color) -> np.ndarray:
        """RGB over normalised radius, blending the core colour if set."""
        rim = _as_rgb(color)
        rr = np.asarray(r, dtype=float)
        if self.core_color is None:
            return np.broadcast_to(rim, (*rr.shape, 3)).copy()
        core = _as_rgb(self.core_color)
        if self.core_size <= 0:
            mix = np.ones_like(rr)
        else:
            mix = np.clip(rr / self.core_size, 0.0, 1.0)
        return core + (rim - core) * mix[..., None]

    def _rebuild(self) -> None:
        if self.submobjects:
            self.remove(*self.submobjects)
        built = self._build_raster() if self.render_mode == "raster" else self._build_vector()
        if built is not None:
            self.add(built)

    def _build_raster(self) -> Mobject | None:
        """One RGBA image covering every dot, alpha-composited per pixel."""
        radii = np.maximum(self.radii, 1e-9)
        low = (self.points[:, :2] - radii[:, None]).min(axis=0)
        high = (self.points[:, :2] + radii[:, None]).max(axis=0)
        span = np.maximum(high - low, 1e-6)

        aspect = span[0] / span[1]
        if aspect >= 1:
            width_px = self.canvas_size
            height_px = max(RASTER_SIZE_STEP, int(round(self.canvas_size / aspect)))
        else:
            height_px = self.canvas_size
            width_px = max(RASTER_SIZE_STEP, int(round(self.canvas_size * aspect)))
        width_px = int(np.clip(width_px, RASTER_SIZE_STEP, MAX_CANVAS_PIXELS))
        height_px = int(np.clip(height_px, RASTER_SIZE_STEP, MAX_CANVAS_PIXELS))
        px_per_unit = width_px / span[0]

        xs = low[0] + (np.arange(width_px) + 0.5) * span[0] / width_px
        ys = high[1] - (np.arange(height_px) + 0.5) * span[1] / height_px
        grid_x, grid_y = np.meshgrid(xs, ys)

        accum_rgb = np.zeros((height_px, width_px, 3))
        accum_a = np.zeros((height_px, width_px))

        for centre, radius, color in zip(self.points, self.radii, self.colors):
            if radius <= 0:
                continue
            r = np.sqrt((grid_x - centre[0]) ** 2 + (grid_y - centre[1]) ** 2) / radius
            alpha = self._alpha_at(r)
            if self.anti_alias_width > 0:
                edge = self.anti_alias_width / max(radius * px_per_unit, 1e-9)
                if edge > 0:
                    t = np.clip((1.0 - r) / max(edge, 1e-9), 0.0, 1.0)
                    alpha = alpha * (t * t * (3.0 - 2.0 * t))
            if not alpha.any():
                continue
            rgb = self._rgb_at(r, color)
            out_a = alpha + accum_a * (1.0 - alpha)
            safe = np.where(out_a > 0, out_a, 1.0)
            accum_rgb = (
                rgb * alpha[..., None] + accum_rgb * accum_a[..., None] * (1.0 - alpha[..., None])
            ) / safe[..., None]
            accum_a = out_a

        rgba = np.zeros((height_px, width_px, 4), dtype=np.uint8)
        rgba[..., :3] = np.clip(accum_rgb * 255, 0, 255).astype(np.uint8)
        rgba[..., 3] = np.clip(accum_a * 255, 0, 255).astype(np.uint8)

        image = ImageMobject(rgba)
        image.stretch_to_fit_width(span[0])
        image.stretch_to_fit_height(span[1])
        image.move_to(np.array([*(low + span / 2), 0.0]))
        return image

    def _build_vector(self) -> Mobject | None:
        """Concentric discs per dot.

        With a flat colour this uses transmission-matched alphas (exact profile).
        With a ``core_color`` each layer additionally carries its own blended RGB
        (solved so the running composite equals the target).
        """
        group = VGroup()
        for centre, radius, color in zip(self.points, self.radii, self.colors):
            if radius <= 0:
                continue
            if self.core_color is None:
                eq = self.falloff if self.falloff is not None else (
                    lambda r: (1.0 - r) ** self.glow_factor
                )
                xs, alphas = layer_alphas(eq, self.num_layers, self.opacity, self.glow_factor)
                rgb = _as_rgb(color)
                for x, a in zip(xs, alphas):
                    if a <= 1e-6:
                        continue
                    group.add(
                        Circle(
                            radius=x * radius,
                            stroke_width=0,
                            fill_color=ManimColor.from_rgb(rgb),
                            fill_opacity=float(a),
                        ).move_to(centre)
                    )
            else:
                edges = np.linspace(1.0, 0.0, self.num_layers + 1)[:-1]
                mids = np.clip(edges - 0.5 / self.num_layers, 0.0, 1.0)
                      targets = self._alpha_at(mids)
                rgbs = self._rgb_at(mids, color)
                running = 0.0
                for edge, target, rgb in zip(edges, targets, rgbs):
                    if edge <= 0 or running >= 1.0:
                        continue
                    layer_alpha = float(np.clip((target - running) / (1.0 - running), 0.0, 1.0))
                    if layer_alpha <= 1e-6:
                        continue
                    group.add(
                        Circle(
                            radius=edge * radius,
                            stroke_width=0,
                            fill_color=ManimColor.from_rgb(rgb),
                            fill_opacity=layer_alpha,
                        ).move_to(centre)
                    )
                    running = target
        return group if len(group) else None

    # ------------------------------------------------------------------
    # manimGL-compatible API
    # ------------------------------------------------------------------
    def set_points(self, points) -> "DotCloud":
        new_points = self._clean_points(points)
        n = len(new_points)
        old = len(self.points)
        if n != old:
            self.radii = np.resize(self.radii, n)
            self.colors = [self.colors[i % len(self.colors)] for i in range(n)]
        self.points = new_points
        self._rebuild()
        return self

    def get_points(self) -> np.ndarray:
        return self.points

    def set_radius(self, radius: float) -> "DotCloud":
        if radius < 0:
            raise ValueError(f"radius must be non-negative, got {radius}.")
        self.radii = np.full(len(self.points), float(radius))
        self._rebuild()
        return self

    def get_radius(self) -> float:
        return float(self.radii.max())

    def set_radii(self, radii) -> "DotCloud":
        values = np.asarray(radii, dtype=float).flatten()
        if values.size == 0:
            raise ValueError("radii cannot be empty.")
        if (values < 0).any():
            raise ValueError("radii must be non-negative.")
        self.radii = np.resize(values, len(self.points))
        self._rebuild()
        return self

    def get_radii(self) -> np.ndarray:
        return self.radii

    def scale_radii(self, scale_factor: float) -> "DotCloud":
        return self.set_radii(self.radii * scale_factor)

    def set_glow_factor(self, glow_factor: float) -> "DotCloud":
        if glow_factor < 0:
            raise ValueError(f"glow_factor must be non-negative, got {glow_factor}.")
        self.glow_factor = glow_factor
        self._rebuild()
        return self

    def get_glow_factor(self) -> float:
        return self.glow_factor

    def set_falloff(self, falloff: Callable | None) -> "DotCloud":
        self.falloff = falloff
        self._rebuild()
        return self

    def get_falloff(self) -> Callable:
        if self.falloff is not None:
            return self.falloff
        return lambda r: (1.0 - r) ** self.glow_factor

    set_distribution_equation = set_falloff
    get_distribution_equation = get_falloff

    def set_core_color(self, core_color) -> "DotCloud":
        self.core_color = core_color
        self._rebuild()
        return self

    def set_color(self, color, **kwargs) -> "DotCloud":
        self.colors = self._clean_colors(color, len(self.points))
        self._rebuild()
        return self

    def set_opacity(self, opacity: float, **kwargs) -> "DotCloud":
        if not 0.0 <= opacity <= 1.0:
            raise ValueError(f"opacity must lie in [0, 1], got {opacity}.")
        self.opacity = opacity
        self._rebuild()
        return self

    def scale(self, scale_factor, scale_radii: bool = True, **kwargs) -> "DotCloud":
        about_point = kwargs.get("about_point")
        if about_point is None:
            about_point = self.get_center()
        self.points = about_point + (self.points - about_point) * scale_factor
        if scale_radii:
            self.radii = self.radii * scale_factor
        self._rebuild()
        return self

    def to_grid(
        self,
        n_rows: int,
        n_cols: int,
        n_layers: int = 1,
        buff_ratio: float | None = None,
        h_buff_ratio: float = 1.0,
        v_buff_ratio: float = 1.0,
        d_buff_ratio: float = 1.0,
        height: float | None = DEFAULT_GRID_HEIGHT,
    ) -> "DotCloud":
        if min(n_rows, n_cols, n_layers) < 1:
            raise ValueError("n_rows, n_cols and n_layers must all be at least 1.")
        n_points = n_rows * n_cols * n_layers
        idx = np.arange(n_points)
        points = np.zeros((n_points, 3))
        points[:, 0] = idx % n_cols
        points[:, 1] = (idx // n_cols) % n_rows
        points[:, 2] = idx // (n_rows * n_cols)

        if buff_ratio is not None:
            h_buff_ratio = v_buff_ratio = d_buff_ratio = buff_ratio

        radius = self.get_radius()
        spacing = [2 * radius * (1 + br) for br in (h_buff_ratio, v_buff_ratio, d_buff_ratio)]
        points *= np.array(spacing)
        points -= points.mean(axis=0)

        self.set_points(points)
        self.set_radius(radius)
        if height is not None:
            span = points[:, 1].max() - points[:, 1].min()
            if span > 0:
                factor = height / span
                self.points = self.points * factor
                self._rebuild()
        return self

    def interpolate_color(self, mobject1, mobject2, alpha) -> "DotCloud":
        """Blend colours between two clouds (keeps FadeIn/Transform working)."""
        for child, m1, m2 in zip(self.submobjects, mobject1.submobjects, mobject2.submobjects):
            if not hasattr(child, "interpolate_color"):
                continue
            if isinstance(child, ImageMobject):
                a1 = m1.pixel_array.astype(float)
                a2 = m2.pixel_array.astype(float)
                if a1.shape != a2.shape:
                    a2 = _resize_rgba(a2, a1.shape[:2])
                child.pixel_array = np.clip((1 - alpha) * a1 + alpha * a2, 0, 255).astype(np.uint8)
            else:
                child.interpolate_color(m1, m2, alpha)
        return self

    def fade(self, darkness: float = 0.5, family: bool = True) -> "DotCloud":
        for child in self.submobjects:
            child.fade(darkness, family=family)
        return self

    def make_3d(self, reflectiveness: float = 0.5, gloss: float = 0.1, shadow: float = 0.2) -> "DotCloud":
        self.reflectiveness = reflectiveness
        self.gloss = gloss
        self.shadow = shadow
        return self


class GlowDots(DotCloud):
    """Several glowing dots.  ManimGL defaults: yellow, radius 0.2, glow 2."""

    def __init__(self, points=None, color=YELLOW, radius: float = DEFAULT_GLOW_DOT_RADIUS,
                 glow_factor: float = 2.0, **kwargs) -> None:
        super().__init__(points, color=color, radius=radius, glow_factor=glow_factor, **kwargs)


class GlowDot(GlowDots):
    """A single glowing dot.

    ::

        GlowDot()                                   # yellow, radius 0.2
        GlowDot(LEFT * 2, color=BLUE, radius=0.5)
        GlowDot(glow_factor=4)                      # tighter, brighter core
        GlowDot(core_color=WHITE)                   # hot white centre
        GlowDot(render_mode="raster")               # per-pixel image
        GlowDot(falloff=lambda r, gf: np.exp(-gf * r))
    """

    def __init__(self, center=ORIGIN, **kwargs) -> None:
        super().__init__(points=np.array([center], dtype=float), **kwargs)


class TrueDot(DotCloud):
    """A crisp, solid dot: ``glow_factor=0``, the ManimGL default radius."""

    def __init__(self, center=ORIGIN, radius: float = DEFAULT_DOT_RADIUS, **kwargs) -> None:
        super().__init__(points=np.array([center], dtype=float), radius=radius, **kwargs)


# ============================================================================
# OpenGL implementation (--renderer=opengl, GPU shader)
# ============================================================================

class OpenGLTrueDot(OpenGLPMobject):
    """A single ordinary dot rendered with manimCE's built-in ``true_dot`` shader."""

    def __init__(self, center=ORIGIN, radius: float = DEFAULT_DOT_RADIUS, color=GREY_C,
                 opacity: float = 1.0, **kwargs):
        super().__init__(color=color, **kwargs)
        self.point_radius = radius
        self.points = np.array([np.asarray(center, dtype=float)], dtype=np.float32)
        self.rgbas = np.array([color_to_rgba(color, opacity)], dtype=np.float32)

    def set_radius(self, radius: float) -> "OpenGLTrueDot":
        self.point_radius = radius
        return self

    def get_radius(self) -> float:
        return float(self.point_radius)

    def scale_radii(self, factor: float) -> "OpenGLTrueDot":
        return self.set_radius(self.get_radius() * factor)

    def make_3d(self, reflectiveness: float = 0.5, gloss: float = 0.1, shadow: float = 0.2) -> "OpenGLTrueDot":
        self.uniforms["gloss"] = gloss
        self.uniforms["shadow"] = shadow
        self.apply_depth_test()
        return self


class OpenGLDotCloud(OpenGLPMobject):
    """A cloud of ordinary dots (``true_dot`` shader) with ``to_grid``."""

    def __init__(self, points=NULL_POINTS, color=GREY_C, opacity: float = 1.0,
                 radius: float = DEFAULT_DOT_RADIUS, **kwargs):
        super().__init__(color=color, **kwargs)
        self.radius = radius
        self.opacity = opacity
        self.point_radius = radius
        if points is not None and len(points) > 0:
            self.set_points(points)

    def set_points(self, points) -> "OpenGLDotCloud":
        pts = np.asarray(points, dtype=float)
        if pts.ndim == 1:
            pts = pts.reshape(1, -1)
        self.points = pts.astype(np.float32)
        self.rgbas = np.array([color_to_rgba(self.color, self.opacity)] * len(pts), dtype=np.float32)
        return self

    def get_points(self) -> np.ndarray:
        return self.points.copy()

    def set_radius(self, radius: float) -> "OpenGLDotCloud":
        self.radius = radius
        self.point_radius = radius
        return self

    def get_radius(self) -> float:
        return self.radius

    def scale_radii(self, factor: float) -> "OpenGLDotCloud":
        return self.set_radius(self.radius * factor)

    def set_opacity(self, opacity: float, recurse: bool = True) -> "OpenGLDotCloud":
        self.opacity = opacity
        if hasattr(self, "points") and len(self.points):
            self.rgbas[:, 3] = opacity
        return self

    def set_color(self, color, family: bool = True) -> "OpenGLDotCloud":
        self.color = color
        if hasattr(self, "points") and len(self.points):
            self.rgbas[:, :3] = color_to_rgba(color, 1.0)[:3]
        return self

    def to_grid(self, n_rows: int, n_cols: int, n_layers: int = 1,
                buff_ratio: float | None = None, h_buff_ratio: float = 1.0,
                v_buff_ratio: float = 1.0, d_buff_ratio: float = 1.0,
                height: float | None = DEFAULT_GRID_HEIGHT) -> "OpenGLDotCloud":
        if buff_ratio is not None:
            h_buff_ratio = v_buff_ratio = d_buff_ratio = buff_ratio
        r = self.get_radius()
        sx = 2 * r * (1 + h_buff_ratio)
        sy = 2 * r * (1 + v_buff_ratio)
        sz = 2 * r * (1 + d_buff_ratio)
        pts = []
        for layer in range(n_layers):
            z = (layer - (n_layers - 1) / 2) * sz
            for row in range(n_rows):
                y = (row - (n_rows - 1) / 2) * sy
                for col in range(n_cols):
                    pts.append([(col - (n_cols - 1) / 2) * sx, y, z])
        self.set_points(pts)
        if height is not None:
            self.set_height(height)
        self.center()
        return self


class OpenGLGlowDots(OpenGLPMobject):
    """Many glowing dots rendered with the custom embedded GLSL shader.

    The default falloff (``None``) is computed **per pixel on the GPU**
    (``pow(1 - r, glow_factor)`` — the same math as manimGL).  A custom
    ``falloff`` Python function — or a ``core_color`` — cannot run in the
    shader, so those are rendered with concentric GPU shells (per-shell radius,
    alpha and colour), using the same transmission-matched math as the Cairo
    vector backend.
    """

    shader_folder = None  # set below via _get_shader_dir()

    shader_dtype = [
        ("point", np.float32, (3,)),
        ("radius", np.float32, (1,)),
        ("color", np.float32, (4,)),
    ]

    def __init__(
        self,
        points=NULL_POINTS,
        color=YELLOW,
        radius: float = DEFAULT_GLOW_DOT_RADIUS,
        glow_factor: float = DEFAULT_GLOW_FACTOR,
        opacity: float = 1.0,
        falloff: Callable | None = None,
        distribution_equation: Callable | None = None,
        core_color=None,
        core_size: float = 0.35,
        num_layers: int = DEFAULT_NUM_LAYERS,
        anti_alias_width: float = 2.0,
        **kwargs,
    ):
        if falloff is None and distribution_equation is not None:
            falloff = distribution_equation
        super().__init__(color=color, **kwargs)
        # manim routes ``self.color = ...`` through ``set_color`` which calls
        # ``_rebuild``, so ``_centers`` must exist before we set color.
        self._centers: np.ndarray = np.zeros((0, 3), dtype=float)
        self.color = color
        self.radius = radius
        self.glow_factor = glow_factor
        self.opacity = opacity
        self.num_layers = num_layers
        self.anti_alias_width = anti_alias_width
        self._falloff = falloff
        self.core_color = core_color
        self.core_size = core_size
        self.uniforms["gloss"] = 0.0
        self.uniforms["shadow"] = 0.0
        if points is not None and len(points) > 0:
            self.set_points(points)
        else:
            self._rebuild()

    # ------------------------------------------------------------ points
    def set_points(self, points) -> "OpenGLGlowDots":
        pts = np.asarray(points, dtype=float)
        if pts.ndim == 1:
            pts = pts.reshape(1, -1)
        self._centers = pts
        return self._rebuild()

    def get_points(self) -> np.ndarray:
        return self._centers.copy()

    # ------------------------------------------------------------ falloff
    def _equation(self) -> Callable:
        if self._falloff is not None:
            return self._falloff
        return lambda r: default_falloff(r, self.glow_factor)

    def get_falloff(self) -> Callable:
        return self._equation()

    get_distribution_equation = get_falloff

    def set_falloff(self, falloff: Callable | None) -> "OpenGLGlowDots":
        self._falloff = falloff
        return self._rebuild()

    def set_distribution_equation(self, falloff: Callable | None) -> "OpenGLGlowDots":
        return self.set_falloff(falloff)

    def set_glow_factor(self, glow_factor: float) -> "OpenGLGlowDots":
        self.glow_factor = glow_factor
        return self._rebuild()

    def set_core_color(self, core_color) -> "OpenGLGlowDots":
        self.core_color = core_color
        return self._rebuild()

    # ------------------------------------------------------------ style
    def set_opacity(self, opacity: float, recurse: bool = True) -> "OpenGLGlowDots":
        self.opacity = opacity
        return self._rebuild()

    def set_color(self, color, family: bool = True) -> "OpenGLGlowDots":
        self.color = color
        return self._rebuild()

    def set_radius(self, radius: float) -> "OpenGLGlowDots":
        self.radius = radius
        return self._rebuild()

    def get_radius(self) -> float:
        return self.radius

    def scale_radii(self, factor: float) -> "OpenGLGlowDots":
        return self.set_radius(self.radius * factor)

    # ------------------------------------------------------------ core
    def _shell_rgb(self, r: np.ndarray) -> np.ndarray:
        """Per-shell RGB: rim colour blended to ``core_color`` near the centre."""
        rim = color_to_rgba(self.color, 1.0)[:3]
        if self.core_color is None:
            return np.tile(rim, (len(r), 1))
        core = color_to_rgba(self.core_color, 1.0)[:3]
        if self.core_size <= 0:
            mix = np.ones_like(r)
        else:
            mix = np.clip(r / self.core_size, 0.0, 1.0)
        return core + (rim - core) * mix[:, None]

    def _rebuild(self) -> "OpenGLGlowDots":
        # guard: during super().__init__ manim calls set_color before our
        # attributes exist — do nothing in that case.
        if not hasattr(self, "_centers"):
            return self
        n_centers = len(self._centers)
        if self._falloff is None and self.core_color is None:
            # pixel-perfect shader path: one point per dot
            self.uniforms["glow_factor"] = float(self.glow_factor)
            centers = self._centers
            radii = np.full(n_centers, self.radius)
            alphas = np.full(n_centers, self.opacity)
            rgb = color_to_rgba(self.color, 1.0)[:3]
            rgbs = np.tile(rgb, (n_centers, 1))
        else:
            # shells: per-shell radius, alpha and blended colour
            self.uniforms["glow_factor"] = 0.0
            eq = self._falloff if self._falloff is not None else (
                lambda r: (1.0 - r) ** self.glow_factor
            )
            xs, shell_alphas = layer_alphas(eq, self.num_layers, self.opacity, self.glow_factor)
            centers = np.repeat(self._centers, self.num_layers, axis=0)
            radii = np.tile(self.radius * xs, n_centers)
            alphas = np.tile(shell_alphas, n_centers)
            rgbs = np.tile(self._shell_rgb(xs), (n_centers, 1))

        self.points = centers.astype(np.float32)
        self.radii = radii.reshape(-1, 1).astype(np.float32)
        self.rgbas = np.empty((len(centers), 4), dtype=np.float32)
        self.rgbas[:, :3] = rgbs
        self.rgbas[:, 3] = alphas
        return self

    def get_shader_data(self):
        shader_data = np.zeros(len(self.points), dtype=self.shader_dtype)
        shader_data["point"] = self.points
        if len(self.radii) == len(self.points):
            shader_data["radius"] = self.radii
        shader_data["color"] = self.rgbas
        return shader_data


OpenGLGlowDots.shader_folder = _get_shader_dir()


class OpenGLGlowDot(OpenGLGlowDots):
    """A single glowing dot (shader-based, manimGL's ``GlowDot`` for OpenGL)."""

    def __init__(self, center=ORIGIN, **kwargs):
        super().__init__(points=np.array([np.asarray(center, dtype=float)]), **kwargs)
