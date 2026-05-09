---
title: "AVR под Linux"
date: 2025-06-08
tags: ['avr', 'max7219']
summary: "Общая информация и коллекция ссылок по работе с AVR и MAX7219 под линуксом"
---

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

Справочники по AVR:  
[https://github.com/amirbawab/AVR-cheat-sheet](https://github.com/amirbawab/AVR-cheat-sheet)  
[https://en.wikipedia.org/wiki/Atmel_AVR_instruction_set](https://en.wikipedia.org/wiki/Atmel_AVR_instruction_set)  
[http://www.gaw.ru/html.cgi/txt/doc/micros/avr/asm/start.htm](http://www.gaw.ru/html.cgi/txt/doc/micros/avr/asm/start.htm)  

Программирование AVR на C  
[https://narodstream.ru/programmirovanie-mk-avr/](https://narodstream.ru/programmirovanie-mk-avr/)  
[https://ph0en1x.net/67-avr-microcontrollers-programming-in-linux-with-assembler-and-c.html](https://ph0en1x.net/67-avr-microcontrollers-programming-in-linux-with-assembler-and-c.html)  

Ссылки по работе с LED матрицами под управлением MAX7219:

Про max7219, но не про матрицы, а про 7 сегментные индикаторы  
[https://narodstream.ru/avr-urok-28-spi-drajver-led-max7219/](https://narodstream.ru/avr-urok-28-spi-drajver-led-max7219/)  
[https://gist.github.com/adnbr/2352797](https://gist.github.com/adnbr/2352797)  
[https://dzen.ru/a/XydXNDaFGS4R-8n-](https://dzen.ru/a/XydXNDaFGS4R-8n-)  
[http://avr-start.ru/?p=3788](http://avr-start.ru/?p=3788)  

Тут уже про матрицы:  
[https://embeddedthoughts.com/2016/04/19/scrolling-text-on-the-8x8-led-matrix-with-max7219-drivers/](https://embeddedthoughts.com/2016/04/19/scrolling-text-on-the-8x8-led-matrix-with-max7219-drivers/)  

На самом деле основным и лучшим источником информации при работе с МК AVR является официальная документация.  
Просто не сразу понимаешь как ее читать, но после определенного момента полностью пересел на нее.  

