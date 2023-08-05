// Copyright 2021 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#ifndef _STIM_IO_READ_WRITE_PYBIND_H
#define _STIM_IO_READ_WRITE_PYBIND_H

#include <cstddef>
#include <pybind11/pybind11.h>

#include "stim/mem/simd_bit_table.h"

namespace stim_pybind {

stim::simd_bit_table<stim::MAX_BITWORD_WIDTH> numpy_array_to_transposed_simd_table(
    const pybind11::object &data, size_t expected_bits_per_shot, size_t *num_shots_out);

pybind11::object transposed_simd_bit_table_to_numpy(
    const stim::simd_bit_table<stim::MAX_BITWORD_WIDTH> &table, size_t bits_per_shot, size_t num_shots, bool bit_pack_result);

void pybind_read_write(pybind11::module &m);

}  // namespace stim_pybind

#endif