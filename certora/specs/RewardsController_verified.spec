import "methods/Methods_base.spec";

using DummyERC20_rewardToken as _DummyERC20_rewardToken;
using TransferStrategyHarness as _TransferStrategyHarness;
using DummyERC20_AToken as _DummyERC20_AToken;

/////////////////// Methods ////////////////////////

methods {
    // AToken functions    
    function _.scaledBalanceOf(address) external => DISPATCHER(true);

    // RewardsControllerHarness envfree
    function getAssetRewardIndex(address, address) external returns (uint256) envfree;
    function getAssetRewardEmissionPerSecond(address, address) external returns (uint256) envfree;
    function getAssetRewardLastUpdateTimestamp(address, address) external returns (uint256) envfree;
    function getAssetRewardDistributionEnd(address, address) external returns (uint256) envfree;
    function getRewardToken(uint256) external returns (address) envfree;
    function getRewardsListLength() external returns (uint256) envfree;
    function getAssetToken(uint256) external returns (address) envfree;
    function getAssetsListLength() external returns (uint256) envfree;
    function getAssetAvailableReward(address, uint128) external returns (address) envfree;
    function getAssetAvailableRewardsCount(address) external returns (uint128) envfree;

    // RewardsControllerHarness
    function updateDataMultiple(address) external;

    // RewardsController envfree
    function getRewardOracle(address) external returns (address) envfree;
    function getTransferStrategy(address) external returns (address) envfree;
    function getAssetDecimals(address) external returns (uint8) envfree;
    function getEmissionManager() external returns (address) envfree;
}

///////////////// Definitions ///////////////////////

definition CLAIM_REWARDS(method f) returns bool = 
    f.selector == sig:claimRewards(address[], uint256, address, address).selector;

definition CLAIM_REWARDS_FUNCTIONS(method f) returns bool = 
    CLAIM_REWARDS(f)
    || f.selector == sig:claimRewardsOnBehalf(address[], uint256, address, address, address).selector
    || f.selector == sig:claimRewardsToSelf(address[], uint256, address).selector;

definition CLAIM_ALL_REWARDS(method f) returns bool = 
    f.selector == sig:claimAllRewards(address[], address).selector;

definition CLAIM_ALL_REWARDS_FUNCTIONS(method f) returns bool = 
    CLAIM_ALL_REWARDS(f) || f.selector == sig:claimAllRewardsOnBehalf(address[], address, address).selector;

definition HANDLE_FUNCTION(method f) returns bool = 
    f.selector == sig:handleAction(address, uint256, uint256).selector;

definition ONLY_AUTHORIZED_CLAIMERS_FUNCTIONS(method f) returns bool = 
    f.selector == sig:claimRewardsOnBehalf(address[], uint256, address, address, address).selector
    || f.selector == sig:claimAllRewardsOnBehalf(address[], address, address).selector;

definition ONLY_EMISSION_MANAGER_FUNCTIONS(method f) returns bool = 
    f.selector == sig:configureAssets(RewardsDataTypes.RewardsConfigInput[]).selector
    || f.selector == sig:setTransferStrategy(address, address).selector
    || f.selector == sig:setRewardOracle(address, address).selector
    || f.selector == sig:setClaimer(address, address).selector;

///////////////// Functions ///////////////////////

// CVL functions for precondition assumptions 

function setupUser(env e, address user) {
    require user != 0;
    require user != currentContract;
    require user != _DummyERC20_AToken;
    require user != _DummyERC20_rewardToken;
    require user != _TransferStrategyHarness;

    require _DummyERC20_AToken.scaledBalanceOf(e, user) <= _DummyERC20_AToken.scaledTotalSupply(e);
}

function setup(env e) {

    setupUser(e, e.msg.sender);

    require e.block.timestamp != 0;
    require getRewardsListLength() == 1;
    require getRewardToken(0) == _DummyERC20_rewardToken;
    require getTransferStrategy(_DummyERC20_rewardToken) == _TransferStrategyHarness;
    require getAssetsListLength() == 1;
    require getAssetToken(0) == _DummyERC20_AToken;
    require getAssetAvailableReward(_DummyERC20_AToken, 0) == _DummyERC20_rewardToken;
    require getAssetAvailableRewardsCount(_DummyERC20_AToken) == 1;
    
    require getAssetDecimals(_DummyERC20_AToken) > 0;
    require getAssetDecimals(_DummyERC20_AToken) < 77;
    require _DummyERC20_AToken.scaledTotalSupply(e) >= require_uint256(1000 * 10 ^ getAssetDecimals(_DummyERC20_AToken));

    require _DummyERC20_rewardToken != _TransferStrategyHarness;
    require _DummyERC20_rewardToken != _DummyERC20_AToken;
    require _DummyERC20_rewardToken != currentContract;
    require _DummyERC20_AToken != currentContract;
    require _DummyERC20_AToken != _TransferStrategyHarness;
    require _TransferStrategyHarness != currentContract;
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

// [bug1] Possibility of update reward index when executing claim rewards
rule claimAllRewardsPossibleUpdateRewardIndex(method f, env e, address[] assets, address to, address reward) 
    filtered { f -> CLAIM_REWARDS(f) || CLAIM_ALL_REWARDS(f) } {

    setup(e);
    setupUser(e, to);

    require assets.length == 1;
    require assets[0] == _DummyERC20_AToken;
    require reward == _DummyERC20_rewardToken;

    // Precondition assumptions in _getAssetIndex()
    require getAssetRewardEmissionPerSecond(assets[0], reward) != 0;
    require getAssetRewardLastUpdateTimestamp(assets[0], reward) != e.block.timestamp;
    require getAssetRewardLastUpdateTimestamp(assets[0], reward) < getAssetRewardDistributionEnd(assets[0], reward);

    uint256 indexBefore = getAssetRewardIndex(assets[0], reward);

    if(CLAIM_REWARDS(f)) {
        uint256 amount;
        claimRewards(e, assets, amount, to, reward);
    } else if (CLAIM_ALL_REWARDS(f)) {
        claimAllRewards(e, assets, to);
    }

    uint256 indexAfter = getAssetRewardIndex(assets[0], reward);

    satisfy(indexBefore != indexAfter);
}

// [bug2] Claiming rewards to zero address should revert
rule claimRewardsToZeroAddress(env e, address[] assets, uint256 amount, address to, address reward) {

    setup(e);
    setupUser(e, to);

    claimRewards@withrevert(e, assets, amount, to, reward);

    assert to == 0 => lastReverted;
}

// TODO: long working time
// [bug3] Claim rewards should return amount of accrued rewards
rule claimAllRewardsReturnClaimedAmounts(env e, address[] assets, address user, address to) {

    setup(e);
    setupUser(e, to);

    require assets.length == 1;
    require assets[0] == _DummyERC20_AToken;
    require user == e.msg.sender;

    updateDataMultiple(e, assets, user);

    uint256 rewards = getUserAccruedRewards(user, _DummyERC20_rewardToken);

    address[] rewardsList;
    uint256[] claimedAmounts;
    rewardsList, claimedAmounts = claimAllRewards(e, assets, to);

    assert claimedAmounts[0] == rewards;
}

// [bug4] Claiming rewards on behalf from or to zero address should revert
rule claimRewardsOnBehalfFromOrToZeroAddress(env e, address[] assets, uint256 amount, address user, address to, address reward) {

    setup(e);
    setupUser(e, user);
    setupUser(e, to);

    claimRewardsOnBehalf@withrevert(e, assets, amount, user, to, reward);

    assert user == 0 || to == 0 => lastReverted;
}

// [bug5] Claiming all rewards to zero address should revert
rule claimAllRewardsToZeroAddress(env e, address[] assets, address to) {

    setup(e);
    setupUser(e, to);

    claimAllRewards@withrevert(e, assets, to);

    assert to == 0 => lastReverted;
}

// [bug6] Claiming all rewards on behalf from or to zero address should revert
rule claimAllRewardsOnBehalfFromOrToZeroAddress(env e, address[] assets, address user, address to) {

    setup(e);
    setupUser(e, user);

    claimAllRewardsOnBehalf@withrevert(e, assets, user, to);

    assert user == 0 || to == 0 => lastReverted;
}

// [bug7] onlyAuthorizedClaimers() security modifier
rule integrityOnlyAuthorizedClaimers(method f, env e, address[] assets, uint256 amount, address user, address to, address reward) 
    filtered { f -> ONLY_AUTHORIZED_CLAIMERS_FUNCTIONS(f) } {
    
    setup(e);
    setupUser(e, user);

    if(f.selector == sig:claimRewardsOnBehalf(address[], uint256, address, address, address).selector) {
        claimRewardsOnBehalf(e, assets, amount, user, to, reward);
    } else if(f.selector == sig:claimAllRewardsOnBehalf(address[], address, address).selector) {
        claimAllRewardsOnBehalf(e, assets, user, to);
    }

    assert e.msg.sender == getClaimer(user);
}

// [bug8] onlyEmissionManager() security modifier
rule integrityOnlyEmissionManager(method f, env e, calldataarg args) filtered { f -> ONLY_EMISSION_MANAGER_FUNCTIONS(f) } {

    setup(e);

    f(e, args);

    assert e.msg.sender == getEmissionManager();
}