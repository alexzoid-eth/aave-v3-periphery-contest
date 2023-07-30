// SPDX-License-Identifier: BUSL-1.1
pragma solidity ^0.8.10;

import {RewardsController} from '../../contracts/rewards/RewardsController.sol';
import {RewardsDataTypes} from '../../contracts/rewards/libraries/RewardsDataTypes.sol';
import {ITransferStrategyBase} from '../../contracts/rewards/interfaces/ITransferStrategyBase.sol';
import {IEACAggregatorProxy} from '../../contracts/misc/interfaces/IEACAggregatorProxy.sol';
import {IScaledBalanceToken} from '@aave/core-v3/contracts/interfaces/IScaledBalanceToken.sol';

contract RewardsControllerHarness is RewardsController {

    mapping(uint256 => address) public _rewardsMap;

    constructor(address emissionManager) RewardsController(emissionManager) {}

    function getAssetRewardIndex(address asset, address reward) external view returns (uint256) {
        return _assets[asset].rewards[reward].index;
    }

    function getAssetRewardEmissionPerSecond(address asset, address reward) external view returns (uint256) {
        return _assets[asset].rewards[reward].emissionPerSecond;
    }

    function getAssetRewardLastUpdateTimestamp(address asset, address reward) external view returns (uint256) {
        return _assets[asset].rewards[reward].lastUpdateTimestamp;
    }

    function getAssetRewardDistributionEnd(address asset, address reward) external view returns (uint256) {
        return _assets[asset].rewards[reward].distributionEnd;
    }

    function getAssetRewardUserIndex(address user, address asset, address reward) external view returns (uint256) {
        return _assets[asset].rewards[reward].usersData[user].index;
    }

    function getAssetRewardUserAccrued(address user, address asset, address reward) external view returns (uint256) {
        return _assets[asset].rewards[reward].usersData[user].accrued;
    }

    function getRewardToken(uint256 i) external view returns (address) {
        return _rewardsList[i];
    }

    function getRewardsListLength() external view returns (uint256) {
        return _rewardsList.length;
    }

    function fillMapFromRewardsList(address[] memory rewardsList_) external {
        uint256 key = 0; 
        for (uint256 i = 0; i < rewardsList_.length; i++) {
            _rewardsMap[key] = rewardsList_[i];
            key++;
        }
    }

    function isRewardInList(address reward) external view returns (bool) {
        uint256 length = _rewardsList.length;
        for(uint i; i < length; ++i) {
            if(_rewardsList[i] == reward) {
                return true;
            }
        }

        return false;
    }

    function getAssetToken(uint256 i) external view returns (address) {
        return _assetsList[i];
    }

    function getAssetsListLength() external view returns (uint256) {
        return _assetsList.length;
    }

    function isAssetInList(address asset) external view returns (bool) {
        uint256 length = _assetsList.length;
        for(uint i; i < length; ++i) {
            if(_assetsList[i] == asset) {
                return true;
            }
        }

        return false;
    }

    function getAssetAvailableReward(address asset, uint128 i) external view returns (address) {
        return _assets[asset].availableRewards[i];
    }

    function getAssetAvailableRewardsCount(address asset) external view returns (uint128) {
        return _assets[asset].availableRewardsCount;
    }

    function isRewardEnabled(address reward) external view returns (bool) {
        return _isRewardEnabled[reward];
    }

    function isContract(address contractAddress) external view returns (bool) {
        return _isContract(contractAddress);
    }

    function getRevisionHarness() external pure returns (uint256) {
        return getRevision();
    }

    function getEmissionManagerHarness() external view returns (address) {
        return EMISSION_MANAGER;
    }

    function updateDataMultiple(address[] calldata assets, address user) external {
        _updateDataMultiple(user, _getUserAssetBalances(assets, user));
    }

    function updateData(address asset, address user, uint256 userBalance, uint256 totalSupply) external {
        _updateData(asset, user, userBalance, totalSupply);
    }

    function updateRewardData(address asset, address reward, uint256 totalSupply, uint256 assetUnit) external returns (uint256, bool) {
        RewardsDataTypes.RewardData storage rewardConfig = _assets[asset].rewards[reward];
        return _updateRewardData(rewardConfig, totalSupply, assetUnit);
    }

    function configureAssetsHarness(
        uint88 emissionPerSecond, 
        uint32 distributionEnd,
        address asset,
        address reward,
        address transferStrategy,
        address rewardOracle
    ) external {
        RewardsDataTypes.RewardsConfigInput[] memory config = new RewardsDataTypes.RewardsConfigInput[](1);
        config[0].emissionPerSecond = emissionPerSecond;
        config[0].distributionEnd = distributionEnd;
        config[0].asset = asset;
        config[0].reward = reward;
        config[0].transferStrategy = ITransferStrategyBase(transferStrategy);
        config[0].rewardOracle = IEACAggregatorProxy(rewardOracle);
        this.configureAssets(config);
    }

    function claimRewardsHarness(
        address[] calldata assets, 
        uint256 amount,
        address claimer,
        address user,
        address to,
        address reward
    ) external returns (uint256) {
        return _claimRewards(assets, amount, claimer, user, to, reward);
    }

    function claimAllRewardsHarness(
        address[] calldata assets,
        address claimer,
        address user,
        address to
    ) external returns (address[] memory rewardsList, uint256[] memory claimedAmounts) {
        return _claimAllRewards(assets, claimer, user, to);
    }
}