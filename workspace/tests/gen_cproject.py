#!/usr/bin/env python3

import argparse
import os
import sys


#
# Path to the root directory of whole project.
#
root = os.path.abspath(os.path.dirname(sys.argv[0]) + '/../..')

#
# Path to our Clang.
#
clang_path = root + '/build/llvm/bin/clang'

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
project_name = 'tests'


#
# Dict of libraries that need to be linked.
#
libraries = {
    'c': {
        'includes': [
            newlib_path + '/arm-none-eabihf/include',
        ],
        'library_paths': [
            newlib_path + '/arm-none-eabihf/lib',
        ],
    },
    'm': {},
    'clang_rt.builtins-armhf': {
        'library_paths': [
            compiler_rt_path + '/lib/baremetal',
        ],
    },
    'mimxrt685s': {
        'defines': [
            'CPU_MIMXRT685SFVKB',
            'CPU_MIMXRT685SFVKB_cm33',
            'SDK_DEBUGCONSOLE=0',
            'SDK_DEBUGCONSOLE_UART',
        ],
        'includes': [
            '${workspace_loc:/mimxrt685s/CMSIS}',
            '${workspace_loc:/mimxrt685s/board}',
            '${workspace_loc:/mimxrt685s/component/lists}',
            '${workspace_loc:/mimxrt685s/component/uart}',
            '${workspace_loc:/mimxrt685s/device}',
            '${workspace_loc:/mimxrt685s/drivers}',
            '${workspace_loc:/mimxrt685s/flash_config}',
            '${workspace_loc:/mimxrt685s/utilities}',
        ],
        'library_paths': [
            '${workspace_loc:/mimxrt685s/mimxrt685s}',
        ],
    },
}


#
# Dict of common components that are used.
#
components = {
}


#
# Dict of programs to compile and link.
#
programs = {
    'test1': {
    },
}


#
# Dict of configurations.
#
configurations = {
    'baseline': {
        'cflags': [
        ],
        'ldflags': [
            '-Wl,-save-temps',
        ],
    },
}


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
    xml += '    <project id="' + project_name + '.null" name="' + project_name + '" projectType="com.crt.advproject.projecttype.exe"/>\n'
    xml += '  </storageModule>\n'
    xml += '  <storageModule moduleId="org.eclipse.cdt.core.LanguageSettingsProviders"/>\n'
    xml += '  <storageModule moduleId="org.eclipse.cdt.make.core.buildtargets"/>\n'
    xml += '</cproject>\n'
    return xml

#
# Generate and return the header of refresh scopes.
#
def gen_refresh_scope_header():
    return '  <storageModule moduleId="refreshScope" versionNumber="2">\n'


#
# Generate and return the refresh scope for a given program.
#
# @program: the name of the program.
#
def gen_refresh_scope_config(program):
    xml =  '    <configuration configurationName="' + program + '">\n'
    xml += '      <resource resourceType="PROJECT" workspacePath="/' + project_name + '"/>\n'
    xml += '    </configuration>\n'
    return xml


#
# Generate and return the footer of refresh scopes.
#
def gen_refresh_scope_footer():
    return '  </storageModule>\n'


#
# Generate and return the header of scanner configurations.
#
def gen_scanner_header():
    xml =  '  <storageModule moduleId="scannerConfiguration">\n'
    xml += '    <autodiscovery enabled="false" problemReportingEnabled="false" selectedProfileId=""/>\n'
    return xml


#
# Generate and return the scanner configuration for a given program.
#
# @program: the name of the program.
#
def gen_scanner_config(program):
    program_id = programs[program]['id']
    xml =  '    <scannerConfigBuildInfo instanceId="com.crt.advproject.config.exe.release.' + program_id + ';com.crt.advproject.config.exe.release.' + program_id + '.;com.crt.advproject.gcc.exe.release.' + program_id + ';com.crt.advproject.compiler.input.' + program_id + '">\n'
    xml += '      <autodiscovery enabled="false" problemReportingEnabled="false" selectedProfileId=""/>\n'
    xml += '    </scannerConfigBuildInfo>\n'
    xml =  '    <scannerConfigBuildInfo instanceId="com.crt.advproject.config.exe.release.' + program_id + ';com.crt.advproject.config.exe.release.' + program_id + '.;com.crt.advproject.gas.exe.release.' + program_id + ';com.crt.advproject.assembler.input.' + program_id + '">\n'
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
    xml =  '    <storageModule moduleId="com.nxp.mcuxpresso.core.datamodels">\n'
    xml += '      <sdkName>SDK_2.x_EVK-MIMXRT685</sdkName>\n'
    xml += '      <sdkExample>evkmimxrt685_hello_world</sdkExample>\n'
    xml += '      <sdkVersion>2.8.2</sdkVersion>\n'
    xml += '      <sdkComponents>platform.drivers.common.MIMXRT685S;platform.drivers.reset.MIMXRT685S;platform.drivers.clock.MIMXRT685S;device.MIMXRT685S_CMSIS.MIMXRT685S;platform.Include_core_cm33.MIMXRT685S;platform.Include_common.MIMXRT685S;platform.Include_dsp.MIMXRT685S;platform.drivers.power.MIMXRT685S;utility.debug_console.MIMXRT685S;component.serial_manager.MIMXRT685S;component.lists.MIMXRT685S;platform.utilities.assert.MIMXRT685S;component.usart_adapter.MIMXRT685S;platform.drivers.flexcomm_usart.MIMXRT685S;platform.drivers.flexcomm.MIMXRT685S;platform.drivers.flash_config.MIMXRT685S;platform.drivers.flexspi.MIMXRT685S;platform.drivers.cache_cache64.MIMXRT685S;component.serial_manager_uart.MIMXRT685S;device.MIMXRT685S_startup.MIMXRT685S;platform.drivers.lpc_iopctl.MIMXRT685S;platform.drivers.lpc_gpio.MIMXRT685S;platform.utilities.misc_utilities.MIMXRT685S;evkmimxrt685_hello_world;</sdkComponents>\n'
    xml += '      <boardId>evkmimxrt685</boardId>\n'
    xml += '      <package>MIMXRT685SFVKB</package>\n'
    xml += '      <core>cm33</core>\n'
    xml += '      <coreId>cm33_MIMXRT685S</coreId>\n'
    xml += '    </storageModule>\n'
    return xml


#
# Generate and return the MCU configuration.
#
def gen_crt_config():
    xml =  '    <storageModule moduleId="com.crt.config">\n'
    xml += '      <projectStorage>&lt;?xml version="1.0" encoding="UTF-8"?&gt;\n'
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
    xml += '      </projectStorage>\n'
    xml += '    </storageModule>\n'
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
    program_id = programs[program]['id']

    xml =  '    <!-- Configuration of ' + program + ' -->\n'
    xml += '    <cconfiguration id="com.crt.advproject.config.exe.release.' + program_id + '">\n'
    xml += '      <storageModule buildSystemId="org.eclipse.cdt.managedbuilder.core.configurationDataProvider" id="com.crt.advproject.config.exe.release.' + program_id + '" moduleId="org.eclipse.cdt.core.settings" name="' + program + '">\n'
    xml += '        <externalSettings/>\n'
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
    xml += '        <configuration artifactExtension="axf" artifactName="${ConfigName}" buildArtefactType="org.eclipse.cdt.build.core.buildArtefactType.exe" buildProperties="org.eclipse.cdt.build.core.buildArtefactType=org.eclipse.cdt.build.core.buildArtefactType.exe" cleanCommand="rm -rf" description="Release build of ' + program + '" errorParsers="org.eclipse.cdt.core.CWDLocator;org.eclipse.cdt.core.GmakeErrorParser;org.eclipse.cdt.core.GCCErrorParser;org.eclipse.cdt.core.GLDErrorParser;org.eclipse.cdt.core.GASErrorParser" id="com.crt.advproject.config.exe.release.' + program_id + '" name="' + program + '" parent="com.crt.advproject.config.exe.release" postannouncebuildStep="Performing post-build steps" postbuildStep="arm-none-eabi-size &quot;${BuildArtifactFileName}&quot;">\n'
    xml += '          <folderInfo id="com.crt.advproject.config.exe.release.' + program_id + '." name="/" resourcePath="">\n'
    xml += '            <toolChain id="com.crt.advproject.toolchain.exe.release.' + program_id + '" name="NXP MCU Tools" superClass="com.crt.advproject.toolchain.exe.release">\n'
    xml += '              <targetPlatform binaryParser="org.eclipse.cdt.core.ELF;org.eclipse.cdt.core.GNU_ELF" id="com.crt.advproject.platform.exe.release.' + program_id + '" name="ARM-based MCU (Release)" superClass="com.crt.advproject.platform.exe.release"/>\n'
    xml += '              <builder buildPath="${ProjDirPath}/' + program + '" id="com.crt.advproject.builder.exe.release.' + program_id + '" keepEnvironmentInBuildfile="false" managedBuildOn="true" name="Gnu Make Builder" superClass="com.crt.advproject.builder.exe.release"/>\n'
    ###########################################################################
    # Set up C compiler
    ###########################################################################
    xml += '              <tool command="' + clang_path + '" id="com.crt.advproject.gcc.exe.release.' + program_id + '" name="MCU C Compiler" superClass="com.crt.advproject.gcc.exe.release">\n'
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
    # Other optmization flags: -ffunction-sections -fdata-sections -fomit-frame-pointer
    xml += '                <option id="gnu.c.compiler.option.optimization.flags.' + program_id + '" name="Other optimization flags" superClass="gnu.c.compiler.option.optimization.flags" useByScannerDiscovery="false" value="-ffunction-sections -fdata-sections -fomit-frame-pointer" valueType="string"/>\n'
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
    xml += '                <option id="com.crt.advproject.gcc.exe.release.option.debugging.level.' + program_id + '" name="Debug Level" superClass="com.crt.advproject.gcc.exe.release.option.debugging.level" useByScannerDiscovery="false" value="gnu.c.debugging.level.default" valueType="enumerated"/>\n'
    # Optimization level: -Os
    xml += '                <option id="com.crt.advproject.gcc.exe.release.option.optimization.level.' + program_id + '" name="Optimization Level" superClass="com.crt.advproject.gcc.exe.release.option.optimization.level" useByScannerDiscovery="false" value="gnu.c.optimization.level.size" valueType="enumerated"/>\n'
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
                xml += '                  <listOptionValue builtIn="false" value="' + define + '"/>\n'
    for comp in components:
        if 'defines' in components[comp]:
            for define in components[comp]['defines']:
                xml += '                  <listOptionValue builtIn="false" value="' + define + '"/>\n'
    if 'defines' in configurations[conf]:
        for define in configurations[conf]['defines']:
            xml += '                  <listOptionValue builtIn="false" value="' + define + '"/>\n'
    if 'defines' in programs[program]:
        for define in programs[program]['defines']:
            xml += '                  <listOptionValue builtIn="false" value="' + define + '"/>\n'
    xml += '                  <listOptionValue builtIn="false" value="BENCHMARK_NAME=\&quot;' + program + '\&quot;"/>\n'
    xml += '                </option>\n'
    # Add include paths
    xml += '                <option id="gnu.c.compiler.option.include.paths.' + program_id + '" name="Include paths (-I)" superClass="gnu.c.compiler.option.include.paths" useByScannerDiscovery="false" valueType="includePath" IS_BUILTIN_EMPTY="false" IS_VALUE_EMPTY="false">\n'
    for library in libraries:
        if 'includes' in libraries[library]:
            for include in libraries[library]['includes']:
                xml += '                  <listOptionValue builtIn="false" value="&quot;' + include + '&quot;"/>\n'
    for comp in components:
        if 'includes' in components[comp]:
            for include in components[comp]['includes']:
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
    for comp in components:
        if 'cflags' in components[comp]:
            for cflag in components[comp]['cflags']:
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
    # Set up C linker
    ###########################################################################
    xml += '              <tool command="' + clang_path + '" id="com.crt.advproject.link.exe.release.' + program_id + '" name="MCU Linker" superClass="com.crt.advproject.link.exe.release">\n'
    # Add -nostartfiles: true
    xml += '                <option id="gnu.c.link.option.nostart.' + program_id + '" name="Do not use standard start files (-nostartfiles)" superClass="gnu.c.link.option.nostart" useByScannerDiscovery="false" value="true" valueType="boolean"/>\n'
    # Add -nodefaultlibs: true
    xml += '                <option id="gnu.c.link.option.nodeflibs.' + program_id + '" name="Do not use default libraries (-nodefaultlibs)" superClass="gnu.c.link.option.nodeflibs" useByScannerDiscovery="false" value="true" valueType="boolean"/>\n'
    # Add -nostdlibs: true
    xml += '                <option id="gnu.c.link.option.nostdlibs.' + program_id + '" name="No startup or default libs (-nostdlib)" superClass="gnu.c.link.option.nostdlibs" useByScannerDiscovery="false" value="true" valueType="boolean"/>\n'
    # Add -static: true
    xml += '                <option id="gnu.c.link.option.noshared.' + program_id + '" name="No shared libraries (-static)" superClass="gnu.c.link.option.noshared" useByScannerDiscovery="false" value="true" valueType="boolean"/>\n'
    # Add -s: false
    xml += '                <option id="gnu.c.link.option.strip.' + program_id + '" name="Omit all symbol information (-s)" superClass="gnu.c.link.option.strip" useByScannerDiscovery="false"/>\n'
    # Add -shared: false
    xml += '                <option id="gnu.c.link.option.shared.' + program_id + '" name="Shared (-shared)" superClass="gnu.c.link.option.shared" useByScannerDiscovery="false" value="false" valueType="boolean"/>\n'
    # Add -Wl,-soname=...: false
    xml += '                <option id="gnu.c.link.option.soname.' + program_id + '" name="Shared object name (-Wl,-soname=)" superClass="gnu.c.link.option.soname" useByScannerDiscovery="false" value="" valueType="string"/>\n'
    # Add -Wl,--out-implib=...: false
    xml += '                <option id="gnu.c.link.option.implname.' + program_id + '" name="Import Library name (-Wl,--out-implib=)" superClass="gnu.c.link.option.implname" useByScannerDiscovery="false" value="" valueType="string"/>\n'
    # Add -Wl,--output-def=...: false
    xml += '                <option id="gnu.c.link.option.defname.' + program_id + '" name="DEF file name (-Wl,--output-def=)" superClass="gnu.c.link.option.defname" useByScannerDiscovery="false" value="" valueType="string"/>\n'
    # Add Xlinker flags
    xml += '                <option id="gnu.c.link.option.other.' + program_id + '" name="Other options (-Xlinker [option])" superClass="gnu.c.link.option.other" useByScannerDiscovery="false" valueType="stringList" IS_BUILTIN_EMPTY="false" IS_VALUE_EMPTY="false">\n'
    xml += '                  <listOptionValue builtIn="false" value="-Map=&quot;${BuildArtifactFileBaseName}.map&quot;"/>\n'
    xml += '                  <listOptionValue builtIn="false" value="--gc-sections"/>\n'
    xml += '                  <listOptionValue builtIn="false" value="--undefined=flexspi_config"/>\n'  # XXX: Hack!
    xml += '                  <listOptionValue builtIn="false" value="--undefined-glob=__aeabi_*"/>\n'  # XXX: Hack!
    xml += '                </option>\n'
    # Architecture: Cortex-M33
    xml += '                <option id="com.crt.advproject.link.arch.' + program_id + '" name="Architecture" superClass="com.crt.advproject.link.arch" useByScannerDiscovery="false" value="com.crt.advproject.link.target.cm33" valueType="enumerated"/>\n'
    # FPU: FPv5-SP-D16 Hard ABI
    xml += '                <option id="com.crt.advproject.link.fpu.' + program_id + '" name="Floating point" superClass="com.crt.advproject.link.fpu" useByScannerDiscovery="false" value="com.crt.advproject.link.fpu.fpv5sp.hard" valueType="enumerated"/>\n'
    # TrustZone type: none
    xml += '                <option id="com.crt.advproject.link.securestate.' + program_id + '" name="TrustZone Project Type" superClass="com.crt.advproject.link.securestate" useByScannerDiscovery="false" value="com.crt.advproject.link.securestate.none" valueType="enumerated"/>\n'
    xml += '                <option id="com.crt.advproject.link.sgstubs.placement.' + program_id + '" name="Secure Gateway Placement" superClass="com.crt.advproject.link.sgstubs.placement" useByScannerDiscovery="false" value="com.crt.advproject.link.sgstubs.append" valueType="enumerated"/>\n'
    xml += '                <option id="com.crt.advproject.link.sgstubenable.' + program_id + '" name="Enable generation of Secure Gateway Import Library" superClass="com.crt.advproject.link.sgstubenable" useByScannerDiscovery="false"/>\n'
    xml += '                <option id="com.crt.advproject.link.nonsecureobject.' + program_id + '" name="Secure Gateway Import Library" superClass="com.crt.advproject.link.nonsecureobject" useByScannerDiscovery="false"/>\n'
    xml += '                <option id="com.crt.advproject.link.inimplib.' + program_id + '" name="Input Secure Gateway Import Library" superClass="com.crt.advproject.link.inimplib" useByScannerDiscovery="false"/>\n'
    # Thumb mode: true
    xml += '                <option id="com.crt.advproject.link.thumb.' + program_id + '" name="Thumb mode" superClass="com.crt.advproject.link.thumb" value="true" valueType="boolean"/>\n'
    # Linker script path: "${ProjDirPath}/LinkerScript.ld"
    xml += '                <option id="com.crt.advproject.link.script.' + program_id + '" name="Linker script" superClass="com.crt.advproject.link.script" useByScannerDiscovery="false" value="&quot;${ProjDirPath}/LinkerScript.ld&quot;" valueType="string"/>\n'
    # Linker script directory: none
    xml += '                <option id="com.crt.advproject.link.scriptdir.' + program_id + '" name="Script path" superClass="com.crt.advproject.link.scriptdir" useByScannerDiscovery="false" value="" valueType="string"/>\n'
    # Manage linker script: false
    xml += '                <option id="com.crt.advproject.link.manage.' + program_id + '" name="Manage linker script" superClass="com.crt.advproject.link.manage" useByScannerDiscovery="false" value="false" valueType="boolean"/>\n'
    xml += '                <option id="com.crt.advproject.link.memory.load.image.' + program_id + '" name="Plain load image" superClass="com.crt.advproject.link.memory.load.image" useByScannerDiscovery="false" value="false;" valueType="string"/>\n'
    xml += '                <option id="com.crt.advproject.link.memory.heapAndStack.' + program_id + '" name="Heap and Stack options" superClass="com.crt.advproject.link.memory.heapAndStack" useByScannerDiscovery="false" value="&amp;Heap:Default;Post Data;Default&amp;Stack:Default;End;Default" valueType="string"/>\n'
    xml += '                <option id="com.crt.advproject.link.memory.heapAndStack.style.' + program_id + '" name="Heap and Stack placement" superClass="com.crt.advproject.link.memory.heapAndStack.style" useByScannerDiscovery="false" defaultValue="com.crt.advproject.heapAndStack.mcuXpressoStyle" valueType="enumerated"/>\n'
    xml += '                <option id="com.crt.advproject.link.memory.data.' + program_id + '" name="Global data placement" superClass="com.crt.advproject.link.memory.data" useByScannerDiscovery="false" value="Default" valueType="string"/>\n'
    xml += '                <option id="com.crt.advproject.link.memory.sections.' + program_id + '" name="Extra linker script input sections" superClass="com.crt.advproject.link.memory.sections" useByScannerDiscovery="false" valueType="stringList" IS_BUILTIN_EMPTY="false" IS_VALUE_EMPTY="true"/>\n'
    xml += '                <option id="com.crt.advproject.link.toram.' + program_id + '" name="Link application to RAM" superClass="com.crt.advproject.link.toram" useByScannerDiscovery="false" value="false" valueType="boolean"/>\n'
    xml += '                <option id="com.crt.advproject.link.stackOffset.' + program_id + '" name="Stack offset" superClass="com.crt.advproject.link.stackOffset" useByScannerDiscovery="false" value="0" valueType="string"/>\n'
    xml += '                <option id="com.crt.advproject.link.gcc.hdrlib.' + program_id + '" name="Library" superClass="com.crt.advproject.link.gcc.hdrlib" useByScannerDiscovery="false" value="com.crt.advproject.gcc.link.hdrlib.none" valueType="enumerated"/>\n'
    xml += '                <option id="com.crt.advproject.link.gcc.nanofloat.' + program_id + '" name="Enable printf float " superClass="com.crt.advproject.link.gcc.nanofloat" useByScannerDiscovery="false"/>\n'
    xml += '                <option id="com.crt.advproject.link.gcc.nanofloat.scanf.' + program_id + '" name="Enable scanf float " superClass="com.crt.advproject.link.gcc.nanofloat.scanf" useByScannerDiscovery="false"/>\n'
    # Add -flto: true
    xml += '                <option id="com.crt.advproject.link.gcc.lto.' + program_id + '" name="Enable Link-time optimization (-flto)" superClass="com.crt.advproject.link.gcc.lto" useByScannerDiscovery="false" value="true" valueType="boolean"/>\n'
    # LTO optimization level: -Os
    xml += '                <option id="com.crt.advproject.link.gcc.lto.optmization.level.' + program_id + '" name="Link-time optimization level" superClass="com.crt.advproject.link.gcc.lto.optmization.level" useByScannerDiscovery="false" value="link.c.optimization.level.size" valueType="enumerated"/>\n'
    # No multicore options: true
    xml += '                <option id="com.crt.advproject.link.gcc.multicore.empty.' + program_id + '" name="No Multicore options for this project" superClass="com.crt.advproject.link.gcc.multicore.empty" useByScannerDiscovery="false" value="true" valueType="string"/>\n'
    xml += '                <option id="com.crt.advproject.link.gcc.multicore.master.' + program_id + '" name="Multicore master" superClass="com.crt.advproject.link.gcc.multicore.master" useByScannerDiscovery="false"/>\n'
    xml += '                <option id="com.crt.advproject.link.gcc.multicore.master.userobjs.' + program_id + '" name="Slave Objects (not visible)" superClass="com.crt.advproject.link.gcc.multicore.master.userobjs" useByScannerDiscovery="false" valueType="userObjs" IS_BUILTIN_EMPTY="false" IS_VALUE_EMPTY="true"/>\n'
    xml += '                <option id="com.crt.advproject.link.gcc.multicore.slave.' + program_id + '" name="Multicore configuration" superClass="com.crt.advproject.link.gcc.multicore.slave" useByScannerDiscovery="false"/>\n'
    # Unused options
    xml += '                <option id="com.crt.advproject.link.crpenable.' + program_id + '" name="Enable automatic placement of Code Read Protection field in image" superClass="com.crt.advproject.link.crpenable" useByScannerDiscovery="false"/>\n'
    xml += '                <option id="com.crt.advproject.link.flashconfigenable.' + program_id + '" name="Enable automatic placement of Flash Configuration field in image" superClass="com.crt.advproject.link.flashconfigenable" useByScannerDiscovery="false" value="true" valueType="boolean"/>\n'
    xml += '                <option id="com.crt.advproject.link.ecrp.' + program_id + '" name="Enhanced CRP" superClass="com.crt.advproject.link.ecrp" useByScannerDiscovery="false"/>\n'
    xml += '                <option id="com.crt.advproject.link.config.' + program_id + '" name="Obsolete (Config)" superClass="com.crt.advproject.link.config" useByScannerDiscovery="false"/>\n'
    xml += '                <option id="com.crt.advproject.link.store.' + program_id + '" name="Obsolete (Store)" superClass="com.crt.advproject.link.store" useByScannerDiscovery="false"/>\n'
    # Add linked libraries
    xml += '                <option id="gnu.c.link.option.libs.' + program_id + '" name="Libraries (-l)" superClass="gnu.c.link.option.libs" useByScannerDiscovery="false" valueType="libs" IS_BUILTIN_EMPTY="false" IS_VALUE_EMPTY="false">\n'
    for library in libraries:
        xml += '                  <listOptionValue builtIn="false" value="' + library + '"/>\n'
    xml += '                </option>\n'
    # Add linker flags
    xml += '                <option id="gnu.c.link.option.ldflags.' + program_id + '" name="Linker flags" superClass="gnu.c.link.option.ldflags" useByScannerDiscovery="false" value="-fuse-ld=lld --target=arm-none-eabihf'
    for library in libraries:
        if 'ldflags' in libraries[library]:
            for ldflag in libraries[library]['ldflags']:
                xml += ' ' + ldflag
    for comp in components:
        if 'ldflags' in components[comp]:
            for ldflag in components[comp]['ldflags']:
                xml += ' ' + ldflag
    if 'ldflags' in configurations[conf]:
        for ldflag in configurations[conf]['ldflags']:
            xml += ' ' + ldflag
    if 'ldflags' in programs[program]:
        for ldflag in programs[program]['ldflags']:
            xml += ' ' + ldflag
    xml += '" valueType="string"/>\n'
    # Add library search paths
    xml += '                <option id="gnu.c.link.option.paths.' + program_id + '" name="Library search path (-L)" superClass="gnu.c.link.option.paths" useByScannerDiscovery="false" valueType="libPaths" IS_BUILTIN_EMPTY="false" IS_VALUE_EMPTY="false">\n'
    for library in libraries:
        if 'library_paths' in libraries[library]:
            for library_path in libraries[library]['library_paths']:
                xml += '                  <listOptionValue builtIn="false" value="&quot;' + library_path + '&quot;"/>\n'
    xml += '                </option>\n'
    # Add other objects
    xml += '                <option id="gnu.c.link.option.userobjs.' + program_id + '" name="Other objects" superClass="gnu.c.link.option.userobjs" useByScannerDiscovery="false" valueType="userObjs" IS_BUILTIN_EMPTY="false" IS_VALUE_EMPTY="false">\n'
    for library in libraries:
        if 'objects' in libraries[library]:
            for obj in libraries[library]['objects']:
                xml += '                  <listOptionValue builtIn="false" value="&quot;' + obj + '&quot;"/>\n'
    xml += '                </option>\n'
    xml += '                <inputType id="cdt.managedbuild.tool.gnu.c.linker.input.' + program_id + '" superClass="cdt.managedbuild.tool.gnu.c.linker.input">\n'
    xml += '                  <additionalInput kind="additionalinputdependency" paths="$(USER_OBJS)"/>\n'
    xml += '                  <additionalInput kind="additionalinput" paths="$(LIBS)"/>\n'
    xml += '                </inputType>\n'
    xml += '              </tool>\n'
    ###########################################################################
    # Set up assembler
    ###########################################################################
    xml += '              <tool command="' + clang_path + '" id="com.crt.advproject.gas.exe.release.' + program_id + '" name="MCU Assembler" superClass="com.crt.advproject.gas.exe.release">\n'
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
    for comp in components:
        if 'includes' in components[comp]:
            for include in components[comp]['includes']:
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
    xml += '              <tool id="com.crt.advproject.cpp.exe.release.' + program_id + '" name="MCU C++ Compiler" superClass="com.crt.advproject.cpp.exe.release">\n'
    xml += '                <option id="com.crt.advproject.cpp.fpu.' + program_id + '" name="Floating point" superClass="com.crt.advproject.cpp.fpu"/>\n'
    xml += '                <option id="com.crt.advproject.cpp.hdrlib.' + program_id + '" name="Library headers" superClass="com.crt.advproject.cpp.hdrlib"/>\n'
    xml += '              </tool>\n'
    ###########################################################################
    # Set up C++ linker
    ###########################################################################
    xml += '              <tool id="com.crt.advproject.link.cpp.exe.release.' + program_id + '" name="MCU C++ Linker" superClass="com.crt.advproject.link.cpp.exe.release">\n'
    xml += '                <option id="com.crt.advproject.link.cpp.fpu.' + program_id + '" name="Floating point" superClass="com.crt.advproject.link.cpp.fpu"/>\n'
    xml += '                <option id="com.crt.advproject.link.cpp.hdrlib.' + program_id + '" name="Library" superClass="com.crt.advproject.link.cpp.hdrlib"/>\n'
    xml += '              </tool>\n'
    ###########################################################################
    # Set up debugger
    ###########################################################################
    xml += '              <tool id="com.crt.advproject.tool.debug.release.' + program_id + '" name="MCU Debugger" superClass="com.crt.advproject.tool.debug.release"/>\n'
    xml += '            </toolChain>\n'
    xml += '          </folderInfo>\n'
    ###########################################################################
    # Set up source entries
    ###########################################################################
    xml += '          <sourceEntries>\n'
    for comp in components:
        if 'directories' in components[comp]:
            for directory in components[comp]['directories']:
                if components[comp]['directories'][directory]:
                    xml += '            <entry excluding="' + components[comp]['directories'][directory] + '" flags="LOCAL|VALUE_WORKSPACE_PATH|RESOLVED" kind="sourcePath" name="' + directory + '"/>\n'
                else:
                    xml += '            <entry flags="LOCAL|VALUE_WORKSPACE_PATH|RESOLVED" kind="sourcePath" name="' + directory + '"/>\n'
    tests_exclude = ''
    for p in programs:
        if p != program:
            tests_exclude += p + '|'
    tests_exclude = tests_exclude[:-1]
    xml += '            <entry excluding="' + tests_exclude + '" flags="LOCAL|VALUE_WORKSPACE_PATH|RESOLVED" kind="sourcePath" name="src"/>\n'
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
# Generate and return the whole cproject file content for the given
# configuration.
#
# @conf: the name of the configuration to use.
#
def gen_cproject(conf):
    xml =  gen_header()

    # Generate core settings for each program
    xml += gen_core_settings_header()
    for program in sorted(programs.keys()):
        xml += gen_core_settings_config(conf, program)
    xml += gen_core_settings_footer()

    # Generate refresh scope for each program
    xml += gen_refresh_scope_header()
    for program in sorted(programs.keys()):
        xml += gen_refresh_scope_config(program)
    xml += gen_refresh_scope_footer()

    # Generate scanner configuration for each program
    xml += gen_scanner_header()
    for program in sorted(programs.keys()):
        xml += gen_scanner_config(program)
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
    for program in sorted(programs.keys()):
        xml += '  <configuration id="com.crt.advproject.config.exe.release.' + programs[program]['id'] + '" name="' + program + '">\n'
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
    # Assign an ID to each program
    program_id = 0
    for program in sorted(programs.keys()):
        programs[program]['id'] = str(program_id)
        program_id += 1

    # Generate cproject file for each configuration
    for conf in configurations:
        conf_filename = project_dir + '/cproject_' + conf
        xml = gen_cproject(conf)
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
    main()
