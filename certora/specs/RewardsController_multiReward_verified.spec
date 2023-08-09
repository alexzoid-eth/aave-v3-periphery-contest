import "RewardsController_base.spec";

using TransferStrategyMultiRewardHarness as transferStrategyMultiAddress;
using DummyERC20_rewardTokenB as rewardTokenBAddress;

////////////////// FUNCTIONS //////////////////////

function setupUser(env e, address user) {
    require user != 0;
    require user != currentContract;
    require user != ATokenAddress;
    require user != rewardTokenAddress;
    require user != transferStrategyMultiAddress;

    require ATokenAddress.scaledBalanceOf(e, user) <= ATokenAddress.scaledTotalSupply(e);
}

function setup(env e) {

    setupEssential(e);

    require getRewardsListLength() == 2;
    require getRewardToken(0) == rewardTokenAddress;
    require getRewardToken(1) == rewardTokenBAddress;
    require getTransferStrategy(rewardTokenAddress) == transferStrategyMultiAddress;
    require getTransferStrategy(rewardTokenBAddress) == transferStrategyMultiAddress;
    require getAssetsListLength() == 1;
    require getAssetToken(0) == ATokenAddress;
    require getAssetAvailableReward(ATokenAddress, 0) == rewardTokenAddress;
    require getAssetAvailableReward(ATokenAddress, 1) == rewardTokenBAddress;
    require getAssetAvailableRewardsCount(ATokenAddress) == 2;

    require ATokenAddress != rewardTokenBAddress;
    require ATokenAddress != rewardTokenAddress;
    require ATokenAddress != transferStrategyMultiAddress;
    require ATokenAddress != currentContract;
    require rewardTokenBAddress != rewardTokenAddress;
    require rewardTokenBAddress != transferStrategyMultiAddress;
    require rewardTokenBAddress != currentContract;
    require rewardTokenAddress != transferStrategyMultiAddress;
    require rewardTokenAddress != currentContract;
    require transferStrategyMultiAddress != currentContract;
}

///////////////// Properties ///////////////////////

// [participants 200-201] configureAssets() iteration
rule configureAssetsIteration(
    env e, 
    uint88 emissionPerSecond, 
    uint32 distributionEnd,
    address asset,
    address reward,
    address reward2,
    address transferStrategy,
    address rewardOracle
    ) {

    require e.msg.sender == getEmissionManager();
    require asset == ATokenAddress;
    require reward == rewardTokenAddress;
    require reward2 == rewardTokenBAddress;

    require isRewardEnabled(reward2) == false;
    require isRewardInList(reward2) == false;
    require getTransferStrategy(reward2) == 0;

    // revert when length reach uin256 limit 
    require getAssetsListLength() < 1000;
    require getRewardsListLength() < 1000;

    configureAssetsHarness2rewards(
        e, 
        emissionPerSecond, 
        distributionEnd,
        asset,
        reward,
        reward2,
        transferStrategy,
        rewardOracle
    );

    satisfy(isRewardEnabled(reward2) && isRewardInList(reward2) && transferStrategy == getTransferStrategy(reward2));
}

// [participants 202] Claim rewards should return amount of accrued rewards (2 rewards)
rule claimAllRewardsReturnClaimedAmountsIteration(env e, address[] assets, address user, address to) {

    setup(e);
    setupUser(e, to);

    require assets.length == 1;
    require assets[0] == ATokenAddress;
    require user == e.msg.sender;

    uint256 i;
    require i < 2;

    updateDataMultipleHarness(e, assets, user);

    uint256 rewards2 = getUserAccruedRewards(user, rewardTokenBAddress);

    address[] rewardsList;
    uint256[] claimedAmounts;
    rewardsList, claimedAmounts = claimAllRewards(e, assets, to);

    satisfy(rewardsList[i] == rewardTokenBAddress && claimedAmounts[i] == rewards2); 
}

// [participants 203] getRewardsByAsset() iteration
rule getRewardsByAssetIteration(env e, address asset) {

    setup(e);

    require asset == ATokenAddress;

    address reward2 = getAssetAvailableReward(asset, 1);
    
    address[] rewards = getRewardsByAsset(asset);

    satisfy(reward2 == rewards[1]);
}

// [participants 204] getAllUserRewards() iteration
rule getAllUserRewardsIntegrity(env e, address[] assets, address user) {

    setup(e);
    setupUser(e, user);

    require assets.length == 1;
    require assets[0] == ATokenAddress;

    uint256 i;
    require i < 2;

    address[] rewardsList; 
    uint256[] unclaimedAmounts;
    rewardsList, unclaimedAmounts = getAllUserRewards(e, assets, user);

    // One asset, two rewards
    satisfy(rewardsList[i] == rewardTokenBAddress);
}
