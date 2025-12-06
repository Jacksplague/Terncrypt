<html>
<body>
<!--StartFragment--><h1 data-start="404" data-end="424">📘 <strong data-start="409" data-end="422">Terncrypt</strong></h1>
<h3 data-start="425" data-end="494"><em data-start="429" data-end="494">A balanced-ternary AEAD cipher and command-line encryption tool</em></h3>
<p data-start="496" data-end="793">Terncrypt is an experimental <strong data-start="525" data-end="580">balanced-ternary authenticated encryption algorithm</strong> implemented in Python.<br data-start="603" data-end="606">
It uses a custom AES-style block cipher operating on <strong data-start="659" data-end="678">108-trit blocks</strong>, combined with CTR mode and a ternary CBC-MAC to provide <strong data-start="736" data-end="792">AEAD (authenticated encryption with associated data)</strong>.</p>
<p data-start="795" data-end="877">Unlike binary ciphers, Terncrypt operates entirely on <strong data-start="849" data-end="876">balanced ternary digits</strong>:</p>
<pre class="overflow-visible!" data-start="879" data-end="907"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span><span class="hljs-deletion">-1 → T</span></span><span>
 0 → 0
</span><span><span class="hljs-addition">+1 → 1</span></span><span>
</span></span></code></div></div></pre>
<p data-start="909" data-end="1171">Although this system is mathematically interesting and fully functional, it is <strong data-start="988" data-end="1034">not intended for production-grade security</strong>. It is a research toy, a cryptographic art project, and a demonstration of what encryption might look like in a ternary computing world.</p>
<hr data-start="1173" data-end="1176">
<h1 data-start="1178" data-end="1191">🚀 Features</h1>
<h3 data-start="1193" data-end="1240">✔ Balanced-ternary symmetric block cipher</h3>
<ul data-start="1241" data-end="1548">
<li data-start="1241" data-end="1264">
<p data-start="1243" data-end="1264">108-trit block size</p>
</li>
<li data-start="1265" data-end="1304">
<p data-start="1267" data-end="1304">162-trit key (27 bytes → 162 trits)</p>
</li>
<li data-start="1305" data-end="1382">
<p data-start="1307" data-end="1382">AES-inspired structure (SubTrytes → ShiftRows → MixColumns → AddRoundKey)</p>
</li>
<li data-start="1383" data-end="1443">
<p data-start="1385" data-end="1443">S-Box defined via multiplicative inversion in <strong data-start="1431" data-end="1441">GF(3³)</strong></p>
</li>
<li data-start="1444" data-end="1490">
<p data-start="1446" data-end="1490">Diffusion via a 3×3 matrix over <strong data-start="1478" data-end="1488">GF(3³)</strong></p>
</li>
<li data-start="1491" data-end="1548">
<p data-start="1493" data-end="1548">Full key schedule (18 tryte words → 198 expanded words)</p>
</li>
</ul>
<h3 data-start="1550" data-end="1584">✔ AEAD mode (Encrypt-then-MAC)</h3>
<ul data-start="1585" data-end="1755">
<li data-start="1585" data-end="1624">
<p data-start="1587" data-end="1624">Encryption: <strong data-start="1599" data-end="1611">CTR mode</strong> over trits</p>
</li>
<li data-start="1625" data-end="1667">
<p data-start="1627" data-end="1667">Authentication: <strong data-start="1643" data-end="1665">CBC-MAC over trits</strong></p>
</li>
<li data-start="1668" data-end="1701">
<p data-start="1670" data-end="1701">Associated data (AAD) support</p>
</li>
<li data-start="1702" data-end="1755">
<p data-start="1704" data-end="1755">Tamper detection via constant-time MAC comparison</p>
</li>
</ul>
<h3 data-start="1757" data-end="1801">✔ Fully pip-installable Python package</h3>
<p data-start="1802" data-end="1817">Organized with:</p>
<pre class="overflow-visible!" data-start="1818" data-end="1855"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>pyproject.toml
src/terncrypt/
</span></span></code></div></div></pre>
<h3 data-start="1857" data-end="1889">✔ Clean, user-friendly CLI</h3>
<p data-start="1890" data-end="1904">After install:</p>
<pre class="overflow-visible!" data-start="1906" data-end="1984"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>terncrypt encrypt ...
terncrypt decrypt ...
terncrypt gen-keys ...
</span></span></code></div></div></pre>
<h3 data-start="1986" data-end="2023">✔ Binary-safe ciphertext format</h3>
<p data-start="2024" data-end="2059">Ternary ciphertext is packed using:</p>
<ul data-start="2060" data-end="2117">
<li data-start="2060" data-end="2084">
<p data-start="2062" data-end="2084">4-byte length header</p>
</li>
<li data-start="2085" data-end="2117">
<p data-start="2087" data-end="2117">Base-3 → base-256 conversion</p>
</li>
</ul>
<p data-start="2119" data-end="2157">Makes ciphertext compact and portable.</p>
<hr data-start="2159" data-end="2162">
<h1 data-start="2164" data-end="2181">📦 Installation</h1>
<h3 data-start="2183" data-end="2216">Install from a local checkout</h3>
<pre class="overflow-visible!" data-start="2217" data-end="2245"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>pip install -e .
</span></span></code></div></div></pre>
<p data-start="2247" data-end="2286">(Use <code data-start="2252" data-end="2263">py -m pip</code> on Windows if needed.)</p>
<h3 data-start="2288" data-end="2347">After install, the following command becomes available:</h3>
<pre class="overflow-visible!" data-start="2348" data-end="2369"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>terncrypt
</span></span></code></div></div></pre>
<hr data-start="2371" data-end="2374">
<h1 data-start="2376" data-end="2395">🔐 Key Generation</h1>
<p data-start="2397" data-end="2449">Terncrypt uses <strong data-start="2412" data-end="2424">two keys</strong>, each <strong data-start="2431" data-end="2443">27 bytes</strong> long:</p>
<ul data-start="2451" data-end="2506">
<li data-start="2451" data-end="2482">
<p data-start="2453" data-end="2482"><strong data-start="2453" data-end="2471">Encryption key</strong> (CTR mode)</p>
</li>
<li data-start="2483" data-end="2506">
<p data-start="2485" data-end="2506"><strong data-start="2485" data-end="2496">MAC key</strong> (CBC-MAC)</p>
</li>
</ul>
<p data-start="2508" data-end="2522">Generate both:</p>
<pre class="overflow-visible!" data-start="2524" data-end="2576"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>terncrypt gen-keys -k enc.key -m mac.key
</span></span></code></div></div></pre>
<p data-start="2578" data-end="2610">Overwrite existing files safely:</p>
<pre class="overflow-visible!" data-start="2612" data-end="2667"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>terncrypt gen-keys -k enc.key -m mac.key -f
</span></span></code></div></div></pre>
<hr data-start="2669" data-end="2672">
<h1 data-start="2674" data-end="2689">🔒 Encryption</h1>
<pre class="overflow-visible!" data-start="2691" data-end="2853"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>terncrypt encrypt \
  -i plaintext.bin \
  -o ciphertext.tenc \
  -t ciphertext.tag \
  -k enc.key \
  -m mac.key \
  -n 12345 \
  -a optional_aad.bin
</span></span></code></div></div></pre>
<ul data-start="2855" data-end="3059">
<li data-start="2855" data-end="2915">
<p data-start="2857" data-end="2915"><code data-start="2857" data-end="2874">ciphertext.tenc</code> contains the packed ternary ciphertext</p>
</li>
<li data-start="2916" data-end="2968">
<p data-start="2918" data-end="2968"><code data-start="2918" data-end="2934">ciphertext.tag</code> contains the authentication tag</p>
</li>
<li data-start="2969" data-end="3016">
<p data-start="2971" data-end="3016">The nonce <strong data-start="2981" data-end="3014">must be reused for decryption</strong></p>
</li>
<li data-start="3017" data-end="3059">
<p data-start="3019" data-end="3059">AAD is authenticated but <em data-start="3044" data-end="3059">not encrypted</em></p>
</li>
</ul>
<hr data-start="3061" data-end="3064">
<h1 data-start="3066" data-end="3081">🔓 Decryption</h1>
<pre class="overflow-visible!" data-start="3083" data-end="3245"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>terncrypt decrypt \
  -i ciphertext.tenc \
  -t ciphertext.tag \
  -o recovered.bin \
  -k enc.key \
  -m mac.key \
  -n 12345 \
  -a optional_aad.bin
</span></span></code></div></div></pre>
<p data-start="3247" data-end="3273">If the tag does not match:</p>
<pre class="overflow-visible!" data-start="3275" data-end="3323"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span><span class="hljs-selector-attr">[!]</span></span><span> Authentication failed (tag mismatch)
</span></span></code></div></div></pre>
<p data-start="3325" data-end="3374">Terncrypt never outputs plaintext on MAC failure.</p>
<hr data-start="3376" data-end="3379">
<h1 data-start="3381" data-end="3411">🧠 Balanced Ternary Overview</h1>
<p data-start="3413" data-end="3446">Balanced ternary uses the digits:</p>
<div class="TyagGW_tableContainer"><div tabindex="-1" class="group TyagGW_tableWrapper flex w-fit flex-col-reverse">
Value | Trit
-- | --
-1 | T
0 | 0
+1 | 1

</div></div>
<p data-start="3534" data-end="3602">Arithmetic is performed modulo 3, mapping <code data-start="3576" data-end="3583">T → 2</code>, <code data-start="3585" data-end="3592">1 → 1</code>, <code data-start="3594" data-end="3601">0 → 0</code>.</p>
<p data-start="3604" data-end="3713">This makes ternary addition analogous to XOR in binary ciphers—but with three possible states instead of two.</p>
<p data-start="3715" data-end="3869">Terncrypt internally represents trytes as elements of <strong data-start="3769" data-end="3779">GF(3³)</strong>, allowing full S-box and MixColumns operations analogous to AES but over a ternary field.</p>
<hr data-start="3871" data-end="3874">
<h1 data-start="3876" data-end="3896">🧮 Cipher Overview</h1>
<h3 data-start="3898" data-end="3914">Block size</h3>
<p data-start="3915" data-end="3969">108 trits → 36 trytes → 3×12 matrix of GF(3³) elements</p>
<h3 data-start="3971" data-end="3985">Key size</h3>
<p data-start="3986" data-end="4007">162 trits → 54 trytes</p>
<h3 data-start="4009" data-end="4029">Round function</h3>
<pre class="overflow-visible!" data-start="4030" data-end="4347"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span><span class="hljs-keyword">state</span></span><span> = AddRoundKey(</span><span><span class="hljs-keyword">state</span></span><span>, round_keys[</span><span><span class="hljs-number">0</span></span><span>])

</span><span><span class="hljs-keyword">for</span></span><span> r = </span><span><span class="hljs-number">1</span></span><span>..</span><span><span class="hljs-number">9</span></span><span>:
    </span><span><span class="hljs-keyword">state</span></span><span> = SubTrytes(</span><span><span class="hljs-keyword">state</span></span><span>)
    </span><span><span class="hljs-keyword">state</span></span><span> = ShiftRows(</span><span><span class="hljs-keyword">state</span></span><span>)
    </span><span><span class="hljs-keyword">state</span></span><span> = MixColumns(</span><span><span class="hljs-keyword">state</span></span><span>)
    </span><span><span class="hljs-keyword">state</span></span><span> = AddRoundKey(</span><span><span class="hljs-keyword">state</span></span><span>, round_keys[r])

Final round:
    </span><span><span class="hljs-keyword">state</span></span><span> = SubTrytes(</span><span><span class="hljs-keyword">state</span></span><span>)
    </span><span><span class="hljs-keyword">state</span></span><span> = ShiftRows(</span><span><span class="hljs-keyword">state</span></span><span>)
    </span><span><span class="hljs-keyword">state</span></span><span> = AddRoundKey(</span><span><span class="hljs-keyword">state</span></span><span>, round_keys[</span><span><span class="hljs-number">10</span></span><span>])
</span></span></code></div></div></pre>
<h3 data-start="4349" data-end="4370">AEAD mode outline</h3>
<pre class="overflow-visible!" data-start="4371" data-end="4473"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span><span class="hljs-attr">ciphertext</span></span><span> = CTR(key_enc, nonce, plaintext)
</span><span><span class="hljs-attr">tag</span></span><span> = CBC-MAC(key_mac, AAD || nonce || ciphertext)
</span></span></code></div></div></pre>
<hr data-start="4475" data-end="4478">
<h1 data-start="4480" data-end="4499">⚠️ Security Notes</h1>
<p data-start="4501" data-end="4569">Terncrypt is <strong data-start="4514" data-end="4568">not intended for real-world cryptographic security</strong>.</p>
<p data-start="4571" data-end="4663">It has not been analyzed by cryptographers and should not be used to protect sensitive data.</p>
<p data-start="4665" data-end="4673">Reasons:</p>
<ul data-start="4675" data-end="4974">
<li data-start="4675" data-end="4738">
<p data-start="4677" data-end="4738">Novel balanced-ternary S-box may have exploitable structure</p>
</li>
<li data-start="4739" data-end="4807">
<p data-start="4741" data-end="4807">Round count (10) chosen for experimentation, not proven security</p>
</li>
<li data-start="4808" data-end="4867">
<p data-start="4810" data-end="4867">Field GF(3³) operations haven't undergone cryptanalysis</p>
</li>
<li data-start="4868" data-end="4931">
<p data-start="4870" data-end="4931">CBC-MAC construction is simple and works but isn’t hardened</p>
</li>
<li data-start="4932" data-end="4974">
<p data-start="4934" data-end="4974">Side-channel resistance not considered</p>
</li>
</ul>
<p data-start="4976" data-end="5001">This project is meant as:</p>
<ul data-start="5003" data-end="5109">
<li data-start="5003" data-end="5035">
<p data-start="5005" data-end="5035">a cryptographic research toy</p>
</li>
<li data-start="5036" data-end="5068">
<p data-start="5038" data-end="5068">an educational demonstration</p>
</li>
<li data-start="5069" data-end="5109">
<p data-start="5071" data-end="5109">an experiment in ternary computation</p>
</li>
</ul>
<hr data-start="5111" data-end="5114">
<h1 data-start="5116" data-end="5147">🧪 Example: Encrypting a file</h1>
<pre class="overflow-visible!" data-start="5149" data-end="5320"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>terncrypt gen-keys -k enc.key -m mac.key

terncrypt encrypt \
  -i image.jpg \
  -o image.jpg.tenc \
  -t image.jpg.tag \
  -k enc.key \
  -m mac.key \
  -n 42
</span></span></code></div></div></pre>
<p data-start="5322" data-end="5333">Decryption:</p>
<pre class="overflow-visible!" data-start="5335" data-end="5474"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>terncrypt decrypt \
  -i image.jpg.tenc \
  -t image.jpg.tag \
  -o image_recovered.jpg \
  -k enc.key \
  -m mac.key \
  -n 42
</span></span></code></div></div></pre>
<hr data-start="5476" data-end="5479">
<h1 data-start="5481" data-end="5497">🛠 Development</h1>
<p data-start="5499" data-end="5516">Install dev copy:</p>
<pre class="overflow-visible!" data-start="5518" data-end="5546"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>pip install -e .
</span></span></code></div></div></pre>
<p data-start="5548" data-end="5589">Run tests (if we build you a test suite):</p>
<pre class="overflow-visible!" data-start="5591" data-end="5609"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>pytest
</span></span></code></div></div></pre>
<hr data-start="5611" data-end="5614">
<h1 data-start="5616" data-end="5628">📄 License</h1>
<p data-start="5630" data-end="5712">MIT License</p>
<hr data-start="5714" data-end="5717">
<h1 data-start="5719" data-end="5731">🙌 Credits</h1>
<p data-start="5733" data-end="5778">Terncrypt was created as an exploration into:</p>
<ul data-start="5780" data-end="5965">
<li data-start="5780" data-end="5811">
<p data-start="5782" data-end="5811">balanced ternary arithmetic</p>
</li>
<li data-start="5812" data-end="5862">
<p data-start="5814" data-end="5862">AES-style cipher design in a non-binary domain</p>
</li>
<li data-start="5863" data-end="5919">
<p data-start="5865" data-end="5919">experimenting with GF(3³) substitution and diffusion</p>
</li>
<li data-start="5920" data-end="5965">
<p data-start="5922" data-end="5965">constructing a full ternary AEAD pipeline</p></li></ul><!--EndFragment-->
</body>
</html>
