"""Bounce 2.0 – eigener 3D-Raytracer (NumPy, vektorisiert), gebaut für perfekte Ball-Bounce-Videos.

Szene: Ellipsoide (Kugeln mit Squash & Stretch), ein Boden (Ebene) ODER eine unendliche Treppe, prozedurale
Studio-Umgebung mit Softboxen. Materialien: chrome, glass (Fresnel + Brechung), ceramic (Klarlack), rubber, gold,
floor: mirror (schwarzer Spiegel), matte, wet. Weiche Schatten + Ambient Occlusion analytisch (Kugel-Formeln).
Koordinaten: y nach oben. Alle Funktionen arbeiten auf Arrays von Strahlen (N,3).
"""
import numpy as np

W, H = 1080, 1920
EPS = 1e-4


def norm(v):
    return v / (np.linalg.norm(v, axis=-1, keepdims=True) + 1e-12)


def camera_rays(pos, look, fov_deg=40.0, w=W, h=H, roll=0.0):
    pos, look = np.asarray(pos, float), np.asarray(look, float)
    fwd = norm(look - pos)
    right = norm(np.cross(fwd, [0.0, 1.0, 0.0]))
    up = np.cross(right, fwd)
    if roll:
        c, s = np.cos(roll), np.sin(roll)
        right, up = right * c + up * s, -right * s + up * c
    th = np.tan(np.radians(fov_deg) / 2)
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float64)
    u = (xs + 0.5 - w / 2) / (h / 2) * th
    v = -(ys + 0.5 - h / 2) / (h / 2) * th
    d = fwd[None, None] + u[..., None] * right[None, None] + v[..., None] * up[None, None]
    return np.broadcast_to(pos, (h * w, 3)).copy(), norm(d.reshape(-1, 3))


# ------------------------------------------------------------------ objects
class Ball:
    def __init__(self, c, r, mat="chrome", color=(1, 1, 1), sy=1.0, ior=1.5, tint=(1, 1, 1), spin=0.0):
        self.c, self.r, self.mat, self.color = np.asarray(c, float), float(r), mat, np.asarray(color, float)
        self.sy = float(sy)                       # squash (<1) / stretch (>1) along y, volume kept in x/z
        self.sxz = 1.0 / np.sqrt(self.sy)
        self.ior, self.tint, self.spin = ior, np.asarray(tint, float), spin

    def scale(self):
        return np.array([self.r * self.sxz, self.r * self.sy, self.r * self.sxz])

    def hit(self, o, d, inside=False):
        s = self.scale()
        o2, d2 = (o - self.c) / s, d / s
        a = (d2 * d2).sum(1)
        b = (o2 * d2).sum(1)
        cc = (o2 * o2).sum(1) - 1
        disc = b * b - a * cc
        ok = disc > 0
        sq = np.sqrt(np.maximum(disc, 0))
        t = np.where(inside, (-b + sq) / a, (-b - sq) / a)
        t = np.where(ok & (t > EPS), t, np.inf)
        return t

    def normal(self, p):
        s = self.scale()
        return norm((p - self.c) / (s * s))


class Floor:
    def __init__(self, y=0.0, mat="mirror", color=(0.05, 0.05, 0.06), tile=None):
        self.y, self.mat, self.color, self.tile = y, mat, np.asarray(color, float), tile

    def hit(self, o, d):
        t = (self.y - o[:, 1]) / np.where(np.abs(d[:, 1]) < 1e-9, -1e-9, d[:, 1])
        return np.where((t > EPS) & (d[:, 1] < 0), t, np.inf)

    def normal(self, p):
        return np.broadcast_to(np.array([0.0, 1.0, 0.0]), p.shape)

    def albedo(self, p):
        if self.tile is None:
            return np.broadcast_to(self.color, p.shape)
        a, b, size = self.tile
        k = (np.floor(p[:, 0] / size) + np.floor(p[:, 2] / size)) % 2
        c = np.where(k[:, None] > 0, np.asarray(a), np.asarray(b))
        fade = np.exp(-np.hypot(p[:, 0], p[:, 2]) / 7.0)[:, None]          # no moire in the distance
        return c * fade + (np.asarray(a) + np.asarray(b)) / 2 * (1 - fade)


class Stairs:
    """Infinite staircase going down along +x: step k has top y = -k*rise for x in [k*run, (k+1)*run]."""

    def __init__(self, run=1.0, rise=0.5, kmin=-6, kmax=30, colors=None, mat="ceramic_floor", width=1.0, thick=0.32):
        self.run, self.rise, self.kmin, self.kmax = run, rise, kmin, kmax
        self.width, self.thick = width, thick
        self.colors = colors or [(0.9, 0.9, 0.92), (0.2, 0.2, 0.22)]
        self.mat = mat

    def hit(self, o, d):
        """Each step is a floating block (slab): x in [k*run,(k+1)*run], y in [top-thick, top], z in [-w, w]."""
        best = np.full(len(o), np.inf)
        nrm = np.zeros((len(o), 3))
        kid = np.zeros(len(o), int)
        inv = 1.0 / np.where(np.abs(d) < 1e-9, 1e-9, d)
        for k in range(self.kmin, self.kmax):
            top = -k * self.rise
            lo = np.array([k * self.run, top - self.thick, -self.width])
            hi = np.array([(k + 1) * self.run, top, self.width])
            t1 = (lo - o) * inv
            t2 = (hi - o) * inv
            tmin = np.minimum(t1, t2)
            tmax = np.maximum(t1, t2)
            tn = tmin.max(1)
            tf = tmax.min(1)
            ok = (tn <= tf) & (tn > EPS) & (tn < best)
            if ok.any():
                ax = tmin.argmax(1)
                best = np.where(ok, tn, best)
                n = np.zeros((len(o), 3))
                n[np.arange(len(o)), ax] = -np.sign(d[np.arange(len(o)), ax])
                nrm[ok] = n[ok]
                kid[ok] = k
        self._n, self._k = nrm, kid
        return best

    def albedo(self, k):
        c = np.array(self.colors, float)
        return c[np.asarray(k) % len(c)]


# ------------------------------------------------------------------ environment / lighting
def studio_env(d, top=(0.02, 0.02, 0.03), horizon=(0.10, 0.10, 0.13), boxes=None):
    """Dark studio with soft rectangular light panels (what chrome / glass reflect)."""
    y = d[:, 1:2]
    col = np.asarray(horizon) * (1 - np.clip(y, 0, 1)) + np.asarray(top) * np.clip(y, 0, 1)
    col = np.where(y < 0, np.asarray(horizon) * 0.6, col)
    for (dirn, size, rgb, power) in (boxes or []):
        dirn = norm(np.asarray(dirn, float))
        cosang = d @ dirn
        a = np.clip((cosang - np.cos(size)) / (1 - np.cos(size)), 0, 1)
        col = col + np.asarray(rgb) * power * (a ** 0.35)[:, None] * (cosang[:, None] > 0)
    return col


def sphere_shadow(p, ldir, balls, k=8.0):
    """Soft shadow of spheres (IQ's sphere soft-shadow approximation). 1 = lit."""
    res = np.ones(len(p))
    for b in balls:
        if b.mat == "glass":
            pass
        oc = b.c - p
        bb = (oc * ldir).sum(1)
        h = np.sqrt(np.maximum((oc * oc).sum(1) - bb * bb, 0))
        r = b.r * (b.sxz * 0.5 + b.sy * 0.5)
        s = np.clip(k * (h - r) / np.maximum(bb, 1e-3), 0, 1)
        s = np.where(bb > 0, s * s * (3 - 2 * s), 1.0)
        res = np.minimum(res, s * (0.55 if b.mat == "glass" else 1.0) + (0.45 if b.mat == "glass" else 0.0))
    return res


def sphere_ao(p, n, balls):
    """Ambient occlusion from spheres (analytic)."""
    occ = np.zeros(len(p))
    for b in balls:
        v = b.c - p
        l = np.linalg.norm(v, axis=1) + 1e-9
        r = b.r * (b.sxz + b.sy) / 2
        occ += np.clip((n * v).sum(1) / l, 0, 1) * (r / l) ** 2
    return np.clip(1 - occ, 0, 1)


def fresnel(cosi, f0):
    return f0 + (1 - f0) * (1 - np.clip(cosi, 0, 1)) ** 5


def refract(d, n, eta):
    cosi = -(d * n).sum(1, keepdims=True)
    k = 1 - eta * eta * (1 - cosi * cosi)
    t = eta * d + (eta * cosi - np.sqrt(np.maximum(k, 0))) * n
    return norm(t), (k[:, 0] < 0)


# ------------------------------------------------------------------ renderer
class Scene:
    def __init__(self, balls, ground, env_fn, lights, ambient=0.25, floor_reflect=0.5):
        self.balls, self.ground, self.env_fn, self.lights = balls, ground, env_fn, lights
        self.ambient, self.floor_reflect = ambient, floor_reflect

    def nearest(self, o, d, skip=None):
        t = np.full(len(o), np.inf)
        idx = np.full(len(o), -1)
        for i, b in enumerate(self.balls):
            if skip is not None and i == skip:
                continue
            ti = b.hit(o, d)
            m = ti < t
            t = np.where(m, ti, t)
            idx = np.where(m, i, idx)
        tg = self.ground.hit(o, d)
        g = tg < t
        t = np.where(g, tg, t)
        idx = np.where(g, -2, idx)
        return t, idx

    def ground_shade(self, p, d, depth):
        g = self.ground
        if isinstance(g, Stairs):
            n = g._n_last
            alb = g._alb_last
        else:
            n = g.normal(p)
            alb = g.albedo(p)
        col = np.zeros_like(p)
        for (ldir, lcol, soft) in self.lights:
            ldir = norm(np.asarray(ldir, float))
            ndl = np.clip((n * ldir).sum(1), 0, 1)
            sh = sphere_shadow(p + n * 1e-3, ldir, self.balls, soft)
            col += alb * np.asarray(lcol) * (ndl * sh)[:, None]
        ao = sphere_ao(p, n, self.balls)
        col += alb * self.ambient * ao[:, None]
        for b in self.balls:                      # fake caustic: a glass ball focuses the key light onto the floor
            if b.mat == "glass" and self.lights:
                ldir = norm(np.asarray(self.lights[0][0], float))
                hgt = b.c[1] - p[:, 1]
                foc = b.c[None] - ldir[None] * (hgt / max(ldir[1], 1e-3))[:, None]
                dd = np.linalg.norm((p - foc)[:, [0, 2]], axis=1)
                spot = np.exp(-(dd / (b.r * (0.25 + 0.25 * hgt / (b.r * 4)))) ** 2)
                col += spot[:, None] * b.tint[None] * (1.6 / (1 + hgt))[:, None]
        if self.floor_reflect > 0 and depth > 0 and g.mat in ("mirror", "wet", "ceramic_floor"):
            rd = norm(d - 2 * (d * n).sum(1, keepdims=True) * n)
            fr = fresnel(-(d * n).sum(1), 0.04 if g.mat != "mirror" else 0.08)
            refl = self.trace(p + n * 1e-3, rd, depth - 1, no_ground=True)
            k = self.floor_reflect * (fr if g.mat != "mirror" else 0.35 + 0.65 * fr)
            col = col * (1 - k[:, None] * 0.5) + refl * k[:, None]
            col *= ao[:, None] ** 0.5
        return col

    def ball_shade(self, b, p, d, depth, bi):
        n = b.normal(p)
        cosi = -(d * n).sum(1)
        rd = norm(d - 2 * (d * n).sum(1, keepdims=True) * n)
        if b.mat in ("chrome", "gold"):
            refl = self.trace(p + n * 1e-3, rd, depth - 1, skip=bi) if depth > 0 else self.env_fn(rd)
            base = b.color if b.mat == "chrome" else np.array([1.0, 0.76, 0.36])
            f = fresnel(cosi, 0.75 if b.mat == "chrome" else 0.6)[:, None]
            return refl * (base * f + (1 - f) * base * 0.95)
        if b.mat == "glass":
            refl = self.trace(p + n * 1e-3, rd, depth - 1, skip=bi) if depth > 0 else self.env_fn(rd)
            td, _ = refract(d, n, 1.0 / b.ior)
            p2o = p - n * 1e-3
            t2 = b.hit(p2o, td, inside=True)
            t2 = np.where(np.isfinite(t2), t2, 0)
            p2 = p2o + td * t2[:, None]
            n2 = b.normal(p2)
            td2, tir = refract(td, -n2, b.ior)
            td2 = np.where(tir[:, None], norm(td - 2 * (td * -n2).sum(1, keepdims=True) * -n2), td2)
            trans = self.trace(p2 + n2 * 1e-3, td2, depth - 1, skip=bi) if depth > 0 else self.env_fn(td2)
            fr = fresnel(cosi, 0.04)[:, None]
            absorb = np.exp(-t2 / (b.r * 2.0))[:, None] * b.tint + (1 - np.exp(-t2 / (b.r * 2.0)))[:, None] * b.tint * 0.6
            return trans * absorb * (1 - fr) + refl * fr
        # ceramic / rubber: diffuse + specular + clearcoat reflection
        col = np.zeros_like(p)
        for (ldir, lcol, soft) in self.lights:
            ldir = norm(np.asarray(ldir, float))
            ndl = np.clip((n * ldir).sum(1), 0, 1)
            hv = norm(ldir[None] - d)
            spec_pow, spec_k = (180.0, 0.9) if b.mat == "ceramic" else (25.0, 0.25)
            spec = np.clip((n * hv).sum(1), 0, 1) ** spec_pow * spec_k
            col += b.color * np.asarray(lcol) * ndl[:, None] + np.asarray(lcol) * spec[:, None]
        col += b.color * self.ambient * (0.6 + 0.4 * n[:, 1:2])
        if b.mat == "ceramic" and depth > 0:
            fr = fresnel(cosi, 0.05)[:, None]
            refl = self.trace(p + n * 1e-3, rd, depth - 1, skip=bi)
            col = col * (1 - fr) + refl * fr
        return col

    def trace(self, o, d, depth=2, skip=None, no_ground=False):
        col = self.env_fn(d)
        if len(o) == 0:
            return col
        t, idx = self.nearest(o, d, skip)
        if no_ground:
            idx = np.where(idx == -2, -1, idx)
        for i, b in enumerate(self.balls):
            m = idx == i
            if m.any():
                p = o[m] + d[m] * t[m, None]
                col[m] = self.ball_shade(b, p, d[m], depth, i)
        m = idx == -2
        if m.any():
            p = o[m] + d[m] * t[m, None]
            if isinstance(self.ground, Stairs):
                self.ground.hit(o[m], d[m])
                self.ground._n_last = self.ground._n
                self.ground._alb_last = self.ground.albedo(self.ground._k)
            col[m] = self.ground_shade(p, d[m], depth)
        return col

    def render(self, o, d, depth=2, exposure=1.0):
        col = self.trace(o, d, depth)
        col = col * exposure
        col = col / (1 + col * 0.15)                    # soft highlight roll-off
        col = np.clip(col, 0, 1) ** (1 / 2.2)
        return (col.reshape(H, W, 3) * 255).astype(np.uint8)
