# MountPenglai
'''---------------------------------------------------------------------------------
Powered by RMSHE / 2022.09.08;

将 turtle 的绘图逻辑更改为 Organ-Field GUI 样式;
Organ-Field GUI 的绘图逻辑我参考的是 AutoCAD;
turtle 的使用逻辑过于直观,因此造成了使用不便,翻了一遍文档,
还好基础该有的都有,我要重新将它封装成C++图形库的使用逻辑;

项目代号: 蓬莱山(MountPenglai) / 生命周期: 一个月(大作业结束可能就不值得我继续维护了);
还有,开发时间不足代码是赶出来的屎山能跑就行(这种意义不明的短期项目没必要花时间去优化代码结构);
---------------------------------------------------------------------------------'''
# 逻辑坐标是在程序中用于绘图的坐标体系;
# 坐标默认的原点在窗口的左上角，X 轴向右为正，Y 轴向下为正，度量单位是点;


import _thread
from math import *
from turtle import *
import time


# 色彩变换是图像处理中最重要的一环
# (这部分我引入一些仿 Photoshop Camera Raw 色彩处理功能,当然PS是C++写的我也不知道它的代码,我只是根据公开的公式对部分功能进行仿制);
class MPColorSystem:
    # RGB to HEX; More details on RGB: https://en.wikipedia.org/wiki/RGB_color_model
    def RGB(self, R, G, B):
        return str("#" + ('{:02X}' * 3).format(R, G, B))

    # HSV to HEX; More details on HSV: https://en.wikipedia.org/wiki/HSL_and_HSV
    def HSV(self, H, S, V):
        if H > 360.0:
            H = H - 360.0
        if H < 0.0:
            H = H + 360.0

        if S > 1.0:
            S = S - 1.0
        if S < 0.0:
            S = S + 1.0

        if V > 1.0:
            V = V - 1.0
        if V < 0.0:
            V = V + 1.0

        R, G, B = self.HSVtoRGB(H, S, V)
        return self.RGB(R, G, B)

    # HEX to RGB;
    def GetRGBValue(self, ColorHex):
        return tuple(int(ColorHex[1:][i:i + 2], 16) for i in (0, 2, 4))

    # 返回指定HEX颜色值中的红色分量;
    # Returns the red decomposition of the HEX color value;
    def GetRValue(self, ColorHex):
        return self.GetRGBValue(ColorHex)[0]

    # 返回指定HEX颜色值中的绿色分量;
    # Returns the green decomposition of the HEX color value;
    def GetGValue(self, ColorHex):
        return self.GetRGBValue(ColorHex)[1]

    # 返回指定HEX颜色值中的蓝色分量;
    # Returns the blue decomposition of the HEX color value;
    def GetBValue(self, ColorHex):
        return self.GetRGBValue(ColorHex)[2]

    # HEX to HSV;
    def GetHSVValue(self, ColorHex):
        R, G, B = self.GetRGBValue(ColorHex)
        return self.RGBtoHSV(R, G, B)

    # 返回指定HEX颜色值中的色相分量;
    # Returns the Hue decomposition of the HEX color value;
    def GetHValue(self, ColorHex):
        return self.GetHSVValue(ColorHex)[0]

    # 返回指定HEX颜色值中的饱和度分量;
    # Returns the Saturation decomposition of the HEX color value;
    def GetSValue(self, ColorHex):
        return self.GetHSVValue(ColorHex)[1]

    # 返回指定HEX颜色值中的明度分量;
    # Returns the Value decomposition of the HEX color value;
    def GetVValue(self, ColorHex):
        return self.GetHSVValue(ColorHex)[2]

    # HSV色彩空间转RGB色彩空间(色相分量,饱和度分量,明度分量);
    # HSV to RGB(Hue,Saturation,Value);
    def HSVtoRGB(self, H, S, V):
        if not (0.0 <= H <= 360.0 and 0.0 <= S <= 1.0 and 0.0 <= V <= 1.0):
            return "Parameter error."

        C = V * S
        X = C * (1 - abs((H / 60) % 2 - 1))
        m = V - C

        RGB2 = []
        if 0.0 <= H <= 60.0:
            RGB2 = [C, X, 0]
        elif 60.0 <= H <= 120.0:
            RGB2 = [X, C, 0]
        elif 120.0 <= H <= 180.0:
            RGB2 = [0, C, X]
        elif 180.0 <= H <= 240.0:
            RGB2 = [0, X, C]
        elif 240.0 <= H <= 300.0:
            RGB2 = [X, 0, C]
        elif 300.0 <= H <= 360.0:
            RGB2 = [C, 0, X]

        return int((RGB2[0] + m) * 255), int((RGB2[1] + m) * 255), int((RGB2[2] + m) * 255)

    # RGB色彩空间转HSV色彩空间(R,G,B);
    # RGB to HSV;
    def RGBtoHSV(self, R, G, B):
        r_, g_, b_ = R / 255, G / 255, B / 255
        c_max = max(r_, g_, b_)
        c_min = min(r_, g_, b_)
        dela = c_max - c_min

        h = None
        if dela == 0:
            h = 0
        elif c_max == r_:
            h = 60 * (((g_ - b_) / dela) % 6)
        elif c_max == g_:
            h = 60 * ((b_ - r_) / dela + 2)
        elif c_max == b_:
            h = 60 * ((r_ - g_) / dela + 4)

        s = 0 if c_max == 0 else dela / c_max
        v = c_max

        return h, s, v

    # 返回与指定RGB颜色对应的灰度值颜色;
    # RGB to GrayScale(R,G,B)
    def RGBtoGRAY(self, R, G, B):
        return (R * 38 + G * 75 + B * 15) >> 7

    # RGB色彩通道提取:提取像素组的特定颜色通道,并且支持自定义提取范围(像素组颜色的十六进制值列表,提取通道[R,G,B],提取范围[0,255],其余通道填充值);
    # RGB color channel extraction: extracts specific color channels of pixel groups, and supports custom extraction range;
    def RGBChannelExtraction(self, ColorGroupHex=(), Channel="R", MIN=0, MAX=255, Fill=(0, 0, 0)):
        ChannelValue = {"R": Fill[0], "G": Fill[1], "B": Fill[2]}
        OutputChannelGroupHex = []
        for i in ColorGroupHex:
            if Channel == "R":
                ChannelValue["R"] = self.GetRValue(i)
                if not MIN <= ChannelValue["R"] <= MAX:
                    ChannelValue["R"] = Fill[0]

            elif Channel == "G":
                ChannelValue["G"] = self.GetGValue(i)
                if not MIN <= ChannelValue["G"] <= MAX:
                    ChannelValue["G"] = Fill[1]

            elif Channel == "B":
                ChannelValue["B"] = self.GetBValue(i)
                if not MIN <= ChannelValue["B"] <= MAX:
                    ChannelValue["B"] = Fill[2]

            OutputChannelGroupHex.append(self.RGB(ChannelValue["R"], ChannelValue["G"], ChannelValue["B"]))

        return OutputChannelGroupHex

    # RGB色彩通道编辑:提取像素组特点通道后将其值替换为指定值,并且支持自定义编辑范围(像素组颜色的十六进制值列表,需要编辑的通道[R,G,B],替换值[0,255],编辑范围[0,255]);
    # RGB color channel edit: After extracts the pixel group specific channel, replace its value with the specified value, and support custom edit range.
    def RGBChannelEdit(self, ColorGroupHex=(), Channel="R", AlternateValue=None, MIN=0, MAX=255):
        ChannelValue = {"R": 0, "G": 0, "B": 0}
        OutputChannelGroupHex = []
        for i in ColorGroupHex:
            if Channel == "R":
                R, G, B = self.GetRGBValue(i)
                if MIN <= R <= MAX:
                    ChannelValue["R"] = AlternateValue
                else:
                    ChannelValue["R"] = R

                ChannelValue["G"] = G
                ChannelValue["B"] = B

            elif Channel == "G":
                R, G, B = self.GetRGBValue(i)
                if MIN <= G <= MAX:
                    ChannelValue["G"] = AlternateValue
                else:
                    ChannelValue["G"] = G

                ChannelValue["R"] = R
                ChannelValue["B"] = B


            elif Channel == "B":
                R, G, B = self.GetRGBValue(i)
                if MIN <= B <= MAX:
                    ChannelValue["B"] = AlternateValue
                else:
                    ChannelValue["B"] = B

                ChannelValue["R"] = R
                ChannelValue["G"] = G

            OutputChannelGroupHex.append(self.RGB(ChannelValue["R"], ChannelValue["G"], ChannelValue["B"]))

        return OutputChannelGroupHex

    # RGB色彩通道线性偏移:提取像素组特点通道后将其值偏移,并且支持自定义编辑范围(像素组颜色的十六进制值列表,需要编辑的通道[R,G,B],偏移量,编辑范围[0,255]);
    # RGB color channel linear drift: extract the pixel group specific channel and drift its value;
    def RGBChannelDrift(self, ColorGroupHex=(), Channel="R", DriftValue=None, MIN=0, MAX=255):
        ChannelValue = {"R": 0, "G": 0, "B": 0}
        OutputChannelGroupHex = []
        for i in ColorGroupHex:
            if Channel == "R":
                R, G, B = self.GetRGBValue(i)
                if MIN <= R <= MAX:
                    composite = R + DriftValue
                    if composite > 255:
                        composite = 255
                    elif composite < 0:
                        composite = 0

                    ChannelValue["R"] = composite
                else:
                    ChannelValue["R"] = R

                ChannelValue["G"] = G
                ChannelValue["B"] = B

            elif Channel == "G":
                R, G, B = self.GetRGBValue(i)
                if MIN <= G <= MAX:
                    composite = G + DriftValue
                    if composite > 255:
                        composite = 255
                    elif composite < 0:
                        composite = 0

                    ChannelValue["G"] = composite
                else:
                    ChannelValue["G"] = G

                ChannelValue["R"] = R
                ChannelValue["B"] = B


            elif Channel == "B":
                R, G, B = self.GetRGBValue(i)
                if MIN <= B <= MAX:
                    composite = B + DriftValue
                    if composite > 255:
                        composite = 255
                    elif composite < 0:
                        composite = 0

                    ChannelValue["B"] = composite
                else:
                    ChannelValue["B"] = B

                ChannelValue["R"] = R
                ChannelValue["G"] = G

            OutputChannelGroupHex.append(self.RGB(ChannelValue["R"], ChannelValue["G"], ChannelValue["B"]))

        return OutputChannelGroupHex

    # HSV色彩通道提取:提取像素组的特定颜色通道,并且支持自定义提取范围(像素组颜色的十六进制值列表,提取通道[H,S,V],提取范围{H:[0,360],S:[0,1],V:[0,1]},其余通道填充值);
    # HSV color channel linear drift: extract the pixel group specific channel and drift its value;
    def HSVChannelExtraction(self, ColorGroupHex=(), Channel="H", MIN=0.0, MAX=360.0, Fill=(0.0, 1.0, 1.0)):
        if Channel != "H" and MAX > 1.0:
            MAX = 1

        OutputChannelGroupHex = []
        for i in ColorGroupHex:
            ChannelValue = {"H": Fill[0], "S": Fill[1], "V": Fill[2]}
            if Channel == "H":
                ChannelValue["H"] = self.GetHValue(i)
                if not MIN <= ChannelValue["H"] <= MAX:
                    ChannelValue["H"] = Fill[0]
                    ChannelValue["S"] = 0.0
                    ChannelValue["V"] = 0.0

            elif Channel == "S":
                ChannelValue["S"] = self.GetSValue(i)
                if not MIN <= ChannelValue["S"] <= MAX:
                    ChannelValue["S"] = Fill[1]
                    ChannelValue["V"] = 0.0

            elif Channel == "V":
                ChannelValue["V"] = self.GetVValue(i)
                if not MIN <= ChannelValue["V"] <= MAX:
                    ChannelValue["S"] = 0.0
                    ChannelValue["V"] = Fill[2]

            OutputChannelGroupHex.append(self.HSV(ChannelValue["H"], ChannelValue["S"], ChannelValue["V"]))

        return OutputChannelGroupHex

    # HSV色彩通道编辑(值替换);
    # 将像素组的HSV颜色通道全部提取出来,然后选择一个通道作为基通道,并且选择基通道的范围,最后选择要编辑的通道并指定替换值.程序将会把基通道范围内的编辑通道值替换为指定值;
    # 例如: 我对鲜花拍摄了一张照片,这张照片的蓝色部分饱和度太高,那么我们编辑的通道就是饱和度通道(EditChannel = "S"),替换值我们将其设为较低的值(AlternateValue = 0.3),
    # 我们指定基通道为色相通道(BaseChannel = "H"),基通道范围为图片都蓝色部分(大致在MIN = 180°到MAX = 300°之间).这样程序就会将基通道的蓝色颜色的饱和度整体替换为一个低值.
    # 这一过程中我们只改变了图片中蓝色颜色像素的饱和度,其他颜色不受影响,而且蓝色颜色的色相和明度也不受影响.
    # HSVChannelEdit(像素组颜色的十六进制值列表,编辑通道[H/S/V],替换值,基通道[H/S/V],基通道范围);
    # 注意:当编辑通道为H时,替换值必须在[0,360]区间内; 当编辑通道为S或V时,替换值必须在[0,1]区间内;
    # 当基通道为H时,基通道范围MIN-MAX必须在[0,360]区间内; 当基通道为S或V时基通道范围MIN-MAX必须在[0,1]区间内;
    def HSVChannelEdit(self, ColorGroupHex=(), EditChannel="H", AlternateValue=0.0, BaseChannel="H", MIN=0.0, MAX=360.0):
        BC = {"H": 0, "S": 1, "V": 2}

        if EditChannel != "H":
            if AlternateValue < 0.0:
                AlternateValue = abs(AlternateValue)
            if AlternateValue > 1.0:
                AlternateValue = 1.0
        else:
            if AlternateValue < 0.0:
                AlternateValue = abs(AlternateValue)
            if AlternateValue > 360.0:
                AlternateValue = 360.0

        if BaseChannel != "H":
            if MIN < 0.0:
                MIN = abs(MIN)
            if MIN > 1.0:
                MIN = 0.0

            if MAX < 0.0:
                MAX = abs(MAX)
            if MAX > 1.0:
                MAX = 1.0
        else:
            if MIN < 0.0:
                MIN = abs(MIN)
            if MIN > 360.0:
                MIN = 0.0
            if MAX < 0.0:
                MAX = abs(MAX)
            if MAX > 360.0:
                MAX = 360.0

        global ChannelValue
        OutputChannelGroupHex = []
        for i in ColorGroupHex:
            ChannelValue = {"H": 0.0, "S": 1.0, "V": 1.0}
            if EditChannel == "H":
                HSV = self.GetHSVValue(i)

                if MIN <= HSV[BC[BaseChannel]] <= MAX:
                    ChannelValue["H"] = AlternateValue
                else:
                    ChannelValue["H"] = HSV[0]

                ChannelValue["S"] = HSV[1]
                ChannelValue["V"] = HSV[2]

            elif EditChannel == "S":
                HSV = self.GetHSVValue(i)
                if MIN <= HSV[BC[BaseChannel]] <= MAX:
                    ChannelValue["S"] = AlternateValue
                else:
                    ChannelValue["S"] = HSV[1]

                ChannelValue["H"] = HSV[0]
                ChannelValue["V"] = HSV[2]

            elif EditChannel == "V":
                HSV = self.GetHSVValue(i)
                if MIN <= HSV[BC[BaseChannel]] <= MAX:
                    ChannelValue["V"] = AlternateValue
                else:
                    ChannelValue["V"] = HSV[2]

                ChannelValue["H"] = HSV[0]
                ChannelValue["S"] = HSV[1]

            OutputChannelGroupHex.append(self.HSV(ChannelValue["H"], ChannelValue["S"], ChannelValue["V"]))

        return OutputChannelGroupHex

    # HSV色彩通道偏移(值偏移);
    # 将像素组的HSV颜色通道全部提取出来,然后选择一个通道作为基通道,并且选择基通道的范围,最后选择要编辑的通道并指定偏移量.程序将会把基通道范围内的编辑通道值偏移;
    # 例如: 我对鲜花拍摄了一张照片,这张照片的蓝色部分饱和度太高,那么我们编辑的通道就是饱和度通道(EditChannel = "S"),偏移量我们将其设为负值(DriftValue = -0.5),
    # 我们指定基通道为色相通道(BaseChannel = "H"),基通道范围为图片都蓝色部分(大致在MIN = 180°到MAX = 300°之间).这样程序就会将基通道的蓝色颜色的饱和度整体向下偏移.
    # 这一过程中我们只改变了图片中蓝色颜色像素的饱和度,其他颜色不受影响,而且蓝色颜色的色相和明度也不受影响.
    # HSVChannelEdit(像素组颜色的十六进制值列表,编辑通道[H/S/V],偏移量,基通道[H/S/V],基通道范围);
    # 注意:当编辑通道为H时,偏移量尽量在[-360,360]区间内; 当编辑通道为S或V时,偏移量尽量在[-1,1]区间内;
    # 当基通道为H时,基通道范围MIN-MAX必须在[0,360]区间内; 当基通道为S或V时基通道范围MIN-MAX必须在[0,1]区间内;
    def HSVChannelDrift(self, ColorGroupHex=(), EditChannel="H", DriftValue=0.0, BaseChannel="H", MIN=0.0, MAX=360.0):
        BC = {"H": 0, "S": 1, "V": 2}

        if BaseChannel != "H":
            if MIN < 0.0:
                MIN = abs(MIN)
            if MIN > 1.0:
                MIN = 0.0

            if MAX < 0.0:
                MAX = abs(MAX)
            if MAX > 1.0:
                MAX = 1.0
        else:
            if MIN < 0.0:
                MIN = abs(MIN)
            if MIN > 360.0:
                MIN = 0.0
            if MAX < 0.0:
                MAX = abs(MAX)
            if MAX > 360.0:
                MAX = 360.0

        global ChannelValue
        OutputChannelGroupHex = []
        for i in ColorGroupHex:
            ChannelValue = {"H": 0.0, "S": 1.0, "V": 1.0}
            if EditChannel == "H":
                HSV = self.GetHSVValue(i)

                if MIN <= HSV[BC[BaseChannel]] <= MAX:
                    ChannelValue["H"] = HSV[0] + DriftValue

                    if ChannelValue["H"] > 360.0:
                        ChannelValue["H"] = ChannelValue["H"] - 360.0
                    elif ChannelValue["H"] < 0:
                        ChannelValue["H"] = abs(ChannelValue["H"])

                else:
                    ChannelValue["H"] = HSV[0]

                ChannelValue["S"] = HSV[1]
                ChannelValue["V"] = HSV[2]

            elif EditChannel == "S":
                HSV = self.GetHSVValue(i)
                if MIN <= HSV[BC[BaseChannel]] <= MAX:
                    ChannelValue["S"] = HSV[1] + DriftValue

                    if ChannelValue["S"] > 1.0:
                        ChannelValue["S"] = 1.0
                    elif ChannelValue["S"] < 0:
                        ChannelValue["S"] = 0

                else:
                    ChannelValue["S"] = HSV[1]

                ChannelValue["H"] = HSV[0]
                ChannelValue["V"] = HSV[2]

            elif EditChannel == "V":
                HSV = self.GetHSVValue(i)
                if MIN <= HSV[BC[BaseChannel]] <= MAX:
                    ChannelValue["V"] = HSV[2] + DriftValue

                    if ChannelValue["V"] > 1.0:
                        ChannelValue["V"] = 1.0
                    elif ChannelValue["V"] < 0:
                        ChannelValue["V"] = 0

                else:
                    ChannelValue["V"] = HSV[2]

                ChannelValue["H"] = HSV[0]
                ChannelValue["S"] = HSV[1]

            OutputChannelGroupHex.append(self.HSV(ChannelValue["H"], ChannelValue["S"], ChannelValue["V"]))

        return OutputChannelGroupHex


class MountPenglai:
    SelfMPCS = MPColorSystem()

    canvwidth = None
    canvheight = None
    backgroundcolor = "#282c34"
    DefaultEllipticCurvePrecision = 1

    # Initialize the canvas;
    # 初始化型表观海龟灭绝处理器;
    def initgraph(self, width, height, BGcolor=None):
        setup(width + 20, height + 20)
        title("RMSHE MountPenglai for Turtle")
        screensize(width, height)
        speed("fastest")
        hideturtle()
        self.canvwidth = width
        self.canvheight = height

        if BGcolor == None:
            bgcolor("#282c34")
        else:
            bgcolor(BGcolor)
            self.backgroundcolor = BGcolor

        pencolor("#abb2bf")
        fillcolor("#70a1ff")
        pass

    # 开始批量绘图. 执行后,任何绘图操作都将暂时不输出到绘图窗口上,直到执行 FlushBatchDraw 或 EndBatchDraw 才将之前的绘图输出;
    def BeginBatchDraw(self):
        tracer(False)
        pass

    # 执行未完成的绘制任务; 执行一次 TurtleScreen 刷新. 在禁用追踪时使用;
    def FlushBatchDraw(self):
        update()
        pass

    # 结束批量绘制，并执行未完成的绘制任务;
    def EndBatchDraw(self):
        tracer(True)
        update()
        pass

    # 清空矩形区域;
    # Clear the rectangular area(Specify the coordinates of the four vertices of the rectangle);
    def clearrectangle(self, left, top, right, bottom, angle=0, xbase=None, ybase=None):
        OriginalColor = [pencolor(), fillcolor()]
        fillcolor(self.backgroundcolor)
        self.solidrectangle(left, top, right, bottom, angle, xbase, ybase)
        pencolor(OriginalColor[0])
        fillcolor(OriginalColor[1])
        pass

    # 清空圆角矩形区域;
    # clear a rounded rectangular region;
    def clearroundrect(self, left, top, right, bottom, radius, angle=0, xbase=None, ybase=None):
        OriginalColor = [pencolor(), fillcolor()]
        fillcolor(self.backgroundcolor)

        self.solidroundrect(left, top, right, bottom, radius, angle, xbase, ybase)

        pencolor(OriginalColor[0])
        fillcolor(OriginalColor[1])
        pass

    # 清空圆形区域;
    # clear circular area;
    def clearcircle(self, x, y, radius):
        OriginalColor = [pencolor(), fillcolor()]
        fillcolor(self.backgroundcolor)
        self.solidcircle(x, y, radius)
        pencolor(OriginalColor[0])
        fillcolor(OriginalColor[1])
        pass

    # 清空椭圆区域;
    # clear ellipse area;
    def clearellipse(self, left, top, right, bottom, angle=0, xbase=None, ybase=None, steps=DefaultEllipticCurvePrecision):
        OriginalColor = [pencolor(), fillcolor()]
        fillcolor(self.backgroundcolor)

        self.solidellipse(left, top, right, bottom, angle, xbase, ybase, steps)

        pencolor(OriginalColor[0])
        fillcolor(OriginalColor[1])
        pass

    # 清空扇形区域;
    # Clear a sector region;
    def clearpie(self, left, top, right, bottom, stangle=0, endangle=360, angle=0, xbase=None, ybase=None):
        OriginalColor = [pencolor(), fillcolor()]
        fillcolor(self.backgroundcolor)

        self.solidpie(left, top, right, bottom, stangle, endangle, angle, xbase, ybase)

        pencolor(OriginalColor[0])
        fillcolor(OriginalColor[1])
        pass

    # 清空规则的多边形区域;
    # clear a regular polygon region;
    def clearpolygon(self, x, y, radius, steps=72, angle=0, xbase=None, ybase=None):
        OriginalColor = [pencolor(), fillcolor()]
        fillcolor(self.backgroundcolor)

        self.solidpolygon(x, y, radius, steps, angle, xbase, ybase)

        pencolor(OriginalColor[0])
        fillcolor(OriginalColor[1])
        pass

    # 使用当前背景色清空画布;
    # Used to clear the drawing canvas with current background color
    def clearcanvas(self):
        self.clearrectangle(0, 0, self.canvwidth, self.canvheight)
        pass

    # 进行伽利略变换: 将画布原点定在窗口中央是不合适的,一旦涉及到坐标的矩阵变换(特别是旋转)时就要考虑正负,这很麻烦;
    # 应该将原点设在窗口左上角,并且把Y轴方向反转,使其向下为正向,X轴向右为正向.这样整个可用绘图空间都在一个象限内;
    # Perform GalileanTransformation: It is inappropriate to set the origin of the canvas in the center of the window.
    # Once it involves the matrix transformation of coordinates (especially rotation), it is very troublesome to consider the positive and negative;
    def GalileanTransformation(self, x, y):
        x = x - 0.5 * self.canvwidth
        y = -(y - 0.5 * self.canvheight)
        return x, y

    # 指定点绕基点旋转(待旋转的点的坐标,基点坐标,旋转角度);
    # RMSHE built-in tool [rotation matrix for 2D plane];
    def RotationMatrix(self, x, y, xbase, ybase, angle):
        Rx = (x - xbase) * cos(pi / 180.0 * angle) - (y - ybase) * sin(pi / 180.0 * angle) + xbase
        Ry = (x - xbase) * sin(pi / 180.0 * angle) + (y - ybase) * cos(pi / 180.0 * angle) + ybase
        return Rx, Ry

    # 将画笔传送到指定位置;
    # Teleport the pen to the specified location;
    def teleport(self, x, y):
        Point = self.GalileanTransformation(x, y)
        penup()
        setposition(Point[0], Point[1])
        pendown()
        pass

    # 画点(点的坐标,点的视觉半径)
    # draw dots;
    def putpixel(self, x, y, radius=2):
        self.teleport(x, y)

        pencolor(fillcolor())
        width(0)
        begin_fill()
        dot(radius)
        end_fill()
        pass

    # 画一条线段(两点坐标);
    # draw straight lines(Two points define a line segment);
    def line(self, x0, y0, x1, y1):
        self.teleport(x0, y0)
        setposition(self.GalileanTransformation(x1, y1))
        pass

    # 画连续的多条线段(控制点列表);
    # Draw multiple consecutive line segments;
    def polyline(self, POINTs=None):
        if POINTs is None:
            return "POINTs cannot be NULL"
        elif int(len(POINTs) / 2) - 1 <= 0:
            return "The number of POINTs must be greater than one"

        i = 0
        j = 0
        while True:
            self.line(POINTs[i], POINTs[i + 1], POINTs[i + 2], POINTs[i + 3])

            j += 1
            if j == int(len(POINTs) / 2) - 1:
                break
            i += 2

        pass

    # 画无填充矩形(矩形四个顶点坐标,旋转角度,旋转基点);
    # draw unfilled rectangle(Specify the coordinates of the four vertices of the rectangle, Rotation angle, Rotation base point);
    def rectangle(self, left, top, right, bottom, angle=0, xbase=None, ybase=None):
        if angle != 0:
            if xbase is None and ybase is None:
                xbase = int((right - left) / 2) + left
                ybase = int((bottom - top) / 2) + top

            RotationResult0 = self.RotationMatrix(left, top, xbase, ybase, angle)
            RotationResult1 = self.RotationMatrix(left, bottom, xbase, ybase, angle)

            RotationResult2 = self.RotationMatrix(right, bottom, xbase, ybase, angle)
            RotationResult3 = self.RotationMatrix(right, top, xbase, ybase, angle)

            self.line(RotationResult0[0], RotationResult0[1], RotationResult1[0], RotationResult1[1])
            self.line(RotationResult1[0], RotationResult1[1], RotationResult2[0], RotationResult2[1])
            self.line(RotationResult2[0], RotationResult2[1], RotationResult3[0], RotationResult3[1])
            self.line(RotationResult3[0], RotationResult3[1], RotationResult0[0], RotationResult0[1])
        else:
            self.line(left, top, left, bottom)
            self.line(left, bottom, right, bottom)
            self.line(right, bottom, right, top)
            self.line(right, top, left, top)
        pass

    # 画无边框的填充矩形(矩形四个顶点坐标,旋转角度,旋转基点);
    # draw a Solid-rectangle;
    def solidrectangle(self, left, top, right, bottom, angle=0, xbase=None, ybase=None):
        pencolor(fillcolor())
        width(0)
        begin_fill()
        self.rectangle(left, top, right, bottom, angle, xbase, ybase)
        end_fill()
        pass

    # 画有边框的填充矩形(矩形四个顶点坐标,旋转角度,旋转基点);
    # Draw a Fill-rectangle;
    def fillrectangle(self, left, top, right, bottom, angle=0, xbase=None, ybase=None):
        begin_fill()
        self.rectangle(left, top, right, bottom, angle, xbase, ybase)
        end_fill()
        pass

    # 画无填充的圆角矩形(矩形四个顶点坐标,圆角半径,旋转角度,旋转基点);
    # Draw a rounded rectangle with no fill;
    def roundrect(self, left, top, right, bottom, radius, angle=0, xbase=None, ybase=None):
        if radius + radius > right - left:
            radius = 0.5 * (right - left)
        if radius + radius > bottom - top:
            radius = 0.5 * (bottom - top)

        RoundrectPoints = []
        global _left, _top, _right, _bottom, stangle, endangle
        for i in range(4):
            if i == 0:
                _left = left
                _top = top
                _right = left + 2 * radius
                _bottom = top + 2 * radius

                stangle = 180
                endangle = 270
            elif i == 1:
                _left = left
                _top = bottom - 2 * radius
                _right = left + 2 * radius
                _bottom = bottom

                stangle = 90
                endangle = 180
            elif i == 2:
                _left = right - 2 * radius
                _top = bottom - 2 * radius
                _right = right
                _bottom = bottom

                stangle = 0
                endangle = 91
            elif i == 3:
                _left = right - 2 * radius
                _top = top
                _right = right
                _bottom = top + 2 * radius

                stangle = 270
                endangle = 360

            a = (_right - _left) / 2
            b = (_bottom - _top) / 2
            c = pi / 180
            d = _left + a
            e = _top + b

            _thread.start_new_thread(self.EllipseXEngine, (a, c, d, self.DefaultEllipticCurvePrecision, stangle, endangle))
            _thread.start_new_thread(self.EllipseYEngine, (b, c, e, self.DefaultEllipticCurvePrecision, stangle, endangle))

            while True:
                if self.EllipseEngineState[0] == True and self.EllipseEngineState[1] == True:
                    self.EllipsePoints.reverse()

                    RoundrectPoints.extend(self.EllipsePoints)
                    self.EllipsePoints.clear()
                    self.EllipseEngineState = [False, False]
                    break

        RoundrectPoints.append(RoundrectPoints[0])
        RoundrectPoints.append(RoundrectPoints[1])

        if angle != 0:
            EllipsePointsTransform = []
            if xbase is None and ybase is None:
                if xbase is None and ybase is None:
                    xbase = int((right - left) / 2) + left
                    ybase = int((bottom - top) / 2) + top

            for i in range(0, len(RoundrectPoints), 2):
                EllipsePointsTransformTemp = self.RotationMatrix(RoundrectPoints[i], RoundrectPoints[i + 1], xbase, ybase, angle)
                EllipsePointsTransform.append(EllipsePointsTransformTemp[0])
                EllipsePointsTransform.append(EllipsePointsTransformTemp[1])

            self.polyline(EllipsePointsTransform)
        else:
            self.polyline(RoundrectPoints)

        pass

    # 画无边框的填充圆角矩形(矩形四个顶点坐标,圆角半径,旋转角度,旋转基点);
    # Draw a filled rounded rectangle without a border;
    def solidroundrect(self, left, top, right, bottom, radius, angle=0, xbase=None, ybase=None):
        pencolor(fillcolor())
        width(0)
        begin_fill()

        self.roundrect(left, top, right, bottom, radius, angle, xbase, ybase)

        end_fill()
        pass

    # 画有边框的填充圆角矩形(矩形四个顶点坐标,圆角半径,旋转角度,旋转基点);
    # Draw a filled rounded rectangle with a border;
    def fillroundrect(self, left, top, right, bottom, radius, angle=0, xbase=None, ybase=None):
        begin_fill()

        self.roundrect(left, top, right, bottom, radius, angle, xbase, ybase)

        end_fill()
        pass

    # 画无填充多边形(指定外切圆圆心坐标,指定外切圆半径,指定多边形边数,图形旋转角度,旋转基点坐标);
    # Draw a polygon,This function is very widespread, it can create polygons with any number of sides and any rotation angle in any position.
    def polygon(self, x, y, radius, steps=72, angle=0, xbase=None, ybase=None):
        if xbase is None and ybase is None:
            xbase = x
            ybase = y

        CurrentPoint = []
        i = 0
        j = 0.0
        k = 0
        while True:
            RotationResult = self.RotationMatrix(radius * cos(pi / 180.0 * j) + x, radius * sin(pi / 180.0 * j) + y, xbase, ybase, angle)
            CurrentPoint.append(int(RotationResult[0]))
            CurrentPoint.append(int(RotationResult[1]))

            i += 1
            j += 360 / steps
            if i >= steps:
                break
            k += 2

        CurrentPoint.append(CurrentPoint[0])
        CurrentPoint.append(CurrentPoint[1])
        self.polyline(CurrentPoint)

        pass

    # 画无边框的填充多边形(指定外切圆圆心坐标,指定外切圆半径,指定多边形边数,图形旋转角度,旋转基点坐标);
    # Draw a Solid-polygon,This function is very widespread, it can create polygons with any number of sides and any rotation angle in any position.
    def solidpolygon(self, x, y, radius, steps=72, angle=0, xbase=None, ybase=None):
        pencolor(fillcolor())
        width(0)
        begin_fill()

        self.polygon(x, y, radius, steps, angle, xbase, ybase)

        end_fill()
        pass

    # 画有边框的填充多边形(指定外切圆圆心坐标,指定外切圆半径,指定多边形边数,图形旋转角度,旋转基点坐标);
    # Draw a Fill-polygon,This function is very widespread, it can create polygons with any number of sides and any rotation angle in any position.
    def fillpolygon(self, x, y, radius, steps=72, angle=0, xbase=None, ybase=None):
        begin_fill()

        self.polygon(x, y, radius, steps, angle, xbase, ybase)

        end_fill()
        pass

    EllipsePoints = []  # Temporary storage list of ellipse discrete points;
    EllipseEngineState = [False, False]  # List of thread state flags for ellipse calculate;

    # Ellipse calculate 'X' Thread;
    def EllipseXEngine(self, a, c, d, steps, stangle=0, endangle=360):
        i = stangle
        endangle = endangle + 1
        j = 0
        while True:
            self.EllipsePoints.insert(j, a * cos(c * i) + d)

            i += steps
            j += 2
            if i >= endangle:
                break

        self.EllipseEngineState[0] = True
        pass

    # Ellipse calculate 'Y' Thread;
    def EllipseYEngine(self, b, c, e, steps, stangle=0, endangle=360):
        i = stangle
        endangle = endangle + 1
        j = 1
        while True:
            self.EllipsePoints.insert(j, b * sin(c * i) + e)

            i += steps
            j += 2
            if i >= endangle:
                break

        self.EllipseEngineState[1] = True
        pass

    # 画无填充的椭圆(椭圆外切矩形,旋转角度,旋转基点,圆弧起始角角度,圆弧终止角角度,绘图计算精度[值越小越精细]);
    # draw an unfilled ellipse(Specifies the rectangle circumscribing the ellipse);
    def ellipse(self, left, top, right, bottom, angle=0, xbase=None, ybase=None, stangle=0, endangle=360, steps=DefaultEllipticCurvePrecision):
        a = (right - left) / 2
        b = (bottom - top) / 2
        c = pi / 180
        d = left + a
        e = top + b

        _thread.start_new_thread(self.EllipseXEngine, (a, c, d, steps, stangle, endangle))
        _thread.start_new_thread(self.EllipseYEngine, (b, c, e, steps, stangle, endangle))

        while True:
            if self.EllipseEngineState[0] == True and self.EllipseEngineState[1] == True:
                break

        if angle != 0:
            EllipsePointsTransform = []
            if xbase is None and ybase is None:
                xbase = int((right - left) / 2) + left
                ybase = int((bottom - top) / 2) + top

            for i in range(0, len(self.EllipsePoints), 2):
                EllipsePointsTransformTemp = self.RotationMatrix(self.EllipsePoints[i], self.EllipsePoints[i + 1], xbase, ybase, angle)
                EllipsePointsTransform.append(EllipsePointsTransformTemp[0])
                EllipsePointsTransform.append(EllipsePointsTransformTemp[1])

            self.polyline(EllipsePointsTransform)
        else:
            self.polyline(self.EllipsePoints)

        self.EllipsePoints.clear()
        self.EllipseEngineState = [False, False]

        pass

    # 画无边框的填充椭圆(椭圆外切矩形,旋转角度,旋转基点,圆弧起始角角度,圆弧终止角角度,绘图计算精度[值越小越精细]);
    # draw an Solid-ellipse;
    def solidellipse(self, left, top, right, bottom, angle=0, xbase=None, ybase=None, stangle=0, endangle=360, steps=DefaultEllipticCurvePrecision):
        pencolor(fillcolor())
        width(0)
        begin_fill()

        self.ellipse(left, top, right, bottom, angle, xbase, ybase, stangle, endangle, steps)

        end_fill()
        pass

    # 画有边框的填充椭圆(椭圆外切矩形,旋转角度,旋转基点,圆弧起始角角度,圆弧终止角角度,绘图计算精度[值越小越精细]);
    # Draw a filled ellipse with a border;
    def fillellipse(self, left, top, right, bottom, angle=0, xbase=None, ybase=None, stangle=0, endangle=360, steps=DefaultEllipticCurvePrecision):
        begin_fill()

        self.ellipse(left, top, right, bottom, angle, xbase, ybase, stangle, endangle, steps)

        end_fill()
        pass

    # 画椭圆弧(椭圆外切矩形,圆弧起始角角度,圆弧终止角角度);
    # Draw ellipse arc;
    def arc(self, left, top, right, bottom, stangle=0, endangle=360):
        self.ellipse(left, top, right, bottom, 0, None, None, stangle, endangle)
        pass

    # 画无填充的扇形(扇形外切矩形四个顶点坐标,扇形的起始角的角度,扇形的终止角的角度,旋转角度,旋转基点)
    # Draw a sector without filling;
    def pie(self, left, top, right, bottom, stangle=0, endangle=360, angle=0, xbase=None, ybase=None):
        a = (right - left) / 2
        b = (bottom - top) / 2
        c = pi / 180
        d = left + a
        e = top + b

        _thread.start_new_thread(self.EllipseXEngine, (a, c, d, self.DefaultEllipticCurvePrecision, stangle, endangle))
        _thread.start_new_thread(self.EllipseYEngine, (b, c, e, self.DefaultEllipticCurvePrecision, stangle, endangle))

        while True:
            if self.EllipseEngineState[0] == True and self.EllipseEngineState[1] == True:
                break

        _xbase = int((right - left) / 2) + left
        _ybase = int((bottom - top) / 2) + top
        self.EllipsePoints.append(_xbase)
        self.EllipsePoints.append(_ybase)

        if angle != 0:
            EllipsePointsTransform = []

            if xbase is None and ybase is None:
                xbase = _xbase
                ybase = _ybase

            for i in range(0, len(self.EllipsePoints), 2):
                EllipsePointsTransformTemp = self.RotationMatrix(self.EllipsePoints[i], self.EllipsePoints[i + 1], xbase, ybase, angle)
                EllipsePointsTransform.append(EllipsePointsTransformTemp[0])
                EllipsePointsTransform.append(EllipsePointsTransformTemp[1])

            EllipsePointsTransform.append(EllipsePointsTransform[0])
            EllipsePointsTransform.append(EllipsePointsTransform[1])
            self.polyline(EllipsePointsTransform)
        else:
            self.EllipsePoints.append(self.EllipsePoints[0])
            self.EllipsePoints.append(self.EllipsePoints[1])
            self.polyline(self.EllipsePoints)

        self.EllipsePoints.clear()
        self.EllipseEngineState = [False, False]
        pass

    # 画无边框的填充扇形(扇形外切矩形四个顶点坐标,扇形的起始角的角度,扇形的终止角的角度,旋转角度,旋转基点)
    # Draw a filled sector without a border;
    def solidpie(self, left, top, right, bottom, stangle=0, endangle=360, angle=0, xbase=None, ybase=None):
        pencolor(fillcolor())
        width(0)
        begin_fill()

        self.pie(left, top, right, bottom, stangle, endangle, angle, xbase, ybase)

        end_fill()
        pass

    # 画有边框的填充扇形(扇形外切矩形四个顶点坐标,扇形的起始角的角度,扇形的终止角的角度,旋转角度,旋转基点)
    # Draw a filled sector with a border;
    def fillpie(self, left, top, right, bottom, stangle=0, endangle=360, angle=0, xbase=None, ybase=None):
        begin_fill()

        self.pie(left, top, right, bottom, stangle, endangle, angle, xbase, ybase)

        end_fill()
        pass

    # 画无填充的圆(圆心 x 坐标,圆心 y 坐标,圆的半径);
    # draw unfilled circle;
    def Circle(self, x, y, radius):
        steps = 0.3 * radius + 45
        self.teleport(x, y + radius)
        circle(radius, None, int(steps))
        pass

    # 画无边框的填充圆(圆心 x 坐标,圆心 y 坐标,圆的半径)
    # Draw a filled circle without borders;
    def solidcircle(self, x, y, radius):
        self.teleport(x, y)
        size = pensize()
        pencolor(fillcolor())
        width(0)
        begin_fill()

        self.Circle(x, y, radius)

        end_fill()
        width(size)
        pass

    # 画有边框的填充圆(圆心 x 坐标,圆心 y 坐标,圆的半径)
    # Draw a filled circle with a border
    def fillcircle(self, x, y, radius):
        begin_fill()

        self.Circle(x, y, radius)

        end_fill()
        pass

    # 获取点的颜色(点的坐标);
    # Gets the color of the point;
    def getpixel(self, x, y):
        _x, _y = self.GalileanTransformation(x, y)

        canvas = getcanvas()
        ids = canvas.find_overlapping(_x, -_y, _x, -_y)

        if ids:  # if list is not empty
            index = ids[-1]
            color = canvas.itemcget(index, "fill")
            if color != '':
                return color.lower()

        return self.backgroundcolor  # default color

    # 在指定区域内以指定格式输出字符串(指定输出坐标,文本内容,字体,字号,字形,文本对齐方式);
    # Output a string in the specified format within the specified area;
    def drawtext(self, x, y, TextStr="", fontname="微软雅黑", fontsize=12, fonttype="normal", align="left"):
        font = (fontname, fontsize, fonttype)

        self.teleport(x, y)
        write(TextStr, False, align, font)
        pass

    # 将画布导出为矢量图(文件名);
    # Export the canvas as a vector image;
    def saveimage(self, fileName):
        IMG = getscreen()
        IMG.getcanvas().postscript(file=str(fileName) + "_RMSHE_MountPenglai_Vector.eps")
        pass

    def radialgradient(self, x, y, StartRadius, EndRadius, StartColorHex, EndColorHex, steps=1.0):
        pensize(int(steps) + 1)

        RadiusDifference = float(abs(EndRadius - StartRadius))

        SH, SS, SV = self.SelfMPCS.GetHSVValue(StartColorHex)
        EH, ES, EV = self.SelfMPCS.GetHSVValue(EndColorHex)

        dH = ((EH - SH) / RadiusDifference) * steps
        dS = ((ES - SS) / RadiusDifference) * steps
        dV = ((EV - SV) / RadiusDifference) * steps

        # SR, SG, SB = self.SelfMPCS.GetRGBValue(StartColorHex)
        # ER, EG, EB = self.SelfMPCS.GetRGBValue(EndColorHex)

        # dR = ((ER - SR) / RadiusDifference) * steps
        # dG = ((EG - SG) / RadiusDifference) * steps
        # dB = ((EB - SB) / RadiusDifference) * steps

        Hue = SH
        Saturation = SS
        Value = SV
        Radius = StartRadius

        # self.BeginBatchDraw()
        while True:
            Hue = Hue + dH
            Saturation = Saturation + dS
            Value = Value + dV

            pencolor(self.SelfMPCS.HSV(Hue, Saturation, Value))
            self.Circle(x, y, Radius)

            if EndRadius - StartRadius > 0:
                Radius = Radius + steps
                if Radius >= EndRadius:
                    break
            else:
                Radius = Radius - steps
                if Radius <= EndRadius:
                    break

        # self.FlushBatchDraw()
        pass


class MountPenglaiMath:
    def COMPLEXSUM(self, a=(), b=()):
        return [a[0] + b[0], a[1] + b[1]]

    def COMPLEXMUL(self, a=(), b=()):
        return [a[0] * b[0] - a[1] * b[1], a[1] * b[0] + a[0] * b[1]]


class MountPenglaiExamples:
    SelfMP = MountPenglai()
    SelfMPCS = MPColorSystem()
    SelfMath = MountPenglaiMath()

    # 渲染伪3D平面;
    def MPE01(self, Resolution=400):
        self.SelfMP.initgraph(Resolution, Resolution)
        self.SelfMP.drawtext(Resolution * 0.5, Resolution * 0.5 + 12, "正在渲染", "微软雅黑", 24, "normal", "center")

        self.SelfMP.BeginBatchDraw()

        for i in range(0, Resolution):
            for j in range(0, Resolution):
                s = 3.0 / (j + 99)
                HD = (int((i + Resolution) * s + j * s) % 2 + int((Resolution * 2 - i) * s + j * s) % 2) * 127

                fillcolor(self.SelfMPCS.RGB(HD, HD, HD))
                self.SelfMP.putpixel(i, j)

            if i % 16 == 0:
                self.SelfMP.FlushBatchDraw()

        self.SelfMP.EndBatchDraw()
        pass

    # CircleLineLink;
    def MPE02(self, k_END=2, steps=3, Resolution=900):
        self.SelfMP.initgraph(Resolution, Resolution)
        for k in range(k_END):
            self.SelfMP.BeginBatchDraw()
            clear()

            origin = [Resolution * 0.5, Resolution * 0.5]
            CirclePoints = []

            for i in range(0, 360, steps):
                x, y = self.SelfMP.RotationMatrix(1.9 * origin[0], origin[1], origin[0], origin[1], i)
                self.SelfMP.putpixel(x, y, 6)

                CirclePoints.append(int(x))
                CirclePoints.append(int(y))

            pensize(1)

            i = 0
            j = 0
            H = 0
            while True:
                m = k * i % int(360 / steps)
                pencolor(self.SelfMPCS.HSV(H, 0.6, 0.8))
                self.SelfMP.line(CirclePoints[i], CirclePoints[i + 1], CirclePoints[m], CirclePoints[m + 1])
                self.SelfMP.FlushBatchDraw()

                j += 1
                H += steps
                if j == int(len(CirclePoints) / 2) - 1:
                    break
                i += 2

            self.SelfMP.EndBatchDraw()
            done()

    # [分形] 渲染 Mandelbrot Set (曼德布洛特集);
    def MPE03(self, width=400, height=300):
        self.SelfMP.initgraph(width, height)
        self.SelfMP.drawtext(width * 0.5, height * 0.5 + 12, "正在渲染", "微软雅黑", 24, "normal", "center")

        self.SelfMP.BeginBatchDraw()

        c_re = 0
        c_im = 0
        z_re = 0
        z_im = 0
        for x in range(0, width):
            c_re = -2.1 + (1.1 - (-2.1)) * (x / width)
            for y in range(0, height):
                c_im = -1.2 + (1.2 - -1.2) * (y / height)
                z_re = z_im = 0

                H = 0
                for k in range(0, 180):
                    H = k
                    if z_re * z_re + z_im * z_im > 4.0:
                        break

                    z_re, z_im = self.SelfMath.COMPLEXSUM(self.SelfMath.COMPLEXMUL((z_re, z_im), (z_re, z_im)), (c_re, c_im))

                fillcolor(self.SelfMPCS.HSV(float(((H << 5) % 360)) + 60, 1, 1))
                self.SelfMP.putpixel(x, y)

            if x % 16 == 0:
                self.SelfMP.FlushBatchDraw()

        self.SelfMP.EndBatchDraw()
        pass

    # Organ-Field GUI 风格时钟(我把我一年半前的祖传C++代码移植过来了);
    def MPE04(self, Resolution=900):
        from datetime import datetime
        halfResolution = 0.5 * Resolution
        Resolution0_1 = 0.1 * Resolution
        Resolution0_3 = 0.3 * Resolution
        R = Resolution0_4 = 0.4 * Resolution
        Resolution0_45 = 0.45 * Resolution
        halfResolution0_01 = 0.01 * halfResolution
        halfResolution0_021 = 0.021 * halfResolution
        halfResolution0_035 = 0.035 * halfResolution
        halfResolution0_04 = 0.04 * halfResolution
        wochentag = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]

        SX0 = []
        SY0 = []
        SXS = []
        SYS = []
        Second = 0
        while Second < 2 * pi:
            Second = (2 * pi / 60) + Second

            SXS.append(int((R - 20) * cos(Second)))
            SX0.append(int((R - 40) * cos(Second)))

            SYS.append(int((R - 20) * sin(Second)))
            SY0.append(int((R - 40) * sin(Second)))

        BX0 = []
        BY0 = []
        BXS = []
        BYS = []
        Second = 0
        while Second < 2 * pi:
            Second = (2 * pi / 12) + Second

            BXS.append(int((R - 20) * cos(Second)))
            BX0.append(int((R - 52) * cos(Second)))

            BYS.append(int((R - 20) * sin(Second)))
            BY0.append(int((R - 52) * sin(Second)))

        XT = []
        YT = []
        Second = 0
        while Second < 2 * pi:
            Second = (2 * pi / 12) + Second

            XT.append(int((R - 90) * cos(Second)))
            YT.append(int((R - 90) * sin(Second)))

        Angle_Precompute = (2 * pi) / 60
        Angle_H_Precompute = (2 * pi) / 12

        AC = 180 / pi

        self.SelfMP.BeginBatchDraw()
        self.SelfMP.initgraph(Resolution, Resolution)
        setundobuffer(63)
        while True:
            self.SelfMP.radialgradient(halfResolution, halfResolution, Resolution0_4, Resolution0_45, "#23272e", "#282c34", 2)

            fillcolor("#313640")
            self.SelfMP.solidcircle(halfResolution, halfResolution, Resolution0_4)

            self.SelfMP.radialgradient(halfResolution, halfResolution, Resolution0_3, Resolution0_1, "#313640", "#282c34", 2)
            fillcolor("#282c34")
            self.SelfMP.solidcircle(halfResolution, halfResolution, Resolution0_1)

            pensize(4)
            pencolor("#737780")
            for i in range(60):
                self.SelfMP.line(SX0[i] + halfResolution, SY0[i] + halfResolution, SXS[i] + halfResolution, SYS[i] + halfResolution)

            pensize(8)
            pencolor("#737780")
            for i in range(12):
                self.SelfMP.line(BX0[i] + halfResolution, BY0[i] + halfResolution, BXS[i] + halfResolution, BYS[i] + halfResolution)

            pencolor("#abb2bf")
            TextNum = 4
            for i in range(12):
                if TextNum > 12:
                    TextNum = 1
                self.SelfMP.drawtext(XT[i] + halfResolution, YT[i] + halfResolution + 21, str(int(TextNum)), "微软雅黑", 24, "normal", "center")
                TextNum += 1

            pencolor("#676b73")
            self.SelfMP.drawtext(halfResolution, halfResolution - 0.3 * R, "R M S H E", "微软雅黑", 24, "normal", "center")

            t1 = datetime.today()
            self.SelfMP.drawtext(halfResolution, halfResolution + 26 + 0.3 * R, wochentag[t1.weekday()], "微软雅黑", 24, "normal", "center")

            MinuteNLast = MinuteNow = t1.minute
            while True:
                # // 计算时、分、秒针的弧度值;
                t = datetime.today()
                # Angle_MicroSecond = t.microsecond * (2 * pi) / 60
                # Angle_Second = t.second * (2 * pi) / 60 + Angle_MicroSecond * 0.000001

                MinuteNow = t.minute
                if MinuteNow - MinuteNLast == 2:
                    clear()
                    break

                Angle_Second = t.second * Angle_Precompute
                Angle_Minute = t.minute * Angle_Precompute + Angle_Second / 60
                Angle_Hour = t.hour * Angle_H_Precompute + Angle_Minute / 12

                # // 计算时、分、秒针的坐标;
                Angle_Second_cos = cos(Angle_Second)
                Angle_Second_sin = sin(Angle_Second)
                Second_Y = -(R - 62) * Angle_Second_cos + halfResolution
                Y0 = -(-R + 320) * Angle_Second_cos + halfResolution
                Second_X = (R - 62) * Angle_Second_sin + halfResolution
                X0 = (-R + 320) * Angle_Second_sin + halfResolution

                Minute_hand_Y = -(R - 90) * cos(Angle_Minute) + halfResolution
                Minute_hand_X = (R - 90) * sin(Angle_Minute) + halfResolution

                Hour_hand_Y = -(R - 120) * cos(Angle_Hour) + halfResolution
                Hour_hand_X = (R - 120) * sin(Angle_Hour) + halfResolution

                # //指针圆心投影;
                fillcolor("#23272e")
                self.SelfMP.solidcircle(halfResolution + 3, halfResolution + 3, halfResolution0_04)

                # //分针投影;
                pencolor("#282c34")
                pensize(12)
                self.SelfMP.line(halfResolution + 5, halfResolution + 5, Minute_hand_X + 5, Minute_hand_Y + 5)

                # //时针投影;
                pencolor("#23272e")
                pensize(14)
                self.SelfMP.line(halfResolution + 5, halfResolution + 5, Hour_hand_X + 5, Hour_hand_Y + 5)

                # // 时针;
                pensize(12)
                pencolor("#959ba6")
                self.SelfMP.line(halfResolution, halfResolution, Hour_hand_X, Hour_hand_Y)

                # // 分针;
                pensize(8)
                pencolor("#abb2bf")
                self.SelfMP.line(halfResolution, halfResolution, Minute_hand_X, Minute_hand_Y)

                # // 分针圆心;
                fillcolor("#abb2bf")
                self.SelfMP.solidcircle(halfResolution, halfResolution, halfResolution0_035)

                # // 秒针;
                ASAC = Angle_Second * AC
                pensize(4)
                pencolor(self.SelfMPCS.HSV(ASAC, 0.5, 0.8))
                self.SelfMP.line(X0, Y0, Second_X, Second_Y)

                # // 秒针圆心;
                fillcolor(self.SelfMPCS.HSV(ASAC, 0.5, 0.8))
                self.SelfMP.solidcircle(halfResolution, halfResolution, halfResolution0_021)

                # // 圆心;
                fillcolor("#313640")
                self.SelfMP.solidcircle(halfResolution, halfResolution, halfResolution0_01)

                self.SelfMP.FlushBatchDraw()
                # self.SelfMP.saveimage("01")

                # 刷新视图;
                for i in range(64):
                    undo()

            '''
            pensize(4)
            pencolor("#313640")
            self.SelfMP.line(X0, Y0, Second_X, Second_Y)
            pensize(8)
            self.SelfMP.line(halfResolution, halfResolution, Minute_hand_X, Minute_hand_Y)
            pensize(12)
            self.SelfMP.line(halfResolution, halfResolution, Hour_hand_X, Hour_hand_Y)
            pensize(12)
            self.SelfMP.line(halfResolution + 5, halfResolution + 5, Minute_hand_X + 5, Minute_hand_Y + 5)
            pensize(14)
            self.SelfMP.line(halfResolution + 5, halfResolution + 5, Hour_hand_X + 5, Hour_hand_Y + 5)
            '''


'''------------------------------------------------------------------------------------------
Python根本不适合用来写GUI和渲染引擎,特别是在图形渲染这一块,C++一秒就能完成的计算,Python需要一分钟以上.
而且两者底层代码的复杂程度是差不多的,也就是说在底层这块使用Python并不能很好就降低开发难度. 何况C/C++的
速度对Python来说是降维打击. C/C++能够直接操作内存等计算机资源,当开发者的水平足够高时就能够写出运行速度
非常块并且占用资源非常低的程序.
    
目前情况是, 本项目: MountPenglai 的运行速度非常的"优雅"(优雅到窒息), 当然主要原因是 turtle 库太慢.
我在C++那边一直在开发的一个项目: Organ-Field GUI 它在做与 MountPenglai 相同图形渲染时目测几毫秒内
就能完成, 而 MountPenglai 则需要破天荒的花上几秒.
------------------------------------------------------------------------------------------'''
