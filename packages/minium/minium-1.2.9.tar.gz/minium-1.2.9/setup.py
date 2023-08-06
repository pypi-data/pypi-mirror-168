#!/usr/bin/env python3
import sys

__version__ = "1.2.9"

from setuptools import setup, find_packages

# We do not support Python <3.8
if sys.version_info < (3, 8):
    print(
        "Unfortunately, your python version is not supported!\n"
        "Please upgrade at least to Python 3.8!",
        file=sys.stderr,
    )
    sys.exit(1)

install_requires = [
    "ddt",
    "pyyaml",
    "websocket_client",
    "requests",
    # "facebook-wda",
    # "matplotlib",
    "future",
    "tidevice==0.4.10",
    "pyee",
    # "cssselect",
    # "case-repair-sdk==1.0.3",
]

entry_points = {
    "console_scripts": [
        "minitest=minium.framework.loader:main",
        "miniruntest=minium.framework.loader:main",
        "minireport=minium.framework.report:main",
        "miniErrorReport=minium.framework.errorReport:main",
        "mininative=minium.native.nativeapp:start_server",
    ]
}


config_path = "miniprogram/base_driver/version.json"
package_data = {
    "minium": [
        config_path,
        "framework/dist/*",
        "framework/dist/*/*",
        "native/wx_native/*/*",
        "native/qq_native/*/*",
        "native/*/*",
        "native/*/*/*/*",
        "native/*/*/*/*/*",
        "native/*/*/*/*/*/*",
        "utils/js/min/*",
        "utils/js/es5/*",
    ]
}

exclude_package_data = {"": ["*pyc", "readme.md", "build.py"]}

if __name__ == "__main__":
    setup(
        name="minium",
        version=__version__,
        license="MIT",
        url="https://minitest.weixin.qq.com/#/",
        packages=find_packages(),
        description="Minium is the best MiniProgram auto test framework.",
        long_description="""See the [document](https://minitest.weixin.qq.com/#/minium/Python/readme) for details""",
        package_data=package_data,
        exclude_package_data=exclude_package_data,
        entry_points=entry_points,
        install_requires=install_requires,
        setup_requires=["setuptools"],
        python_requires=">=3.8",
        author="WeChat-Test",
        author_email="minitest@tencent.com",
        platforms=["MacOS", "Windows"],
        keywords=["minium", "WeApp", "MiniProgram", "Automation", "Test"],
    )
