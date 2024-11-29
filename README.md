# [Nand2Tetris](https://www.nand2tetris.org)

    From Nand to Tetris
    Building a Modern Computer From First Principles

В этом репозитории я сохраняю свои работы в ходе прохождения курса [nand2tetris](https://www.nand2tetris.org)

Курс состоит из двух частей, в первой части 6 проектов:
- [Project 1: Boolean Logic](./Assignments/1_Boolean_Logic)
    > Реализация [NAND-логики](https://en.wikipedia.org/wiki/NAND_logic), то есть создание основных логических блоков (AND, OR, NOT, XOR, MUX, DMUX, а так же их версий для работы с 16-битной шиной) с помощью операции NAND ([И-НЕ или Штрих Шеффера](https://ru.wikipedia.org/wiki/Штрих_Шеффера))
- [Project 2: Boolean Arithmetic](./Assignments/2_Boolean_Arithmetic/)
    > Создание [простого арифметико-логического устройства (ALU)](./Assignments/2_Boolean_Arithmetic/ALU.hdl) с помощью логических блоков из первого проекта, способного складывать и вычитать 16-битные числа
- [Project 3: Memory](./Assignments/3_Sequential_Logic/)
    > Вводим единицу времени - такт, за счёт чего появляется текущее и следующее состояние, которое можно запоминать и изменять. Создаём простейшую память. На основе DFF компонента создаём [однобитный регистр](./Assignments/3_Sequential_Logic/Bit.hdl), затем [16-битный регистр](./Assignments/3_Sequential_Logic/Register.hdl), из них собираем блоки оперативной памяти ([RAM8](./Assignments/3_Sequential_Logic/RAM8.hdl), [RAM64](./Assignments/3_Sequential_Logic/RAM64.hdl), [RAM512](./Assignments/3_Sequential_Logic/RAM512.hdl), [RAM4K](./Assignments/3_Sequential_Logic/RAM4K.hdl), [RAM16K](./Assignments/3_Sequential_Logic/RAM16K.hdl)), а так же создаём простой [счётчик](./Assignments/3_Sequential_Logic/PC.hdl), который может использоваться для хранения текущей выполняемой инструкции и перехода к новой инструкции
- Project 4: Machine Language
- Project 5: Computer Architecture
- Project 6: Assembler

## Основная идея курса в коротком видео:
[![](./cover.jpg)](https://youtu.be/wTl5wRDT0CU)