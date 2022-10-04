#!/usr/bin/env python3

# Copyright (c) 2021-2022, University of Rochester
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import os
import sys


#
# Path to the root directory of whole project.
#
root = '${workspace_loc}/..'

#
# Path to our Clang.
#
clang_path = root + '/build/llvm/install/bin/clang'

#
# Path to our archiver.
#
ar_path = root + '/build/llvm/bin/llvm-ar'

#
# Path to the newlib install directory.
#
newlib_path = root + '/build/newlib-cygwin/install'

#
# Path to the custom compiler-rt install directory.
#
compiler_rt_path = root + '/build/compiler-rt/install'

#
# Path to the directory of this project.
#
project_dir = os.path.abspath(os.path.dirname(sys.argv[0]))

#
# Project name.
#
project_name = 'mimxrt685s'


#
# Dict of libraries that need to be linked.
#
libraries = {
    'c': {
        'includes': [
            newlib_path + '/arm-none-eabihf/include',
        ],
    },
}


#
# Dict of programs to compile.
#
programs = {
    'mimxrt685s': {
        'defines': [
            'BOOT_HEADER_ENABLE=1',
            'CPU_MIMXRT685SFVKB',
            'CPU_MIMXRT685SFVKB_cm33',
            'NDEBUG',
            'PRINTF_FLOAT_ENABLE=1',
            'SD_ENABLED',
            'SDK_DEBUGCONSOLE=0',
            'SDK_DEBUGCONSOLE_UART',
            'SDK_I2C_BASED_COMPONENT_USED=1',
            'SERIAL_PORT_TYPE_UART=1',
            '__MCUXPRESSO',
            '__USE_CMSIS',
        ],
        'includes': [
            '${ProjDirPath}/CMSIS',
            '${ProjDirPath}/board',
            '${ProjDirPath}/component/lists',
            '${ProjDirPath}/component/osa',
            '${ProjDirPath}/component/serial_manager',
            '${ProjDirPath}/component/uart',
            '${ProjDirPath}/device',
            '${ProjDirPath}/drivers',
            '${ProjDirPath}/flash_config',
            '${ProjDirPath}/pmic_driver',
            '${ProjDirPath}/sdmmc/host',
            '${ProjDirPath}/sdmmc/inc',
            '${ProjDirPath}/sdmmc/osa',
            '${ProjDirPath}/utilities',
        ],
        'directories': {
            'CMSIS': '',
            'board': '',
            'component': '',
            'device': '',
            'drivers': '',
            'flash_config': '',
            'pmic_driver': '',
            'sdmmc': '',
            'startup': '',
            'utilities': '',
        },
    },
}


#
# Dict of configurations.
#
configurations = {
    'baseline': {},
    'cve': {
        'defines': [
            'CVE_2021_27421',
        ],
    },
}


#
# Extra settings that cannot be specified statically and need to be populated
# by a function at runtime.
#
extras = {}


#
# Populate extra settings.
#
def populate_extra_settings():
    number = 0
    for conf in configurations:
        for program in programs:
            extras[(conf, program)] = {
                'id': str(number),
                'defines': [],
                'includes': [],
                'cflags': [],
                'ldflags': [],
            }
            number += 1


###############################################################################

#
# Generate and return the cproject header.
#
def gen_header():
    xml =  '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
    xml += '<?fileVersion 4.0.0?>\n'
    xml += '<cproject storage_type_id="org.eclipse.cdt.core.XmlProjectDescriptionStorage">\n'
    return xml


#
# Generate and return the cproject footer.
#
def gen_footer():
    xml =  '  <storageModule moduleId="cdtBuildSystem" version="4.0.0">\n'
    xml += '    <project id="' + project_name + '.null" name="' + project_name + '" projectType="com.crt.advproject.projecttype.lib"/>\n'
    xml += '  </storageModule>\n'
    xml += '  <storageModule moduleId="org.eclipse.cdt.core.LanguageSettingsProviders"/>\n'
    xml += '  <storageModule moduleId="org.eclipse.cdt.make.core.buildtargets"/>\n'
    xml += '</cproject>\n'
    return xml


#
# Generate and return the header of scanner configurations.
#
def gen_scanner_header():
    xml =  '  <storageModule moduleId="scannerConfiguration">\n'
    xml += '    <autodiscovery enabled="false" problemReportingEnabled="false" selectedProfileId=""/>\n'
    return xml


#
# Generate and return the scanner configuration for a given configuration and
# program.
#
# @conf: the name of the configuration.
# @program: the name of the program.
#
def gen_scanner_config(conf, program):
    program_id = extras[(conf, program)]['id']
    xml =  '    <scannerConfigBuildInfo instanceId="com.crt.advproject.config.lib.release.' + program_id + ';com.crt.advproject.config.lib.release.' + program_id + '.;com.crt.advproject.gcc.lib.release.' + program_id + ';com.crt.advproject.compiler.input.' + program_id + '">\n'
    xml += '      <autodiscovery enabled="false" problemReportingEnabled="false" selectedProfileId=""/>\n'
    xml += '    </scannerConfigBuildInfo>\n'
    xml =  '    <scannerConfigBuildInfo instanceId="com.crt.advproject.config.lib.release.' + program_id + ';com.crt.advproject.config.lib.release.' + program_id + '.;com.crt.advproject.gas.lib.release.' + program_id + ';com.crt.advproject.assembler.input.' + program_id + '">\n'
    xml += '      <autodiscovery enabled="false" problemReportingEnabled="false" selectedProfileId=""/>\n'
    xml += '    </scannerConfigBuildInfo>\n'
    return xml


#
# Generate and return the footer of scanner configurations.
#
def gen_scanner_footer():
    return '  </storageModule>\n'


#
# Generate and return the core data models of the project.
#
def gen_core_datamodels():
    xml =  '  <storageModule moduleId="com.nxp.mcuxpresso.core.datamodels">\n'
    xml += '    <sdkName>SDK_2.x_EVK-MIMXRT685</sdkName>\n'
    xml += '    <sdkVersion>2.8.2</sdkVersion>\n'
    xml += '    <sdkComponents>component.lists.MIMXRT685S;component.serial_manager.MIMXRT685S;component.serial_manager_uart.MIMXRT685S;component.usart_adapter.MIMXRT685S;device.MIMXRT685S_CMSIS.MIMXRT685S;device.MIMXRT685S_startup.MIMXRT685S;platform.Include_common.MIMXRT685S;platform.Include_core_cm33.MIMXRT685S;platform.Include_dsp.MIMXRT685S;platform.drivers.cache_cache64.MIMXRT685S;platform.drivers.clock.MIMXRT685S;platform.drivers.common.MIMXRT685S;platform.drivers.flash_config.MIMXRT685S;platform.drivers.flexcomm.MIMXRT685S;platform.drivers.flexcomm_usart.MIMXRT685S;platform.drivers.flexspi.MIMXRT685S;platform.drivers.lpc_gpio.MIMXRT685S;platform.drivers.lpc_iopctl.MIMXRT685S;platform.drivers.power.MIMXRT685S;platform.drivers.reset.MIMXRT685S;platform.utilities.assert.MIMXRT685S;platform.utilities.misc_utilities.MIMXRT685S;project_template.evkmimxrt685.MIMXRT685S;utility.debug_console.MIMXRT685S;</sdkComponents>\n'
    xml += '    <boardId>evkmimxrt685</boardId>\n'
    xml += '    <package>MIMXRT685SFVKB</package>\n'
    xml += '    <core>cm33</core>\n'
    xml += '    <coreId>cm33_MIMXRT685S</coreId>\n'
    xml += '  </storageModule>\n'
    return xml


#
# Generate and return the MCU configuration.
#
def gen_crt_config():
    xml =  '  <storageModule moduleId="com.crt.config">\n'
    xml += '    <projectStorage>&lt;?xml version="1.0" encoding="UTF-8"?&gt;\n'
    xml += '&lt;TargetConfig&gt;\n'
    xml += '  &lt;Properties property_3="NXP" property_4="MIMXRT685S" property_count="5" version="100300"/&gt;\n'
    xml += '  &lt;infoList vendor="NXP"&gt;\n'
    xml += '    &lt;info chip="MIMXRT685S" name="MIMXRT685S"&gt;\n'
    xml += '      &lt;chip&gt;\n'
    xml += '        &lt;name&gt;MIMXRT685S&lt;/name&gt;\n'
    xml += '        &lt;family&gt;MIMXRT600&lt;/family&gt;\n'
    xml += '        &lt;vendor&gt;NXP&lt;/vendor&gt;\n'
    xml += '        &lt;memory can_program="true" id="Flash" is_ro="true" size="0" type="Flash"/&gt;\n'
    xml += '        &lt;memory id="RAM" size="4608" type="RAM"/&gt;\n'
    xml += '        &lt;memoryInstance derived_from="Flash" driver="MIMXRT600_FlexSPI_B_SFDP_QSPI.cfx" edited="true" id="QSPI_FLASH" location="0x8000000" size="0x4000000"/&gt;\n'
    xml += '        &lt;memoryInstance derived_from="RAM" edited="true" id="SRAM" location="0x20000000" size="0x480000"/&gt;\n'
    xml += '      &lt;/chip&gt;\n'
    xml += '      &lt;processor&gt;\n'
    xml += '        &lt;name gcc_name="cortex-m33"&gt;Cortex-M33&lt;/name&gt;\n'
    xml += '        &lt;family&gt;Cortex-M&lt;/family&gt;\n'
    xml += '      &lt;/processor&gt;\n'
    xml += '    &lt;/info&gt;\n'
    xml += '  &lt;/infoList&gt;\n'
    xml += '&lt;/TargetConfig&gt;\n'
    xml += '    </projectStorage>\n'
    xml += '  </storageModule>\n'
    return xml


#
# Generate and return the header of core settings.
#
def gen_core_settings_header():
    return '  <storageModule moduleId="org.eclipse.cdt.core.settings">\n'


#
# Generate and return the core setting for a given program.
#
# @conf: the name of the configuration to use.
# @program: the name of the program.
#
def gen_core_settings_config(conf, program):
    program_id = extras[(conf, program)]['id']
    program_name = conf + '-' + program

    xml =  '    <!-- Configuration of ' + program_name + ' -->\n'
    xml += '    <cconfiguration id="com.crt.advproject.config.lib.release.' + program_id + '">\n'
    xml += '      <storageModule buildSystemId="org.eclipse.cdt.managedbuilder.core.configurationDataProvider" id="com.crt.advproject.config.lib.release.' + program_id + '" moduleId="org.eclipse.cdt.core.settings" name="' + program_name + '">\n'
    xml += '        <externalSettings>\n'
    xml += '          <externalSetting>\n'
    xml += '            <entry flags="VALUE_WORKSPACE_PATH" kind="includePath" name="/' + project_name + '"/>\n'
    xml += '            <entry flags="VALUE_WORKSPACE_PATH" kind="libraryPath" name="/' + project_name + '/' + program_name + '"/>\n';
    xml += '            <entry flags="RESOLVED" kind="libraryFile" name="' + project_name + '" srcPrefixMapping="" srcRootPath=""/>\n'
    xml += '          </externalSetting>\n'
    xml += '        </externalSettings>\n'
    xml += '        <extensions>\n'
    xml += '          <extension id="org.eclipse.cdt.core.ELF" point="org.eclipse.cdt.core.BinaryParser"/>\n'
    xml += '          <extension id="org.eclipse.cdt.core.GNU_ELF" point="org.eclipse.cdt.core.BinaryParser"/>\n'
    xml += '          <extension id="org.eclipse.cdt.core.GmakeErrorParser" point="org.eclipse.cdt.core.ErrorParser"/>\n'
    xml += '          <extension id="org.eclipse.cdt.core.GASErrorParser" point="org.eclipse.cdt.core.ErrorParser"/>\n'
    xml += '          <extension id="org.eclipse.cdt.core.GLDErrorParser" point="org.eclipse.cdt.core.ErrorParser"/>\n'
    xml += '          <extension id="org.eclipse.cdt.core.CWDLocator" point="org.eclipse.cdt.core.ErrorParser"/>\n'
    xml += '          <extension id="org.eclipse.cdt.core.GCCErrorParser" point="org.eclipse.cdt.core.ErrorParser"/>\n'
    xml += '        </extensions>\n'
    xml += '      </storageModule>\n'
    xml += '      <storageModule moduleId="cdtBuildSystem" version="4.0.0">\n'
    xml += '        <configuration artifactExtension="a" artifactName="${ProjName}" buildArtefactType="org.eclipse.cdt.build.core.buildArtefactType.staticLib" buildProperties="org.eclipse.cdt.build.core.buildArtefactType=org.eclipse.cdt.build.core.buildArtefactType.staticLib" cleanCommand="rm -rf" description="Release build of ' + program_name + '" errorParsers="org.eclipse.cdt.core.CWDLocator;org.eclipse.cdt.core.GmakeErrorParser;org.eclipse.cdt.core.GCCErrorParser;org.eclipse.cdt.core.GLDErrorParser;org.eclipse.cdt.core.GASErrorParser" id="com.crt.advproject.config.lib.release.' + program_id + '" name="' + program_name + '" parent="com.crt.advproject.config.lib.release" postannouncebuildStep="Performing post-build steps" postbuildStep="">\n'
    xml += '          <folderInfo id="com.crt.advproject.config.lib.release.' + program_id + '." name="/" resourcePath="">\n'
    xml += '            <toolChain id="com.crt.advproject.toolchain.lib.release.' + program_id + '" name="NXP MCU Tools" superClass="com.crt.advproject.toolchain.lib.release">\n'
    xml += '              <targetPlatform binaryParser="org.eclipse.cdt.core.ELF;org.eclipse.cdt.core.GNU_ELF" id="com.crt.advproject.platform.lib.release.' + program_id + '" name="ARM-based MCU (Release)" superClass="com.crt.advproject.platform.lib.release"/>\n'
    xml += '              <builder buildPath="${ProjDirPath}/' + program_name + '" id="com.crt.advproject.builder.lib.release.' + program_id + '" keepEnvironmentInBuildfile="false" managedBuildOn="true" name="Gnu Make Builder" superClass="com.crt.advproject.builder.lib.release"/>\n'
    ###########################################################################
    # Set up C compiler
    ###########################################################################
    xml += '              <tool command="' + clang_path + '" id="com.crt.advproject.gcc.lib.release.' + program_id + '" name="MCU C Compiler" superClass="com.crt.advproject.gcc.lib.release">\n'
    # Other C dialect flags: none
    xml += '                <option id="gnu.c.compiler.option.dialect.flags.' + program_id + '" name="Other dialect flags" superClass="gnu.c.compiler.option.dialect.flags" useByScannerDiscovery="false"/>\n'
    # Add -nostdinc: false
    xml += '                <option id="gnu.c.compiler.option.preprocessor.nostdinc.' + program_id + '" name="Do not search system directories (-nostdinc)" superClass="gnu.c.compiler.option.preprocessor.nostdinc" useByScannerDiscovery="false" value="false" valueType="boolean"/>\n'
    # Add -E: false
    xml += '                <option id="gnu.c.compiler.option.preprocessor.preprocess.' + program_id + '" name="Preprocess only (-E)" superClass="gnu.c.compiler.option.preprocessor.preprocess" useByScannerDiscovery="false" value="false" valueType="boolean"/>\n'
    # Add macro undefs: none
    xml += '                <option id="gnu.c.compiler.option.preprocessor.undef.symbol.' + program_id + '" name="Undefined symbols (-U)" superClass="gnu.c.compiler.option.preprocessor.undef.symbol" useByScannerDiscovery="false"/>\n'
    # Add -include's: none
    xml += '                <option id="gnu.c.compiler.option.include.files.' + program_id + '" name="Include files (-include)" superClass="gnu.c.compiler.option.include.files" useByScannerDiscovery="false"/>\n'
    # Other optmization flags: -ffunction-sections -fdata-sections -fomit-frame-pointer -ffreestanding
    xml += '                <option id="gnu.c.compiler.option.optimization.flags.' + program_id + '" name="Other optimization flags" superClass="gnu.c.compiler.option.optimization.flags" useByScannerDiscovery="false" value="-ffunction-sections -fdata-sections -fomit-frame-pointer -ffreestanding" valueType="string"/>\n'
    # Other debug flags: none
    xml += '                <option id="gnu.c.compiler.option.debugging.other.' + program_id + '" name="Other debugging flags" superClass="gnu.c.compiler.option.debugging.other" useByScannerDiscovery="false" value="" valueType="string"/>\n'
    # Add -p: false
    xml += '                <option id="gnu.c.compiler.option.debugging.prof.' + program_id + '" name="Generate prof information (-p)" superClass="gnu.c.compiler.option.debugging.prof" useByScannerDiscovery="false" value="false" valueType="boolean"/>\n'
    # Add -pg: false
    xml += '                <option id="gnu.c.compiler.option.debugging.gprof.' + program_id + '" name="Generate gprof information (-pg)" superClass="gnu.c.compiler.option.debugging.gprof" useByScannerDiscovery="false" value="false" valueType="boolean"/>\n'
    # Add -ftest-coverage and -fprofile-arcs: false
    xml += '                <option id="gnu.c.compiler.option.debugging.codecov.' + program_id + '" name="Generate gcov information (-ftest-coverage -fprofile-arcs)" superClass="gnu.c.compiler.option.debugging.codecov" useByScannerDiscovery="false" value="false" valueType="boolean"/>\n'
    # Add -fsyntax-only: false
    xml += '                <option id="gnu.c.compiler.option.warnings.syntax.' + program_id + '" name="Check syntax only (-fsyntax-only)" superClass="gnu.c.compiler.option.warnings.syntax" useByScannerDiscovery="false" value="false" valueType="boolean"/>\n'
    # Add -pedantic: false
    xml += '                <option id="gnu.c.compiler.option.warnings.pedantic.' + program_id + '" name="Pedantic (-pedantic)" superClass="gnu.c.compiler.option.warnings.pedantic" useByScannerDiscovery="false" value="false" valueType="boolean"/>\n'
    # Add -pedantic-errors: false
    xml += '                <option id="gnu.c.compiler.option.warnings.pedantic.error.' + program_id + '" name="Pedantic warnings as errors (-pedantic-errors)" superClass="gnu.c.compiler.option.warnings.pedantic.error" useByScannerDiscovery="false" value="false" valueType="boolean"/>\n'
    # Add -w: false
    xml += '                <option id="gnu.c.compiler.option.warnings.nowarn.' + program_id + '" name="Inhibit all warnings (-w)" superClass="gnu.c.compiler.option.warnings.nowarn" useByScannerDiscovery="false" value="false" valueType="boolean"/>\n'
    # Add -Wall: true
    xml += '                <option id="gnu.c.compiler.option.warnings.allwarn.' + program_id + '" name="All warnings (-Wall)" superClass="gnu.c.compiler.option.warnings.allwarn" useByScannerDiscovery="false" value="true" valueType="boolean"/>\n'
    # Add -Wextra: true
    xml += '                <option id="gnu.c.compiler.option.warnings.extrawarn.' + program_id + '" name="Extra warnings (-Wextra)" superClass="gnu.c.compiler.option.warnings.extrawarn" useByScannerDiscovery="false" value="true" valueType="boolean"/>\n'
    # Add -Werror: false
    xml += '                <option id="gnu.c.compiler.option.warnings.toerrors.' + program_id + '" name="Warnings as errors (-Werror)" superClass="gnu.c.compiler.option.warnings.toerrors" useByScannerDiscovery="false" value="false" valueType="boolean"/>\n'
    # Add -Wconversion: false
    xml += '                <option id="gnu.c.compiler.option.warnings.wconversion.' + program_id + '" name="Implicit conversion warnings (-Wconversion)" superClass="gnu.c.compiler.option.warnings.wconversion" useByScannerDiscovery="false" value="false" valueType="boolean"/>\n'
    # Add -v: false
    xml += '                <option id="gnu.c.compiler.option.misc.verbose.' + program_id + '" name="Verbose (-v)" superClass="gnu.c.compiler.option.misc.verbose" useByScannerDiscovery="false" value="false" valueType="boolean"/>\n'
    # Add -ansi: false
    xml += '                <option id="gnu.c.compiler.option.misc.ansi.' + program_id + '" name="Support ANSI programs (-ansi)" superClass="gnu.c.compiler.option.misc.ansi" useByScannerDiscovery="false" value="false" valueType="boolean"/>\n'
    # Add -fPIC: false
    xml += '                <option id="gnu.c.compiler.option.misc.pic.' + program_id + '" name="Position Independent Code (-fPIC)" superClass="gnu.c.compiler.option.misc.pic" useByScannerDiscovery="false" value="false" valueType="boolean"/>\n'
    # C dialect: default
    xml += '                <option id="com.crt.advproject.c.misc.dialect.' + program_id + '" name="Language standard" superClass="com.crt.advproject.c.misc.dialect" useByScannerDiscovery="false" value="com.crt.advproject.misc.dialect.default" valueType="enumerated"/>\n'
    # Architecture: Cortex-M33
    xml += '                <option id="com.crt.advproject.gcc.arch.' + program_id + '" name="Architecture" superClass="com.crt.advproject.gcc.arch" useByScannerDiscovery="false" value="com.crt.advproject.gcc.target.cm33" valueType="enumerated"/>\n'
    # FPU: FPv5-SP-D16 Hard ABI
    xml += '                <option id="com.crt.advproject.gcc.fpu.' + program_id + '" name="Floating point" superClass="com.crt.advproject.gcc.fpu" useByScannerDiscovery="true" value="com.crt.advproject.gcc.fpu.fpv5sp.hard" valueType="enumerated"/>\n'
    # TrustZone type: none
    xml += '                <option id="com.crt.advproject.gcc.securestate.' + program_id + '" name="TrustZone Project Type" superClass="com.crt.advproject.gcc.securestate" useByScannerDiscovery="false" value="com.crt.advproject.gcc.securestate.none" valueType="enumerated"/>\n'
    # Thumb mode: true
    xml += '                <option id="com.crt.advproject.gcc.thumb.' + program_id + '" name="Thumb mode" superClass="com.crt.advproject.gcc.thumb" useByScannerDiscovery="false" value="true" valueType="boolean"/>\n'
    # Thumb interworking: false
    xml += '                <option id="com.crt.advproject.gcc.thumbinterwork.' + program_id + '" name="Enable Thumb interworking" superClass="com.crt.advproject.gcc.thumbinterwork" useByScannerDiscovery="false" value="false" valueType="boolean"/>\n'
    # Debug level: -g
    xml += '                <option id="com.crt.advproject.gcc.lib.release.option.debugging.level.' + program_id + '" name="Debug Level" superClass="com.crt.advproject.gcc.lib.release.option.debugging.level" useByScannerDiscovery="false" value="gnu.c.debugging.level.default" valueType="enumerated"/>\n'
    # Optimization level: -Os
    xml += '                <option id="com.crt.advproject.gcc.lib.release.option.optimization.level.' + program_id + '" name="Optimization Level" superClass="com.crt.advproject.gcc.lib.release.option.optimization.level" useByScannerDiscovery="false" value="gnu.c.optimization.level.size" valueType="enumerated"/>\n'
    # Library headers and specs: none
    xml += '                <option id="com.crt.advproject.gcc.hdrlib.' + program_id + '" name="Library headers" superClass="com.crt.advproject.gcc.hdrlib" useByScannerDiscovery="false" value="com.crt.advproject.gcc.hdrlib.none" valueType="enumerated"/>\n'
    xml += '                <option id="com.crt.advproject.gcc.specs.' + program_id + '" name="Specs" superClass="com.crt.advproject.gcc.specs" useByScannerDiscovery="false" value="com.crt.advproject.gcc.specs.none" valueType="enumerated"/>\n'
    # Add -flto: true
    xml += '                <option id="com.crt.advproject.gcc.lto.' + program_id + '" name="Enable Link-time optimization (-flto)" superClass="com.crt.advproject.gcc.lto" useByScannerDiscovery="false" value="true" valueType="boolean"/>\n'
    # Add -ffat-lto-objects: false
    xml += '                <option id="com.crt.advproject.gcc.lto.fat.' + program_id + '" name="Fat lto objects (-ffat-lto-objects)" superClass="com.crt.advproject.gcc.lto.fat" useByScannerDiscovery="false" value="false" valueType="boolean"/>\n'
    # Add -fmerge-constants: true
    xml += '                <option id="com.crt.advproject.gcc.merge.constants.' + program_id + '" name="Merge Identical Constants (-fmerge-constants)" superClass="com.crt.advproject.gcc.merge.constants" useByScannerDiscovery="false" value="true" valueType="boolean"/>\n'
    # Add -fmacro-prefix-map=...: false
    xml += '                <option id="com.crt.advproject.gcc.prefixmap.' + program_id + '" name="Remove path from __FILE__ (-fmacro-prefix-map)" superClass="com.crt.advproject.gcc.prefixmap" useByScannerDiscovery="false" value="" valueType="string"/>\n'
    # Add -fstack-usage: false
    xml += '                <option id="com.crt.advproject.gcc.stackusage.' + program_id + '" name="Generate Stack Usage Info (-fstack-usage)" superClass="com.crt.advproject.gcc.stackusage" useByScannerDiscovery="false" value="false" valueType="boolean"/>\n'
    # Unused options
    xml += '                <option id="com.crt.advproject.gcc.config.' + program_id + '" name="Obsolete (Config)" superClass="com.crt.advproject.gcc.config" useByScannerDiscovery="false"/>\n'
    xml += '                <option id="com.crt.advproject.gcc.store.' + program_id + '" name="Obsolete (Store)" superClass="com.crt.advproject.gcc.store" useByScannerDiscovery="false"/>\n'
    # Add macro definitions
    xml += '                <option id="gnu.c.compiler.option.preprocessor.def.symbols.' + program_id + '" name="Defined symbols (-D)" superClass="gnu.c.compiler.option.preprocessor.def.symbols" useByScannerDiscovery="false" valueType="definedSymbols" IS_BUILTIN_EMPTY="false" IS_VALUE_EMPTY="false">\n'
    for library in libraries:
        if 'defines' in libraries[library]:
            for define in libraries[library]['defines']:
                define = define.replace('"', '\&quot;')
                xml += '                  <listOptionValue builtIn="false" value="' + define + '"/>\n'
    if 'defines' in configurations[conf]:
        for define in configurations[conf]['defines']:
            define = define.replace('"', '\&quot;')
            xml += '                  <listOptionValue builtIn="false" value="' + define + '"/>\n'
    if 'defines' in programs[program]:
        for define in programs[program]['defines']:
            define = define.replace('"', '\&quot;')
            xml += '                  <listOptionValue builtIn="false" value="' + define + '"/>\n'
    xml += '                </option>\n'
    # Add include paths
    xml += '                <option id="gnu.c.compiler.option.include.paths.' + program_id + '" name="Include paths (-I)" superClass="gnu.c.compiler.option.include.paths" useByScannerDiscovery="false" valueType="includePath" IS_BUILTIN_EMPTY="false" IS_VALUE_EMPTY="false">\n'
    for library in libraries:
        if 'includes' in libraries[library]:
            for include in libraries[library]['includes']:
                xml += '                  <listOptionValue builtIn="false" value="&quot;' + include + '&quot;"/>\n'
    if 'includes' in configurations[conf]:
        for include in configurations[conf]["includes"]:
            xml += '                  <listOptionValue builtIn="false" value="&quot;' + include + '&quot;"/>\n'
    if 'includes' in programs[program]:
        for include in programs[program]['includes']:
            xml += '                  <listOptionValue builtIn="false" value="&quot;' + include + '&quot;"/>\n'
    xml += '                </option>\n'
    # Add other C flags
    xml += '                <option id="gnu.c.compiler.option.misc.other.' + program_id + '" name="Other flags" superClass="gnu.c.compiler.option.misc.other" useByScannerDiscovery="false" value="-c --target=arm-none-eabihf'
    for library in libraries:
        if 'cflags' in libraries[library]:
            for cflag in libraries[library]['cflags']:
                xml += ' ' + cflag
    if 'cflags' in configurations[conf]:
        for cflag in configurations[conf]['cflags']:
            xml += ' ' + cflag
    if 'cflags' in programs[program]:
        for cflag in programs[program]['cflags']:
            xml += ' ' + cflag
    xml += '" valueType="string"/>\n'
    xml += '                <inputType id="com.crt.advproject.compiler.input.' + program_id + '" superClass="com.crt.advproject.compiler.input"/>\n'
    xml += '              </tool>\n'
    ###########################################################################
    # Set up assembler
    ###########################################################################
    xml += '              <tool command="' + clang_path + '" id="com.crt.advproject.gas.lib.release.' + program_id + '" name="MCU Assembler" superClass="com.crt.advproject.gas.lib.release">\n'
    # Other assembler flags: -c --target=arm-none-eabihf
    xml += '                <option id="gnu.both.asm.option.flags.crt.' + program_id + '" name="Assembler flags" superClass="gnu.both.asm.option.flags.crt" useByScannerDiscovery="false" value="-c --target=arm-none-eabihf" valueType="string"/>\n'
    # Add -W: false
    xml += '                <option id="gnu.both.asm.option.warnings.nowarn.' + program_id + '" name="Suppress warnings (-W)" superClass="gnu.both.asm.option.warnings.nowarn" value="false" valueType="boolean"/>\n'
    # Add -v: false
    xml += '                <option id="gnu.both.asm.option.version.1432171472" name="Announce version (-v)" superClass="gnu.both.asm.option.version" value="false" valueType="boolean"/>\n'
    # Architecture: Cortex-M33
    xml += '                <option id="com.crt.advproject.gas.arch.' + program_id + '" name="Architecture" superClass="com.crt.advproject.gas.arch" value="com.crt.advproject.gas.target.cm33" valueType="enumerated"/>\n'
    # FPU: FPv5-SP-D16 Hard ABI
    xml += '                <option id="com.crt.advproject.gas.fpu.' + program_id + '" name="Floating point" superClass="com.crt.advproject.gas.fpu" value="com.crt.advproject.gas.fpu.fpv5sp.hard" valueType="enumerated"/>\n'
    # Thumb mode: true
    xml += '                <option id="com.crt.advproject.gas.thumb.' + program_id + '" name="Thumb mode" superClass="com.crt.advproject.gas.thumb" value="true" valueType="boolean"/>\n'
    # Thumb interworking: false
    xml += '                <option id="com.crt.advproject.gas.thumbinterwork.' + program_id + '" name="Enable Thumb interworking" superClass="com.crt.advproject.gas.thumbinterwork" value="false" valueType="boolean"/>\n'
    # Debug level: none
    xml += '                <option id="com.crt.advproject.gas.debug.' + program_id + '" name="Debug level" superClass="com.crt.advproject.gas.debug" value="com.crt.advproject.gas.debug.none" valueType="enumerated"/>\n'
    # Library headers and specs: none
    xml += '                <option id="com.crt.advproject.gas.hdrlib.' + program_id + '" name="Library headers" superClass="com.crt.advproject.gas.hdrlib" useByScannerDiscovery="false" value="com.crt.advproject.gas.hdrlib.none" valueType="enumerated"/>\n'
    xml += '                <option id="com.crt.advproject.gas.specs.' + program_id + '" name="Specs" superClass="com.crt.advproject.gas.specs" useByScannerDiscovery="false" value="com.crt.advproject.gas.specs.none" valueType="enumerated"/>\n'
    # Unused options
    xml += '                <option id="com.crt.advproject.gas.config.' + program_id + '" name="Obsolete (Config)" superClass="com.crt.advproject.gas.config" useByScannerDiscovery="false"/>\n'
    xml += '                <option id="com.crt.advproject.gas.store.' + program_id + '" name="Obsolete (Store)" superClass="com.crt.advproject.gas.store" useByScannerDiscovery="false"/>\n'
    # Add include paths
    xml += '                <option id="gnu.both.asm.option.include.paths.' + program_id + '" name="Include paths (-I)" superClass="gnu.both.asm.option.include.paths" useByScannerDiscovery="false" valueType="includePath" IS_BUILTIN_EMPTY="false" IS_VALUE_EMPTY="false">\n'
    for library in libraries:
        if 'includes' in libraries[library]:
            for include in libraries[library]['includes']:
                xml += '                  <listOptionValue builtIn="false" value="&quot;' + include + '&quot;"/>\n'
    if 'includes' in configurations[conf]:
        for include in configurations[conf]["includes"]:
            xml += '                  <listOptionValue builtIn="false" value="&quot;' + include + '&quot;"/>\n'
    if 'includes' in programs[program]:
        for include in programs[program]['includes']:
            xml += '                  <listOptionValue builtIn="false" value="&quot;' + include + '&quot;"/>\n'
    xml += '                </option>\n'
    xml += '                <inputType id="cdt.managedbuild.tool.gnu.assembler.input.' + program_id + '" superClass="cdt.managedbuild.tool.gnu.assembler.input"/>\n'
    xml += '                <inputType id="com.crt.advproject.assembler.input.' + program_id + '" name="Additional Assembly Source Files" superClass="com.crt.advproject.assembler.input"/>\n'
    xml += '              </tool>\n'
    ###########################################################################
    # Set up C++ compiler
    ###########################################################################
    xml += '              <tool id="com.crt.advproject.cpp.lib.release.' + program_id + '" name="MCU C++ Compiler" superClass="com.crt.advproject.cpp.lib.release"/>\n'
    ###########################################################################
    # Set up archiver
    ###########################################################################
    xml += '              <tool command="' + ar_path + '" id="com.crt.advproject.ar.lib.release.' + program_id + '" name="MCU Archiver" superClass="com.crt.advproject.ar.lib.release"/>\n'
    xml += '            </toolChain>\n'
    xml += '          </folderInfo>\n'
    ###########################################################################
    # Set up source entries
    ###########################################################################
    xml += '          <sourceEntries>\n'
    if 'directories' in programs[program]:
        for directory in programs[program]['directories']:
            if programs[program]['directories'][directory]:
                xml += '            <entry excluding="' + programs[program]['directories'][directory] + '" flags="LOCAL|VALUE_WORKSPACE_PATH|RESOLVED" kind="sourcePath" name="' + directory + '"/>\n'
            else:
                xml += '            <entry flags="LOCAL|VALUE_WORKSPACE_PATH|RESOLVED" kind="sourcePath" name="' + directory + '"/>\n'
    xml += '          </sourceEntries>\n'
    xml += '        </configuration>\n'
    xml += '      </storageModule>\n'
    xml += '      <storageModule moduleId="org.eclipse.cdt.core.externalSettings"/>\n'
    xml += '    </cconfiguration>\n'

    return xml


#
# Generate and return the footer of core settings.
#
def gen_core_settings_footer():
    return '  </storageModule>\n'


#
# Generate and return the whole cproject file content for a given pair of
# configuration and program.
#
# @conf: the name of the configuration.
# @program: the name of the program.
#
def gen_cproject(conf, program):
    xml =  gen_header()

    # Generate core settings for each program
    xml += gen_core_settings_header()
    xml += gen_core_settings_config(conf, program)
    xml += gen_core_settings_footer()

    # Generate scanner configuration for each program
    xml += gen_scanner_header()
    xml += gen_scanner_config(conf, program)
    xml += gen_scanner_footer()

    # Generate other miscellaneous stuffs
    xml += gen_core_datamodels()
    xml += gen_crt_config()

    xml += gen_footer()

    return xml


#
# Generate and return the file content of language.settings.xml which disables
# discovering compiler's built-in language settings.
#
def gen_language_settings():
    xml  = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
    xml += '<project>\n'
    for conf in configurations:
        for program in sorted(programs.keys()):
            program_id = extras[(conf, program)]['id']
            program_name = conf + '-' + program
            xml += '  <configuration id="com.crt.advproject.config.lib.release.' + program_id + '" name="' + program_name + '">\n'
            xml += '    <extension point="org.eclipse.cdt.core.LanguageSettingsProvider">\n'
            xml += '      <provider copy-of="extension" id="org.eclipse.cdt.ui.UserLanguageSettingsProvider"/>\n'
            xml += '      <provider-reference id="org.eclipse.cdt.core.ReferencedProjectsLanguageSettingsProvider" ref="shared-provider"/>\n'
            xml += '      <provider-reference id="org.eclipse.cdt.managedbuilder.core.MBSLanguageSettingsProvider" ref="shared-provider"/>\n'
            xml += '    </extension>\n'
            xml += '  </configuration>\n'
    xml += '</project>\n'

    return xml


#
# The main function.
#
def main():
    # Generate a .cproject file for each pair of configuration and program
    for conf in configurations:
        for program in programs:
            conf_filename = project_dir + '/.cproject_' + conf + '_' + program
            xml = gen_cproject(conf, program)
            with open(conf_filename, 'w') as f:
                f.write(xml)

    # In addition, also generate language.settings.xml that disable discovering
    # compiler's built-in language settings
    settings_dir = project_dir + '/.settings'
    if not os.path.isdir(settings_dir):
        os.mkdir(settings_dir)
    with open(settings_dir + '/language.settings.xml', 'w') as f:
        f.write(gen_language_settings())


if __name__ == '__main__':
    populate_extra_settings()
    main()
