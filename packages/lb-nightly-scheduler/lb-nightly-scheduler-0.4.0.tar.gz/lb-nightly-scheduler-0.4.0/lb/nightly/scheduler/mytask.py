import datetime
from random import random
from time import sleep

import luigi


class AbortedSlotError(Exception):
    pass


class Checkout(luigi.Task):
    def output(self):
        return luigi.LocalTarget("checkout.txt")

    def run(self):
        print("running")
        sleep(5)
        if random() < 0.033:
            raise AbortedSlotError
        with self.output().open("w") as f:
            f.write(str(datetime.datetime.now()))


class Build(luigi.Task):
    def output(self):
        return luigi.LocalTarget("build.txt")

    def run(self):
        if random() < 0.033:
            raise AbortedSlotError
        sleep(5)
        with self.output().open("w") as f:
            f.write(str(datetime.datetime.now()))

    def requires(self):
        return Checkout()


class Test(luigi.Task):
    def output(self):
        return luigi.LocalTarget("test.txt")

    def run(self):
        if random() < 0.033:
            raise AbortedSlotError
        sleep(5)
        with self.output().open("w") as f:
            f.write(str(datetime.datetime.now()))

    def requires(self):
        return Checkout(), Build()


class Slot(luigi.WrapperTask):
    slot = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget("slot.txt")

    def requires(self):
        print(self.task_id)
        yield Checkout()
        yield Build()
        yield Test()

    def run(self):
        with self.output().open("w") as f:
            f.write(f"{self.slot} done at {str(datetime.datetime.now())}")


if __name__ == "__main__":
    import logging

    logger = logging.getLogger("luigi-interface")
    fh = logging.FileHandler("/tmp/luigi-interface")
    logger.addHandler(fh)

    summary = luigi.build(
        [Slot("myslot/1")], local_scheduler=True, detailed_summary=True
    )
    print(summary.summary_text)
