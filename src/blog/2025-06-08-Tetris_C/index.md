---
title: "Tetris C"
date: 2025-06-08
author: Eugene
tags: ['avr', 'max7219', 'tetris_c']
summary: "*21:16* Добрался наконец до работы с atmega под линукс на C Здесь, в принципе, все описано gcc-avr - компилятор avr-libc - имплементация стандартной библиотеки для AVR ) avrdude - тулза для заливки..."
---

*21:16*  
Добрался наконец до работы с atmega под линукс на C

[https://www.tonymitchell.ca/posts/setup-avr-toolchain-on-linux/](https://www.tonymitchell.ca/posts/setup-avr-toolchain-on-linux/)

Здесь, в принципе, все описано
gcc-avr - компилятор
avr-libc - имплементация стандартной библиотеки для AVR [https://avr-libc.nongnu.org/user-manual/index.html](https://avr-libc.nongnu.org/user-manual/index.html))
avrdude - тулза для заливки в МК
```shell
sudo apt install make gcc-avr avr-libc avrdude
```

Код "мигалки"

```c
#include <avr/io.h>
#include <util/delay.h>

int main()
{
    // Set built-in LED pin as output
    DDRB |= (1 << DDB5);
    while (1) {
        PORTB |=  (1 << PB5);   // LED on
        _delay_ms(500);
        PORTB &= ~(1 << PB5);   // LED off
        _delay_ms(500);
    }
    return 0;
}

```

Команды для компиляции и заливки. Единственное я поменял программатор на usbasp

```shell
avr-gcc blink.c -o blink.elf -mmcu=atmega328p -DF_CPU=16000000UL -Os
avr-objcopy blink.elf -O ihex blink.hex
avrdude -c usbasp -p m328p -U flash:w:"blink.hex":a
```

Здесь  -DF_CPU=тактовая частота в Гц, 

#tetris_c #avr

---

*22:05*  
Небольшой курс программирования под AVR. В основном на ассемблере [https://easyelectronics.ru/category/avr-uchebnyj-kurs/page/5](https://easyelectronics.ru/category/avr-uchebnyj-kurs/page/5)
А здесь дополнение о том как  работать с AVR ассемблером под Линукс
[https://habr.com/ru/articles/373677/](https://habr.com/ru/articles/373677/)

Справочники по командам AVR
[https://pcbisolation.com/blog/atmel-coding-reference/](https://pcbisolation.com/blog/atmel-coding-reference/)
[https://github.com/amirbawab/AVR-cheat-sheet](https://github.com/amirbawab/AVR-cheat-sheet)
[https://en.wikipedia.org/wiki/Atmel_AVR_instruction_set](https://en.wikipedia.org/wiki/Atmel_AVR_instruction_set)
[http://www.gaw.ru/html.cgi/txt/doc/micros/avr/asm/start.htm](http://www.gaw.ru/html.cgi/txt/doc/micros/avr/asm/start.htm)

Программирование AVR на C
[https://atmega32-avr.com/programming-the-microchip-atmega328p-in-c/](https://atmega32-avr.com/programming-the-microchip-atmega328p-in-c/)
[https://narodstream.ru/programmirovanie-mk-avr/](https://narodstream.ru/programmirovanie-mk-avr/)
[https://ph0en1x.net/67-avr-microcontrollers-programming-in-linux-with-assembler-and-c.html](https://ph0en1x.net/67-avr-microcontrollers-programming-in-linux-with-assembler-and-c.html)

#tetris_c #avr

---

*22:05*  


---

*22:05*  


---

*10:02*  
Еще пачка ссылок. Теперь по работе с LED матрицами под управлением MAX7219

Про max7219, но не про матрицы, а про 7 сегментные индикаторы
[https://narodstream.ru/avr-urok-28-spi-drajver-led-max7219/](https://narodstream.ru/avr-urok-28-spi-drajver-led-max7219/) 
[https://gist.github.com/adnbr/2352797](https://gist.github.com/adnbr/2352797) 
[https://dzen.ru/a/XydXNDaFGS4R-8n-](https://dzen.ru/a/XydXNDaFGS4R-8n-)
[http://avr-start.ru/?p=3788](http://avr-start.ru/?p=3788)
[https://we.easyelectronics.ru/Theory/srednechastotnyy-chastotomer-na-avr-chast-2-staticheskaya-indikaciya.html](https://we.easyelectronics.ru/Theory/srednechastotnyy-chastotomer-na-avr-chast-2-staticheskaya-indikaciya.html)

Тут уже про матрицы
[https://embeddedthoughts.com/2016/04/19/scrolling-text-on-the-8x8-led-matrix-with-max7219-drivers/](https://embeddedthoughts.com/2016/04/19/scrolling-text-on-the-8x8-led-matrix-with-max7219-drivers/)
[https://tinusaur.com/tutorials/max7219-attiny85-interface/](https://tinusaur.com/tutorials/max7219-attiny85-interface/)
[https://www.avrfreaks.net/s/topic/a5C3l000000UV5JEAW/t133283](https://www.avrfreaks.net/s/topic/a5C3l000000UV5JEAW/t133283)
[https://habr.com/ru/articles/846656/](https://habr.com/ru/articles/846656/) - Про написание библиотеки для MAX7219, работающей с любым МК 

Edit - Отсеянное:
[http://1io.ru/articles/microcontroller/avr_max7219/](http://1io.ru/articles/microcontroller/avr_max7219/) - непонятно, что за библиотека используется

#tetris_c #avr #max7219