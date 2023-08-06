from .base import *
from ..constants.baidu import *


class Baidu(Base):
    URL = "https://fanyi.baidu.com"
    SUPPORT_TTS = True

    def __init__(self, debug=False):
        super().__init__(debug)
        self.url_map = {
            ("v2transapi",): Handlers(
                [self._get_simple_result, self._get_dict_result], self._debug_save_json
            ),
        }
        self.skip_guide = False

    def preprocess(self):
        if not self.skip_guide:
            elem = self.driver.find_element(
                By.XPATH, "//span[@class='app-guide-close']"
            )
            elem.click()
            self.skip_guide = True

    def validate_lang(self):
        if self.source not in VALID_LANG:
            raise Exception(f"{self.source} is not a valid source language.")
        if self.target not in VALID_LANG[self.source]:
            raise Exception(f"{self.target} is not a valid target language.")

    def set_source_lang(self):
        lang_btn = self.driver.find_element(
            By.XPATH, "//a[@class='language-btn select-from-language']"
        )
        lang_btn.click()
        if self.source == "auto":
            elem = self.wait_and_find_elem(
                By.XPATH, "//li[contains(@class,'lang-item')]"
            )
            elem.click()
        else:
            elem = self.wait_and_find_elem(By.XPATH, "//input[@class='search-input']")
            elem.send_keys(self.source)
            elem = self.wait_and_find_elem(
                By.XPATH, "//div[@class='search-result-item']"
            )
            elem.click()
        textarea = self.get_textarea()
        if not self.try_click(textarea):
            lang_btn.click()

    def set_target_lang(self):
        lang_btn = self.driver.find_element(
            By.XPATH, "//a[@class='language-btn select-to-language']"
        )
        lang_btn.click()
        elem = self.wait_and_find_elem(By.XPATH, "//input[@class='search-input']")
        elem.send_keys(self.target)
        elem = self.wait_and_find_elem(By.XPATH, "//div[@class='search-result-item']")
        elem.click()
        textarea = self.get_textarea()
        if not self.try_click(textarea):
            lang_btn.click()

    def _get_simple_result(self, body):
        resp = json.loads(body)
        self.result = [resp["trans_result"]["data"][0]["dst"]]
        return True

    def _get_dict_result(self, body):
        resp = json.loads(body)
        if "dict_result" not in resp:
            self.dict_result = ""
            return False
        dict_result = []
        parts = resp["dict_result"]["simple_means"]["symbols"][0]["parts"]
        for part in parts:
            if "part" in part:
                wmeans = part["means"]
                wtype = part["part"]
                dict_result.append({"type": wtype, "means": wmeans})
            else:
                means = part["means"]
                for mean in means:
                    if "means" not in mean:
                        continue
                    wmeans = mean["means"]
                    wtype = mean["part"]
                    dict_result.append({"type": wtype, "means": wmeans})
        self.dict_result = dict_result
        return True

    def _play_sound(self, check_interval=0.1):
        elem = self.wait_and_find_elem(By.XPATH, "//div[@class='input-operate']")
        elem = elem.find_element(
            By.XPATH, "//a[@class='operate-btn op-sound data-hover-tip']"
        )
        class_attr = elem.get_attribute("class")
        if not self.try_click(elem):
            ActionChains(self.driver).send_keys_to_element(
                self.get_textarea(), Keys.ENTER
            ).perform()
        elem.click()
        while True:
            _attr = elem.get_attribute("class")
            if _attr == class_attr:
                break
            time.sleep(check_interval)
        time.sleep(check_interval)


register("baidu", Baidu)
