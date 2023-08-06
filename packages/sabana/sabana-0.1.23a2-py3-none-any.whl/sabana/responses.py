# Copyright 2022 Sabana Technologies, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sabana.sabana_pb2 as proto
from sabana.common import into_value
from sabana.common import ty_from_value
from numpy import zeros, ndarray, uint64

zero = zeros((1,), dtype=uint64)


def execute_response():
    return proto.ExecuteResponse()


def invalid():
    response = proto.Response()
    response.resource = proto.RESOURCE_INVALID
    return response


def write(name):
    response = proto.Response()
    response.write.name = name
    return response


def read(name, value):
    response = proto.Response()
    response.read.name = name
    [v, l] = into_value(value)
    response.read.shape.extend(value.shape)
    response.read.values.CopyFrom(v)
    response.read.datatype = ty_from_value(value)
    return response


def wait(name):
    response = proto.Response()
    response.wait.name = name
    return response


def alloc(name, device_address):
    if (not isinstance(device_address, ndarray)) or (
        device_address.dtype.type != uint64
    ):
        raise RuntimeError("device_address must be a numpy ndarray of uint64")
    response = proto.Response()
    response.alloc.name = name
    response.alloc.device_address = device_address[0]
    return response


def dealloc(name):
    response = proto.Response()
    response.dealloc.name = name
    return response


def buffer_res(res):
    res.resource = proto.RESOURCE_BUFFER
    return res


def mmio_res(res):
    res.resource = proto.RESOURCE_MMIO
    return res


def dma_send_res(res):
    res.resource = proto.RESOURCE_DMA_SEND
    return res


def dma_recv_res(res):
    res.resource = proto.RESOURCE_DMA_RECV
    return res


def mmio_write(name):
    return mmio_res(write(name))


def mmio_read(name, value):
    return mmio_res(read(name, value))


def mmio_wait(name):
    return mmio_res(wait(name))


def mmio_alloc(name):
    return mmio_res(alloc(name, zero))


def mmio_dealloc(name):
    return mmio_res(dealloc(name))


def buffer_write(name):
    return buffer_res(write(name))


def buffer_read(name, value):
    return buffer_res(read(name, value))


def buffer_wait(name):
    return buffer_res(wait(name))


def buffer_alloc(name, device_address):
    return buffer_res(alloc(name, device_address))


def buffer_dealloc(name):
    return buffer_res(dealloc(name))


def dma_send_write(name):
    return dma_send_res(write(name))


def dma_recv_read(name, value):
    return dma_recv_res(read(name, value))


def dma_send_wait(name):
    return dma_send_res(wait(name))


def dma_send_alloc(name):
    return dma_send_res(alloc(name, zero))


def dma_send_dealloc(name):
    return dma_send_res(dealloc(name))


def dma_recv_wait(name):
    return dma_recv_res(wait(name))


def dma_recv_alloc(name):
    return dma_recv_res(alloc(name, zero))


def dma_recv_dealloc(name):
    return dma_recv_res(dealloc(name))


def is_write(res):
    return res.HasField("write")


def is_read(res):
    return res.HasField("read")


def is_wait(res):
    return res.HasField("wait")


def is_alloc(res):
    return res.HasField("alloc")


def is_dealloc(res):
    return res.HasField("dealloc")


def outcome_invalid(res, info=""):
    res.outcome.outcome_type = proto.OUTCOME_INVALID
    res.outcome.info = info
    return res


def outcome_ok(res, info=""):
    res.outcome.outcome_type = proto.OUTCOME_OK
    res.outcome.info = info
    return res


def outcome_error(res, info=""):
    res.outcome.outcome_type = proto.OUTCOME_ERROR
    res.outcome.info = info
    return res


def is_invalid(res):
    return res.outcome.outcome_type == proto.OUTCOME_INVALID


def is_ok(res):
    return res.outcome.outcome_type == proto.OUTCOME_OK


def is_error(res):
    return res.outcome.outcome_type == proto.OUTCOME_ERROR


def is_mmio(res):
    return res.resource == proto.RESOURCE_MMIO


def is_buffer(res):
    return res.resource == proto.RESOURCE_BUFFER


def is_dma_send(res):
    return res.resource == proto.RESOURCE_DMA_SEND


def is_dma_recv(res):
    return res.resource == proto.RESOURCE_DMA_RECV


def is_invalid_resource(res):
    return res.resource == proto.RESOURCE_INVALID
