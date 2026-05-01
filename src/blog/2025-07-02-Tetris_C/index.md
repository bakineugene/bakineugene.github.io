---
title: "Tetris C"
date: 2025-07-02
author: Eugene
tags: ['avr', 'sound', 'tetris_c']
summary: "*22:13* Раздумываю о том, чтобы добавить звук. Нашел у себя два излучателя. Пьезоизлучатель и электромагнитный. Первый звучит погромче. Но вообще от 5 вольт оба слабовато работают."
---

*22:13*  
Раздумываю о том, чтобы добавить звук.

Нашел у себя два излучателя. Пьезоизлучатель и электромагнитный.
Первый звучит погромче. Но вообще от 5 вольт оба слабовато работают. Нужно по крайней мере 10 для хорошей громкости.

#tetris_c #sound
[Video: (File exceeds maximum size. Change data exporting settings to download.)]((File exceeds maximum size. Change data exporting settings to download.))

---

*22:13*  

[Video: (File exceeds maximum size. Change data exporting settings to download.)]((File exceeds maximum size. Change data exporting settings to download.))

---

*11:46*  
Внезапно я узнал, что плату в форм факторе ардуино уно нужно питать напряжением от 7 до 12 В. 
А я подавал 5 и питающее напряжение (как и напряжение на выходе ШИМ) в итоге было = 3.3В.
RTFM

В общем я попробовал оба излучателя уже при работе с МК и теперь мне кажется, что громче звучит HC12G.

Музычка отсюда: [https://radioparty.ru/programming/avr/c/284-lesson12-music](https://radioparty.ru/programming/avr/c/284-lesson12-music)
Но нужно будет чтобы звуки производились "в фоне"
+ Сначала я заметил, что HC12G жрет 0.1А даже когда не звучит. Оказалось, что код оставляет пин в состоянии логической 1 при отсутствии музыки
Нужно добавить сброс пина в 0 при окончании проигрывания ноты

Сейчас мне уже кажется, что громкости достаточно

#avr #sound
[Video: videos/video_5@03-07-2025_11-46-59.mp4](videos/video_5@03-07-2025_11-46-59.mp4)

---

*11:47*  

[Video: videos/video_6@03-07-2025_11-47-00.mp4](videos/video_6@03-07-2025_11-47-00.mp4)