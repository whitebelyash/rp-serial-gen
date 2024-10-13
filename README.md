# rp-serial-gen
RP Serial Generator

#### I don't like being forced to use specific OS, because someone wants to "implement better security measures".  
#### And I don't like using a mod with VMP protected dll - wtf, why does a minecraft mod need a protected dll at all?

There was (is) a Minecraft server, which added a hwid protection system one day. That system used a Fabric mod with a windows dll protected with VMProtect. Mod itself wasn't obfuscated at all, so decompiling it and writing a stub was very trivial. I even wrote a server-side implementation (as plugin used a messages channel, which is easy), but it only checked for serial existence, validation wasn't implemented.  

As I said, mod used a dll dependency, which was packed/protected with VMProtect. ~~Decompiling~~ Analyzing VMProtect is uhh.. not trivial, as it virtualizes code, also adds VM protection and a antidebugger.  
I was testing everything in a VM (VMware, to be specific), this thing gave me a generic VMP error about running in a vm. Yes. Switching to KVM with vmhide args made it work without issues.  
Antidebug protection was harder to break, ScyllaHide wasn't working for me. But, then I found TitanHide, and... dll finally launched with x64dbg! 

Still, the code is obfuscated and virtualized. Add here is my inability to understand assembler at all (skill issue) and... was there any sense to do this at all? You'll say no, but...

Seems like memory contents wasn't encrypted, so I found two strings (and some other magic). One was decryptable with base64 (let it be "A"), other not ("B"), but they were similar, i.e. starting and ending with same magic.  
Then, with help of @artdeell, I managed to find a pattern, which converted base64-decoded string A into a B, which was a valid serial string.  
<sub>There was also a prefix "[RP-SERIAL]" concatenated to a serial in the start, was the server checking it or no - no one know...  </sub>  
I don't think this pattern is 100% indentical to dll's variant - I still don't know anything about magic strings in the end of a line. But...
I pasted a line into my client stub and... managed to the join server! From my Linux PC, yes.

Interesting things.  
So, here lies a Python script, which generates a valid ReProtect serial string.


--------------------------

Генерирует фейковый серийник для использования на одном сервере.
По сути - обход бана по железу.
Алгоритм вытащен из DLL, упакованной вмпротектом.
