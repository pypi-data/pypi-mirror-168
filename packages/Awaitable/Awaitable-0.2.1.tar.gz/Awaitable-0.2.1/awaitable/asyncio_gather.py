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

import asyncio
import typing


class AsyncioGather(object):
    def __init__(self):
        self._tasks = []

    def __len__(self):
        """
        Returns the tasks count

        :return: number of tasks in the queue
        """
        return len(self._tasks)

    def add(self, coroutine: typing.Coroutine) -> int:
        """
        Add a new task to the queue

        :param coroutine: awaitable coroutine to add
        :return: tasks count
        """
        self._tasks.append(coroutine)
        return len(self._tasks)

    def count(self) -> int:
        """
        Returns the tasks count

        :return: number of tasks in the queue
        """
        return len(self)

    async def run(self) -> None:
        """
        Process asynchronously every task in the queue

        :return: None
        """
        await asyncio.gather(*self._tasks)
