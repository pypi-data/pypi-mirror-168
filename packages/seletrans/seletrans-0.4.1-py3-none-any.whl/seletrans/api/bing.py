from .base import *
from ..constants.bing import *
from selenium.webdriver.support.ui import Select


class Bing(Base):
    URL = "https://www.bing.com/translator"
    DEFAULT_SOURCE = "auto-detect"
    DEFAULT_TARGET = "zh-Hans"
    SUPPORT_TTS = True

    def __init__(self, debug=False):
        super().__init__(debug)
        self.url_map = {
            ("ttranslate",): Handlers(self._get_simple_result, self._debug_save_json),
            ("tlookup",): Handlers(self._get_dict_result, self._debug_save_json),
        }

    def validate_lang(self):
        if self.source not in SOURCE_LANG:
            raise Exception(f"{self.source} is not a valid source language.")
        if self.target not in TARGET_LANG:
            raise Exception(f"{self.target} is not a valid target language.")
        self.has_dict_result = True

    def set_source_lang(self):
        select = Select(self.driver.find_element(By.ID, "tta_srcsl"))
        select.select_by_value(self.source)

    def set_target_lang(self):
        select = Select(self.driver.find_element(By.ID, "tta_tgtsl"))
        select.select_by_value(self.target)
        time.sleep(0.1)

    def _check_simple_response(self, log_json):
        requestId = log_json["params"]["requestId"]
        try:
            response_body = self.driver.execute_cdp_cmd(
                "Network.getResponseBody", {"requestId": requestId}
            )
            body = response_body["body"]
            if self._get_simple_result(body):
                resp = json.loads(body)
                translations = resp[0]["translations"]
                srcSentLen = translations[0]["sentLen"]["srcSentLen"][0]
                transSentLen = translations[0]["sentLen"]["transSentLen"][0]
                if srcSentLen == 1 or transSentLen == 1:
                    self.has_dict_result = True
                else:
                    self.has_dict_result = False
                return True
            else:
                return False
        except WebDriverException:
            return False
        except:
            return False

    def _check_dict_response(self, log_json):
        requestId = log_json["params"]["requestId"]
        try:
            response_body = self.driver.execute_cdp_cmd(
                "Network.getResponseBody", {"requestId": requestId}
            )
            body = response_body["body"]
            if self._get_dict_result(body):
                return True
            else:
                return False
        except WebDriverException:
            return False
        except:
            return False

    def wait_for_response(self, text, urls=None):
        self._wait_for_network_idle()
        if urls is None:
            urls = {
                "ttranslate": self._check_simple_response,
                "tlookup": self._check_dict_response,
            }
        st_time = time.time()
        while True:
            self._get_net_logs()
            flags = [False] * len(urls)
            for log in self.net_logs:
                log_json = json.loads(log["message"])["message"]
                if log_json["method"] != "Network.responseReceived":
                    continue
                url = log_json["params"]["response"]["url"]
                for idx, _url in enumerate(urls):
                    if self.check_url((_url,), url) and (
                        urls[_url] is None or urls[_url](log_json)
                    ):
                        flags[idx] = True
                if not self.has_dict_result:
                    flags[1] = True
                if all(flags):
                    break
            if all(flags):
                break
            time.sleep(0.1)
            if time.time() - st_time > self.TIMEOUT_MAX:
                raise Exception("Timeout for waiting response")

    def _get_simple_result(self, body):
        resp = json.loads(body)
        translations = resp[0]["translations"]
        self.result = [translations[0]["text"]]
        return True

    def _get_dict_result(self, body):
        resp = json.loads(body)
        dict_trans = {}
        translations = resp[0]["translations"]
        for trans in translations:
            tag = trans["posTag"]
            if tag not in dict_trans:
                dict_trans[tag] = []
            dict_trans[tag].append(trans["normalizedTarget"])
        dict_result = []
        for k, v in dict_trans.items():
            dict_result.append({"type": k, "means": v})
        self.dict_result = dict_result
        return True

    def _play_sound(self, check_interval=0.1):
        elem = self.wait_and_find_elem(By.XPATH, "//div[@id='tta_playiconsrc']")
        elem = elem.find_element(By.XPATH, "//div[@id='tta_playiconsrc']")
        parent = elem.find_element(By.XPATH, "..")
        tag = "tta_playfocus"
        elem.click()
        while True:
            _attr = parent.get_attribute("class")
            if tag in _attr:
                break
            time.sleep(check_interval)
        while True:
            _attr = parent.get_attribute("class")
            if tag not in _attr:
                break
            time.sleep(check_interval)


register("bing", Bing)
