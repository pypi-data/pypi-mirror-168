from colors import Colors


class WrapperComponents:
    @staticmethod
    def textWrap(text, color: Colors=Colors.WHITE, bold=False) -> str:
        if bold:
            return f"{color}{Colors.BOLD}{text}{Colors.END}"
        else:
            return f"{color}{text}{Colors.END}"

    @staticmethod
    def textWrapBold(text, color: Colors=Colors.WHITE) -> str:
        return WrapperComponents.textWrap(text, color, bold=True)

    @staticmethod
    def textWrapUnderline(text, color: Colors) -> str:
        return f"{color}{Colors.UNDERLINE}{text}{Colors.END}"

    @staticmethod
    def textWrapBoldUnderline(text, color: Colors) -> str:
        return f"{color}{Colors.UNDERLINE}{Colors.BOLD}{text}{Colors.END}"

