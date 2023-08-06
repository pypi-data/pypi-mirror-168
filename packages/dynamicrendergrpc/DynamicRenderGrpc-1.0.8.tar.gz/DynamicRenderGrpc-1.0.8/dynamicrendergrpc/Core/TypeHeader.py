# -*- encoding: utf-8 -*-
"""
@File    :   TypeHeader.py
@Time    :   2022/06/18 21:34:04
@Author  :   DMC
"""

from abc import ABCMeta, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from os import path, getcwd
from typing import Union

import cv2 as cv
import httpx
import numpy as np
import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from numpy import ndarray

from .Config import ConfigReader
from .Dynamic import logger


class AbstractHeadedr(metaclass=ABCMeta):
    @abstractmethod
    async def header_render(self, auther):
        pass


class Header(AbstractHeadedr, ConfigReader):
    def __init__(self) -> None:
        super().__init__()
        self.relative_path = getcwd()
        self.cache_path = path.join(self.relative_path, "Static", "Cache")
        self.font_path = path.join(
            self.relative_path, "Static", "Font", self.config_content.font.main_font_name)

    async def header_render(self, auther) -> Union[ndarray, None]:
        """图片头的渲染入口函数

        :param auther: 动态作者的所有信息
        :type auther
        """
        try:
            self.back_groud_img = Image.new(
                "RGBA", (1080, 400), self.config_content.color.backgroud_color)
            self.draw = ImageDraw.Draw(self.back_groud_img)
            completed_info = await self.auther_info_classification(auther=auther)
            text_list = completed_info[0]
            all_pic = await self.get_all_pic(completed_info[1], auther.author)
            info_list = text_list + all_pic
            for i in info_list:
                await self.assemble_img(i)
            return cv.cvtColor(np.asarray(self.back_groud_img), cv.COLOR_RGBA2BGRA)
        except Exception as e:
            logger.exception("What?!")
            logger.error("图片头渲染错误")
            return None

    async def auther_info_classification(self, auther) -> list:
        """对信息进行分类

        :param auther: 所有信息
        :type auther
        :return: 装有所有信息的列表
        :rtype: list
        """
        # 将动态作者昵称和动态的ptime信息放入列表信息
        text_info_list = [{"type": "text",
                           "content": auther.author.name,
                           "size": self.config_content.size.uname_size,
                           "color": auther.author.vip.nickname_color or self.config_content.color.text_color,
                           "position": (200, 250)},
                          {
                              "type": "text",
                              "content": auther.ptime_label_text,
                              "size": self.config_content.size.sub_title_size,
                              "color": self.config_content.color.sub_font_color,
                              "position": (200, 320)
        }]

        # 将头像的url链接放入列表中及头像在本地的路径放入url列表中
        # 本地的路径是为了方便后续查询头像是否在本地中有存储，如果没有存储则下载后存在该路径，如果有则直接打开该路径的头像不发送网络请求
        url_info_list = [{"type": "face",
                          "url": f"{auther.author.face}@120w_120h_1c_1s.webp",
                          "path": path.join(self.cache_path, "Face", f"{auther.mid}.webp")}]

        # 如果动态作者有头像挂件，将头像挂件url及挂件在本地的路径放入url列表中
        # 本地的路径是为了方便后续查询挂件是否在本地中有存储，如果没有存储则下载后存在该路径，如果有则直接打开该路径的挂件不发送网络请求
        if auther.author.pendant.image:
            url_info_list.append({
                "type": "pendant",
                "url": f"{auther.author.pendant.image}@210w_2100h.webp",
                "path": path.join(self.cache_path, "Pendant", f"{auther.author.pendant.name}.png")
            })

        return [text_info_list, url_info_list]

    async def get_all_pic(self, url_list: list, auther) -> list:
        """获取所有图片

        :param url_list: 装有图片的url的列表
        :type url_list: list
        :param auther: 动态作者的信息
        :type auther
        :return: 返回装有所有图片的列表
        :rtype: list
        """

        # 通过线程池发送网络请求
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = pool.map(self.pic_reader, url_list)
        pic_info = list(results)

        # 打开bilibili的logo图片并重设尺寸
        bili_logo = Image.open(path.join(self.relative_path, "Static", "Picture", "bilibili.png")).convert(
            "RGBA").resize((231, 105))

        # 将logo放入图片信息列表内
        pic_info.append(
            {"type": "img", "content": bili_logo, "position": (433, 20)})

        # 如果用户有小闪电就打开小闪电的图片放入图片列表内
        if auther.official.type != -1:
            official_verify_path = [path.join(self.relative_path, "Static", "Picture", "official_yellow.png"),
                                    path.join(self.relative_path, "Static", "Picture", "official_blue.png")]
            img = Image.open(
                official_verify_path[auther.official.type]).resize((45, 45))
            pic_info.append(
                {"type": "img", "content": img, "position": (120, 330)})

        # 用户没有小闪电的话如果是大会员(在特殊的日子大会员会变成小会员)，就打开大会员标志的图片放入图片信息列表
        elif auther.vip:
            avatar_subscript = auther.vip.avatar_subscript
            if avatar_subscript and avatar_subscript != 0:
                avatar_path = {2: path.join(self.relative_path, "Static", "Picture", "small_vip.png"),
                               1: path.join(self.relative_path, "Static", "Picture", "big_vip.png")}[avatar_subscript]
                avatar_img = Image.open(avatar_path).resize(
                    (45, 45)).convert("RGBA")
                pic_info.append(
                    {"type": "img", "content": avatar_img, "position": (120, 330)})
        return pic_info

    def pic_reader(self, pic_info: dict) -> dict:
        """读取或请求图片

        :param pic_info: 装有图片信息的字典
        :type pic_info: dict
        """
        # 头像或者头像挂件在本地的路径
        img_path = pic_info["path"]
        # 头像或者头像挂件的url
        img_url = pic_info["url"]
        # 图片是头像还是头像挂件
        pic_type = pic_info["type"]
        # 如果头像或者头像挂件在本地缓存的有
        if path.exists(img_path):
            # 如果图片类型是头像则看一看缓存时间是否超过了一天
            if pic_type == "face":
                # 如果头像的修改时间大于一天，重新下载头像
                if time.time() - int(path.getmtime(img_path)) > 86400:
                    resp = httpx.get(img_url)
                    # 将图片保存在img_path
                    with open(img_path, "wb") as f:
                        f.write(resp.content)
                    # 将图片读取为opencv格式
                    img = cv.imdecode(np.asarray(
                        bytearray(resp.content), dtype="uint8"), cv.IMREAD_UNCHANGED)
                # 如果头像缓存时间小于一天直接读取缓存图片
                else:
                    img = cv.imread(img_path)
                return {"type": "img", "content": self.convert_circle(img), "position": (45, 245)}
            # 如果图片是头像挂件直接读取
            else:
                img = Image.open(img_path).convert("RGBA")
                return {"type": "img", "content": img, "position": (1, 202)}
        # 如果图片在本地缓存的没有直接发送请求
        else:
            resp = httpx.get(img_url)
            with open(img_path, "wb") as f:
                f.write(resp.content)
            if pic_type != "face":
                return {"type": "img", "content": Image.open(BytesIO(resp.content)), "position": (1, 202)}
            img = cv.imdecode(np.asarray(
                bytearray(resp.content), dtype="uint8"), cv.IMREAD_UNCHANGED)
            return {"type": "img", "content": self.convert_circle(img), "position": (45, 245)}

    def convert_png(self, img: ndarray) -> ndarray:
        """将jpg转为png,头像可能为jpg格式,ndarry不能粘贴shape不同的图,所以将
            jpg图片转换成png
        :param img: 头像
        :type img: ndarray
        :return: png图片
        :rtype: ndarray
        """
        # 查看图片的通道数
        chennal = img.shape[2]
        # 如果图片是4通道即BGRA直接吧图片返回回去
        if chennal != 3:
            return img
        # 如果图片是BGR三通道，先分离三个通道，再新建一个通道，再将四个通道合并
        b_channel, g_channel, r_channel = cv.split(img)  # 剥离jpg图像通道
        alpha_channel = np.ones(
            b_channel.shape, dtype=b_channel.dtype) * 255  # 创建Alpha通道
        # 融合通道
        return cv.merge((b_channel, g_channel, r_channel, alpha_channel))

    def convert_circle(self, img: ndarray) -> Image.Image:
        """将头像转为圆形

        :param img: 头像
        :type img: ndarray
        :return: 处理后的图片
        :rtype: Image.Image
        """
        # 要处理的图
        img = cv.resize(img, (121, 121), interpolation=cv.INTER_NEAREST)
        img = self.convert_png(img)
        # 遮罩
        img_mask = np.ones((121, 121, 4)) * (255, 255, 255, 0)
        cv.circle(img_mask, (61, 61), 60, (0, 0, 0, 255), -1,lineType=cv.LINE_AA)
        cv.circle(img, (61, 61), 58, (153, 114, 251, 255), 3,lineType=cv.LINE_AA)
        img[:, :, 3] = img_mask[:, :, 3]
        return Image.fromarray(cv.cvtColor(img, cv.COLOR_BGRA2RGBA))

    async def assemble_img(self, info_dict:dict) -> None:
        """将图片以及文字写入背景图

        Arguments:
            info_dict {dict} -- 要写入的内容的信息
        """
        # 取出要写入的信息的类型
        info_type = info_dict["type"]
        # 如果要写入的是文字
        if info_type == "text":
            font = ImageFont.truetype(
                self.font_path, size=info_dict["size"], encoding='utf-8')
            self.draw.text(xy=info_dict["position"], text=info_dict["content"], font=font,
                           fill=info_dict["color"])
        # 如果要写入的信息是图片
        else:
            img = info_dict["content"]
            self.back_groud_img.paste(img, info_dict["position"], img)


class ForwardHeader(AbstractHeadedr, ConfigReader):
    def __init__(self):
        super().__init__()

    async def header_render(self, author):
        """渲染转发动态的 被转发的动态的头

        :param author:
        :return:
        """
        name = author.title[0].text
        font = ImageFont.truetype(path.join(getcwd(), "Static", "Font",
                                            self.config_content.font.main_font_name),
                                  self.config_content.size.uname_size)
        font_size = font.getsize(name)
        height = font_size[1] + 40
        background = Image.new("RGBA", (1080, height),
                               self.config_content.color.forward_color)
        draw = ImageDraw.Draw(background)
        draw.text((35, 20), name, self.config_content.color.extra_color, font)

        return cv.cvtColor(np.asarray(background), cv.COLOR_RGBA2BGRA)
