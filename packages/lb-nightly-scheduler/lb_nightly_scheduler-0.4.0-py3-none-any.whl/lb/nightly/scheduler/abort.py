import asyncio
import random


async def _run_slot(slot):
    cmd = [
        "luigi",
        "--workers=300",
        "--module=lb.nightly.scheduler.mytask",
        "Slot",
        "--slot",
        slot,
    ]
    luigi_call = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    try:
        output = await asyncio.gather(
            luigi_call.communicate(),
        )
    except (asyncio.TimeoutError, asyncio.CancelledError):
        luigi_call.kill()
        raise

    print(luigi_call.returncode)
    print(output[0][0].decode())
    print(output[0][1].decode())


async def _abort_slot(slot=None):
    while True:
        await asyncio.sleep(1)
        magic = random.random()
        print(f"{magic=}")
        if magic > 0.9:
            return True
        # slot = get(slot)
        # if "aborted" in db[slot.flavour, slot.name, slot.build_id]:
        #     return True


async def main(slot):
    task = asyncio.create_task(_run_slot(slot))
    abort = asyncio.create_task(_abort_slot(slot))
    done, pending = await asyncio.wait(
        [task, abort],
        return_when=asyncio.FIRST_COMPLETED,
        timeout=60 * 60 * 24,
    )
    for _task in done:
        if _task is task:
            print("task run_slot done")
            abort.cancel()
            try:
                await abort
            except asyncio.CancelledError:
                print("abort cancelled")
        elif _task is abort:
            print("abort done")
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                print("task run_slot cancelled")
    else:
        print(f"Slot {slot} is building for more than 24h. Aborting.")
        return


def start_slot(slot):
    return asyncio.run(main(slot))


if __name__ == "__main__":
    start_slot(f"testing/my-slot/{random.randint(0,1000)}")
