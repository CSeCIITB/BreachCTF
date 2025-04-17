# Snak-ASM

Even before getting into the challenge, from the fact that this is a web challenge and the name given, we can be pretty sure that this is going to be a web assembly (wasm) challenge.

> [!TIP]
> You can read more about wasm [here](https://webassembly.org/)

An interesting thing to note is that there is not hosted version for this challenge. That means that the flag has to be hidden somewhere inside the binary. However, from some preliminary analysis using `strings` and other tools, it isn't giving anything useful.

On running the app, it reveals a snake game and says that we need to get a score of 10,000 to get the flag. This is the first hint we can get that we don't need to actually play the game directly because it isn't possible to get a score of 10,000 on the grid size given in the game.

So we can start by using the tools from the _Web Assembly Tool Box_ (a.k.a `wabt`) to decompile the wasm binary and try to make sense of it. Running `wasm2wat` on the given binary reveals some interesting stuff. The flag seems to be obfuscated very heavily and it doesn't seem possible to decode it directly. However, we can try to change the score requirement of 10,000 to something lower.

On searching for 10,000, there are only a few matches. We can now hit-and-try all of these matches to see which one works by recompiling the app (using `wat2wasm` from `wabt`) and running the app. One of them will help you get the flag!

`Breach{r3vv1ng_w45m_15_fun}`
