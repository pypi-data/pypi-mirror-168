from .base import *
from ..constants.deepl import *
from bs4 import BeautifulSoup


class DeepL(Base):
    URL = "https://www.deepl.com/translator"
    SUPPORT_TTS = False

    def __init__(self, debug=False):
        super().__init__(debug)
        self.url_map = {
            ("jsonrpc",): Handlers(self._get_simple_result, self._debug_save_json),
            ("dict.deepl.com",): Handlers(
                self._get_dict_result, lambda x, y: self._debug_save_raw(x, y, "html")
            ),
        }

    def validate_lang(self):
        if self.source not in SOURCE_LANG:
            raise Exception(f"{self.source} is not a valid source language.")
        if self.target not in TARGET_LANG:
            raise Exception(f"{self.target} is not a valid target language.")

    def set_source_lang(self):
        elem = self.driver.find_element(
            By.XPATH, "//button[@dl-test='translator-source-lang-btn']"
        )
        elem.click()
        WebDriverWait(self.driver, self.TIMEOUT_MAX).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//button[@dl-test='translator-lang-option-auto']")
            )
        )
        elem = self.driver.find_element(
            By.XPATH, f"//button[@dl-test='translator-lang-option-{self.source}']"
        )
        elem.click()

    def set_target_lang(self):
        elem = self.driver.find_element(
            By.XPATH, "//button[@dl-test='translator-target-lang-btn']"
        )
        elem.click()
        WebDriverWait(self.driver, self.TIMEOUT_MAX).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//button[@dl-test='translator-lang-option-en-US']")
            )
        )
        elem = self.driver.find_element(
            By.XPATH, f"//button[@dl-test='translator-lang-option-{self.target}']"
        )
        elem.click()

    def _get_simple_result(self, body):
        resp = json.loads(body)
        if not resp["result"] or (
            resp["result"] and "translations" not in resp["result"]
        ):
            return False
        translations = resp["result"]["translations"][0]["beams"]
        self.result = [t["sentences"][0]["text"] for t in translations]
        return True

    def _get_dict_result(self, body):
        soup = BeautifulSoup(body, features="html.parser")
        wmeans = soup.select("a[class*='dictLink']")
        if len(wmeans) == 0:
            self.dict_result = ""
            return False
        wtypes = soup.select("span[class*='type']")
        words = zip([i.text for i in wmeans], [i.text for i in wtypes])
        dict_result = []
        for wmean, wtypes in words:
            if self.text in wmean:
                dict_result.append({"type": wtypes, "means": []})
                continue
            dict_result[-1]["means"].append(wmean)
        self.dict_result = dict_result
        return True

    def _play_sound(self, check_interval=0.1):
        elem = self.driver.find_element(
            By.XPATH, f"//button[@dl-test='translator-speaker-source']"
        )
        class_attr = elem.get_attribute("class")
        elem.click()
        while True:
            _attr = elem.get_attribute("class")
            if _attr == class_attr:
                break
            time.sleep(check_interval)
        time.sleep(check_interval)

    def _check_response(self, log_json):
        requestId = log_json["params"]["requestId"]
        try:
            # https://chromedevtools.github.io/devtools-protocol/
            post_data = self.driver.execute_cdp_cmd(
                "Network.getRequestPostData", {"requestId": requestId}
            )["postData"]
            post_data = json.loads(post_data)
            if post_data['params']['jobs'][0]['sentences'][0]['text'] != self.text:
                return False
            response_body = self.driver.execute_cdp_cmd(
                "Network.getResponseBody", {"requestId": requestId}
            )
            body = response_body["body"]
            if self._get_simple_result(body):
                return True
            else:
                return False
        except WebDriverException:
            return False
        except:
            return False

    def wait_for_response(self, text, urls=None):
        super().wait_for_response(
            text, {"dict.deepl.com": None, "jsonrpc": self._check_response}
        )


register("deepl", DeepL)
