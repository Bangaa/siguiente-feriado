from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

def wait(max_wait):
    """Decorator. Wait for a helper to be executed succesfully for 'max_wait'
    seconds top. If the helper keep raissing a exception past the 10 seconds
    mark, said exception is raissed and the test should be considered failed.

    Args:
        fn: helper function to be waited for
        max_wait: wait at most this amount of time
    """
    def wait_for_success(fn):
        def mod_helper(*args, **kwargs):
            start_time = time.time()
            while True:
                try:
                    return fn(*args, **kwargs)
                except (AssertionError, WebDriverException) as e:
                    if time.time() - start_time > max_wait:
                        raise e
                    else:
                        time.sleep(0.2)
        return mod_helper
    return wait_for_success

class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)

    def tearDown(self):
        if self._test_has_failed():
            if not os.path.exists(SCREEN_DUMP_LOCATION):
                os.makedirs(SCREEN_DUMP_LOCATION)
            for ix, handle in enumerate(self.browser.window_handles):
                self._windowid = ix
                self.browser.switch_to_window(handle)
                self.take_screenshot()
                self.dump_html()
        self.browser.quit()
        super().tearDown()

    def _test_has_failed(self):
        return any(error for (method, error) in self._outcome.errors)

    def take_screenshot(self):
        filename = self._get_filename() + '.png'
        print('screenshotting to', filename)
        self.browser.get_screenshot_as_file(filename)

    def dump_html(self):
        filename = self._get_filename() + '.html'
        print('dumping page HTML to', filename)
        with open(filename, 'w') as f:
            f.write(self.browser.page_source)

    def _get_filename(self):
        timestamp = datetime.now().isoformat().replace(':', '.')[:19]
        m = re.match(r'(?P<module>.*)?\.(?P<testname>\w+)$', self.id())
        return '{folder}/{method}-{module}-window{windowid}'.format(
            folder=SCREEN_DUMP_LOCATION,
            method=m.group('testname'),
            module=m.group('module'),
            windowid=self._windowid
        )