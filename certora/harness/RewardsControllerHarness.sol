// SPDX-License-Identifier: BUSL-1.1
pragma solidity ^0.8.10;

import {RewardsController} from '../../contracts/rewards/RewardsController.sol';

contract RewardsControllerHarness is RewardsController {

    constructor(address emissionManager) RewardsController(emissionManager) {}

    function getAssetRewardIndex(address asset, address reward) external view returns (uint256) {
        return _assets[asset].rewards[reward].index;
    }

    function getRewardToken(uint256 i) external view returns (address) {
        return _rewardsList[i];
    }

    function getRewardsListLength() external view returns (uint256) {
        return _rewardsList.length;
    }

    function getAssetToken(uint256 i) external view returns (address) {
        return _assetsList[i];
    }

    function getAssetsListLength() external view returns (uint256) {
        return _assetsList.length;
    }
}