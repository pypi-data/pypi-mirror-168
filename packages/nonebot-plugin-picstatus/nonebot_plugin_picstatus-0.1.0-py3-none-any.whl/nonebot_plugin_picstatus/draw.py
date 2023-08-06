import asyncio
import platform
import time
from datetime import datetime
from io import BytesIO
from typing import Union

import nonebot
import psutil
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from nonebot import logger
from nonebot.adapters.onebot.v11 import Bot
from psutil._common import sdiskusage  # noqa

from .config import config
from .const import DEFAULT_AVATAR_PATH, DEFAULT_BG_PATH, DEFAULT_FONT_PATH
from .statistics import (
    get_bot_connect_time,
    get_nonebot_run_time,
)
from .util import (
    async_open_img,
    async_request,
    format_timedelta,
    get_anime_pic,
    get_qq_avatar,
)
from .version import __version__

GRAY_BG_COLOR = "#aaaaaaaa"
WHITE_BG_COLOR = "#ffffff99"


def get_font(size: int):
    default = str(DEFAULT_FONT_PATH)
    try:
        return ImageFont.truetype(config.ps_font or default, size=size)
    except:
        logger.exception("加载自定义字体失败，使用默认字体")
        return ImageFont.truetype(default, size)


def get_usage_color(usage: float):
    usage = round(usage)
    if usage >= 90:
        return "orangered"
    elif usage >= 70:
        return "orange"
    else:
        return "lightgreen"


async def draw_header(bot: Bot):
    # 获取Bot头像
    try:
        avatar = await get_qq_avatar(bot.self_id)
        avatar = Image.open(BytesIO(avatar))
    except:
        logger.exception("获取Bot头像失败，使用默认头像替代")
        avatar = await async_open_img(DEFAULT_AVATAR_PATH)

    # bot状态信息
    bot_stat = (await bot.get_status())["stat"]
    msg_rec = bot_stat["message_received"]
    msg_sent = bot_stat["message_sent"]
    nick = (await bot.get_login_info())["nickname"]
    bot_connected = (
        format_timedelta(datetime.now() - t) if (t := get_bot_connect_time()) else "未知"
    )
    nb_run = (
        format_timedelta(datetime.now() - t) if (t := get_nonebot_run_time()) else "未知"
    )

    # 系统启动时间
    booted = format_timedelta(
        datetime.now() - datetime.fromtimestamp(psutil.boot_time())
    )

    font_30 = get_font(30)
    font_80 = get_font(80)

    bg = Image.new("RGBA", (1200, 300), WHITE_BG_COLOR)
    bg_draw = ImageDraw.Draw(bg)

    # 圆形遮罩
    circle_mask = Image.new("RGBA", (250, 250), "#ffffff00")
    ImageDraw.Draw(circle_mask).ellipse((0, 0, 250, 250), fill="black")

    # 利用遮罩裁剪圆形图片
    avatar = avatar.convert("RGBA").resize((250, 250))
    bg.paste(avatar, (25, 25), circle_mask)

    # 标题
    bg_draw.text((300, 140), nick, "black", font_80, "ld")

    # 详细信息
    bg_draw.multiline_text(
        (300, 160),
        f"Bot已连接 {bot_connected} | 收 {msg_rec} | 发 {msg_sent}\nNoneBot运行 {nb_run} | 系统运行 {booted}",
        "black",
        font_30,
    )

    # 标题与详细信息的分隔线
    bg_draw.line((300, 150, 500, 150), GRAY_BG_COLOR, 3)

    return bg


async def draw_cpu_memory_usage():
    # 获取占用信息
    psutil.cpu_percent()
    await asyncio.sleep(0.1)
    cpu_percent = psutil.cpu_percent()  # async wait

    cpu_count = psutil.cpu_count(logical=False)
    cpu_freq = psutil.cpu_freq()
    ram_stat = psutil.virtual_memory()
    swap_stat = psutil.swap_memory()

    font_70 = get_font(70)
    font_45 = get_font(45)

    bg = Image.new("RGBA", (1200, 550), WHITE_BG_COLOR)
    bg_draw = ImageDraw.Draw(bg)

    # 背景灰色圆环
    circle_bg = Image.new("RGBA", (300, 300), "#ffffff00")
    ImageDraw.Draw(circle_bg).arc((0, 0, 300, 300), 0, 360, GRAY_BG_COLOR, 30)
    bg.paste(circle_bg, (50, 50), circle_bg)
    bg.paste(circle_bg, (450, 50), circle_bg)
    bg.paste(circle_bg, (850, 50), circle_bg)

    # 写字
    bg_draw.text((200, 350), "CPU", "black", font_70, "ma")
    bg_draw.text((600, 350), "RAM", "black", font_70, "ma")
    bg_draw.text((1000, 350), "SWAP", "black", font_70, "ma")

    # 写占用率
    bg_draw.text((200, 200), f"{cpu_percent:.0f}%", "black", font_70, "mm")
    bg_draw.text((600, 200), f"{ram_stat.percent:.0f}%", "black", font_70, "mm")
    bg_draw.text((1000, 200), f"{swap_stat.percent:.0f}%", "black", font_70, "mm")

    # 画占用率圆环
    bg_draw.arc(
        (50, 50, 350, 350),
        -90,
        (3.6 * cpu_percent) - 90,
        get_usage_color(cpu_percent),
        30,
    )
    bg_draw.arc(
        (450, 50, 750, 350),
        -90,
        (3.6 * ram_stat.percent) - 90,
        get_usage_color(ram_stat.percent),
        30,
    )
    bg_draw.arc(
        (850, 50, 1150, 350),
        -90,
        (3.6 * swap_stat.percent) - 90,
        get_usage_color(swap_stat.percent),
        30,
    )

    # 写详细信息
    bg_draw.text(
        (200, 500), f"{cpu_count}核 {cpu_freq.max:.0f}MHz", "darkslategray", font_45,
        "ms"
    )
    bg_draw.text(
        (600, 500),
        f"{ram_stat.used / 1024 / 1024:.0f}M / {ram_stat.total / 1024 / 1024:.0f}M",
        "darkslategray",
        font_45,
        "ms",
    )
    bg_draw.text(
        (1000, 500),
        f"{swap_stat.used / 1024 / 1024:.0f}M / {swap_stat.total / 1024 / 1024:.0f}M",
        "darkslategray",
        font_45,
        "ms",
    )

    return bg


async def draw_disk_usage():
    font_45 = get_font(45)
    font_40 = get_font(40)

    # 获取磁盘状态
    disks = {}
    left_padding = 0
    for d in psutil.disk_partitions():
        # 根据盘符长度计算左侧留空长度用于写字
        s = font_45.getlength(d.mountpoint) + 25
        if s > left_padding:
            left_padding = s

        try:
            disks[d.mountpoint] = psutil.disk_usage(d.mountpoint)
        except Exception as e:
            logger.exception(f"读取 {d.mountpoint} 占用失败")
            disks[d.mountpoint] = e

    # 计算图片高度，创建背景图
    count = len(disks)
    bg = Image.new(
        "RGBA",
        (1200, 100 + (50 * count) + (25 * (count - 1))),  # 上下边距50 一个磁盘50 间距25
        WHITE_BG_COLOR,
    )
    bg_draw = ImageDraw.Draw(bg)

    max_len = 990 - (50 + left_padding)  # 进度条长度

    its: list[tuple[str, sdiskusage | Exception]] = disks.items()  # noqa
    for i, (name, usage) in enumerate(its):
        fail = isinstance(usage, Exception)

        top = 50 * (i + 1) + 25 * i

        # 进度条背景
        bg_draw.rectangle((50 + left_padding, top, 990, top + 50), GRAY_BG_COLOR)

        # 写盘符
        bg_draw.text((50, top + 25), name, "black", font_45, "lm")

        # 写占用百分比
        bg_draw.text(
            (1150, top + 25),
            f"{usage.percent:.1f}%" if not fail else "??.?%",
            "black",
            font_45,
            "rm",
        )

        # 画进度条
        if not fail:
            bg_draw.rectangle(
                (
                    50 + left_padding,
                    top,
                    50 + left_padding + (max_len * (usage.percent / 100)),
                    top + 50,
                ),
                get_usage_color(usage.percent),
            )

        # 写容量信息/报错信息
        bg_draw.text(
            ((max_len / 2) + 50 + left_padding, top + 25),
            (
                f"{usage.used / 1024 / 1024 / 1024:.2f}G / {usage.total / 1024 / 1024 / 1024:.2f}G"
                if not fail
                else str(usage)
            ),
            "black",
            font_40,
            "mm",
        )

    return bg


async def draw_footer(img: Image.Image):
    font_24 = get_font(24)
    draw = ImageDraw.Draw(img)
    w, h = img.size
    padding = 15

    draw.text(
        (padding, h - padding),
        (
            f"NoneBot {nonebot.__version__} × PicStatus {__version__} | "
            f"Python {platform.python_version()} | "
            f"{platform.platform()}"
        ),
        "darkslategray",
        font_24,
        "ls",
    )
    draw.text(
        (w - padding, h - padding),
        time.strftime("%Y-%m-%d %H:%M:%S"),
        "darkslategray",
        font_24,
        "rs",
    )


async def get_bg(pic: Union[str, bytes, BytesIO] = None) -> Image.Image:
    if pic:
        try:
            if isinstance(pic, str):
                pic = await async_request(pic)
            if isinstance(pic, bytes):
                pic = BytesIO(pic)
            return Image.open(pic)
        except:
            logger.exception("下载/打开自定义背景图失败，使用随机背景图")

    try:
        return Image.open(BytesIO(await get_anime_pic()))
    except:
        logger.exception("下载/打开随机背景图失败，使用默认背景图")

    return await async_open_img(DEFAULT_BG_PATH)


async def get_stat_pic(bot: Bot, bg=None):
    img_w = 1300
    img_h = 50  # 这里是上边距，留给下面代码统计图片高度

    # 获取背景及各模块图片
    ret: list[Image.Image] = await asyncio.gather(  # noqa
        get_bg(bg), draw_header(bot), draw_cpu_memory_usage(), draw_disk_usage()
    )
    bg = ret[0]
    ret = ret[1:]

    # 统计图片高度
    for p in ret:
        img_h += p.size[1] + 50

    # 拼接图片
    img = Image.new("RGBA", (img_w, img_h), "#ffffff00")
    h_pos = 50
    for p in ret:
        img.paste(p, (50, h_pos), p)
        h_pos += p.size[1] + 50

    # 写footer
    await draw_footer(img)

    # 居中裁剪背景
    bg = bg.convert("RGBA")
    bg_w, bg_h = bg.size

    scale = img_w / bg_w
    scaled_h = int(bg_h * scale)

    if scaled_h < img_h:  # 缩放后图片不够高（横屏图）
        # 重算缩放比
        scale = img_h / bg_h
        bg_w = int(bg_w * scale)

        crop_l = round((bg_w / 2) - (img_w / 2))
        bg = bg.resize((bg_w, img_h)).crop((crop_l, 0, crop_l + img_w, img_h))
    else:
        bg_h = scaled_h

        crop_t = round((bg_h / 2) - (img_h / 2))
        bg = bg.resize((img_w, bg_h)).crop((0, crop_t, img_w, crop_t + img_h))

    # 背景高斯模糊
    bg = bg.filter(ImageFilter.GaussianBlur(radius=config.ps_blur_radius))

    # 将状态图贴上背景
    bg.paste(img, (0, 0), img)

    # 尝试解决黑底白底颜色不同问题
    bg = bg.convert('RGB')

    bio = BytesIO()
    bg.save(bio, "png")
    return bio
