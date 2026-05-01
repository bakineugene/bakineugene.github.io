---
title: "Avr"
date: 2026-01-20
author: Eugene
tags: ['attiny', 'avr', 'avrlibc', 'eeprom']
summary: "*22:53* **AVR EEPROM programming** В AVR-libc есть очень удобная обертка над EEPROM и я поленился досконально разбираться в работе с регистрами."
---

*22:53*  
**AVR EEPROM programming**

В AVR-libc есть очень удобная обертка над EEPROM и я поленился досконально разбираться в работе с регистрами.  

Документация:
[https://avrdudes.github.io/avr-libc/avr-libc-user-manual/group__avr__eeprom.html](https://avrdudes.github.io/avr-libc/avr-libc-user-manual/group__avr__eeprom.html)

Header:
[https://github.com/avrdudes/avr-libc/blob/main/include/avr/eeprom.h](https://github.com/avrdudes/avr-libc/blob/main/include/avr/eeprom.h)

Assembler implementation eeprom_read_byte (attiny13a):
[https://github.com/avrdudes/avr-libc/blob/41441baa6adb440c52c0243058e2931c8160fed9/libc/misc/eerd_byte.S#L87](https://github.com/avrdudes/avr-libc/blob/41441baa6adb440c52c0243058e2931c8160fed9/libc/misc/eerd_byte.S#L87)

Для определенного списка стандартных типов есть набор из функций `read`, `write`, `update`;
`read`, `write` - говорят сами за себя
`update` сперва проверяет, что значение отличается от желаемого, и только затем пишет в eeprom.

Каждая из функций доступа к EEPROM сперва ждет (в цикле), пока память не будет готова к работе
```
1:  sbic    _SFR_IO_ADDR (EECR), EEWE
    rjmp    1b
```
```
All of the read/write functions first make sure the EEPROM is ready to be accessed. Since this may cause long delays if a write operation is still pending, time-critical applications should first poll the EEPROM e. g. using eeprom_is_ready() before attempting any actual I/O.
```

Переменные, которые следует поместить в `EEPROM`, помечаются через `EEMEM` макрос.
Затем указатели на эти переменные используются при вызове eeprom_xxx функций.

Пример:

```c
#include <avr/eeprom.h>

// Определения для uint8_t
uint8_t    eeprom_read_byte   (const uint8_t *__p)
void       eeprom_write_byte  (uint8_t *__p, uint8_t __value)
void       eeprom_update_byte (uint8_t *__p, uint8_t __value)

// Объявляем переменные, которые будут храниться в eeprom (по аналогии с PROGMEM)

uint8_t EEMEM some_variable = 41;

int main(void) {

    eeprom_write_byte(&some_variable, 42);

    // Update проверяет, что значение уже соответствует желаемому и запись не делает
    eeprom_update_byte(&some_variable, 42);

    uint8_t value = eeprom_read_byte(&some_variable);

}
```

Переменные могут быть инициализированы. Результат инициализации будет содержаться в .elf файле в секции .eeprom
Затем его нужно вытащить с помощью `avr-objcopy` и залить в МК
Иначе eeprom не будет инициализирован указанными значениями.
С завода память заполнена `0xFF`, а после использования там может содержаться что угодно.

```shell
avr-objcopy -O ihex -j .eeprom --set-section-flags=.eeprom=alloc,load --no-change-warnings --change-section-lma .eeprom=0 ./main.elf ./main.eep

avrdude -c usbasp -p t13 -U eeprom:w:"./main.eep":i
```

Аналогичным образом eeprom можно считать с МК

```shell
avrdude -c usbasp -p t13 -U eeprom:r:"./dump.eep":i
```

#avr #eeprom #attiny #avrlibc

---

*08:53*  
Результат 

Дефолтный красный цвет был изменён на синий с зелёным оттенком.

Разноцветные мигания - импровизированная индикация сохранения.

Короткое нажатие - смена режима
Длинное нажатие - save settings
[Video: videos/video_15@21-01-2026_08-53-13.mp4](videos/video_15@21-01-2026_08-53-13.mp4)

---

*10:27*  
[https://github.com/bakineugene/attiny13a_new_years_lights/blob/444d1a0762b828f1e80838ef16e4f867794d196d/main.c](https://github.com/bakineugene/attiny13a_new_years_lights/blob/444d1a0762b828f1e80838ef16e4f867794d196d/main.c)

**Обработка долгого нажатия для сохранения настроек**

Работать с debounce через включение/отключение двух прерываний оказалось неудобно.
Тут я вспомнил про SysTick и про то, что в FreeRTOS для AVR в качестве SysTick используется как раз watchdog (оказалось, что это не так 🤔).

Установил WDT на минимальный период срабатывания (примерно 16 ms, но точности никто не обещает) и настроил определение нажатия через количество "тиков" между событиями.

```c
#define LONG_PRESS 50 // ~ 800ms
#define SINGLE_PRESS 3 // ~ 48 ms

ISR(PCINT0_vect) {
    if (PINB_GET(PB4)) {
        if (button_tick_counter > LONG_PRESS) {
            // long press logic
        } else if (button_tick_counter > SINGLE_PRESS) {
            // short press logic
        }
    }
    button_tick_counter = 0;
}

ISR(WDT_vect) {
    ++button_tick_counter;
}
```

**Сохранение режима**

Все мои настройки - это 1 байт mode_num.

```c
volatile uint8_t mode_num = 0;
```

Если сохранять его в одну и ту же ячейку, то при 100 сохранениях в год - ресурса хватит всего на 1000 лет.
Другое дело - если позаботиться о wear leveling. Тогда гирлянда запросто прослужит 64000 лет.  🤔

После нескольких попыток сумничать у меня получился такой вариант - при записи ищем новое место для хранения настроек, а старое стираем.

```c
#define UNDEFINED 0xFF

uint8_t EEMEM ee_values[EE_SIZE] = {
    UNDEFINED, UNDEFINED, UNDEFINED, UNDEFINED, UNDEFINED, UNDEFINED, UNDEFINED, UNDEFINED,
    // ...
    UNDEFINED, UNDEFINED, UNDEFINED, UNDEFINED, UNDEFINED, UNDEFINED, UNDEFINED, UNDEFINED
};

// save:
eeprom_update_byte(&ee_values[previous_cell_idx], UNDEFINED);
eeprom_update_byte(&ee_values[cell_idx], mode_num);

// load:
for (int i = 0; i < EE_SIZE; ++i) {
    uint8_t value = eeprom_read_byte(&ee_values[i]);
    if (value != UNDEFINED) {
        cell_idx = i;
        mode_num = value;
    }
}
```

Размер прошивки уже близок к лимиту

```
avrdude: 958 bytes of flash verified
```

**Дальнейшие планы?**

Наблюдая за гирляндой я понял, что мне не нравится эффект "волны", хочется добавить рандома, чтобы казалось, что лампочки гаснут и зажигаются независимо.
Если череcчур пристально наблюдать - то становится заметно, что лампочки меняют цвет "скачками" - можно добавить интерполяцию.
Что из этого влезет в оставшиеся 66 байт (или больше, если упростить работу с eeprom) - не знаю пока.

Елку можно со спокойной душой собирать.

🎄👋

#eeprom #attiny #avr #avrlibc