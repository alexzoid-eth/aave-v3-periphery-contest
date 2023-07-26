import "methods/Methods_base.spec";

using DummyERC20_rewardToken as _DummyERC20_rewardToken;
using DummyERC20_rewardTokenB as _DummyERC20_rewardTokenB;
using TransferStrategyMultiRewardHarnessWithLinks as _TransferStrategyMultiRewardHarnessWithLinks;
using DummyERC20_AToken as _DummyERC20_AToken;

/////////////////// Methods ////////////////////////

methods {
    // Harness envfree
    function getRewardToken(uint256) external returns (address) envfree;
    function getRewardsListLength() external returns (uint256) envfree;
    function getAssetToken(uint256) external returns (address) envfree;
    function getAssetsListLength() external returns (uint256) envfree;
    function getAssetAvailableReward(address, uint128) external returns (address) envfree;
    function getAssetAvailableRewardsCount(address) external returns (uint128) envfree;

    // RewardsController envfree
    function getRewardOracle(address) external returns (address) envfree;
    function getTransferStrategy(address) external returns (address) envfree;
    function getAssetDecimals(address) external returns (uint8) envfree;
}

///////////////// Definitions ///////////////////////

definition CLAIM_REWARDS_FUNCTIONS(method f) returns bool = 
    f.selector == sig:claimRewards(address[], uint256, address, address).selector
    || f.selector == sig:claimRewardsOnBehalf(address[], uint256, address, address, address).selector
    || f.selector == sig:claimRewardsToSelf(address[], uint256, address).selector;

definition CLAIM_ALL_REWARDS_FUNCTIONS(method f) returns bool = 
    f.selector == sig:claimAllRewards(address[], address).selector
    || f.selector == sig:claimAllRewardsOnBehalf(address[], address, address).selector;

definition HANDLE_FUNCTION(method f) returns bool = 
    f.selector == sig:handleAction(address, uint256, uint256).selector;

///////////////// Functions ///////////////////////

// A cvl function for precondition assumptions 
function setup(env e) {
    require e.msg.sender != 0;
    require e.msg.sender != currentContract;
    require e.block.timestamp != 0;
    require getRewardsListLength() == 2;
    require getRewardToken(0) == _DummyERC20_rewardToken;
    require getRewardToken(1) == _DummyERC20_rewardTokenB;
    require getTransferStrategy(_DummyERC20_rewardToken) == _TransferStrategyMultiRewardHarnessWithLinks;
    require getAssetsListLength() == 1;
    require getAssetToken(0) == _DummyERC20_AToken;
    require getAssetAvailableReward(_DummyERC20_AToken, 0) == _DummyERC20_rewardToken;
    require getAssetAvailableReward(_DummyERC20_AToken, 1) == _DummyERC20_rewardTokenB;
    require getAssetAvailableRewardsCount(_DummyERC20_AToken) == 2;
}

// Ghost copy of _authorizedClaimers[]

ghost mapping(address => address) ghostAuthorizedClaimers {
    init_state axiom forall address x. ghostAuthorizedClaimers[x] == 0;
}

hook Sstore _authorizedClaimers[KEY address user] address claimer STORAGE {
    ghostAuthorizedClaimers[user] = claimer;
}

hook Sload address claimer _authorizedClaimers[KEY address user] STORAGE {
    require ghostAuthorizedClaimers[user] == claimer;
}

// Ghost copy of _transferStrategy[]

ghost mapping(address => address) ghostTransferStrategy {
    init_state axiom forall address x. ghostTransferStrategy[x] == 0;
}

hook Sstore _transferStrategy[KEY address reward] address strategy STORAGE {
    ghostAuthorizedClaimers[reward] = strategy;
}

hook Sload address reward _transferStrategy[KEY address strategy] STORAGE {
    require ghostAuthorizedClaimers[reward] == strategy;
}

// Ghost copy of _rewardOracle[]

ghost mapping(address => address) ghostRewardOracle {
    init_state axiom forall address x. ghostRewardOracle[x] == 0;
}

hook Sstore _rewardOracle[KEY address reward] address oracle STORAGE {
    ghostAuthorizedClaimers[reward] = oracle;
}

hook Sload address reward _rewardOracle[KEY address oracle] STORAGE {
    require ghostAuthorizedClaimers[reward] == oracle;
}

// Ghost copy of _isRewardEnabled[]

ghost mapping(address => bool) ghostIsRewardEnabled {
    init_state axiom forall address x. ghostIsRewardEnabled[x] == false;
}

hook Sstore _isRewardEnabled[KEY address reward] bool enabled STORAGE {
    ghostIsRewardEnabled[reward] = enabled;
}

hook Sload bool enabled _isRewardEnabled[KEY address reward] STORAGE {
    require ghostIsRewardEnabled[reward] == enabled;
}

// Ghost copy of _assets[].availableRewardsCount

ghost mapping (address => uint128) assetsAvailableRewardsCount {
    init_state axiom forall address asset. assetsAvailableRewardsCount[asset] == 0;
}

hook Sstore _assets[KEY address asset].availableRewardsCount uint128 val STORAGE {
    assetsAvailableRewardsCount[asset] = val;
}

// Ghost copy of _assets[].decimals

ghost mapping (address => uint8) assetsDecimals {
    init_state axiom forall address asset. assetsDecimals[asset] == 0;
}

hook Sstore _assets[KEY address asset].decimals uint8 val STORAGE {
    assetsDecimals[asset] = val;
}

///////////////// Properties ///////////////////////

// [bug1] Possibility of update user asset data
rule possibleToUserDataUpdate(env e, method f, calldataarg args, address user, address asset, address reward) 
    filtered { f -> CLAIM_REWARDS_FUNCTIONS(f) || CLAIM_ALL_REWARDS_FUNCTIONS(f) || HANDLE_FUNCTION(f) } {
    
    setup(e);

    require asset == _DummyERC20_AToken;
    require reward == _DummyERC20_rewardToken;

    uint256 indexBefore = getUserAssetIndex(user, asset, reward);

    f(e, args);

    uint256 indexAfter = getUserAssetIndex(user, asset, reward);

    satisfy(indexBefore != indexAfter);
}

// [bug2] Claiming rewards to zero address should revert
rule claimRewardsToZeroAddress(env e, address[] assets, uint256 amount, address to, address reward) {

    setup(e);

    claimRewards@withrevert(e, assets, amount, to, reward);

    assert to == 0 => lastReverted;
}

// [bug3] Possibility of returning array of claimed amounts while claiming all rewards 
rule claimAllRewardsReturnClaimedAmounts(env e, address[] assets, address to) {

    setup(e);

    address[] rewardsList;
    uint256[] claimedAmounts;
    rewardsList, claimedAmounts = claimAllRewards(e, assets, to);

    satisfy(claimedAmounts[0] > 0);
}

// [bug4] Claiming rewards on behalf from or to zero address should revert
rule claimRewardsOnBehalfFromOrToZeroAddress(env e, address[] assets, uint256 amount, address user, address to, address reward) {

    setup(e);

    claimRewardsOnBehalf@withrevert(e, assets, amount, user, to, reward);

    assert user == 0 || to == 0 => lastReverted;
}

// [bug5] Claiming all rewards to zero address should revert
rule claimAllRewardsToZeroAddress(env e, address[] assets, address to) {

    setup(e);

    claimAllRewards@withrevert(e, assets, to);

    assert to == 0 => lastReverted;
}

// [bug6] Claiming all rewards on behalf from or to zero address should revert
rule claimAllRewardsOnBehalfFromOrToZeroAddress(env e, address[] assets, address user, address to) {

    setup(e);

    claimAllRewardsOnBehalf@withrevert(e, assets, user, to);

    assert user == 0 || to == 0 => lastReverted;
}