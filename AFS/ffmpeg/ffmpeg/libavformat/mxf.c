/*
 * MXF
 * Copyright (c) 2006 SmartJog S.A., Baptiste Coudurier <baptiste dot coudurier at smartjog dot com>
 *
 * This file is part of FFmpeg.
 *
 * FFmpeg is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * FFmpeg is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with FFmpeg; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
 */

#include "mxf.h"

/**
 * SMPTE RP224 http://www.smpte-ra.org/mdd/index.html
 */
const MXFCodecUL ff_mxf_data_definition_uls[] = {
    { { 0x06,0x0E,0x2B,0x34,0x04,0x01,0x01,0x01,0x01,0x03,0x02,0x02,0x01,0x00,0x00,0x00 }, 13, AVMEDIA_TYPE_VIDEO },
    { { 0x06,0x0E,0x2B,0x34,0x04,0x01,0x01,0x01,0x01,0x03,0x02,0x02,0x02,0x00,0x00,0x00 }, 13, AVMEDIA_TYPE_AUDIO },
    { { 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00 },  0,  AVMEDIA_TYPE_DATA },
};

const MXFCodecUL ff_mxf_codec_uls[] = {
    /* PictureEssenceCoding */
    { { 0x06,0x0E,0x2B,0x34,0x04,0x01,0x01,0x03,0x04,0x01,0x02,0x02,0x01,0x01,0x11,0x00 }, 14, CODEC_ID_MPEG2VIDEO }, /* MP@ML Long GoP */
    { { 0x06,0x0E,0x2B,0x34,0x04,0x01,0x01,0x01,0x04,0x01,0x02,0x02,0x01,0x02,0x01,0x01 }, 14, CODEC_ID_MPEG2VIDEO }, /* D-10 50Mbps PAL */
    { { 0x06,0x0E,0x2B,0x34,0x04,0x01,0x01,0x03,0x04,0x01,0x02,0x02,0x01,0x03,0x03,0x00 }, 14, CODEC_ID_MPEG2VIDEO }, /* MP@HL Long GoP */
    { { 0x06,0x0E,0x2B,0x34,0x04,0x01,0x01,0x03,0x04,0x01,0x02,0x02,0x01,0x04,0x02,0x00 }, 14, CODEC_ID_MPEG2VIDEO }, /* 422P@HL I-Frame */
    { { 0x06,0x0E,0x2B,0x34,0x04,0x01,0x01,0x03,0x04,0x01,0x02,0x02,0x01,0x20,0x02,0x03 }, 14,      CODEC_ID_MPEG4 }, /* XDCAM proxy_pal030926.mxf */
    { { 0x06,0x0E,0x2B,0x34,0x04,0x01,0x01,0x01,0x04,0x01,0x02,0x02,0x02,0x01,0x02,0x00 }, 13,    CODEC_ID_DVVIDEO }, /* DV25 IEC PAL */
    { { 0x06,0x0E,0x2B,0x34,0x04,0x01,0x01,0x07,0x04,0x01,0x02,0x02,0x03,0x01,0x01,0x00 }, 14,   CODEC_ID_JPEG2000 }, /* JPEG2000 Codestream */
    { { 0x06,0x0E,0x2B,0x34,0x04,0x01,0x01,0x01,0x04,0x01,0x02,0x01,0x7F,0x00,0x00,0x00 }, 13,   CODEC_ID_RAWVIDEO }, /* Uncompressed */
    { { 0x06,0x0E,0x2B,0x34,0x04,0x01,0x01,0x01,0x04,0x01,0x02,0x02,0x03,0x02,0x00,0x00 }, 14,      CODEC_ID_DNXHD }, /* SMPTE VC-3/DNxHD */
    /* SoundEssenceCompression */
    { { 0x06,0x0E,0x2B,0x34,0x04,0x01,0x01,0x01,0x04,0x02,0x02,0x01,0x00,0x00,0x00,0x00 }, 13,  CODEC_ID_PCM_S16LE }, /* Uncompressed */
    { { 0x06,0x0E,0x2B,0x34,0x04,0x01,0x01,0x01,0x04,0x02,0x02,0x01,0x7F,0x00,0x00,0x00 }, 13,  CODEC_ID_PCM_S16LE },
    { { 0x06,0x0E,0x2B,0x34,0x04,0x01,0x01,0x07,0x04,0x02,0x02,0x01,0x7E,0x00,0x00,0x00 }, 13,  CODEC_ID_PCM_S16BE }, /* From Omneon MXF file */
    { { 0x06,0x0E,0x2B,0x34,0x04,0x01,0x01,0x04,0x04,0x02,0x02,0x02,0x03,0x01,0x01,0x00 }, 15,   CODEC_ID_PCM_ALAW }, /* XDCAM Proxy C0023S01.mxf */
    { { 0x06,0x0E,0x2B,0x34,0x04,0x01,0x01,0x01,0x04,0x02,0x02,0x02,0x03,0x02,0x01,0x00 }, 15,        CODEC_ID_AC3 },
    { { 0x06,0x0E,0x2B,0x34,0x04,0x01,0x01,0x01,0x04,0x02,0x02,0x02,0x03,0x02,0x05,0x00 }, 15,        CODEC_ID_MP2 }, /* MP2 or MP3 */
  //{ { 0x06,0x0E,0x2B,0x34,0x04,0x01,0x01,0x01,0x04,0x02,0x02,0x02,0x03,0x02,0x1C,0x00 }, 15,    CODEC_ID_DOLBY_E }, /* Dolby-E */
    { { 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00 },  0,       CODEC_ID_NONE },
};

const MXFPixelLayout ff_mxf_pixel_layouts[] = {
    /**
     * See SMPTE 377M E.2.46
     *
     * Note: Only RGB, palette based and "abnormal" YUV pixel formats like 4:2:2:4 go here.
     *       For regular YUV, use CDCIPictureEssenceDescriptor.
     *
     * Note: Do not use these for encoding descriptors for little-endian formats until we
     *       get samples or official word from SMPTE on how/if those can be encoded.
     */
    {PIX_FMT_ABGR,    {'A', 8,  'B', 8,  'G', 8, 'R', 8                 }},
    {PIX_FMT_ARGB,    {'A', 8,  'R', 8,  'G', 8, 'B', 8                 }},
    {PIX_FMT_BGR24,   {'B', 8,  'G', 8,  'R', 8                         }},
    {PIX_FMT_BGRA,    {'B', 8,  'G', 8,  'R', 8, 'A', 8                 }},
    {PIX_FMT_RGB24,   {'R', 8,  'G', 8,  'B', 8                         }},
    {PIX_FMT_RGB444BE,{'F', 4,  'R', 4,  'G', 4, 'B', 4                 }},
    {PIX_FMT_RGB48BE, {'R', 8,  'r', 8,  'G', 8, 'g', 8, 'B', 8, 'b', 8 }},
    {PIX_FMT_RGB48BE, {'R', 16, 'G', 16, 'B', 16                        }},
    {PIX_FMT_RGB48LE, {'r', 8,  'R', 8,  'g', 8, 'G', 8, 'b', 8, 'B', 8 }},
    {PIX_FMT_RGB555BE,{'F', 1,  'R', 5,  'G', 5, 'B', 5                 }},
    {PIX_FMT_RGB565BE,{'R', 5,  'G', 6,  'B', 5                         }},
    {PIX_FMT_RGBA,    {'R', 8,  'G', 8,  'B', 8, 'A', 8                 }},
    {PIX_FMT_PAL8,    {'P', 8                                           }},
};

static const int num_pixel_layouts = sizeof(ff_mxf_pixel_layouts) / sizeof(*ff_mxf_pixel_layouts);

int ff_mxf_decode_pixel_layout(const char pixel_layout[16], enum PixelFormat *pix_fmt)
{
    int x;

    for(x = 0; x < num_pixel_layouts; x++) {
        if (!memcmp(pixel_layout, ff_mxf_pixel_layouts[x].data, 16)) {
            *pix_fmt = ff_mxf_pixel_layouts[x].pix_fmt;
            return 0;
        }
    }

    return -1;
}
