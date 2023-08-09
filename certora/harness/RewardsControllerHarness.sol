// SPDX-License-Identifier: BUSL-1.1
pragma solidity ^0.8.10;

import {RewardsController} from '../../contracts/rewards/RewardsController.sol';
import {RewardsDataTypes} from '../../contracts/rewards/libraries/RewardsDataTypes.sol';
import {ITransferStrategyBase} from '../../contracts/rewards/interfaces/ITransferStrategyBase.sol';
import {IEACAggregatorProxy} from '../../contracts/misc/interfaces/IEACAggregatorProxy.sol';
import {IScaledBalanceToken} from '@aave/core-v3/contracts/interfaces/IScaledBalanceToken.sol';

contract RewardsControllerHarness is RewardsController {

    constructor(address emissionManager) RewardsController(emissionManager) {}

    // View functions

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

    function isContractHarness(address contractAddress) external view returns (bool) {
        return _isContract(contractAddress);
    }

    function getRevisionHarness() external view returns (uint256) {
        return getRevision();
    }

    function getEmissionManagerHarness() external view returns (address) {
        return EMISSION_MANAGER;
    }

    function getUserAssetBalanceHarness(address[] calldata assets, address user, uint256 i) external view returns (address, uint256, uint256) {
        RewardsDataTypes.UserAssetBalance[] memory userAssetBalances = _getUserAssetBalances(assets, user);
        return (userAssetBalances[i].asset, userAssetBalances[i].userBalance, userAssetBalances[i].totalSupply);
    }

    function getAssetIndexHarness(address asset, address reward) external view returns (uint256, uint256) {
        RewardsDataTypes.RewardData storage rewardData = _assets[asset].rewards[reward];
        return
        _getAssetIndex(
            rewardData,
            IScaledBalanceToken(asset).scaledTotalSupply(),
            10**_assets[asset].decimals
        );
    }
 
    function getUserRewardsHarness(address[] calldata assets, address user, address reward) external view returns (uint256) {
        return _getUserReward(user, reward, _getUserAssetBalances(assets, user));
    }

    function getUserAssetBalancesHarnessSum(address[] calldata assets, address user) external view returns (uint256 sum) {
        RewardsDataTypes.UserAssetBalance[] memory userAssetBalances = _getUserAssetBalances(assets, user);
        for(uint256 i; i < userAssetBalances.length; i++) {
            sum += userAssetBalances[i].userBalance;
        }
    }

    function getUserAssetBalancesSum(address[] calldata assets, address user) external view returns (uint256 sum) {
        for (uint256 i; i < assets.length; ++i) {
            (uint256 balance, ) = IScaledBalanceToken(assets[i]).getScaledUserBalanceAndSupply(user);
            sum += balance;
        }
    }

    function getRewardsHarness(uint256 userBalance, uint256 reserveIndex, uint256 userIndex, uint256 assetUnit) external view returns (uint256) {
        return _getRewards(userBalance, reserveIndex, userIndex, assetUnit);
    }

    function getPendingRewardsHarness(address user, address reward, address asset, uint256 userBalance, uint256 totalSupply) external view returns (uint256) {
        RewardsDataTypes.UserAssetBalance memory userAssetBalance;
        userAssetBalance.asset = asset;
        userAssetBalance.userBalance = userBalance;
        userAssetBalance.totalSupply = totalSupply;
        return _getPendingRewards(user, reward, userAssetBalance);
    }

    // Non-view functions

    function updateDataMultipleHarness(address[] calldata assets, address user) external {
        _updateDataMultiple(user, _getUserAssetBalances(assets, user));
    }

    function updateDataHarness(address asset, address user, uint256 userBalance, uint256 totalSupply) external {
        _updateData(asset, user, userBalance, totalSupply);
    }

    function updateRewardDataHarness(address asset, address reward, uint256 totalSupply, uint256 assetUnit) external returns (uint256, bool) {
        RewardsDataTypes.RewardData storage rewardConfig = _assets[asset].rewards[reward];
        return _updateRewardData(rewardConfig, totalSupply, assetUnit);
    }

    function updateUserDataHarness(address asset, address reward, address user, uint256 userBalance, uint256 newAssetIndex, uint256 assetUnit) external returns (uint256, bool) {
        RewardsDataTypes.RewardData storage rewardConfig = _assets[asset].rewards[reward];
        return _updateUserData(rewardConfig, user, userBalance, newAssetIndex, assetUnit);
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

    function configureAssetsHarness2rewards(
        uint88 emissionPerSecond, 
        uint32 distributionEnd,
        address asset,
        address reward,
        address reward2,
        address transferStrategy,
        address rewardOracle
    ) external {
        RewardsDataTypes.RewardsConfigInput[] memory config = new RewardsDataTypes.RewardsConfigInput[](2);
        config[0].emissionPerSecond = emissionPerSecond;
        config[0].distributionEnd = distributionEnd;
        config[0].asset = asset;
        config[0].reward = reward;
        config[0].transferStrategy = ITransferStrategyBase(transferStrategy);
        config[0].rewardOracle = IEACAggregatorProxy(rewardOracle);
        config[1].emissionPerSecond = emissionPerSecond;
        config[1].distributionEnd = distributionEnd;
        config[1].asset = asset;
        config[1].reward = reward2;
        config[1].transferStrategy = ITransferStrategyBase(transferStrategy);
        config[1].rewardOracle = IEACAggregatorProxy(rewardOracle);
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

    function transferRewardsHarness(address to, address reward, uint256 amount) external {
        _transferRewards(to, reward, amount);
    }
}