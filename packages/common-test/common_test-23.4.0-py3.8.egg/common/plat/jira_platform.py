import json

from jsonpath import jsonpath

from common.common.api_driver import APIDriver
from common.data.handle_common import extractor, get_system_key, set_system_key
from common.common.constant import Constant
from requests.auth import HTTPBasicAuth


class JiraPlatForm(object):

    @classmethod
    def getJiraIssueInfo(self, jira_no):
        """
        通过Jira号获取jira信息
        :param jira_no:
        :return:
        """
        return APIDriver.http_request(url=f"{Constant.JIRA_URL}/rest/api/2/issue/{jira_no}",method='get',
                                        _auth=HTTPBasicAuth(get_system_key(Constant.JIRA_USERNAME),get_system_key(Constant.JIRA_PASSWORD)),
                                        _log=False)

    @classmethod
    def getReclyTestCase(self, testPlanIssueKey, cycleName):
        content = APIDriver.http_request(url=f"{Constant.JIRA_URL}/rest/synapse/latest/public/testPlan/{testPlanIssueKey}/cycle/{cycleName}/testRuns", method='get',
                                      _auth=HTTPBasicAuth(get_system_key(Constant.JIRA_USERNAME),
                                                          get_system_key(Constant.JIRA_PASSWORD)),
                                      _log=False)
        try:
            content = json.loads(content.content.decode('gbk'))
        except UnicodeDecodeError as e:
            content = json.loads(content.content.decode('utf-8'))
        return content


    @classmethod
    def updatecaseByrunId(self, caseList, caseName, result_temp):
        result = 4
        runid = 0
        if result_temp == 'passed':
            result=1
        if result_temp == 'failed':
            result=2
        xpath = "$..[?(@.summary =='name')].id".replace('name',caseName)
        try:
            runid=jsonpath(caseList, xpath)[0]
            APIDriver.http_request(
                url=f"{Constant.JIRA_URL}/rest/synapse/1.0/testRun/updateTestRunStatus?runId={runid}&status={result}",
                method='put',
                parametric_key='json',
                _auth=HTTPBasicAuth(get_system_key(Constant.JIRA_USERNAME),
                                    get_system_key(Constant.JIRA_PASSWORD)),
                _log = False
            )
            print("用例名称:" + caseName +" 用例运行ID： "+runid+"  结果:" + result_temp + "推送成功")
        except Exception as e:
            print("用例名称:" + caseName +" 用例运行ID： "+runid+"  结果:" + result_temp + "推送异常")




    @classmethod
    def setJiraFlowStatus(self, jira_key,flow_id):
        """
                触发工作流程
                :param jira_key: Jira_key
                :param flow_id: 流程ID
                :return:
                """
        return APIDriver.http_request(url=f"{Constant.JIRA_URL}/rest/api/2/issue/{jira_key}/transitions?expand=transitions.fields",
                                      method='post',
                                      parametric_key='json',
                                      data=json.loads('{"transition":{"id":"flow_id"}}'.replace('flow_id',flow_id)),
                                      _auth=HTTPBasicAuth(get_system_key(Constant.JIRA_USERNAME),
                                                          get_system_key(Constant.JIRA_PASSWORD))
                                      )

    @classmethod
    def setJiraComment(self, jira_key,comment):
        """
        添加Jira的备注
        :param jira_key:
        :param comment:
        :return:
        """
        return APIDriver.http_request(url=f"{Constant.JIRA_URL}/rest/api/2/issue/{jira_key}/comment",
                                      method='post',
                                      parametric_key='json',
                                      data=json.loads('{"body":"comment"}'.replace('comment',comment)),
                                      _auth=HTTPBasicAuth(get_system_key(Constant.JIRA_USERNAME),
                                                        get_system_key(Constant.JIRA_PASSWORD))
                                     )

    @classmethod
    def getJiraIssueSummer(self, jira_no):
        try:
            if jira_no.find("http://") != -1:
                jira_no = jira_no.split("/")[-1]
            _summary = extractor(self.getJiraIssueInfo(jira_no).json(), "$.fields.summary")
            if str(_summary).find("$") != -1:
                _summary = None
                _link = f'{Constant.JIRA_URL}/browse/{jira_no}'
            else:
                _link = f'{Constant.JIRA_URL}/browse/{jira_no}'
        except Exception as e:
            _summary = None
            _link = f'{Constant.JIRA_URL}/browse/{jira_no}'
        return  _summary, _link, jira_no



if __name__ == '__main__':
    lucky_number = [0, 1, 2, 3, 4, 5, 6,7]
    print(str(lucky_number[::2]))
    print(str(lucky_number[1::2]))







