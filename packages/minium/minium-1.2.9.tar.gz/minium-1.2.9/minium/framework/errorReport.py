import os.path
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "libs"))
sys.path.append(os.path.join(os.path.dirname(__file__)))
import json
import argparse
import tools.report_issue
import requests

work_root = os.path.abspath(".")

# robot_url = "http://in.qyapi.weixin.qq.com/cgi-bin/webhook/send?key=71881e81-7f49-49ce-8ac3-6e00b8508ba4"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-k",
        "--kao",
        dest="upload_failed_case",
        action="store_true",
        default=False,
        help="上传最近失败用例的日志和代码，截图",
    )
    parser.add_argument(
        "-i",
        dest="sync_image",
        action="store_true",
        default=False,
        help="上传最近失败用例的日志和代码，截图",
    )
    parser.add_argument("-m", "--msg", dest="msg", default=None)
    parser.add_argument("-t", "--token", dest="token", default=None)
    parser.add_argument("-a", "--assigns", dest="assigns", default=None)
    parser.add_argument("-id", "--proid", dest="proid", default=None)
    parser_args = parser.parse_args()
    upload_failed_case = parser_args.upload_failed_case
    msg = parser_args.msg
    token = parser_args.token
    assigns = parser_args.assigns
    proid = parser_args.proid

    if upload_failed_case:
        # config_path = os.path.join(work_root, ".git.json")
        last_failed_path = os.path.join(work_root, "outputs", "meta.json")
        # if not os.path.exists(config_path):
        #     print("%s not exists" % config_path)
        #     return
        if not os.path.exists(last_failed_path):
            print("%s not exists", last_failed_path)
        if not msg:
            msg = input("输入问题简述（回车表示无）: ")
        if not proid:
            proid = int(input("输入project ID："))
        else:
            proid = int(proid)
        if assigns:
            assigns = assigns.split(",")
        if not token:
            token = input("输入个人设置中的私人令牌：")
        # git_config = json.load(open(config_path))
        last_failed_cases = json.load(open(last_failed_path))
        # assigns = ["xxx"]
        if "task_datas" not in last_failed_cases:
            return
        if len(last_failed_cases["task_datas"]) < 1:
            return
        if "case_datas" not in last_failed_cases["task_datas"][0]:
            return
        for case_data_item in last_failed_cases["task_datas"][0]["case_datas"]:
            result_filepath = os.path.join(
                work_root,
                "outputs",
                case_data_item["relative"],
                case_data_item["filename"],
            )
            url = tools.report_issue.upload_issue(token, proid, result_filepath, msg, assigns)
            if url != "caseissuccess":
                print(url)
            #     session = requests.Session()
            #     session.trust_env = False
            #     r = session.post(
            #         robot_url,
            #         data=json.dumps(
            #             {
            #                 "msgtype": "text",
            #                 "mentioned_list": assigns,
            #                 "text": {
            #                     "content": f"{git_config['user']}提交了issue:\n{msg}\n请查看: {url}"
            #                 },
            #             }
            #         ),
            #     )
            #     print(r.text)
            #     r.raise_for_status()


if __name__ == "__main__":
    main()
