---
title: "Attiny"
date: 2026-01-02
author: Eugene
tags: ['attiny']
summary: "*00:21* Применил на практике обработчик нажатия, добавив переключатель цветовых режимов для гирлянды. В PROGMEM хранятся две формы волны: более яркая, основной цвет менее яркая."
---

*00:21*  
[https://github.com/bakineugene/attiny13a_new_years_lights/compare/12097c8d8495b1b7e99758096c7da79458e863a9...3108f9a3afa8965de374c698513ea3e4a78e90d8](https://github.com/bakineugene/attiny13a_new_years_lights/compare/12097c8d8495b1b7e99758096c7da79458e863a9...3108f9a3afa8965de374c698513ea3e4a78e90d8)

Применил на практике обработчик нажатия, добавив переключатель цветовых режимов для гирлянды. 

В PROGMEM хранятся две формы волны:
`wave_hard` более яркая, основной цвет
`wave_soft` менее яркая. Используется как оттенок для смешанных режимов.

Всего добавил 9 режимов:
- 3 чистых цвета
- 6 комбинаций R,G,B. Один цвет основной, другой как оттенок.

```cpp
    uint8_t color[3] = {0, 0, 0};
    if (mode.soft != CH_0) color[mode.soft] = pgm_read_byte(&wave_soft[idx]); // idx - индекс шага
    if (mode.hard != CH_0) color[mode.hard] = pgm_read_byte(&wave_hard[idx]);
```

#attiny