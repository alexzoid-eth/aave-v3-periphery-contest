import "RewardsController_base.spec";

using DummyERC20_ATokenB as ATokenBAddress;

////////////////// FUNCTIONS //////////////////////

function setup(env e) {

    setupEssential(e);

    require getRewardsListLength() == 1;
    require getRewardToken(0) == rewardTokenAddress;
    require getTransferStrategy(rewardTokenAddress) == transferStrategyAddress;
    require getAssetsListLength() == 2;
    require getAssetToken(0) == ATokenAddress;
    require getAssetToken(1) == ATokenBAddress;
    require getAssetAvailableReward(ATokenAddress, 0) == rewardTokenAddress;
    require getAssetAvailableRewardsCount(ATokenAddress) == 1;
    require getAssetAvailableReward(ATokenBAddress, 0) == rewardTokenAddress;
    require getAssetAvailableRewardsCount(ATokenBAddress) == 1;

    require ATokenAddress != ATokenBAddress;
    require ATokenAddress != rewardTokenAddress;
    require ATokenAddress != transferStrategyAddress;
    require ATokenAddress != currentContract;
    require ATokenBAddress != rewardTokenAddress;
    require ATokenBAddress != transferStrategyAddress;
    require ATokenBAddress != currentContract;
    require rewardTokenAddress != transferStrategyAddress;
    require rewardTokenAddress != currentContract;
    require transferStrategyAddress != currentContract;
}

///////////////// Properties ///////////////////////

// [RewardsDistributor_181_multiAsset 18] Check iteration in getUserAccruedRewards() with several assets  
rule getUserAccruedRewardsIteration(env e, address user, address reward) {

    setup(e);

    require reward == rewardTokenAddress;

    uint256 accruedAsset0 = getAssetRewardUserAccrued(user, ATokenAddress, rewardTokenAddress);
    uint256 accruedAsset1 = getAssetRewardUserAccrued(user, ATokenBAddress, rewardTokenAddress);
    uint256 accruedAssetSum = require_uint256(accruedAsset0 + accruedAsset1);

    uint256 accruedRewards = getUserAccruedRewards(e, user, reward);

    satisfy(accruedAssetSum == accruedRewards);
}

// [RewardsDistributor_181_multiAsset 32-33] Check iteration in getAllUserRewards() with several assets  
rule getAllUserRewardsIteration(env e, address[] assets, address user) {

    setup(e);

    require assets.length == 2;
    require assets[0] == ATokenAddress;
    require assets[1] == ATokenBAddress;

    require ATokenAddress.scaledBalanceOf(e, user) == 0;
    require ATokenBAddress.scaledBalanceOf(e, user) == 0;

    uint256 accruedAsset0 = getAssetRewardUserAccrued(user, ATokenAddress, rewardTokenAddress);
    uint256 accruedAsset1 = getAssetRewardUserAccrued(user, ATokenBAddress, rewardTokenAddress);
    uint256 accruedAssetSum = require_uint256(accruedAsset0 + accruedAsset1);

    address[] rewardsList; 
    uint256[] unclaimedAmounts;
    rewardsList, unclaimedAmounts = getAllUserRewards(e, assets, user);

    satisfy(accruedAssetSum == unclaimedAmounts[0]);
}

// [RewardsDistributor_181_multiAsset 140] Check iteration in _getUserReward() with several assets  
rule getUserRewardIteration(env e, address[] assets, address user) {

    setup(e);

    require assets.length == 2;
    require assets[0] == ATokenAddress;
    require assets[1] == ATokenBAddress;

    require ATokenAddress.scaledBalanceOf(e, user) == 0;
    require ATokenBAddress.scaledBalanceOf(e, user) == 0;

    uint256 accruedAsset0 = getAssetRewardUserAccrued(user, ATokenAddress, rewardTokenAddress);
    uint256 accruedAsset1 = getAssetRewardUserAccrued(user, ATokenBAddress, rewardTokenAddress);
    uint256 accruedAssetSum = require_uint256(accruedAsset0 + accruedAsset1);

    uint256 rewards = getUserRewards(e, assets, user, rewardTokenAddress);

    satisfy(accruedAssetSum == rewards);
}

// [participants 198] Check iteration in _getUserAssetBalances() with several assets  
rule getUserAssetBalancesIteration(env e, address[] assets, address user) {

    setup(e);

    require assets.length == 2;
    require assets[0] == ATokenAddress;
    require assets[1] == ATokenBAddress;

    satisfy(getUserAssetBalancesHarnessSum(e, assets, user) == getUserAssetBalancesSum(e, assets, user));
}

// [participants 199] Iteration in _updateDataMultiple()
rule updateDataMultipleIteration(env e, address[] assets, address user) {

    setup(e);

    require assets.length == 2;
    require assets[0] == ATokenAddress;
    require assets[1] == ATokenBAddress;

    address asset; 
    uint256 userBalance; 
    uint256 totalSupply;
    asset, userBalance, totalSupply = getUserAssetBalanceHarness(e, assets, user, 0);

    address asset2; 
    uint256 userBalance2; 
    uint256 totalSupply2;
    asset2, userBalance2, totalSupply2 = getUserAssetBalanceHarness(e, assets, user, 1);

    storage initial = lastStorage;

    updateDataMultipleHarness(e, assets, user) at initial;
    storage storage1 = lastStorage;

    updateDataHarness(e, assets[0], user, userBalance, totalSupply) at initial;
    updateDataHarness(e, assets[1], user, userBalance2, totalSupply2);
    storage storage2 = lastStorage;

    // One call to _updateDataMultiple() could be the same as two calls to _updateData()
    satisfy(storage1[currentContract] == storage2[currentContract]);
}