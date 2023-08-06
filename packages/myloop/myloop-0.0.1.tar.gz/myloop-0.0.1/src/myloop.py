import subprocess
import time

import click
import schedule


@click.command()
@click.option("--every", help="How often to iterate. ex., 5s, 1h / 1m / 1s / 1ms")
@click.option("--count-by", type=click.INT, help="Used for iterating over a range of numbers. ex., 1 to 10")
@click.option("--command", help="What should I execute")
def myloop(every, command, count_by):
    if every:
        interval, frequency = parse_time(every)
        if frequency == "s":
            schedule.every(interval).seconds.do(job_func=job, cmd=command)
        elif frequency == "m":
            schedule.every(interval).minutes.do(job_func=job, cmd=command)
        elif frequency == "h":
            schedule.every(interval).hours.do(job_func=job, cmd=command)
        elif frequency == "d":
            schedule.every(interval).days.do(job_func=job, cmd=command)
        else:
            raise TypeError("Frequency should be one of: s / m / h / d")
        while True:
            schedule.run_pending()
            time.sleep(interval)
    if count_by:
        for count in range(0, count_by):
            time.sleep(1)
            job(command)


def job(cmd):
    return subprocess.check_call(cmd, shell=True)


def parse_time(every: str):
    if every[0].isdecimal():
        return int(every[0]), every[1]
    return None


if __name__ == "__main__":
    myloop()
