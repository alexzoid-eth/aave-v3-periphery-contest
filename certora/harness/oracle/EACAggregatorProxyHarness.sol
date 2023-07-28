// SPDX-License-Identifier: BUSL-1.1
pragma solidity ^0.8.10;

contract EACAggregatorProxyHarness {
    function latestAnswer() external pure returns (int256) {
        return 1;
    }
}