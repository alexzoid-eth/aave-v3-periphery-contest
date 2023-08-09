using DummyERC20_AToken as ATokenAddress;
using DummyERC20_rewardToken as rewardTokenAddress;
using TransferStrategyHarness as transferStrategyAddress;

///////////////// METHODS //////////////////////

methods {
    // ERC20
    function _.name() external => DISPATCHER(true);
    function _.symbol() external => DISPATCHER(true);
    function _.totalSupply() external => DISPATCHER(true);
    function _.balanceOf(address) external => DISPATCHER(true);
    function _.allowance(address,address) external => DISPATCHER(true);
    function _.approve(address,uint256) external => DISPATCHER(true);
    function _.transfer(address,uint256) external => DISPATCHER(true);
    function _.transferFrom(address,address,uint256) external => DISPATCHER(true);

    // Harness envfree
    function getAssetRewardIndex(address, address) external returns (uint256) envfree;
    function getAssetRewardEmissionPerSecond(address, address) external returns (uint256) envfree;
    function getAssetRewardLastUpdateTimestamp(address, address) external returns (uint256) envfree;
    function getAssetRewardDistributionEnd(address, address) external returns (uint256) envfree;
    function getAssetRewardUserIndex(address, address, address) external returns (uint256) envfree;
    function getAssetRewardUserAccrued(address, address, address) external returns (uint256) envfree;
    function getRewardToken(uint256) external returns (address) envfree;
    function getRewardsListLength() external returns (uint256) envfree;
    function isRewardInList(address) external returns (bool) envfree;
    function getAssetToken(uint256) external returns (address) envfree;
    function getAssetsListLength() external returns (uint256) envfree;
    function isAssetInList(address) external returns (bool) envfree;
    function isRewardEnabled(address) external returns (bool) envfree;
    function getAssetAvailableReward(address, uint128) external returns (address) envfree;
    function getAssetAvailableRewardsCount(address) external returns (uint128) envfree;
    function isContractHarness(address) external returns (bool) envfree;
    function getRevisionHarness() external returns (uint256) envfree;
    function getEmissionManagerHarness() external returns (address) envfree;
    function getRewardsHarness(uint256, uint256, uint256, uint256) external returns (uint256) envfree;

    // Harness
    function getUserAssetBalanceHarness(address[], address, uint256) external returns(address, uint256, uint256);
    function updateDataMultipleHarness(address) external;
    function updateDataHarness(address, address, uint256, uint256) external;
    function updateRewardDataHarness(address, address, uint256, uint256) external;
    function updateUserDataHarness(address, address, address, uint256, uint256, uint256) external returns (uint256, bool);
    function configureAssetsHarness(uint88, uint32, address, address, address, address) external;
    function claimRewardsHarness(address[], uint256, address, address, address, address) external returns (uint256);
    function claimAllRewardsHarness(address[], address, address, address) external returns (address[], uint256[]);
    function transferRewardsHarness(address, address, uint256) external;
    function getAssetIndexHarness(address, address) external returns (uint256, uint256);
    function getUserRewardsHarness(address[], address, address) external returns (uint256);
    function getPendingRewardsHarness(address user, address reward, address asset, uint256 userBalance, uint256 totalSupply) external returns (uint256);
    function getUserAssetBalancesHarmessSum(address[] assets, address) external returns (uint256);
    function getUserAssetBalancesSum(address[] assets, address) external returns (uint256);

    // RewardsController envfree
    function getRewardOracle(address) external returns (address) envfree;
    function getTransferStrategy(address) external returns (address) envfree;
    function getUserAssetIndex(address, address, address) external returns (uint256) envfree;
    function getClaimer(address) external returns (address) envfree;

    // RewardsController
    function setRewardOracle(address, address) external;
    function setTransferStrategy(address, address) external;
    function initialize(address) external;
    function setClaimer(address, address) external;
    function handleAction(address, uint256, uint256) external;
    function configureAssets(RewardsDataTypes.RewardsConfigInput[]) external;

    // RewardsDistributor envfree
    function getAssetDecimals(address) external returns (uint8) envfree;
    function getEmissionManager() external returns (address) envfree;
    function getRewardsData(address, address) external returns (uint256, uint256, uint256, uint256) envfree;
    function getUserAccruedRewards(address, address) external returns (uint256) envfree; 
    function getDistributionEnd(address, address) external returns (uint256) envfree; 
    function getRewardsList() external returns (address[]) envfree; 
    function getRewardsByAsset(address) external returns (address[]) envfree; 

    // RewardsDistributor
    function getAssetIndex(address, address) external returns (uint256, uint256); 
    function getUserRewards(address[], address, address) external returns (uint256); 
    function setEmissionPerSecond(address, address[], uint88[]) external;
    function setDistributionEnd(address, address, uint32) external;
    function getAllUserRewards(address[], address) external returns (address[], uint256[]);

    // TransferStrategyBase
    function _.performTransfer(address, address, uint256) external => DISPATCHER(true);

    // AToken    
    function _.scaledBalanceOf(address) external => DISPATCHER(true);
    function _.getScaledUserBalanceAndSupply(address) external => DISPATCHER(true);
    function _.scaledTotalSupply() external => DISPATCHER(true);
    function _.decimals() external => ghostDecimals() expect uint256 ALL;

    // Oracle 
    function _.latestAnswer() external => ghostLatestAnswer() expect int256 ALL;
}

///////////////// DEFINITIONS //////////////////////

definition VALID_DECIMALS(uint8 decimals) returns bool = decimals > 0 && decimals < 35;

definition GET_ASSET_INDEX_VALID_PARAMS(env e, uint256 index, uint256 totalSupply, uint256 emissionPerSecond, uint256 lastUpdateTimestamp, uint256 distributionEnd) returns bool =
    emissionPerSecond != 0 
    && totalSupply != 0 
    && lastUpdateTimestamp != e.block.timestamp 
    && lastUpdateTimestamp < distributionEnd;

definition VIEW_FUNCTIONS(method f) returns bool = f.isView || f.isPure;

definition HARNESS_FUNCTIONS(method f) returns bool = 
    f.selector == sig:getAssetRewardIndex(address, address).selector
    || f.selector == sig:getAssetRewardEmissionPerSecond(address, address).selector
    || f.selector == sig:getAssetRewardLastUpdateTimestamp(address, address).selector
    || f.selector == sig:getAssetRewardDistributionEnd(address, address).selector
    || f.selector == sig:getAssetRewardUserIndex(address, address, address).selector
    || f.selector == sig:getAssetRewardUserAccrued(address, address, address).selector
    || f.selector == sig:getRewardToken(uint256).selector
    || f.selector == sig:getRewardsListLength().selector
    || f.selector == sig:isRewardInList(address).selector
    || f.selector == sig:getAssetToken(uint256).selector
    || f.selector == sig:getAssetsListLength().selector
    || f.selector == sig:isAssetInList(address).selector
    || f.selector == sig:getAssetAvailableReward(address, uint128).selector
    || f.selector == sig:getAssetAvailableRewardsCount(address).selector
    || f.selector == sig:isRewardEnabled(address).selector
    || f.selector == sig:isContractHarness(address).selector
    || f.selector == sig:getRevisionHarness().selector
    || f.selector == sig:getEmissionManagerHarness().selector
    || f.selector == sig:getUserAssetBalanceHarness(address[], address, uint256).selector
    || f.selector == sig:getAssetIndexHarness(address, address).selector
    || f.selector == sig:getUserRewardsHarness(address[], address, address).selector
    || f.selector == sig:getRewardsHarness(uint256, uint256, uint256, uint256).selector
    || f.selector == sig:updateDataMultipleHarness(address[], address).selector
    || f.selector == sig:updateDataHarness(address, address, uint256, uint256).selector
    || f.selector == sig:updateRewardDataHarness(address, address, uint256, uint256).selector
    || f.selector == sig:updateUserDataHarness(address, address, address, uint256, uint256, uint256).selector
    || f.selector == sig:configureAssetsHarness(uint88, uint32, address, address, address, address).selector
    || f.selector == sig:claimRewardsHarness(address[], uint256, address, address, address, address).selector
    || f.selector == sig:claimAllRewardsHarness(address[], address, address, address).selector
    || f.selector == sig:transferRewardsHarness(address, address, uint256).selector;

definition CLAIM_REWARDS_FUNCTION(method f) returns bool = 
    f.selector == sig:claimRewards(address[], uint256, address, address).selector;

definition CLAIM_REWARDS_FUNCTIONS(method f) returns bool = 
    CLAIM_REWARDS_FUNCTION(f)
    || f.selector == sig:claimRewardsOnBehalf(address[], uint256, address, address, address).selector
    || f.selector == sig:claimRewardsToSelf(address[], uint256, address).selector;

definition CLAIM_ALL_REWARDS_FUNCTION(method f) returns bool = 
    f.selector == sig:claimAllRewards(address[], address).selector;

definition CLAIM_ALL_REWARDS_FUNCTIONS(method f) returns bool = 
    CLAIM_ALL_REWARDS_FUNCTION(f) || f.selector == sig:claimAllRewardsOnBehalf(address[], address, address).selector;

definition HANDLE_FUNCTION(method f) returns bool = 
    f.selector == sig:handleAction(address, uint256, uint256).selector;

definition ONLY_AUTHORIZED_CLAIMERS_FUNCTIONS(method f) returns bool = 
    f.selector == sig:claimRewardsOnBehalf(address[], uint256, address, address, address).selector
    || f.selector == sig:claimAllRewardsOnBehalf(address[], address, address).selector;

definition ONLY_EMISSION_MANAGER_FUNCTIONS(method f) returns bool = 
    f.selector == sig:configureAssets(RewardsDataTypes.RewardsConfigInput[]).selector
    || f.selector == sig:setTransferStrategy(address, address).selector
    || f.selector == sig:setRewardOracle(address, address).selector
    || f.selector == sig:setClaimer(address, address).selector
    || f.selector == sig:setDistributionEnd(address, address, uint32).selector
    || f.selector == sig:setEmissionPerSecond(address, address[], uint88[]).selector;

definition NEVER_REVERTED_FUNCTIONS(method f) returns bool = 
    f.selector == sig:getClaimer(address).selector
    || f.selector == sig:getRevisionHarness().selector
    || f.selector == sig:getRewardOracle(address).selector
    || f.selector == sig:getTransferStrategy(address).selector
    || f.selector == sig:getRewardsData(address, address).selector
    || f.selector == sig:getDistributionEnd(address, address).selector
    || f.selector == sig:getRewardsByAsset(address).selector
    || f.selector == sig:getRewardsList().selector
    || f.selector == sig:getUserAssetIndex(address, address, address).selector
    || f.selector == sig:getUserAccruedRewards(address, address).selector
    || f.selector == sig:getAssetDecimals(address).selector
    || f.selector == sig:getEmissionManager().selector;

definition POSSIBLY_NOT_REVERTED_FUNCTIONS(method f) returns bool = 
    f.selector == sig:configureAssets(RewardsDataTypes.RewardsConfigInput[]).selector
    || f.selector == sig:handleAction(address, uint256, uint256).selector
    || f.selector == sig:claimRewards(address[], uint256, address, address).selector
    || f.selector == sig:claimRewardsOnBehalf(address[], uint256, address, address, address).selector
    || f.selector == sig:claimRewardsToSelf(address[], uint256, address).selector
    || f.selector == sig:claimAllRewards(address[], address).selector
    || f.selector == sig:claimAllRewardsOnBehalf(address[], address, address).selector
    || f.selector == sig:claimAllRewardsToSelf(address[]).selector
    || f.selector == sig:setEmissionPerSecond(address, address[], uint88[]).selector
    || f.selector == sig:getAssetIndex(address, address).selector
    || f.selector == sig:getUserRewards(address[], address, address).selector
    || f.selector == sig:getAllUserRewards(address[], address).selector;

definition MAX_UINT32() returns uint256 = 0xffffffff;
definition MAX_UINT88() returns uint256 = 0xffffffffffffffffffffff;
definition MAX_UINT104() returns uint256 = 0xffffffffffffffffffffffffff;
definition MAX_UINT256() returns uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff;

////////////////// FUNCTIONS //////////////////////

// CVL functions for precondition assumptions 

function setupUser(env e, address user) {
    require user != 0;
    require user != currentContract;
    require user != ATokenAddress;
    require user != rewardTokenAddress;
    require user != transferStrategyAddress;

    require ATokenAddress.scaledBalanceOf(e, user) <= ATokenAddress.scaledTotalSupply(e);
}

function setupTokenDecimals(address token) {
    require VALID_DECIMALS(getAssetDecimals(token));
}

function setupTokenTotalSupply(env e, address token) {
    require ATokenAddress.scaledTotalSupply(e) >= require_uint256(1000 * 10 ^ getAssetDecimals(ATokenAddress));
}

function setupEssential(env e) {
    require e.msg.value == 0;
    require e.block.number != 0;
    require e.block.timestamp != 0 && e.block.timestamp <= MAX_UINT32();
}

///////////////// Ghosts & hooks ///////////////////////

// Ghost for access _transferStrategy[reward]
ghost bool ghostTransferStrategyRead;

// Ghost for `_.latestAnswer()` summarize
ghost ghostLatestAnswer() returns int256;

// Ghost for `asset.decimals()` summarize
ghost ghostDecimals() returns uint8;

// Hook for `EXTCODESIZE` opcode

ghost uint256 ghostExtcodesize;

hook EXTCODESIZE(address addr) uint v {
    ghostExtcodesize = v;
}

// VersionedInitializable initial values

hook Sload bool val initializing STORAGE {
    require val == false;
}

hook Sload uint256 val lastInitializedRevision STORAGE {
    require val == 0;
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
    ghostTransferStrategy[reward] = strategy;
}

hook Sload address strategy _transferStrategy[KEY address reward] STORAGE {
    require ghostTransferStrategy[reward] == strategy;
    ghostTransferStrategyRead = true;
}

// Ghost copy of _rewardOracle[]

ghost mapping(address => address) ghostRewardOracle {
    init_state axiom forall address x. ghostRewardOracle[x] == 0;
}

hook Sstore _rewardOracle[KEY address reward] address oracle STORAGE {
    ghostRewardOracle[reward] = oracle;
}

hook Sload address oracle _rewardOracle[KEY address reward] STORAGE {
    require ghostRewardOracle[reward] == oracle;
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

// Ghost copy of _rewardsList[]

ghost uint128 ghostRewardsListLength {
    init_state axiom ghostRewardsListLength == 0;
}

ghost mapping(address => bool) ghostRewardsList {
    init_state axiom forall address reward. ghostRewardsList[reward] == false;
}

hook Sstore _rewardsList[INDEX uint256 i] address reward STORAGE {
    ghostRewardsList[reward] = true;
    ghostRewardsListLength = require_uint128(ghostRewardsListLength + 1);
}

hook Sload address reward _rewardsList[INDEX uint256 i] STORAGE {
    require ghostRewardsList[reward] == true;
}

// Ghost copy of _assetsList[]

ghost mapping(address => bool) ghostAssetsList {
    init_state axiom forall address asset . ghostAssetsList[asset] == false;
}

hook Sstore _assetsList[INDEX uint256 i] address asset STORAGE {
    ghostAssetsList[asset] = true;
}

hook Sload address asset _assetsList[INDEX uint256 i] STORAGE {
    require ghostAssetsList[asset] == true;
}

// Ghost copy of _assets[].availableRewardsCount

ghost mapping (address => uint128) ghostAssetsAvailableRewardsCount {
    init_state axiom forall address asset. ghostAssetsAvailableRewardsCount[asset] == 0;
}

ghost mapping (address => uint128) ghostAssetsAvailableRewardsCountIncremented {
    init_state axiom forall address asset. ghostAssetsAvailableRewardsCountIncremented[asset] == ghostAssetsAvailableRewardsCount[asset];
}

hook Sstore _assets[KEY address asset].availableRewardsCount uint128 count STORAGE {
    ghostAssetsAvailableRewardsCountIncremented[asset] = require_uint128(ghostAssetsAvailableRewardsCountIncremented[asset] + 1);
    ghostAssetsAvailableRewardsCount[asset] = count;
}

hook Sload uint128 count _assets[KEY address asset].availableRewardsCount STORAGE {
    require ghostAssetsAvailableRewardsCount[asset] == count;
}

// Ghost copy of _assets[].decimals

ghost mapping (address => uint8) ghostAssetsDecimals {
    init_state axiom forall address asset. ghostAssetsDecimals[asset] == 0;
}

hook Sstore _assets[KEY address asset].decimals uint8 decimals STORAGE {
    ghostAssetsDecimals[asset] = decimals;
}

hook Sload uint8 decimals _assets[KEY address asset].decimals STORAGE {
    require ghostAssetsDecimals[asset] == decimals;
}

// Ghost copy of _assets[asset].rewards[reward].lastUpdateTimestamp

ghost mapping (address => uint32) ghostAssetLastUpdateTimestamp {
    init_state axiom forall address reward. ghostAssetLastUpdateTimestamp[reward] == 0;
}

hook Sstore _assets[KEY address asset].rewards[KEY address reward].lastUpdateTimestamp uint32 lastUpdateTimestamp STORAGE {
    ghostAssetLastUpdateTimestamp[reward] = lastUpdateTimestamp;
}

hook Sload uint32 lastUpdateTimestamp _assets[KEY address asset].rewards[KEY address reward].lastUpdateTimestamp STORAGE {
    require ghostAssetLastUpdateTimestamp[reward] == lastUpdateTimestamp;
}

// Hook write access to _assets[asset].rewards[reward].usersData[user].accrued

ghost bool ghostUsersDataAccruedWrite;

hook Sstore _assets[KEY address asset].rewards[KEY address reward].usersData[KEY address user].accrued uint128 accrued STORAGE {
    ghostUsersDataAccruedWrite = true;
}

// Hook read access to _assets[asset].rewards[reward].usersData[user].index

ghost bool ghostUsersDataIndexRead;

hook Sload uint104 index _assets[KEY address asset].rewards[KEY address reward].usersData[KEY address user].index STORAGE {
    ghostUsersDataIndexRead = true;
}