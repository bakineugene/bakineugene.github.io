---
title: "Avr"
date: 2026-02-16
author: Eugene
tags: ['attiny', 'avr', 'pwm', 'timer']
summary: "*12:31* Просматривал свои телеграмные конспекты и пришёл к выводу, что держать их здесь неудобно. Тут и ограничение по объёму, и нет возможности вставить изображение посреди текста."
---

*12:31*  
Просматривал свои телеграмные конспекты и пришёл к выводу, что держать их здесь неудобно.
Тут и ограничение по объёму, и нет возможности вставить изображение посреди текста.

Но писать конспекты в электронном виде мне, внезапно, понравилось.
Конспекты лекций на бумаге мне никогда не помогали. 
А возможность упорядочить информацию, пусть даже только для себя, с возможностью вносить правки - бесценно.

Видимо, для этого люди используют Notion и Obsidian 🤔

В качестве эксперимента закинул новый конспект/шпаргалку на github.pages:

ATtiny13A Timers - [https://bakineugene.github.io/attiny13a/timer.html](https://bakineugene.github.io/attiny13a/timer.html)

Пока что без информации по PWM.

Highlights:

**prescaler**
У `AVR` очень бедный prescaler, по сравнению с `STM32`. Варианты: 1, 8, 64, 256, 1024.
Это даже не все степени двойки.
Кроме того, prescaler работает только с внутренним источником тактирования.

**while(a < 100) {}**
Из разряда "конструкции, которые взрывают мозг неподготовленному человеку". 
Объясняешь своему мозгу: "тут все в порядке", смотришь в следующий раз - и опять глаз дергается.
Видимо из-за того, что я в основном с однопоточным кодом работал.

```c
ISR(TIM0_COMPA_vect) {
    ++delay_counter;
}

volatile uint32_t delay_counter = 0;
void delay(uint32_t value) {
    delay_counter = 0;
    while (delay_counter < value) {}
}
```

#avr #timer #attiny

---

*23:42*  
Edge Aligned PWM | AVR Fast PWM
vs
Center Aligned PWM | AVR Phase Correct PWM

#pwm
[Video: videos/Edge Aligned.mp4](videos/Edge Aligned.mp4)

---

*23:42*  

[Video: videos/Center Aligned.mp4](videos/Center Aligned.mp4)

---

*20:38*  

[Video: videos/video_17@17-02-2026_20-38-20.mp4](videos/video_17@17-02-2026_20-38-20.mp4)

---

*20:38*  

![Photo](images/photo_68@17-02-2026_20-38-20.jpg)