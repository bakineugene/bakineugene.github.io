## ATtiny13A pinout


```{=html}
<div id="attiny13a-pinout">
<svg xmlns="http://www.w3.org/2000/svg" width="720" height="420" viewBox="0 0 720 420">
  <defs>
    <!-- Metallic lead gradient -->
    <linearGradient id="leadGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0"   stop-color="#8f8f8f"/>
      <stop offset="0.22" stop-color="#e6e6e6"/>
      <stop offset="0.55" stop-color="#bdbdbd"/>
      <stop offset="1"   stop-color="#7f7f7f"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="1.2" stdDeviation="1.2" flood-color="#000" flood-opacity="0.25"/>
    </filter>
  </defs>
  <style>
    .chip { fill:#2f2f2f; stroke:#111; stroke-width:2.2; }
    .notch { fill:#1f1f1f; stroke:#0f0f0f; stroke-width:2.2; }

    .lead { fill:url(#leadGrad); stroke:#4b4b4b; stroke-width:1.2; }
    .leadCap { fill:#1f1f1f; stroke:#4b4b4b; stroke-width:1.2; }

    .pinlabel { font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial; fill:#111; }
    .pinnum { font-size:14px; font-weight:900; }
    .pinfns  { font-size:12px; fill:#333; }

    /* markings on the package */
    .marking { font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial; fill:#c7c7c7; }
    .marking-title { font-size:18px; font-weight:850; letter-spacing:0.6px; }
    .marking-small { font-size:12px; font-weight:850; opacity:0.95; }

    .title { font-size:18px; font-weight:800; }
    .hint { font-size:12px; fill:#444; }

    .clickable { cursor: pointer; }
    .clickable:hover .lead { filter:url(#softShadow); }
  </style>

  <!-- Title -->
  <text x="360" y="42" text-anchor="middle" class="pinlabel title">ATtiny13A — Pinout (DIP-8, top view)</text>

  <!-- Chip body -->
  <rect x="250" y="110" width="220" height="260" rx="18" class="chip"/>
  <!-- Notch -->
  <path class="notch" d="M 315 110 A 45 45 0 0 0 405 110 Z"/>

  <!-- Package markings -->
  <text x="360" y="220" text-anchor="middle" class="marking marking-title">ATtiny13A</text>


  <!-- Pin names ON the package (only PBx / VCC / GND) -->
  <!-- Left side (1..4) -->
  <text x="270" y="143" text-anchor="start" class="marking marking-small">PB5</text>
  <text x="270" y="210" text-anchor="start" class="marking marking-small">PB3</text>
  <text x="270" y="276" text-anchor="start" class="marking marking-small">PB4</text>
  <text x="270" y="346" text-anchor="start" class="marking marking-small">GND</text>

  <!-- Right side (8..5) -->
  <text x="450" y="143" text-anchor="end" class="marking marking-small">VCC</text>
  <text x="450" y="210" text-anchor="end" class="marking marking-small">PB2</text>
  <text x="450" y="276" text-anchor="end" class="marking marking-small">PB1</text>
  <text x="450" y="346" text-anchor="end" class="marking marking-small">PB0</text>

 
  <!-- LEFT leads (pins 1..4) -->
  <!-- Pin 1: PB5 -->
  <g id="pin-1" data-pin="PB5" class="clickable">
    <!-- lead -->
    <rect x="170" y="120" width="85" height="36" rx="6" class="lead"/>
    <!-- small cap near the body -->
    <rect x="248" y="120" width="6" height="36" rx="2" class="leadCap"/>
    <!-- number -->
    <text x="182" y="143" class="pinlabel pinnum">1</text>
    <!-- functions outside -->
    <text x="150" y="144" text-anchor="end" class="pinlabel pinfns">RESET / ADC0 / dW / PCINT5</text>
  </g>

  <!-- Pin 2: PB3 -->
  <g id="pin-2" data-pin="PB3" class="clickable">
    <rect x="170" y="188" width="85" height="36" rx="6" class="lead"/>
    <rect x="248" y="188" width="6" height="36" rx="2" class="leadCap"/>
    <text x="182" y="211" class="pinlabel pinnum">2</text>
    <text x="150" y="212" text-anchor="end" class="pinlabel pinfns">ADC3 / CLKI / PCINT3</text>
  </g>

  <!-- Pin 3: PB4 -->
  <g id="pin-3" data-pin="PB4" class="clickable">
    <rect x="170" y="256" width="85" height="36" rx="6" class="lead"/>
    <rect x="248" y="256" width="6" height="36" rx="2" class="leadCap"/>
    <text x="182" y="279" class="pinlabel pinnum">3</text>
    <text x="150" y="280" text-anchor="end" class="pinlabel pinfns">ADC2 / PCINT4</text>
  </g>

  <!-- Pin 4: GND -->
  <g id="pin-4" data-pin="GND" class="clickable">
    <rect x="170" y="324" width="85" height="36" rx="6" class="lead"/>
    <rect x="248" y="324" width="6" height="36" rx="2" class="leadCap"/>
    <text x="182" y="347" class="pinlabel pinnum">4</text>
  </g>

  <!-- RIGHT leads (pins 8..5) -->
  <!-- Pin 8: VCC -->
  <g id="pin-8" data-pin="VCC" class="clickable">
    <rect x="465" y="120" width="85" height="36" rx="6" class="lead"/>
    <rect x="465" y="120" width="6" height="36" rx="2" class="leadCap"/>
    <text x="538" y="143" text-anchor="end" class="pinlabel pinnum">8</text>
  </g>

  <!-- Pin 7: PB2 -->
  <g id="pin-7" data-pin="PB2" class="clickable">
    <rect x="465" y="188" width="85" height="36" rx="6" class="lead"/>
    <rect x="465" y="188" width="6" height="36" rx="2" class="leadCap"/>
    <text x="538" y="211" text-anchor="end" class="pinlabel pinnum">7</text>
    <text x="570" y="212" text-anchor="start" class="pinlabel pinfns">ADC1 / PCINT2</text>
  </g>

  <!-- Pin 6: PB1 -->
  <g id="pin-6" data-pin="PB1" class="clickable">
    <rect x="465" y="256" width="85" height="36" rx="6" class="lead"/>
    <rect x="465" y="256" width="6" height="36" rx="2" class="leadCap"/>
    <text x="538" y="279" text-anchor="end" class="pinlabel pinnum">6</text>
    <text x="570" y="280" text-anchor="start" class="pinlabel pinfns">OC0B / AIN1 / PCINT1</text>
  </g>

  <!-- Pin 5: PB0 -->
  <g id="pin-5" data-pin="PB0" class="clickable">
    <rect x="465" y="324" width="85" height="36" rx="6" class="lead"/>
    <rect x="465" y="324" width="6" height="36" rx="2" class="leadCap"/>
    <text x="538" y="347" text-anchor="end" class="pinlabel pinnum">5</text>
    <text x="570" y="348" text-anchor="start" class="pinlabel pinfns">OC0A / AIN0 / PCINT0</text>
  </g>
</svg>
</div>
```
