#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author: lockerzhang
@LastEditors: lockerzhang
@Description: 小程序页面
@Date: 2019-03-11 14:42:29
@LastEditTime: 2019-06-05 17:04:02
"""
import re
from minium.framework.exception import MiniElementNotFoundError, MiniAppError
import typing
from .element import *
from .minium_object import MiniumObject
from ...utils.utils import timeout
from .connection import Command

# 需要在setup中加上cssselect库
# from cssselect.xpath import HTMLTranslator
# from cssselect.parser import SelectorError

# translator = HTMLTranslator()


class Page(MiniumObject):
    """
    页面相关接口
    """

    def __init__(self, page_id, path, query, connection):
        """
        初始化页面
        """
        super().__init__()
        self.page_id = page_id
        # 处理下path，普通page以"/"开头，插件以"plugin://" 或 "plugin-private://"开头
        self.plugin_appid = None
        match = re.search(r"^(plugin://|plugin-private://|__plugin__/)(\w+)/", path)
        if match:
            self.plugin_appid = match.group(2)
        elif not path.startswith("/"):
            path = "/" + path
        self.path = path
        self.query = query
        self.connection = connection
        self.is_webview = None  # None: 未知，true: 是，false: 否 

    def __repr__(self):
        return "Page(id={0}, path={1}, query={2})".format(self.page_id, self.path, self.query)

    @property
    def data(self):
        """
        获取页面 Data
        :return: json
        """
        return self._send("Page.getData").result.data

    @data.setter
    def data(self, data):
        """
        设置页面 data
        :param data:
        :return:
        """
        self._send("Page.setData", {"data": data})

    @property
    def inner_size(self):
        """
        get window size
        :return:
        """
        size_arr = self._get_window_properties(["innerWidth", "innerHeight"])
        return {"width": size_arr[0], "height": size_arr[1]}

    @property
    def scroll_height(self):
        """
        get scroll height
        :return:
        """
        return self._get_window_properties(["document.documentElement.scrollHeight"])[0]

    @property
    def scroll_width(self):
        """
        get scroll width
        :return:
        """
        return self._get_window_properties(["document.documentElement.scrollWidth"])[0]

    @property
    def scroll_x(self):
        """
        获取窗口顶点与页面顶点的 x 轴偏移量
        :return:
        """
        return self._get_window_properties(["scrollX"])[0]

    @property
    def scroll_y(self):
        """
        获取窗口顶点与页面顶点的 y 轴偏移量
        :return:
        """
        return self._get_window_properties(["scrollY"])[0]

    def wait_data_contains(self, *keys_list: list or str, max_timeout: int = 10):
        """
        description: 等待Page.data中包含指定keys
        param {*} self
        param {array} keys_list: items is list or str split by "."
        param {int} max_timeout
        return {bool}
        """

        @timeout(max_timeout)
        def f():
            d = self.data
            for keys in keys_list:
                obj = d
                for key in keys if isinstance(keys, (list, tuple)) else keys.split("."):
                    if isinstance(obj, dict) and key in obj:
                        obj = obj[key]
                    else:
                        return False
            return True

        try:
            return f()
        except Exception as e:
            self.logger.exception(e)
            return False

    def element_is_exists(
        self,
        selector: str = None,
        max_timeout: int = 10,
        inner_text=None,
        text_contains=None,
        value=None,
        xpath: str = None,
    ) -> bool:
        """
        查询元素是否存在
        :param selector:
        :param max_timeout: 超时时间
        :param inner_text: inner_text
        :param value: value
        :param text_contains: 包含的文字
        :param xpath: 使用xpath
        :return: bool
        """
        if selector and selector.startswith("/"):
            # 以/或//开头的认为是xpath
            xpath = selector
            selector = None
        return self._wait(
            lambda: self._element_is_exists(
                selector, xpath, inner_text=inner_text, value=value, text_contains=text_contains
            ),
            max_timeout,
        )

    def get_element(
        self,
        selector: str,
        inner_text=None,
        text_contains=None,
        value=None,
        max_timeout=0,
        xpath=None,
    ) -> Elements:
        """
        find elements in current page, by css selector or xpath
        目前支持的css选择器有:

        选择器	              样例	                      样例描述
        .class	             .intro	                    选择所有拥有 class="intro" 的组件
        #id	                 #firstname	                选择拥有 id="firstname" 的组件
        tagname	             view	                    选择所有    view 组件
        tagname, tagname	 view, checkbox	            选择所有文档的 view 组件和所有的 checkbox 组件

        ::after	             view::after	            在 view 组件后边插入内容
        ::before	         view::before	            在 view 组件前边插入内容
        >>>                  ce1>>>.ce2>>>.intro        跨自定义组件的后代选择器

        支持以/或//开头的xpath

        :param selector: CSS选择器/XPATH
        :param inner_text: inner_text
        :param value: value
        :param text_contains: 包含的文字
        :param max_timeout: 超时时间
        :return:element 对象
        """
        if (selector and selector.startswith("/")) or xpath:
            # use xpath
            return self.get_element_by_xpath(
                xpath or selector,
                max_timeout=max_timeout,
                inner_text=inner_text,
                value=value,
                text_contains=text_contains,
            )
        r = self.get_elements(
            selector,
            max_timeout,
            inner_text=inner_text,
            value=value,
            text_contains=text_contains,
            index=0,
        )
        if not r:
            raise MiniElementNotFoundError("element[%s] not found" % selector)
        return r[0]

    def call_method(self, method, args=None):
        if not args:
            args = []
        if isinstance(args, dict):
            args = [args]
        return self._send("Page.callMethod", {"method": method, "args": args})

    def call_function(self, app_function: str, args=None, sync=True, desc=None):
        """
        向 webview 页面注入代码并执行, 仅支持web-view页面
        :param app_function:
        :param args:
        :param sync:
        :param desc: 报错描述
        :return:
        """
        if self.is_webview is None:
            # 检查是否为webview页面
            if self.get_elements("web-view"):
                self.is_webview = True
            else:
                self.is_webview = False
        if self.is_webview:
            return self._page_evaluate(app_function=app_function, args=args, sync=sync)
        return self._evaluate(app_function=app_function, args=args, sync=sync, desc=desc)

    def wait_for(self, condition=None, max_timeout=10):
        s_time = time.time()
        if isinstance(condition, int):
            time.sleep(condition)
            self.logger.debug("waitFor: %s s" % (time.time() - s_time))
            return True
        elif isinstance(condition, str):
            while (time.time() - s_time) < max_timeout:
                if self._element_is_exists(condition):
                    return True
                else:
                    time.sleep(0.25)
            else:
                return False
        elif hasattr(condition, "__call__"):
            while (time.time() - s_time) < max_timeout:
                res = condition()
                if res:
                    return True
                else:
                    time.sleep(0.25)
            else:
                return False

    def get_elements(
        self,
        selector,
        max_timeout=0,
        inner_text=None,
        text_contains=None,
        value=None,
        index=-1,
        xpath=None,
    ) -> typing.List[BaseElement]:
        """
        find elements in current page, by css selector
        :param selector: 选择器
        :param inner_text: inner_text
        :param value: value
        :param text_contains: 包含的文字
        :param max_timeout: 超时时间
        :param index: index == -1: get所有, index >=0: get index+1个
        :param xpath: 使用xpath
        :return:element 对象 list
        """
        if selector and selector.startswith("/"):
            # 以/或//开头的认为是xpath
            xpath = selector
            selector = None
        if inner_text is None and value is None and text_contains is None:
            need_filter = False
        else:
            need_filter = True
        if not need_filter and selector:
            # 不需要过滤内容，直接返回
            return self._get_elements_by_css(selector, max_timeout, index=index)
        elif xpath:
            # xpath支持text() contains()等条件，不需要额外做过滤
            return self.get_elements_by_xpath(
                xpath,
                max_timeout=max_timeout,
                inner_text=inner_text,
                text_contains=text_contains,
                value=value,
            )

        @timeout(max_timeout)
        def filter_elements():
            # 需要过滤内容，有返回元素不是终结条件, 需要获取所有元素后再作过滤
            elements = self._get_elements_by_css(selector, max_timeout, index=-1)
            els = []
            for element in elements:
                if inner_text and element.inner_text != inner_text:
                    continue
                if value and element.value() != value:
                    continue
                if text_contains and text_contains not in element.inner_text:
                    continue
                els.append(element)
                if len(els) == (index + 1):
                    return els
            return els

        return filter_elements()

    def scroll_to(self, scroll_top, duration=300):
        """
        滚动到指定位置
        :param scroll_top:  位置 px
        :param duration:  滚动时长
        :return:
        """
        self.call_wx_method("pageScrollTo", [{"scrollTop": scroll_top, "duration": duration}])

    def get_elements_by_xpath(
        self, xpath, max_timeout=10, inner_text=None, value=None, text_contains=None, index=-1
    ) -> Elements:
        """
        根据xpath查找元素
        :param xpath: xpath
        :param max_timeout: 超时时间
        :param inner_text: inner_text
        :param value: value
        :param text_contains: 包含的文字
        """
        if inner_text is not None:
            xpath += '[text()="%s"]' % inner_text
        elif text_contains is not None:
            xpath += '[contains(text(), "%s")]' % text_contains
        elif value is not None:
            xpath += '[@value="%s"]' % value

        @timeout(max_timeout)
        def search_elements():
            return self._get_elements_by_xpath(xpath, index=index)

        return search_elements()

    def get_element_by_xpath(
        self, xpath, max_timeout=10, inner_text=None, value=None, text_contains=None
    ) -> Elements:
        """
        根据xpath查找元素
        :param xpath: xpath
        :param max_timeout: 超时时间
        :param inner_text: inner_text
        :param value: value
        :param text_contains: 包含的文字
        """
        if inner_text is not None:
            xpath += '[text()="%s"]' % inner_text
        elif text_contains is not None:
            xpath += '[contains(text(), "%s")]' % text_contains
        elif value is not None:
            xpath += '[@value="%s"]' % value

        @timeout(max_timeout)
        def search_element():
            return self._get_element_by_xpath(xpath)

        el = search_element()
        if not el:
            raise MiniElementNotFoundError("element[%s] not found" % xpath)
        return el

    def _get_window_properties(self, names=None):
        """
        获取 window 对象的属性值。
        :param names:
        :return:
        """
        if names is None:
            names = []
        return self._send("Page.getWindowProperties", {"names": names}).result.properties

    def _send(self, method, params=None, sync=True):
        if params is None:
            params = {}
        params["pageId"] = self.page_id
        # self.logger.debug(f"method {method}, params: {params}")
        return self.connection.send(method, params) if sync else self.connection.send_async(method, params)

    def __get_elements(self, selector: str, index=-1):
        elements = []
        ret = self._send("Page.getElements", {"selector": selector})
        for el in ret.result.elements:
            elements.append(create(el, self.page_id, self.connection))
            if len(elements) == (index + 1):  # index==-1时，不会match，就会全部返回
                return elements
        return elements

    def __search_child(
        self, selector_list: list, parent: BaseElement = None, index=-1
    ) -> typing.List[BaseElement]:
        # index == -1: get所有, index >=0: get index+1个
        if len(selector_list) == 0:
            return []
        _selector = selector_list.pop()
        should_be_custom_element = bool(len(selector_list))  # 出了最后一层selector，都需要是自定义组件，不然不能往下走
        if parent:
            els = parent.get_elements(
                _selector, max_timeout=0
            )  # 调用element.get_elements方法，要求立刻返回，不然会影响效率
        else:
            els = self.__get_elements(_selector)
        if len(els) == 0:
            return []
        real_els = []
        for _el in els:
            if should_be_custom_element and isinstance(_el, CustomElement):
                real_els.append(_el)
            elif not should_be_custom_element:
                real_els.append(_el)
            else:
                self.logger.warn("%s should be a custom element" % _selector)
        if not real_els or len(selector_list) == 0:  # 找不到 或 没有子选择器了
            return real_els
        child_els = []
        for _el in real_els:
            child_el = self.__search_child(selector_list[0:], _el)  # selector_list[0:]相当于copy
            child_els += child_el
            if len(child_els) == (index + 1):
                return child_els
        return child_els

    def _get_elements_by_css(
        self, selector: str, max_timeout=0, index=-1
    ) -> typing.List[BaseElement]:
        """
        1. 现存自定义组件中的class会自动加前缀，但不包括slot占位的元素
        2. slot元素的class命名规则
        2.1 <page><test><view class="这个class不会加前缀"></view></test></page>
        2.2 <custom><test><view class="这个class会加上custom组件对应的前缀"></view></test></custom>
        3. 自定义组件中通过id获取元素失败
        """

        @timeout(max_timeout)
        def search_elements(_selector: list or tuple):
            return self.__search_child(
                _selector[0:], index=index
            )  # __search_child回pop元素，第一次search失败后重试会有问题，copy一份

        self.logger.info("try to get elements: %s" % selector)
        _selector_list = selector.split(">>>")
        _selector_list.reverse()  # 新增处理【>>>】穿透自定义组件逻辑
        els = search_elements(_selector_list)
        if len(els) == 0:
            self.logger.warning(f"Could not found any element '{selector}' you need")
        else:
            self.logger.info("find elements success: %s" % str(els))
        return els

    def _get_element(self, selector, max_timeout=0) -> BaseElement:
        def search_element():
            ret = self._send("Page.getElement", {"selector": selector})
            return create(ret.result, self.page_id, self.connection)

        self.logger.info("try to get element: %s" % selector)
        el = search_element()
        self.logger.info("find element success: %s" % str(el))
        return el

    def _element_is_exists(self, selector: str = None, xpath: str = None, **kwargs) -> bool:
        """
        description:
        param {*} self
        param {str} selector: css 选择器
        param {str} xpath: xpath
        param {object} kwargs: inner_text, text_contains, value ...
        return {bool}
        """
        if selector and xpath:
            self.logger.warning("selector and xpath both not None, use selector")
        if not (selector or xpath):
            raise RuntimeError("Must use either selector or xpath")
        try:
            if selector:
                return True if self.get_elements(selector, 0, index=0, **kwargs) else False
            else:
                return True if self.get_elements_by_xpath(xpath, 0, index=0, **kwargs) else False
        except Exception:
            return False

    # 正式支持xpath后，考虑复用get_element接口，通过检测selector类型来决定使用什么选择器
    # def _is_xpath(self, selector):
    #     """
    #     检测一个selector是否是xpath
    #     1. start with "/"
    #     2. start with "//"
    #     3. start with "./" or == "."
    #     4. translator.css_to_xpath(css_selector) fail
    #     """
    #     if selector.startswith("/") or selector.startswith("//") or selector.startswith("./"):
    #         return True
    #     if selector == ".":
    #         return True
    #     try:
    #         translator.css_to_xpath(selector)
    #         return False
    #     except SelectorError:
    #         return True
    #     return False

    def _get_element_by_xpath(self, xpath: str) -> Elements:
        """
        description: 通过xpath获取元素
        param {*} self
        param {str} xpath
        return {*} Elements or None
        """
        xpath = xpath[5:] if xpath.find("/page/") == 0 else xpath  # xpath不能以/page/开头（不存在的根节点）
        try:
            ret = self._send("Page.getElementByXpath", {"selector": xpath})
        except MiniAppError as e:
            if str(e) == "no such element":
                return None
            raise
        return create(ret.result, self.page_id, self.connection)

    def _get_elements_by_xpath(self, xpath: str, index=-1) -> typing.List[BaseElement]:
        """
        description: 通过xpath获取元素
        param {*} self
        param {str} xpath
        return {*} List[BaseElement]
        """
        xpath = xpath[5:] if xpath.find("/page/") == 0 else xpath  # xpath不能以/page/开头（不存在的根节点）
        if not self._can_i_use("Page.getElementsByXpath"):
            el = self._get_element_by_xpath(xpath)  # 降级使用Page.getElementByXpath
            return [el] if el else []
        try:
            ret = self._send("Page.getElementsByXpath", {"selector": xpath})
        except MiniAppError as e:
            if str(e) == "no such element":
                return []
            if (
                str(e).find("Page.getElementsByXpath unimplemented") > 0
            ):  # or str(e) in ["r is not iterable",]:
                self._unset_interface("Page.getElementsByXpath")
                el = self._get_element_by_xpath(xpath)  # 降级使用Page.getElementByXpath
                return [el] if el else []
            raise
        elements = []
        for el in ret.result.elements:
            elements.append(create(el, self.page_id, self.connection))
            if len(elements) == (index + 1):
                return elements
        return elements

    def _page_evaluate(self, app_function: str, args=None, sync=True):
        """
        在当前页面执行命令
        """
        if not args:
            args = []
        return self._send("Page.callFunction", {"functionDeclaration": app_function, "args": args}, sync=sync)
