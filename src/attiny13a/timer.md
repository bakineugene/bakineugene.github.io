# Timer/Counter

8-битный счётчик.

## Прерывания

См. раздел 9.1 *Interrupt Vectors* [ATtiny13A].

| Vector No. | Program Address | Source        | Interrupt Definition           |
|------------|-----------------|---------------|--------------------------------|
| 4          | 0x0003          | `TIM0_OVF`    | Timer/Counter Overflow         |
| 7          | 0x0006          | `TIM0_COMPA`  | Timer/Counter Compare Match A  |
| 8          | 0x0007          | `TIM0_COMPB`  | Timer/Counter Compare Match B  |

## Пины с функциями таймера

См. раздел 10.3.1 *Alternate Functions of Port B* [ATtiny13A].

| Port Pin | Alternate Function                          |
|----------|----------------------------------------------|
| PB2      | T0: Timer/Counter0 Clock Source              |
| PB1      | OC0B: Timer/Counter0 Compare Match B Output  |
| PB0      | OC0A: Timer/Counter0 Compare Match A Output  |

## References

- **[ATtiny13A]** ATtiny13A Datasheet, Microchip Technology, Rev. 8126F–AVR–05/12

