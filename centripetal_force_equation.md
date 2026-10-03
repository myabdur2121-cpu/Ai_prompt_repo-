# Centripetal Force — Script

---

Look at this formula.

$$F = \frac{mv^2}{r}$$

Why is the speed *squared* here? Why not just $v$? Why not $v^3$?

There's actually a really clean reason. And it all comes from one simple idea — velocity is a vector.

---

A vector has two things: a magnitude, and a direction. So if *either* one of them changes, the velocity changes.

Now think about a satellite orbiting the Earth. Its speed stays the same the whole time. But its direction keeps turning. So its velocity is *still* changing — just because of the direction.

---

At some moment, the velocity is $v_1$. A tiny bit of time $t$ later, it becomes $v_2$.

Now place both arrows at the same point. The difference between them — that's the change in velocity. We call it $\Delta v$.

Since acceleration tells us how fast velocity changes:

$$a = \frac{\Delta v}{t}$$

So we need to find $\Delta v$.

---

In that time $t$, the satellite moves along a small arc. Let's call that length $s$.

Since the speed is constant:

$$s = vt$$

Now here's the first key observation.

If the satellite travels *twice* the arc length, its direction changes by *twice* as much. So $\Delta v$ also becomes twice as large. In other words:

$$\Delta v \propto s$$

And since $s = vt$:

$$\Delta v \propto vt$$

---

Now let's bring in the radius.

Imagine the satellite travels the same arc $s$, but on a *smaller* circle. The same distance now bends the direction a lot more — so $\Delta v$ gets larger.

On a bigger circle, the same arc barely changes the direction — so $\Delta v$ gets smaller.

So:

$$\Delta v \propto \frac{1}{r}$$

Combining what we have so far:

$$\Delta v \propto \frac{vt}{r}$$

---

But we're not done yet. There's one more thing.

The $\Delta v$ we're talking about is the *gap* between two velocity arrows. And those arrows — how long are they? They have length $v$.

So if the speed is higher, the arrows are longer. And longer arrows, turning by the same angle, create a *bigger* gap. So:

$$\Delta v \propto v$$

---

Now we have *two separate places* where $v$ shows up.

One from the distance: $s = vt$

And one from the vector itself: the arrows have length $v$.

Put them together:

$$\Delta v \propto v \cdot \frac{vt}{r} = \frac{v^2 t}{r}$$

Divide both sides by $t$:

$$\boxed{a = \frac{v^2}{r}}$$

And from Newton's second law:

$$\boxed{F = \frac{mv^2}{r}}$$

---

And this is actually one of the best real-life examples to understand what vectors are really for — not just the direction part, but why that direction even matters in the first place.
