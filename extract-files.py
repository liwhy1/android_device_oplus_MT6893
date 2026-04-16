#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

import re
from pathlib import Path

from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)
from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)

prop_file = Path(__file__).resolve().parent / "proprietary-files.txt"

if prop_file.exists():
    lines = prop_file.read_text().splitlines()
    new_lines = []

    for line in lines:
        if not re.match(r'^[^\s#]', line):
            new_lines.append(line)
            continue

        line = re.sub(r';?DISABLE_DEPS', '', line)

        if not re.search(r'\.apk', line):
            line = re.sub(r'^([^;|\s]+)(\|.*)?', r'\1;DISABLE_DEPS\2', line)

        new_lines.append(line)

    prop_file.write_text("\n".join(new_lines) + "\n")

blob_fixups: blob_fixups_user_type = {
    'system_ext/lib64/libimsma.so': blob_fixup()
        .replace_needed('libsink.so', 'libsink-mtk.so'),
    'vendor/bin/hw/vendor.mediatek.hardware.pq@2.2-service': blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so')
        .replace_needed('libhidlbase.so', 'libhidlbase-v32.so'),
    'vendor/lib64/hw/vendor.mediatek.hardware.pq@2.15-impl.so': blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so')
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v34.so'),
    'vendor/etc/vintf/manifest/manifest_media_c2_V1_2_default.xml': blob_fixup()
        .regex_replace('1.1', '1.2'),
    ('vendor/lib/hw/audio.primary.mt6893.so',
    'vendor/lib64/hw/audio.primary.mt6893.so'): blob_fixup()
        .replace_needed('libalsautils.so', 'libalsautils-v31.so')
        .replace_needed('libtinyalsa.so', 'libtinyalsa-v32.so'),
    ('vendor/bin/hw/android.hardware.media.c2@1.2-mediatek',
    'vendor/bin/hw/android.hardware.media.c2@1.2-mediatek-64b'): blob_fixup()
        .add_needed('libcodec2_hidl@1.0.so')
        .add_needed('libshim.so')
        .add_needed('libstagefright_foundation_v33.so'),
    'vendor/bin/hw/mtkfusionrild' : blob_fixup()
        .add_needed('libutils-v32.so'),
    ('vendor/bin/hw/android.hardware.gnss-service.mediatek',
    'vendor/lib64/hw/android.hardware.gnss-impl-mediatek.so'): blob_fixup()
        .replace_needed('android.hardware.gnss-V1-ndk_platform.so', 'android.hardware.gnss-V1-ndk.so'),
    'vendor/bin/mtk_agpsd': blob_fixup()
        .replace_needed('libcrypto.so', 'libcrypto-v32.so')
        .replace_needed('libssl.so', 'libssl-v32.so'),
    'vendor/lib64/libmtkcam_featurepolicy.so': blob_fixup()
        .sig_replace('34 E8 87 40 B9', '34 28 02 80 52'),
    'vendor/lib64/libsensor_custom.so': blob_fixup()
        .binary_regex_replace(b'android.sensor.wise_light', b'android.sensor.light\x00\x00\x00\x00\x00')
        .sig_replace('5B 00 01 00', '05 00 00 00'),
    'vendor/bin/hw/android.hardware.wifi@1.0-service-lazy': blob_fixup()
        .replace_needed('libwifi-hal.so', 'libwifi-hal-mtk.so'),
    'system/lib64/libem_support_jni.so': blob_fixup()
        .add_needed('libjni_shim.so'),
    'vendor/lib64/hw/sensors.mt6893.so': blob_fixup()
        .add_needed('libsensors_shim.so'),
    'vendor/lib64/libaalservice.so': blob_fixup()
        .replace_needed('libsensorndkbridge.so', 'libsensorndkbridge-v30.so'),
    'vendor/lib/libcodec2_vndk-mtk.so': blob_fixup()
        .add_needed('libshim_ui.so'),
    ('vendor/bin/hw/android.hardware.neuralnetworks@1.3-service-mtk-neuron',
    'vendor/lib/libnvram.so',
    'vendor/lib64/libnvram.so',
    'odm/bin/hw/vendor.oplus.hardware.charger@1.0-service',
    'vendor/lib64/libsysenv.so'): blob_fixup()
        .add_needed('libbase_shim.so'),
    'odm/bin/hw/vendor.oplus.hardware.cammidasservice@1.0-service': blob_fixup()
        .replace_needed('libhidlbase.so', 'libhidlbase-v32.so'),
    'vendor/lib64/hw/hwcomposer.mt6893.so': blob_fixup()
        .add_needed('libprocessgroup_shim.so')
        .binary_regex_replace(
            b'OnScreenFingerprintPressedIcon',
            b'SurfaceView[UdfpsControllerOve'
    ),
    'vendor/lib64/libmtkcam_stdutils.so': blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so'),
    'vendor/bin/hw/camerahalserver': blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so')
        .replace_needed('libbinder.so', 'libbinder-v32.so')
        .replace_needed('libhidlbase.so', 'libhidlbase-v32.so'),
    'vendor/lib64/hw/android.hardware.camera.provider@2.6-impl-mediatek.so': blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so')
        .replace_needed('libhidlbase.so', 'libhidlbase-v32.so')
        .add_needed('libcamera_metadata_shim.so'),
    'odm/lib64/libui_oplus.so': blob_fixup()
        .replace_needed('android.hardware.graphics.common-V2-ndk_platform.so', 'android.hardware.graphics.common-V2-ndk.so'),
    'vendor/lib64/libmtkisp_metadata.so': blob_fixup()
        .replace_needed('libui.so', 'libui_oplus.so'),
    ('vendor/lib64/libcam.utils.sensorprovider.so',
    'vendor/bin/mnld'): blob_fixup()
        .replace_needed('libsensorndkbridge.so', 'libsensorndkbridge-v30.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'op6893',
    'oplus',
    blob_fixups=blob_fixups,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()

    content = prop_file.read_text()
    content = re.sub(r';?DISABLE_DEPS', '', content)
    prop_file.write_text(content)
