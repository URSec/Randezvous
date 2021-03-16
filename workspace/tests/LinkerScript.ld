/*
 * GENERATED FILE - DO NOT EDIT
 * Copyright (c) 2008-2013 Code Red Technologies Ltd,
 * Copyright 2015, 2018-2019 NXP
 * (c) NXP Semiconductors 2013-2020
 * Generated linker script file for MIMXRT685S
 * Created from linkscript.ldt by FMCreateLinkLibraries
 * Using Freemarker v2.3.23
 * MCUXpresso IDE v11.2.1 [Build 4149] [2020-10-07]
 */

MEMORY
{
    /* Define each memory region */
    QSPI_FLASH (rx) : ORIGIN = 0x8000000, LENGTH = 0x4000000 /* 64M bytes (alias Flash) */
    SRAM       (rw) : ORIGIN = 0x20000000, LENGTH = 0x480000 /* 4608K bytes (alias RAM) */
}

/* Define a symbol for the top of each memory region */
__base_QSPI_FLASH = 0x8000000; /* QSPI_FLASH */
__base_Flash = 0x8000000; /* Flash */
__top_QSPI_FLASH = 0x8000000 + 0x4000000; /* 64M bytes */
__top_Flash = 0x8000000 + 0x4000000; /* 64M bytes */
__base_SRAM = 0x20000000; /* SRAM */
__base_RAM = 0x20000000; /* RAM */
__top_SRAM = 0x20000000 + 0x480000; /* 4608K bytes */
__top_RAM = 0x20000000 + 0x480000; /* 4608K bytes */

ENTRY(ResetISR)

SECTIONS
{
    /* Image Vector Table and Boot Data for booting from external flash */
    .boot_hdr : ALIGN(4)
    {
        FILL(0x00)
        __boot_hdr_start__ = ABSOLUTE(.);
        . = __boot_hdr_start__ + 0x400;
        __flash_conf_hdr_start__ = ABSOLUTE(.);
        KEEP(*(.flash_conf))
        __flash_conf_hdr_end__ = ABSOLUTE(.);
        . = __boot_hdr_start__ + 0x1000;
        __boot_hdr_end__ = ABSOLUTE(.);
    } > QSPI_FLASH

    /* Vector Table */
    .isr_vector : ALIGN(4)
    {
        __vectors_start__ = ABSOLUTE(.);
        KEEP(*(.isr_vector))
    } > QSPI_FLASH

    /* Global Section Table */
    .section_table : ALIGN(4)
    {
        __section_table_start = .;
        __data_section_table = .;
        LONG(LOADADDR(.data));
        LONG(    ADDR(.data));
        LONG(  SIZEOF(.data));
        __data_section_table_end = .;
        __bss_section_table = .;
        LONG(    ADDR(.bss));
        LONG(  SIZEOF(.bss));
        __bss_section_table_end = .;
        __section_table_end = .;
    } > QSPI_FLASH

    /* MAIN TEXT SECTION */
    .text : ALIGN(4)
    {
        FILL(0xff)
        *(.after_vectors*)
        *(.text*)
    } > QSPI_FLASH

    .rodata : ALIGN(4)
    {
        *(.rodata .rodata.* .constdata .constdata.*)
    } > QSPI_FLASH

    .eh_frame : ALIGN(4)
    {
        *(.eh_frame)
    } > QSPI_FLASH

    /*
     * For exception handling/unwind - some Newlib functions (in common
     * with C++ and STDC++) use this.
     */
    .ARM.extab : ALIGN(4)
    {
        *(.ARM.extab* .gnu.linkonce.armextab.*)
    } > QSPI_FLASH

    .ARM.exidx : ALIGN(4)
    {
        __exidx_start = .;
        *(.ARM.exidx* .gnu.linkonce.armexidx.*)
        __exidx_end = .;
    } > QSPI_FLASH

    _etext = .;

    /* MAIN DATA SECTION */
    .uninit_RESERVED (NOLOAD) : ALIGN(4)
    {
        _start_uninit_RESERVED = .;
        KEEP(*(.bss.$RESERVED*))
        . = ALIGN(4);
        _end_uninit_RESERVED = .;
    } > SRAM AT> SRAM

    /* Main DATA section (SRAM) */
    .data : ALIGN(4)
    {
        FILL(0xff)
        _data = .;
        PROVIDE(__start_data_RAM = .);
        PROVIDE(__start_data_SRAM = .);
        *(vtable)
        *(.ctors)
        *(.dtors)

        PROVIDE_HIDDEN (__preinit_array_start = .);
        KEEP(*(.preinit_array))
        PROVIDE_HIDDEN (__preinit_array_end = .);

        PROVIDE_HIDDEN (__init_array_start = .);
        KEEP(*(.init_array))
        PROVIDE_HIDDEN (__init_array_end = .);

        PROVIDE_HIDDEN (__fini_array_start = .);
        KEEP(*(.fini_array))
        PROVIDE_HIDDEN (__fini_array_end = .);

        *(.ramfunc*)
        *(RamFunction)
        KEEP(*(CodeQuickAccess))
        KEEP(*(DataQuickAccess))
        *(.data*)
        . = ALIGN(4);
        _edata = .;
        PROVIDE(__end_data_RAM = .);
        PROVIDE(__end_data_SRAM = .);
    } > SRAM AT> QSPI_FLASH

    /* MAIN BSS SECTION */
    .bss : ALIGN(4)
    {
        _bss = .;
        PROVIDE(__start_bss_RAM = .);
        PROVIDE(__start_bss_SRAM = .);
        *(.bss*)
        *(COMMON)
        . = ALIGN(4);
        _ebss = .;
        PROVIDE(__end_bss_RAM = .);
        PROVIDE(__end_bss_SRAM = .);
        PROVIDE(end = .);
    } > SRAM AT> SRAM

    /* DEFAULT NOINIT SECTION */
    .noinit (NOLOAD) : ALIGN(4)
    {
        _noinit = .;
        PROVIDE(__start_noinit_RAM = .);
        PROVIDE(__start_noinit_SRAM = .);
        *(.noinit*)
        . = ALIGN(4);
        _end_noinit = .;
        PROVIDE(__end_noinit_RAM = .);
        PROVIDE(__end_noinit_SRAM = .);
    } > SRAM AT> SRAM

    /* Reserve and place Heap within memory map */
    _HeapSize = 0x1000;
    .heap (NOLOAD) : ALIGN(4)
    {
        _pvHeapStart = .;
        . += _HeapSize;
        . = ALIGN(4);
        _pvHeapLimit = .;
    } > SRAM

    /* Reserve space in memory for Stack */
    _StackSize = 0x10000;
    .heap2stackfill (NOLOAD) :
    {
        . += _StackSize;
    } > SRAM

    /* Locate actual Stack in memory map */
    .stack ORIGIN(SRAM) + LENGTH(SRAM) - _StackSize - 0 (NOLOAD) : ALIGN(4)
    {
        _vStackBase = .;
        . = ALIGN(4);
        _vStackTop = . + _StackSize;
    } > SRAM

    /*
     * Provide basic symbols giving location and size of main text
     * block, including initial values of RW data sections. Note that
     * these will need extending to give a complete picture with
     * complex images (e.g multiple Flash banks).
     */
    _image_start = LOADADDR(.isr_vector);
    _image_end = LOADADDR(.data) + SIZEOF(.data);
    _image_size = _image_end - _image_start;

    /*
     * Provide symbols for MIMXRT600 parts for startup code to use
     * to set image to be plain load image or XIP.
     * Config : Plain load image = false
     */
    __imghdr_loadaddress = LOADADDR(.text);
    __imghdr_imagetype = 4;
}
