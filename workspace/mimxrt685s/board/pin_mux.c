/*
 * Copyright 2020 NXP
 * All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 */
/***********************************************************************************************************************
 * This file was generated by the MCUXpresso Config Tools. Any manual edits made to this file
 * will be overwritten if the respective MCUXpresso Config Tools is used to update this file.
 **********************************************************************************************************************/

/* clang-format off */
/*
 * TEXT BELOW IS USED AS SETTING FOR TOOLS *************************************
!!GlobalInfo
product: Pins v7.0
processor: MIMXRT685S
package_id: MIMXRT685SFVKB
mcu_data: ksdk2_0
processor_version: 0.0.3
board: MIMXRT685-EVK
 * BE CAREFUL MODIFYING THIS COMMENT - IT IS YAML SETTINGS FOR TOOLS ***********
 */
/* clang-format on */

#include "fsl_common.h"
#include "fsl_iopctl.h"
#include "pin_mux.h"

/* FUNCTION ************************************************************************************************************
 *
 * Function Name : BOARD_InitBootPins
 * Description   : Calls initialization functions.
 *
 * END ****************************************************************************************************************/
void BOARD_InitBootPins(void)
{
    BOARD_InitPins();
}

/* clang-format off */
/*
 * TEXT BELOW IS USED AS SETTING FOR TOOLS *************************************
BOARD_InitPins:
- options: {callFromInitBoot: 'true', coreID: cm33, enableClock: 'true'}
- pin_list:
  - {pin_num: G2, peripheral: FLEXCOMM0, signal: TXD_SCL_MISO_WS, pin_signal: PIO0_1/FC0_TXD_SCL_MISO_WS/CTIMER0_MAT1/I2S_BRIDGE_WS_IN/SEC_PIO0_1, direction: OUTPUT,
    pupdena: disabled, pupdsel: pullDown, ibena: disabled, slew_rate: normal, drive: normal, amena: disabled, odena: disabled, iiena: disabled}
  - {pin_num: G4, peripheral: FLEXCOMM0, signal: RXD_SDA_MOSI_DATA, pin_signal: PIO0_2/FC0_RXD_SDA_MOSI_DATA/CTIMER0_MAT2/I2S_BRIDGE_DATA_IN/SEC_PIO0_2, direction: INPUT,
    pupdena: disabled, pupdsel: pullDown, ibena: enabled, slew_rate: normal, drive: normal, amena: disabled, odena: disabled, iiena: disabled}
  - {pin_num: L16, peripheral: SWD, signal: SWO, pin_signal: PIO2_24/SWO/GPIO_INT_BMAT, pupdena: enabled, pupdsel: pullUp, ibena: disabled, slew_rate: normal, drive: normal,
    amena: disabled, odena: disabled, iiena: disabled}
  - {pin_num: R13, peripheral: USDHC0, signal: USDHC_CD_B, pin_signal: PIO2_9/SD0_CARD_DET_N/SCT0_OUT5/CTIMER1_MAT3, pupdena: enabled, pupdsel: pullUp, ibena: enabled,
    slew_rate: normal, drive: normal, amena: disabled, odena: disabled, iiena: disabled}
  - {pin_num: P10, peripheral: USDHC0, signal: USDHC_CLK, pin_signal: PIO1_30/SD0_CLK/SCT0_GPI0, pupdena: disabled, pupdsel: pullDown, ibena: enabled, slew_rate: normal,
    drive: normal, amena: disabled, odena: disabled, iiena: disabled}
  - {pin_num: R9, peripheral: USDHC0, signal: USDHC_CMD, pin_signal: PIO1_31/SD0_CMD/SCT0_GPI1, pupdena: enabled, pupdsel: pullUp, ibena: enabled, slew_rate: normal,
    drive: normal, amena: disabled, odena: disabled, iiena: disabled}
  - {pin_num: R11, peripheral: USDHC0, signal: 'USDHC_DATA, 0', pin_signal: PIO2_0/SD0_D0/SCT0_GPI2, pupdena: enabled, pupdsel: pullUp, ibena: enabled, slew_rate: normal,
    drive: normal, amena: disabled, odena: disabled, iiena: disabled}
  - {pin_num: T11, peripheral: USDHC0, signal: 'USDHC_DATA, 1', pin_signal: PIO2_1/SD0_D1/SCT0_GPI3, pupdena: enabled, pupdsel: pullUp, ibena: enabled, slew_rate: normal,
    drive: normal, amena: disabled, odena: disabled, iiena: disabled}
  - {pin_num: U11, peripheral: USDHC0, signal: 'USDHC_DATA, 2', pin_signal: PIO2_2/SD0_D2/SCT0_OUT0, pupdena: enabled, pupdsel: pullUp, ibena: enabled, slew_rate: normal,
    drive: normal, amena: disabled, odena: disabled, iiena: disabled}
  - {pin_num: T12, peripheral: USDHC0, signal: 'USDHC_DATA, 3', pin_signal: PIO2_3/SD0_D3/SCT0_OUT1, pupdena: enabled, pupdsel: pullUp, ibena: enabled, slew_rate: normal,
    drive: normal, amena: disabled, odena: disabled, iiena: disabled}
  - {pin_num: T15, peripheral: GPIO, signal: 'PIO2, 10', pin_signal: PIO2_10/SD0_RESET_N/SCT0_GPI6/CTIMER2_MAT0, pupdena: disabled, pupdsel: pullDown, ibena: disabled,
    slew_rate: normal, drive: normal, amena: disabled, odena: disabled, iiena: disabled}
  - {pin_num: T13, peripheral: GPIO, signal: 'PIO2, 4', pin_signal: PIO2_4/SD0_WR_PRT/SCT0_OUT2/SD0_DS, pupdena: disabled, pupdsel: pullDown, ibena: disabled, slew_rate: normal,
    drive: normal, amena: disabled, odena: disabled, iiena: disabled}
  - {pin_num: E16, peripheral: FLEXCOMM15, signal: SCL, pin_signal: PMIC_I2C_SCL, pupdena: enabled, pupdsel: pullUp, ibena: enabled, slew_rate: normal, drive: normal,
    amena: disabled, odena: enabled, iiena: disabled}
  - {pin_num: F16, peripheral: FLEXCOMM15, signal: SDA, pin_signal: PMIC_I2C_SDA, pupdena: enabled, pupdsel: pullUp, ibena: enabled, slew_rate: normal, drive: normal,
    amena: disabled, odena: enabled, iiena: disabled}
 * BE CAREFUL MODIFYING THIS COMMENT - IT IS YAML SETTINGS FOR TOOLS ***********
 */
/* clang-format on */

/* FUNCTION ************************************************************************************************************
 *
 * Function Name : BOARD_InitPins
 * Description   : Configures pin routing and optionally pin electrical features.
 *
 * END ****************************************************************************************************************/
/* Function assigned for the Cortex-M33 */
void BOARD_InitPins(void)
{

    const uint32_t fc15_i2c_scl_config = (/* Pin is configured as I2C_SCL */
                                          IOPCTL_PIO_FUNC0 |
                                          /* Enable pull-up / pull-down function */
                                          IOPCTL_PIO_PUPD_EN |
                                          /* Enable pull-up function */
                                          IOPCTL_PIO_PULLUP_EN |
                                          /* Enables input buffer function */
                                          IOPCTL_PIO_INBUF_EN |
                                          /* Normal mode */
                                          IOPCTL_PIO_SLEW_RATE_NORMAL |
                                          /* Normal drive */
                                          IOPCTL_PIO_FULLDRIVE_DI |
                                          /* Analog mux is disabled */
                                          IOPCTL_PIO_ANAMUX_DI |
                                          /* Pseudo Output Drain is enabled */
                                          IOPCTL_PIO_PSEDRAIN_EN |
                                          /* Input function is not inverted */
                                          IOPCTL_PIO_INV_DI);
    /* FC15_SCL PIN (coords: E16) is configured as I2C SCL */
    IOPCTL->FC15_I2C_SCL = fc15_i2c_scl_config;

    const uint32_t fc15_i2c_sda_config = (/* Pin is configured as I2C_SDA */
                                          IOPCTL_PIO_FUNC0 |
                                          /* Enable pull-up / pull-down function */
                                          IOPCTL_PIO_PUPD_EN |
                                          /* Enable pull-up function */
                                          IOPCTL_PIO_PULLUP_EN |
                                          /* Enables input buffer function */
                                          IOPCTL_PIO_INBUF_EN |
                                          /* Normal mode */
                                          IOPCTL_PIO_SLEW_RATE_NORMAL |
                                          /* Normal drive */
                                          IOPCTL_PIO_FULLDRIVE_DI |
                                          /* Analog mux is disabled */
                                          IOPCTL_PIO_ANAMUX_DI |
                                          /* Pseudo Output Drain is enabled */
                                          IOPCTL_PIO_PSEDRAIN_EN |
                                          /* Input function is not inverted */
                                          IOPCTL_PIO_INV_DI);
    /* FC15_SDA PIN (coords: F16) is configured as I2C SDA */
    IOPCTL->FC15_I2C_SDA = fc15_i2c_sda_config;

    const uint32_t port0_pin1_config = (/* Pin is configured as FC0_TXD_SCL_MISO_WS */
                                        IOPCTL_PIO_FUNC1 |
                                        /* Disable pull-up / pull-down function */
                                        IOPCTL_PIO_PUPD_DI |
                                        /* Enable pull-down function */
                                        IOPCTL_PIO_PULLDOWN_EN |
                                        /* Disable input buffer function */
                                        IOPCTL_PIO_INBUF_DI |
                                        /* Normal mode */
                                        IOPCTL_PIO_SLEW_RATE_NORMAL |
                                        /* Normal drive */
                                        IOPCTL_PIO_FULLDRIVE_DI |
                                        /* Analog mux is disabled */
                                        IOPCTL_PIO_ANAMUX_DI |
                                        /* Pseudo Output Drain is disabled */
                                        IOPCTL_PIO_PSEDRAIN_DI |
                                        /* Input function is not inverted */
                                        IOPCTL_PIO_INV_DI);
    /* PORT0 PIN1 (coords: G2) is configured as FC0_TXD_SCL_MISO_WS */
    IOPCTL_PinMuxSet(IOPCTL, 0U, 1U, port0_pin1_config);

    const uint32_t port0_pin2_config = (/* Pin is configured as FC0_RXD_SDA_MOSI_DATA */
                                        IOPCTL_PIO_FUNC1 |
                                        /* Disable pull-up / pull-down function */
                                        IOPCTL_PIO_PUPD_DI |
                                        /* Enable pull-down function */
                                        IOPCTL_PIO_PULLDOWN_EN |
                                        /* Enables input buffer function */
                                        IOPCTL_PIO_INBUF_EN |
                                        /* Normal mode */
                                        IOPCTL_PIO_SLEW_RATE_NORMAL |
                                        /* Normal drive */
                                        IOPCTL_PIO_FULLDRIVE_DI |
                                        /* Analog mux is disabled */
                                        IOPCTL_PIO_ANAMUX_DI |
                                        /* Pseudo Output Drain is disabled */
                                        IOPCTL_PIO_PSEDRAIN_DI |
                                        /* Input function is not inverted */
                                        IOPCTL_PIO_INV_DI);
    /* PORT0 PIN2 (coords: G4) is configured as FC0_RXD_SDA_MOSI_DATA */
    IOPCTL_PinMuxSet(IOPCTL, 0U, 2U, port0_pin2_config);

    const uint32_t port1_pin30_config = (/* Pin is configured as SD0_CLK */
                                         IOPCTL_PIO_FUNC1 |
                                         /* Disable pull-up / pull-down function */
                                         IOPCTL_PIO_PUPD_DI |
                                         /* Enable pull-down function */
                                         IOPCTL_PIO_PULLDOWN_EN |
                                         /* Enables input buffer function */
                                         IOPCTL_PIO_INBUF_EN |
                                         /* Normal mode */
                                         IOPCTL_PIO_SLEW_RATE_NORMAL |
                                         /* Normal drive */
                                         IOPCTL_PIO_FULLDRIVE_DI |
                                         /* Analog mux is disabled */
                                         IOPCTL_PIO_ANAMUX_DI |
                                         /* Pseudo Output Drain is disabled */
                                         IOPCTL_PIO_PSEDRAIN_DI |
                                         /* Input function is not inverted */
                                         IOPCTL_PIO_INV_DI);
    /* PORT1 PIN30 (coords: P10) is configured as SD0_CLK */
    IOPCTL_PinMuxSet(IOPCTL, 1U, 30U, port1_pin30_config);

    const uint32_t port1_pin31_config = (/* Pin is configured as SD0_CMD */
                                         IOPCTL_PIO_FUNC1 |
                                         /* Enable pull-up / pull-down function */
                                         IOPCTL_PIO_PUPD_EN |
                                         /* Enable pull-up function */
                                         IOPCTL_PIO_PULLUP_EN |
                                         /* Enables input buffer function */
                                         IOPCTL_PIO_INBUF_EN |
                                         /* Normal mode */
                                         IOPCTL_PIO_SLEW_RATE_NORMAL |
                                         /* Normal drive */
                                         IOPCTL_PIO_FULLDRIVE_DI |
                                         /* Analog mux is disabled */
                                         IOPCTL_PIO_ANAMUX_DI |
                                         /* Pseudo Output Drain is disabled */
                                         IOPCTL_PIO_PSEDRAIN_DI |
                                         /* Input function is not inverted */
                                         IOPCTL_PIO_INV_DI);
    /* PORT1 PIN31 (coords: R9) is configured as SD0_CMD */
    IOPCTL_PinMuxSet(IOPCTL, 1U, 31U, port1_pin31_config);

    const uint32_t port2_pin0_config = (/* Pin is configured as SD0_D0 */
                                        IOPCTL_PIO_FUNC1 |
                                        /* Enable pull-up / pull-down function */
                                        IOPCTL_PIO_PUPD_EN |
                                        /* Enable pull-up function */
                                        IOPCTL_PIO_PULLUP_EN |
                                        /* Enables input buffer function */
                                        IOPCTL_PIO_INBUF_EN |
                                        /* Normal mode */
                                        IOPCTL_PIO_SLEW_RATE_NORMAL |
                                        /* Normal drive */
                                        IOPCTL_PIO_FULLDRIVE_DI |
                                        /* Analog mux is disabled */
                                        IOPCTL_PIO_ANAMUX_DI |
                                        /* Pseudo Output Drain is disabled */
                                        IOPCTL_PIO_PSEDRAIN_DI |
                                        /* Input function is not inverted */
                                        IOPCTL_PIO_INV_DI);
    /* PORT2 PIN0 (coords: R11) is configured as SD0_D0 */
    IOPCTL_PinMuxSet(IOPCTL, 2U, 0U, port2_pin0_config);

    const uint32_t port2_pin1_config = (/* Pin is configured as SD0_D1 */
                                        IOPCTL_PIO_FUNC1 |
                                        /* Enable pull-up / pull-down function */
                                        IOPCTL_PIO_PUPD_EN |
                                        /* Enable pull-up function */
                                        IOPCTL_PIO_PULLUP_EN |
                                        /* Enables input buffer function */
                                        IOPCTL_PIO_INBUF_EN |
                                        /* Normal mode */
                                        IOPCTL_PIO_SLEW_RATE_NORMAL |
                                        /* Normal drive */
                                        IOPCTL_PIO_FULLDRIVE_DI |
                                        /* Analog mux is disabled */
                                        IOPCTL_PIO_ANAMUX_DI |
                                        /* Pseudo Output Drain is disabled */
                                        IOPCTL_PIO_PSEDRAIN_DI |
                                        /* Input function is not inverted */
                                        IOPCTL_PIO_INV_DI);
    /* PORT2 PIN1 (coords: T11) is configured as SD0_D1 */
    IOPCTL_PinMuxSet(IOPCTL, 2U, 1U, port2_pin1_config);

    const uint32_t port2_pin10_config = (/* Pin is configured as PIO2_10 */
                                         IOPCTL_PIO_FUNC0 |
                                         /* Disable pull-up / pull-down function */
                                         IOPCTL_PIO_PUPD_DI |
                                         /* Enable pull-down function */
                                         IOPCTL_PIO_PULLDOWN_EN |
                                         /* Disable input buffer function */
                                         IOPCTL_PIO_INBUF_DI |
                                         /* Normal mode */
                                         IOPCTL_PIO_SLEW_RATE_NORMAL |
                                         /* Normal drive */
                                         IOPCTL_PIO_FULLDRIVE_DI |
                                         /* Analog mux is disabled */
                                         IOPCTL_PIO_ANAMUX_DI |
                                         /* Pseudo Output Drain is disabled */
                                         IOPCTL_PIO_PSEDRAIN_DI |
                                         /* Input function is not inverted */
                                         IOPCTL_PIO_INV_DI);
    /* PORT2 PIN10 (coords: T15) is configured as PIO2_10 */
    IOPCTL_PinMuxSet(IOPCTL, 2U, 10U, port2_pin10_config);

    const uint32_t port2_pin2_config = (/* Pin is configured as SD0_D2 */
                                        IOPCTL_PIO_FUNC1 |
                                        /* Enable pull-up / pull-down function */
                                        IOPCTL_PIO_PUPD_EN |
                                        /* Enable pull-up function */
                                        IOPCTL_PIO_PULLUP_EN |
                                        /* Enables input buffer function */
                                        IOPCTL_PIO_INBUF_EN |
                                        /* Normal mode */
                                        IOPCTL_PIO_SLEW_RATE_NORMAL |
                                        /* Normal drive */
                                        IOPCTL_PIO_FULLDRIVE_DI |
                                        /* Analog mux is disabled */
                                        IOPCTL_PIO_ANAMUX_DI |
                                        /* Pseudo Output Drain is disabled */
                                        IOPCTL_PIO_PSEDRAIN_DI |
                                        /* Input function is not inverted */
                                        IOPCTL_PIO_INV_DI);
    /* PORT2 PIN2 (coords: U11) is configured as SD0_D2 */
    IOPCTL_PinMuxSet(IOPCTL, 2U, 2U, port2_pin2_config);

    const uint32_t port2_pin3_config = (/* Pin is configured as SD0_D3 */
                                        IOPCTL_PIO_FUNC1 |
                                        /* Enable pull-up / pull-down function */
                                        IOPCTL_PIO_PUPD_EN |
                                        /* Enable pull-up function */
                                        IOPCTL_PIO_PULLUP_EN |
                                        /* Enables input buffer function */
                                        IOPCTL_PIO_INBUF_EN |
                                        /* Normal mode */
                                        IOPCTL_PIO_SLEW_RATE_NORMAL |
                                        /* Normal drive */
                                        IOPCTL_PIO_FULLDRIVE_DI |
                                        /* Analog mux is disabled */
                                        IOPCTL_PIO_ANAMUX_DI |
                                        /* Pseudo Output Drain is disabled */
                                        IOPCTL_PIO_PSEDRAIN_DI |
                                        /* Input function is not inverted */
                                        IOPCTL_PIO_INV_DI);
    /* PORT2 PIN3 (coords: T12) is configured as SD0_D3 */
    IOPCTL_PinMuxSet(IOPCTL, 2U, 3U, port2_pin3_config);

    const uint32_t port2_pin4_config = (/* Pin is configured as PIO2_4 */
                                        IOPCTL_PIO_FUNC0 |
                                        /* Disable pull-up / pull-down function */
                                        IOPCTL_PIO_PUPD_DI |
                                        /* Enable pull-down function */
                                        IOPCTL_PIO_PULLDOWN_EN |
                                        /* Disable input buffer function */
                                        IOPCTL_PIO_INBUF_DI |
                                        /* Normal mode */
                                        IOPCTL_PIO_SLEW_RATE_NORMAL |
                                        /* Normal drive */
                                        IOPCTL_PIO_FULLDRIVE_DI |
                                        /* Analog mux is disabled */
                                        IOPCTL_PIO_ANAMUX_DI |
                                        /* Pseudo Output Drain is disabled */
                                        IOPCTL_PIO_PSEDRAIN_DI |
                                        /* Input function is not inverted */
                                        IOPCTL_PIO_INV_DI);
    /* PORT2 PIN4 (coords: T13) is configured as PIO2_4 */
    IOPCTL_PinMuxSet(IOPCTL, 2U, 4U, port2_pin4_config);

    const uint32_t port2_pin9_config = (/* Pin is configured as SD0_CARD_DET_N */
                                        IOPCTL_PIO_FUNC1 |
                                        /* Enable pull-up / pull-down function */
                                        IOPCTL_PIO_PUPD_EN |
                                        /* Enable pull-up function */
                                        IOPCTL_PIO_PULLUP_EN |
                                        /* Enables input buffer function */
                                        IOPCTL_PIO_INBUF_EN |
                                        /* Normal mode */
                                        IOPCTL_PIO_SLEW_RATE_NORMAL |
                                        /* Normal drive */
                                        IOPCTL_PIO_FULLDRIVE_DI |
                                        /* Analog mux is disabled */
                                        IOPCTL_PIO_ANAMUX_DI |
                                        /* Pseudo Output Drain is disabled */
                                        IOPCTL_PIO_PSEDRAIN_DI |
                                        /* Input function is not inverted */
                                        IOPCTL_PIO_INV_DI);
    /* PORT2 PIN9 (coords: R13) is configured as SD0_CARD_DET_N */
    IOPCTL_PinMuxSet(IOPCTL, 2U, 9U, port2_pin9_config);

    const uint32_t port2_pin24_config = (/* Pin is configured as SWO */
                                         IOPCTL_PIO_FUNC1 |
                                         /* Enable pull-up / pull-down function */
                                         IOPCTL_PIO_PUPD_EN |
                                         /* Enable pull-up function */
                                         IOPCTL_PIO_PULLUP_EN |
                                         /* Disable input buffer function */
                                         IOPCTL_PIO_INBUF_DI |
                                         /* Normal mode */
                                         IOPCTL_PIO_SLEW_RATE_NORMAL |
                                         /* Normal drive */
                                         IOPCTL_PIO_FULLDRIVE_DI |
                                         /* Analog mux is disabled */
                                         IOPCTL_PIO_ANAMUX_DI |
                                         /* Pseudo Output Drain is disabled */
                                         IOPCTL_PIO_PSEDRAIN_DI |
                                         /* Input function is not inverted */
                                         IOPCTL_PIO_INV_DI);
    /* PORT2 PIN24 (coords: L16) is configured as SWO */
    IOPCTL_PinMuxSet(IOPCTL, 2U, 24U, port2_pin24_config);
}
/***********************************************************************************************************************
 * EOF
 **********************************************************************************************************************/
