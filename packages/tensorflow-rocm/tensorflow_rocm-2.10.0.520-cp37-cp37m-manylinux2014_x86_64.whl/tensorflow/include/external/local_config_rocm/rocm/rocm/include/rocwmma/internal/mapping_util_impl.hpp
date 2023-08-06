/*******************************************************************************
 *
 * MIT License
 *
 * Copyright 2021-2022 Advanced Micro Devices, Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 *
 *******************************************************************************/
#ifndef ROCWMMA_MAPPING_UTIL_IMPL_HPP
#define ROCWMMA_MAPPING_UTIL_IMPL_HPP

#include <hip/hip_runtime.h>
#include <utility>

#include "constants.hpp"
#include "mapping_util.hpp"
#include "types.hpp"

namespace rocwmma
{

    namespace detail
    {
        // Workgroup configuration
        // According to our assumption, the major thread dimension is X, so
        // this determines our laneId.
        __device__ inline uint32_t laneId()
        {
            return threadIdx.x % AMDGCN_WAVE_SIZE;
        }

        __device__ constexpr inline Coord2d waveCount(Coord2d const& threadCount)
        {
            return std::make_pair(std::get<0>(threadCount) / AMDGCN_WAVE_SIZE, // ROW
                                  std::get<1>(threadCount)); // COL
        }

        __device__ constexpr inline Coord2d threadCount(Coord2d const& waveCount)
        {
            return std::make_pair(std::get<0>(waveCount) * AMDGCN_WAVE_SIZE, // ROW
                                  std::get<1>(waveCount)); // COL
        }

        /// WaveSpace

        __device__ inline uint32_t WaveSpace::localLaneId()
        {
            return laneId();
        }

        __device__ inline auto WaveSpace::localWaveCoord() -> WaveCoordT
        {
            return waveCount(std::make_pair(threadIdx.x, threadIdx.y));
        }

        __device__ inline auto WaveSpace::globalWaveCoord() -> WaveCoordT
        {
            return waveCount(std::make_pair(blockIdx.x * blockDim.x + threadIdx.x,
                                            blockIdx.y * blockDim.y + threadIdx.y));
        }

        __device__ inline auto WaveSpace::workgroupCoord() -> WorkgroupCoordT
        {
            return std::make_pair(blockIdx.x, blockIdx.y);
        }

        __device__ inline auto WaveSpace::workgroupDim() -> WorkgroupDimT
        {
            return waveCount(std::make_pair(blockDim.x, blockDim.y));
        }

        /// MatrixSpace
        template <uint32_t BlockHeight, uint32_t BlockWidth>
        __device__ inline auto
            MatrixSpace<BlockHeight, BlockWidth>::fromBlockCoord(BlockCoordT const& blockCoord)
                -> MatrixCoordT
        {
            // Map block to matrix coordinate space.
            return std::make_pair(std::get<0>(blockCoord) * BlockHeight, // ROW
                                  std::get<1>(blockCoord) * BlockWidth); // COL
        }

        /// DataSpace
        template <typename DataOrientation>
        __device__ inline uint32_t
            DataSpace<DataOrientation>::fromMatrixCoord(MatrixCoordT const& matrixCoord,
                                                        uint32_t            leadingDim)
        {
            enum : uint32_t
            {
                MajorIndex = std::is_same<DataOrientation, row_major>::value ? 0 : 1,
                MinorIndex = std::is_same<DataOrientation, row_major>::value ? 1 : 0
            };

            // 1D data element offset transform
            return std::get<MajorIndex>(matrixCoord) * leadingDim
                   + std::get<MinorIndex>(matrixCoord);
        }

    } // namespace detail

    template <uint32_t BlockHeight, uint32_t BlockWidth, typename DataT, typename DataLayout>
    __device__ inline uint32_t MappingUtil<BlockHeight, BlockWidth, DataT, DataLayout>::laneId()
    {
        return WaveSpace::localLaneId();
    }

    template <uint32_t BlockHeight, uint32_t BlockWidth, typename DataT, typename DataLayout>
    __device__ inline auto MappingUtil<BlockHeight, BlockWidth, DataT, DataLayout>::waveCoord()
        -> WaveCoordT
    {
        return WaveSpace::localWaveCoord();
    }

    template <uint32_t BlockHeight, uint32_t BlockWidth, typename DataT, typename DataLayout>
    __device__ inline auto MappingUtil<BlockHeight, BlockWidth, DataT, DataLayout>::blockCoord()
        -> BlockCoordT
    {
        // Map each wave 1 : 1 to global block grid
        return WaveSpace::globalWaveCoord();
    }

    template <uint32_t BlockHeight, uint32_t BlockWidth, typename DataT, typename DataLayout>
    __device__ inline auto MappingUtil<BlockHeight, BlockWidth, DataT, DataLayout>::matrixCoord()
        -> MatrixCoordT
    {
        return MatrixSpace::fromBlockCoord(blockCoord());
    }

    template <uint32_t BlockHeight, uint32_t BlockWidth, typename DataT, typename DataLayout>
    __device__ inline DataT const*
        MappingUtil<BlockHeight, BlockWidth, DataT, DataLayout>::dataCoord(DataT const* baseAddr,
                                                                           uint32_t     ldm)
    {
        return baseAddr + DataSpace::fromMatrixCoord(matrixCoord(), ldm);
    }

    template <uint32_t BlockHeight, uint32_t BlockWidth, typename DataT, typename DataLayout>
    __device__ inline DataT*
        MappingUtil<BlockHeight, BlockWidth, DataT, DataLayout>::dataCoord(DataT*   baseAddr,
                                                                           uint32_t ldm)
    {
        return baseAddr + DataSpace::fromMatrixCoord(matrixCoord(), ldm);
    }

    /// Current workgroup perspective

    template <uint32_t BlockHeight, uint32_t BlockWidth, typename DataT, typename DataLayout>
    __device__ inline auto MappingUtil<BlockHeight, BlockWidth, DataT, DataLayout>::workgroupDim()
        -> WorkgroupDimT
    {
        return WaveSpace::workgroupDim();
    }

    /// Coordinate override helpers

    template <uint32_t BlockHeight, uint32_t BlockWidth, typename DataT, typename DataLayout>
    __device__ inline auto
        MappingUtil<BlockHeight, BlockWidth, DataT, DataLayout>::blockCoordM(uint32_t m)
            -> BlockCoordT
    {
        auto coord         = blockCoord();
        std::get<0>(coord) = m;
        return coord;
    }

    template <uint32_t BlockHeight, uint32_t BlockWidth, typename DataT, typename DataLayout>
    __device__ inline auto
        MappingUtil<BlockHeight, BlockWidth, DataT, DataLayout>::blockCoordN(uint32_t n)
            -> BlockCoordT
    {
        auto coord         = blockCoord();
        std::get<1>(coord) = n;
        return coord;
    }

    template <uint32_t BlockHeight, uint32_t BlockWidth, typename DataT, typename DataLayout>
    __device__ inline auto
        MappingUtil<BlockHeight, BlockWidth, DataT, DataLayout>::matrixCoordM(uint32_t m)
            -> MatrixCoordT
    {
        auto coord         = matrixCoord();
        std::get<0>(coord) = m;
        return coord;
    }

    template <uint32_t BlockHeight, uint32_t BlockWidth, typename DataT, typename DataLayout>
    __device__ inline auto
        MappingUtil<BlockHeight, BlockWidth, DataT, DataLayout>::matrixCoordN(uint32_t n)
            -> MatrixCoordT
    {
        auto coord         = matrixCoord();
        std::get<1>(coord) = n;
        return coord;
    }

    /// Conversion helpers

    template <uint32_t BlockHeight, uint32_t BlockWidth, typename DataT, typename DataLayout>
    __device__ inline auto MappingUtil<BlockHeight, BlockWidth, DataT, DataLayout>::matrixCoord(
        BlockCoordT const& blockCoord) -> MatrixCoordT
    {
        return MatrixSpace::fromBlockCoord(std::forward<BlockCoordT const>(blockCoord));
    }

    template <uint32_t BlockHeight, uint32_t BlockWidth, typename DataT, typename DataLayout>
    __device__ inline uint32_t MappingUtil<BlockHeight, BlockWidth, DataT, DataLayout>::dataOffset(
        MatrixCoordT const& matrixCoord, uint32_t ldm)
    {
        return DataSpace::fromMatrixCoord(std::forward<MatrixCoordT const>(matrixCoord), ldm);
    }

    template <uint32_t BlockHeight, uint32_t BlockWidth, typename DataT, typename DataLayout>
    __device__ inline DataT const*
        MappingUtil<BlockHeight, BlockWidth, DataT, DataLayout>::dataCoord(
            DataT const* baseAddr, MatrixCoordT const& matrixCoord, uint32_t ldm)
    {
        return baseAddr
               + DataSpace::fromMatrixCoord(std::forward<MatrixCoordT const>(matrixCoord), ldm);
    }

    template <uint32_t BlockHeight, uint32_t BlockWidth, typename DataT, typename DataLayout>
    __device__ inline DataT* MappingUtil<BlockHeight, BlockWidth, DataT, DataLayout>::dataCoord(
        DataT* baseAddr, MatrixCoordT const& matrixCoord, uint32_t ldm)
    {
        return baseAddr
               + DataSpace::fromMatrixCoord(std::forward<MatrixCoordT const>(matrixCoord), ldm);
    }

} // namespace rocwmma

#endif // ROCWMMA_MAPPING_UTIL_IMPL_HPP
