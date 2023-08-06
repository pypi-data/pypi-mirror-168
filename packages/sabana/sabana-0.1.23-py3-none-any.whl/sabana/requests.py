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
from sabana.common import into_value, ty_from_value, ty_from_dtype
from numpy import zeros, uint32

zero = zeros((1,), dtype=uint32)


def execute_request():
    return proto.ExecuteRequest()


def alloc(name, size, mmio, offset):
    if not isinstance(name, str) or len(name) == 0:
        raise RuntimeError("name must be a string")
    if all(f is None for f in (mmio, offset)):
        i_mmio = ""
        i_offset = 0
    else:
        if any(f is None for f in (mmio, offset)):
            raise RuntimeError("if mmio or offset are given then both must be defined")
        if not isinstance(mmio, str) or len(mmio) <= 0:
            raise RuntimeError("mmio must be a non-empty string")
        else:
            i_mmio = mmio
        if not isinstance(offset, int) or offset < 0:
            raise RuntimeError("offset must be a positive integer")
        else:
            i_offset = offset

    if not isinstance(size, int) or size < 0:
        raise RuntimeError("size must be a positive integer")

    req = proto.Request()
    req.alloc.name = name
    req.alloc.size = size
    req.alloc.mmio_name = i_mmio
    req.alloc.mmio_offset = i_offset
    return req


def write(name=None, offset=None, value=None, src=None):
    if not isinstance(name, str):
        raise RuntimeError("name must be a string")
    if len(name) == 0:
        raise RuntimeError("name must be a non-empty string")
    req = proto.Request()
    req.write.name = name

    if src is None:
        if not isinstance(offset, int) or offset < 0:
            raise RuntimeError("offset must be a positive integer")
        if value is None:
            raise RuntimeError("need to provide value")
        req.write.offset = offset
        [v, l] = into_value(value)
        req.write.shape.extend(value.shape)
        req.write.values.CopyFrom(v)
        req.write.datatype = ty_from_value(value)
        req.write.shape.extend(value.shape)
        req.write.src = ""
    elif isinstance(src, str) and len(src) > 0:
        req.write.src = src
    else:
        raise RuntimeError("provide offset and value, or src if write is for dma")

    return req


def wait(name, offset, value, timeout):
    if not isinstance(name, str):
        raise RuntimeError("name must be a string")
    if len(name) == 0:
        raise RuntimeError("name must be a non-empty string")
    if not isinstance(offset, int) or offset < 0:
        raise RuntimeError("offset must be a positive integer")
    if not isinstance(timeout, int) or timeout < 0:
        raise RuntimeError("timeout must be a positive integer")
    req = proto.Request()
    req.wait.name = name
    req.wait.offset = offset
    [v, l] = into_value(value)
    req.wait.shape.extend(value.shape)
    req.wait.values.CopyFrom(v)
    req.wait.datatype = ty_from_value(value)
    req.wait.shape.extend(value.shape)
    req.wait.timeout = timeout
    return req


def read(name=None, offset=None, dtype=None, shape=None, dst=None):
    if not isinstance(name, str):
        raise RuntimeError("name must be a string")
    if len(name) == 0:
        raise RuntimeError("name must be a non-empty string")
    req = proto.Request()
    req.read.name = name

    if all(p is not None for p in (offset, dtype, shape)) and dst is None:
        if not isinstance(offset, int) or offset < 0:
            raise RuntimeError("offset must be a positive integer")
        if not isinstance(shape, tuple) and not isinstance(shape, list):
            raise RuntimeError("shape must be a tuple or list")

        req.read.offset = offset
        req.read.datatype = ty_from_dtype(dtype)
        req.read.shape.extend(shape)
    elif isinstance(dst, str) and len(dst) > 0:
        req.read.dst = dst

    else:
        raise RuntimeError("provide offset, dtype, and shape, or dst")

    return req


def dealloc(name):
    if not isinstance(name, str):
        raise RuntimeError("name must be a string")
    if len(name) == 0:
        raise RuntimeError("name must be a non-empty string")
    req = proto.Request()
    req.dealloc.name = name
    return req


def buffer_req(req):
    req.resource = proto.RESOURCE_BUFFER
    return req


def mmio_req(req):
    req.resource = proto.RESOURCE_MMIO
    return req


def dma_send_req(req):
    req.resource = proto.RESOURCE_DMA_SEND
    return req


def dma_recv_req(req):
    req.resource = proto.RESOURCE_DMA_RECV
    return req


def mmio_write(name, offset, value):
    return mmio_req(write(name, offset, value))


def mmio_read(name, offset, dtype, shape):
    return mmio_req(read(name, offset, dtype, shape))


def mmio_wait(name, offset, value, timeout):
    return mmio_req(wait(name, offset, value, timeout))


def mmio_alloc(name, size):
    return mmio_req(alloc(name, size, "0", 0))


def mmio_dealloc(name):
    return mmio_req(dealloc(name))


def buffer_write(name, offset, value):
    return buffer_req(write(name, offset, value))


def buffer_read(name, offset, dtype, shape):
    return buffer_req(read(name, offset, dtype, shape))


def buffer_wait(name, offset, value, timeout):
    return buffer_req(wait(name, offset, value, timeout))


def buffer_alloc(name, size, mmio, offset):
    return buffer_req(alloc(name, size, mmio, offset))


def buffer_dealloc(name):
    return buffer_req(dealloc(name))


def dma_send_write(name, src):
    return dma_send_req(write(name=name, src=src))


def dma_send_alloc(name):
    return dma_send_req(alloc(name, 0, "0", 0))


def dma_send_dealloc(name):
    return dma_send_req(dealloc(name))


def dma_send_wait(name, timeout):
    return dma_send_req(wait(name, 0, zero, timeout))


def dma_recv_read(name, dst):
    return dma_recv_req(read(name=name, dst=dst))


def dma_recv_alloc(name):
    return dma_recv_req(alloc(name, 0, "0", 0))


def dma_recv_dealloc(name):
    return dma_recv_req(dealloc(name))


def dma_recv_wait(name, timeout):
    return dma_recv_req(wait(name, 0, zero, timeout))


def is_write(req):
    return req.HasField("write")


def is_read(req):
    return req.HasField("read")


def is_wait(req):
    return req.HasField("wait")


def is_alloc(req):
    return req.HasField("alloc")


def is_dealloc(req):
    return req.HasField("dealloc")


def is_mmio(req):
    return req.resource == proto.RESOURCE_MMIO


def is_buffer(req):
    return req.resource == proto.RESOURCE_BUFFER


def is_dma_send(req):
    return req.resource == proto.RESOURCE_DMA_SEND


def is_dma_recv(req):
    return req.resource == proto.RESOURCE_DMA_RECV
