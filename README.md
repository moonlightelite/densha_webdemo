# Densha de Go! — Yamanote web demo

A standalone, browser-runnable WASM build of the Densha de Go! clean-room
reimplementation. It loads straight into a **6-stop slice of Yamanote
Diagram #1** (Ōsaki → …, diagram row 1, `-autostart=0:1`), runs the full
audio path (SE + BGM through Emscripten's OpenAL → WebAudio), and ends at
the complete result screen (Get Credit) when the slice's last stop is
served. **The run ends there**: the score screen counts up and HOLDS — the
original's result → line-menu hand-off is cut, no menu screen exists in the
demo. The page's status bar carries the restart affordance: *"Diagram
complete — reload the page to drive again"*.

## Serve

Any static server works.

```sh
cd web && python3 serve.py 8099
# then open http://localhost:8099/dgf.html
```

## Browsers

The demo needs **WebGL2** (the renderer is ES3: `#version 300 es` shaders,
`glBlitFramebuffer`, DEPTH24_STENCIL8) — there is no WebGL1 fallback.

## Controls (identical to the desktop build's keyboard map)

| Input                       | Key                        |
|-----------------------------|----------------------------|
| Autodrive on / off (toggle) | `A`                        |
| Graphics quality Normal/Good/Best (cycle) | `G`          |
| Framerate 60 fps locked / uncapped (toggle) | `F`         |
| Power notches (detents 1–5) | `1` `2` `3` `4` `5`        |
| Neutral (N)                 | `0`                        |
| Brake down / up (B1–B8)     | `[` / `]`                  |
| Emergency brake (EB)        | `\` (or `Delete`)          |
| Horn                        | `X`                        |
| View switch (cab ↔ exterior) | `S` (or `V`)              |
| Doors left / right          | `Q` / `E`                  |
| ATS acknowledge             | `Space` (or `Enter`)       |
| Pause menu (open)           | `Enter`                    |
| Pause menu cursor / confirm | `↑` `↓` / `Enter`          |
| Pause menu cancel (= Resume) | `Esc`                     |

**Pause menu.** `Enter` pauses the run (the original's menu-key bit 11).
`↑`/`↓` move the cursor between **Resume** and **Quit Run**; `Enter`
confirms — Resume unpauses, Quit Run ends the run through the game-over
"No" hand-off into the held **Get Credit** result screen (the demo has no
menu system to return to; the page's status bar carries the reload
affordance). `Esc` cancels the menu, which resumes the run. Inputs are one
pulse per press: the press that opens the menu doesn't also confirm, and a
press that lands inside a long render stall is not lost (the keys ride the
queued key events, not just the sampled key state).

Click the page once (any key also works) so the browser un-suspends the
WebAudio context — a "🔊 Click the page or press any key to enable audio"
badge shows in the page header while the context is suspended and goes away
once it runs. Audio (SE, announcements, BGM) starts with the run.

The demo boots with the **autodrive ON** (the attract AI drives the run);
`A` toggles it at any time. With the autodrive OFF the notch/brake keys
above drive the train manually; an "AUTO DRIVE ON/OFF" hint shows for ~2 s
after each toggle. Toggling back ON hands control to the AI again.

**`G` — graphics quality.** Cycles Normal → Good → Best → Normal with a
"Graphics: …" hint each press. Normal is the untouched original look (no
state is touched until the first press). Good adds trilinear mip filtering
+ 4× anisotropic filtering + 4× MSAA on the scene framebuffer; Best adds
16× anisotropic + 8× MSAA. The switch applies live (the resident textures
are re-sampled in place; the scene FBO is re-attached to multisample
renderbuffers and the existing present blit resolves).

**`F` — framerate mode.** Toggles the frame pacing between the default
**60 fps locked** (the yield sleeps to the next 1/60 s present boundary —
the loop paces at ~60 presented fps) and **uncapped** (a 0 ms yield — the
loop runs as fast as the browser's scheduler allows). Frame pacing only:
the simulation advances in fixed 60 Hz sim frames accumulated on the wall
clock, so the drive speed, the arrival times and the judgments are
identical at either rate (verified: the same autodrive segment produces
the same sim timeline in both modes — the `?aidbg=1` console trace).

All Rights owned Taito. This is a demo for education use only.
