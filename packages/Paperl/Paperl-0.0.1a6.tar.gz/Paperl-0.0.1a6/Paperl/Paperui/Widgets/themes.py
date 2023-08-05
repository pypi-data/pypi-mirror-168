from Paperl.Paperc import prWarring, prSuccess, prError
from typing import Literal


class Themes(object):
    def getSystemStyles(self):
        """
        获取到系统所有的主题名称

        :return: 系统所有的主题
        """

        from tkinter.ttk import Style
        return Style().theme_names()

    def useStyle(self, styleName):
        """
        启用系统主题（无需安装库）

        :param styleName: 系统主题的名称
        """
        try:
            from tkinter.ttk import Style
            Style().theme_use(styleName)
        except:
            prWarring(f"Widget -> Style -> {styleName} -> This system does not support this theme")

    def useStyleAqua(self):
        """
        启用系统Aqua主题（无需安装库）
        """
        self.useStyle("aqua")

    def useStyleVista(self):
        """
        启用系统Vista主题（无需安装库）
        """
        self.useStyle("vista")

    def useStyleWinNative(self):
        """
        启用系统WinNative主题（无需安装库）
        """
        self.useStyle("winnative")

    def useStyleDefault(self):
        """
        启用系统默认主题（无需安装库）
        """
        self.useStyle("default")

    def useStyleClassic(self):
        """
        启用系统Classic全系统通用主题（无需安装库）
        """
        self.useStyle("classic")

    def useStyleAlt(self):
        """
        启用系统Alt主题（无需安装库）
        """
        self.useStyle("alt")

    def useStyleClam(self):
        """
        启用系统Clam主题（无需安装库）
        """
        self.useStyle("clam")

    def useStyleSunValley(self, theme: Literal["light", "dark", "auto"] = "auto"):
        """
        启用太阳谷主题（需安装sv-ttk库）（如果需要打包，请从sv-ttk的Github存储库内找到sv_ttk文件夹，然后下载放到程序目录）

        :param theme: 设置太阳谷主题 参考值 -> "light" "dark"
        """
        try:
            from sv_ttk import use_dark_theme, use_light_theme
        except:
            prWarring("sv_ttk -> Check -> Not Installed")
        else:
            def light():
                use_light_theme()
                self.setLightTheme()
                self.setBackground("#fafafa")

            def dark():
                use_dark_theme()
                self.setDarkTheme()
                self.setBackground("#1c1c1c")

            prSuccess("sv_ttk -> Check -> Installed")
            if theme == "auto":
                try:
                    from darkdetect import isDark
                except:
                    prError("darkdetect -> Check -> Not Installed")
                else:
                    if isDark():
                        dark()
                    else:
                        light()
            elif theme == "dark":
                dark()
            else:
                light()

    def useStyleEx(self, styleName):
        """
        启用扩展主题（需安装ttkthemes库）

        :param styleName: 扩展主题的名称
        """
        try:
            from ttkthemes import ThemedStyle
        except:
            prWarring("ttkthemes -> Check -> Not Installed")
        else:
            prSuccess("ttkthemes -> Check -> Installed")
            try:
                ThemedStyle(self.Me).theme_use(styleName)
            except:
                prError(f"ttkthemes -> {styleName} -> The theme could not be found")

    def useStyleExArc(self):
        """
        启用扩展Arc主题（需安装ttkthemes库）
        """
        self.useStyleEx("arc")

    def useStyleExEquilux(self):
        """
        启用扩展Equilux主题（需安装ttkthemes库）
        """
        self.useStyleEx("equilux")

    def useStyleExWinXpBlue(self):
        """
        启用扩展WinXpBlue主题（需安装ttkthemes库）
        """
        self.useStyleEx("winxpblue")

    def useStyleExAquativo(self):
        """
        启用扩展Aquativo主题（需安装ttkthemes库）
        """
        self.useStyleEx("aquativo")

    def useStyleExAdapta(self):
        """
        启用扩展Adapta主题（需安装ttkthemes库）
        """
        self.useStyleEx("adapta")

    def useStyleExBreeze(self):
        """
        启用扩展Breeze主题（需安装ttkthemes库）
        """
        self.useStyleEx("breeze")

    def useStyleExRadiance(self):
        """
        启用扩展Radiance主题（需安装ttkthemes库）
        """
        self.useStyleEx("radiance")

    def useStyleExYaru(self):
        """
        启用扩展Yaru主题（需安装ttkthemes库）
        """
        self.useStyleEx("yaru")