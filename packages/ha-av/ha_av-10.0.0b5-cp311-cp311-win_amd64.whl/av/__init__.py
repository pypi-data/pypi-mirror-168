

""""""# start delvewheel patch
def _delvewheel_init_patch_0_0_25():
    import os
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'ha_av.libs'))
    if sys.version_info[:2] >= (3, 8) and not os.path.exists(os.path.join(sys.base_prefix, 'conda-meta')) or sys.version_info[:2] >= (3, 10):
        os.add_dll_directory(libs_dir)
    else:
        from ctypes import WinDLL
        with open(os.path.join(libs_dir, '.load-order-ha_av-10.0.0b5')) as file:
            load_order = file.read().split()
        for lib in load_order:
            WinDLL(os.path.join(libs_dir, lib))


_delvewheel_init_patch_0_0_25()
del _delvewheel_init_patch_0_0_25
# end delvewheel patch

import os
import sys


# Some Python versions distributed by Conda have a buggy `os.add_dll_directory`
# which prevents binary wheels from finding the FFmpeg DLLs in the `av.libs`
# directory. We work around this by adding `av.libs` to the PATH.
if (
    os.name == "nt"
    and sys.version_info[:2] in ((3, 8), (3, 9))
    and os.path.exists(os.path.join(sys.base_prefix, "conda-meta"))
):
    os.environ["PATH"] = (
        os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "av.libs"))
        + os.pathsep
        + os.environ["PATH"]
    )

# Capture logging (by importing it).
from av import logging
# MUST import the core before anything else in order to initalize the underlying
# library that is being wrapped.
from av._core import library_versions, time_base
# For convenience, IMPORT ALL OF THE THINGS (that are constructable by the user).
from av.about import __version__
from av.audio.fifo import AudioFifo
from av.audio.format import AudioFormat
from av.audio.frame import AudioFrame
from av.audio.layout import AudioLayout
from av.audio.resampler import AudioResampler
from av.bitstream import (
    BitStreamFilter,
    BitStreamFilterContext,
    bitstream_filters_available
)
from av.codec.codec import Codec, codecs_available
from av.codec.context import CodecContext
from av.container import open
from av.error import *  # noqa: F403; This is limited to exception types.
from av.format import ContainerFormat, formats_available
from av.packet import Packet
from av.video.format import VideoFormat
from av.video.frame import VideoFrame


# Backwards compatibility
AVError = FFmpegError  # noqa: F405
