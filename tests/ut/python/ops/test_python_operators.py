# Copyright 2020 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
""" test control ops """
import functools
import numpy as np
import mindspore as ms
from mindspore import nn
from mindspore import Tensor
from mindspore import context
from mindspore.ops import operations as P
from mindspore.common import dtype as mstype
from ....mindspore_test_framework.mindspore_test import mindspore_test
from ....mindspore_test_framework.pipeline.forward.compile_forward \
    import pipeline_for_compile_forward_ge_graph_for_case_by_case_config

context.set_context(mode=context.GRAPH_MODE, save_graphs=True)

class ComparisonOpsNet(nn.Cell):
    def __init__(self):
        super(ComparisonOpsNet, self).__init__()
    def construct(self, x, y):
        ret = x <= y
        return ret

class LogicalNumberOpsNet(nn.Cell):
    def __init__(self):
        super(LogicalNumberOpsNet, self).__init__()
        self.cond = True
        self.one = 0
        self.zero = 0.0
    def construct(self, x, y):
        if self.cond and self.one or self.zero:
            return x + y
        return x - y

class LogicalTensorOpsNet(nn.Cell):
    def __init__(self):
        """"""
        super(LogicalTensorOpsNet, self).__init__()
        self.const_true = Tensor(True, dtype=mstype.bool_)
    def construct(self, x, y):
        ret = x and y and (y or self.const_true)
        return ret


test_case_ops = [
    ('CompareOpsNet', {
        'block': ComparisonOpsNet(),
        'desc_inputs': [Tensor(np.ones([6, 9, 10]), dtype=mstype.float32),
         Tensor(np.zeros([6, 9, 10]), dtype=mstype.float32)]}),
    ('LogicalNumberOps', {
        'block': LogicalNumberOpsNet(),
        'desc_inputs': [Tensor(np.ones([6, 9, 10]), dtype=mstype.float32),
         Tensor(np.zeros([6, 9, 10]), dtype=mstype.float32)]}),
    ('LogicalTensorOps', {
        'block': LogicalTensorOpsNet(),
        'desc_inputs': [Tensor(np.ones([6, 9, 10]).astype(np.bool_), dtype=mstype.bool_),
         Tensor(np.zeros([6, 9, 10]).astype(np.bool_), dtype=mstype.bool_)]}),
]

test_case_lists = [test_case_ops]
test_exec_case = functools.reduce(lambda x, y: x + y, test_case_lists)

@mindspore_test(pipeline_for_compile_forward_ge_graph_for_case_by_case_config)
def test_compile():
    return test_exec_case