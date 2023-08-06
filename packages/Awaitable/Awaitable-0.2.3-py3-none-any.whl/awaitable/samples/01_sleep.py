##
#     Project: Awaitable
# Description: A decorator to asynchronously execute synchronous functions
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2022 Fabio Castelli
#     License: GPL-3+
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
##

import logging
import time
import random
import typing

import awaitable


@awaitable.awaitable
def do_process(name: str,
               t: typing.Union[int, float]) -> None:
    """
    Await some time before returning
    :param name: task name
    :param t: time to sleep in seconds
    :return: None
    """
    logging.info(f'From {name}: awaiting {t} seconds...')
    starting_time = time.time()
    time.sleep(t)
    logging.info(f'From {name}: task complete '
                 f'in {time.time() - starting_time:.2f} seconds')


async def process(count: int) -> None:
    """
    Run some processes asynchronously
    Each process will await a random number of seconds

    :param count: number of tasks to process
    :return: None
    """
    logging.info(f'Running {count} processes')
    tasks = awaitable.AsyncioGather()
    for i in range(count):
        tasks.add(do_process(name=f'task_{tasks.count() + 1}',
                             t=random.randint(0, count)))
    logging.info(f'Starting to process {len(tasks)} tasks')
    await tasks.run()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s '
                               '%(levelname)-8s '
                               '%(filename)-25s '
                               'line: %(lineno)-5d '
                               '%(funcName)-30s '
                               '%(message)s')
    starting_time = time.time()
    awaitable.run_awaitable(func=process,
                            count=10)
    ending_time = time.time()
    logging.info(f'Operation completed in {ending_time - starting_time:.2f} '
                 'seconds')
