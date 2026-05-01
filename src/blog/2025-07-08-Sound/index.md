---
title: "Sound"
date: 2025-07-08
author: Eugene
tags: ['avr', 'sound']
summary: "*11:49* #sound #avr Генерация звука на avr На пьезодинамике, конечно, голос совсем не слышно. Но звяк от кружки слышно неплохо"
---

*11:49*
#sound #avr

Генерация звука на avr

На пьезодинамике, конечно, голос совсем не слышно. Но звяк от кружки слышно неплохо
[Video: videos/video_7@08-07-2025_11-49-43.mp4](videos/video_7@08-07-2025_11-49-43.mp4)

---

*11:49*  

[Video: videos/video_8@08-07-2025_11-49-43.mp4](videos/video_8@08-07-2025_11-49-43.mp4)

---

*11:52*  
#sound #avr

Как это работает

[https://github.com/bakineugene/sounds_experiments_avr/blob/1d22a4c5126b14fa07055e3f41fd8013c0f2669d/avr_main.c](https://github.com/bakineugene/sounds_experiments_avr/blob/1d22a4c5126b14fa07055e3f41fd8013c0f2669d/avr_main.c)

Задейстовано два таймера (из 3 доступных)

```
● Peripheral features:
● Two 8-bit Timer/Counters with separate prescaler and compare mode
● One 16-bit Timer/Counter with separate prescaler, compare mode, and capture mode
```

```c
void setupTimer1_PWM() {
    DDRB |= (1 << PB1);       // PB1 (OC1A) как выход
    TCCR1A = (1 << COM1A1) | (1 << WGM11);
    TCCR1B = (1 << WGM13) | (1 << WGM12) | (1 << CS10);  // Fast PWM, режим 14
    ICR1 = PWM_TOP;
}
```

Таймер_1 - высокоточный, 16 битный.
Он используется в данном случае для генерации ШИМ сигнала определенной частоты.
Преобразование ШИМ сигнала в звук происходит, судя по всему за счет того, что излучатель и сам своего рода ФНЧ.

Таймер работает в режиме fast pwm (задается битами WGM11, WGM12, WGM13) - т.е. при достижении счетчиком необходимого значения на выводе ОС1A выставляется 1. А при переполнении счетчика высталяется 0. Таким образом мы можем регулировать коэффициент заполнения. 

ICR1 определяет верхнее значение счетчика и задает частоту. Здесь главное, чтобы частоты не перешли в слышимую область. 

```c
void setupTimer0_Interrupt() {
    TCCR0A = (1 << WGM01);   // CTC режим
    TCCR0B = (1 << CS01);    // Предделитель /8
    OCR0A = (F_CPU / 8 / SAMPLE_RATE) - 1;
    TIMSK0 = (1 << OCIE0A);  // Разрешить прерывание
}
```

Второй таймер (timer_0) работает в другом режиме - после достижения значения OCR0A счетчик сбрасывается в 0 и активируется прерывание. Значение OCR0A выставляется равным длине семпла. Таким образом в каждом обработчике прерывания мы переключаем семпл - т.е. меняем коэффициент заполнения для первого таймера.

```c
ISR(TIMER0_COMPA_vect) {
    if (queue_head != queue_end) {
        Sound current_sound = queue[queue_head];
        if (currentSample < current_sound.length) {
            uint8_t sample = pgm_read_byte(&current_sound.start[currentSample++]);
            OCR1A = sample;
        } else {
            ++queue_head;
            currentSample = 0;
        }
    } else {
        TIMSK0 &= ~(1 << OCIE0A);
    }
}
```