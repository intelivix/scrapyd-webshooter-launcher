# -*- coding: utf-8 -*-

from twisted.internet import error
from scrapyd_mongodb import launcher
from scrapyd import runner
from scrapyd import launcher as scrapyd_launcher
from .http import report_webshooter


class ScrapyProcessProtocol(scrapyd_launcher.ScrapyProcessProtocol):

    def processEnded(self, status):  # noqa
        if isinstance(status.value, error.ProcessDone):
            self.log("Process finished: ")
        else:
            with runner.project_environment(self.project):
                try:
                    report_webshooter(
                        reason='ScrapydError: Process died',
                        error='ScrapydError: Process died',
                        state='cancelled')
                except Exception as e:
                    self.log(str(e))
            self.log("Process died: exitstatus=%r " % status.value.exitCode)
        self.deferred.callback(self)


class Launcher(launcher.Launcher):
    protocol_cls = ScrapyProcessProtocol
