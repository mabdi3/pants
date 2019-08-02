# Copyright 2019 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from unittest.mock import MagicMock

from pants.backend.python.targets.python_library import PythonLibrary
from pants_test.task_test_base import TaskTestBase

from pants.contrib.mypy.tasks.mypy_task import MypyTask


class MyPyTests(TaskTestBase):

  @classmethod
  def task_type(cls):
    return MypyTask

  def test_throws_no_warning_on_all_whitelisted_target_roots(self) -> None:
    t1 = self.make_target('t1', PythonLibrary, tags=['type_checked'])
    t2 = self.make_target('t2', PythonLibrary, tags=['type_checked'])
    task = self.create_task(self.context(target_roots=[t1, t2]))
    self.set_options(whitelist_tag_name='type_checked')
    task.execute()

  def test_throws_no_warning_on_some_whitelisted_target_roots_but_all_whitelisted_in_context(self) -> None:
    t1 = self.make_target('t1', PythonLibrary)
    t2 = self.make_target('t2', PythonLibrary, tags=['type_checked'])
    t3 = self.make_target('t3', PythonLibrary, tags=['type_checked'], dependencies=[t2])
    task = self.create_task(self.context(target_roots=[t1, t3]))
    self.set_options(whitelist_tag_name='type_checked')
    task.execute()

  def test_throws_warning_on_some_whitelisted_target_roots_but_all_whitelisted_in_context(self) -> None:
    t1 = self.make_target('t1', PythonLibrary)
    t2 = self.make_target('t2', PythonLibrary, tags=['something_else'])
    t3 = self.make_target('t3', PythonLibrary, tags=['type_checked'], dependencies=[t2])
    self.set_options(whitelist_tag_name='type_checked')
    task = self.create_task(self.context(target_roots=[t1, t3]))
    task._whitelist_warning = MagicMock()
    task.execute()
    task._whitelist_warning.assert_called()

  def test_throws_warning_on_all_whitelisted_target_roots_but_some_whitelisted_transitive_targets(self) -> None:
    t1 = self.make_target('t1', PythonLibrary, tags=['type_checked'])
    t2 = self.make_target('t2', PythonLibrary, tags=['something_else'])
    t3 = self.make_target('t3', PythonLibrary, tags=['type_checked'], dependencies=[t2])
    t4 = self.make_target('t4', PythonLibrary, tags=['type_checked'], dependencies=[t3])
    self.set_options(whitelist_tag_name='type_checked')
    task = self.create_task(self.context(target_roots=[t1, t4]))
    task._whitelist_warning = MagicMock()
    task.execute()
    task._whitelist_warning.assert_called()

  def test_throws_no_warning_if_no_whitelist_specified(self) -> None:
    t1 = self.make_target('t1', PythonLibrary)
    task = self.create_task(self.context(target_roots=[t1]))
    task._whitelist_warning = MagicMock()
    task.execute()
    task._whitelist_warning.assert_not_called()
