import "methods/ERC20_methods.spec";

using DummyERC20_AToken as ATokenAddress;
using DummyERC20_rewardToken as rewardTokenAddress;
using TransferStrategyHarness as transferStrategyAddress;

/////////////////// Methods ////////////////////////

methods {
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
    function getUserAssetBalanceHarness(address[], address) external returns(address, uint256, uint256);
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

    // AToken    
    function _.scaledBalanceOf(address) external => DISPATCHER(true);
    function _.getScaledUserBalanceAndSupply(address) external => DISPATCHER(true);
    function _.scaledTotalSupply() external => DISPATCHER(true);
    function _.decimals() external => ghostDecimals() expect uint256 ALL;

    // TransferStrategyBase
    function _.performTransfer(address, address, uint256) external => DISPATCHER(true);

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
    || f.selector == sig:getUserAssetBalanceHarness(address[], address).selector
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
    || f.selector == sig:setClaimer(address, address).selector
    || f.selector == sig:setDistributionEnd(address, address, uint32).selector
    || f.selector == sig:setEmissionPerSecond(address, address[], uint88[]).selector;

definition GETTERS_NEVER_REVERTED(method f) returns bool = 
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

function setup(env e) {

    setupEssential(e);

    setupUser(e, e.msg.sender);

    require getRewardsListLength() == 1;
    require getRewardToken(0) == rewardTokenAddress;
    require getTransferStrategy(rewardTokenAddress) == transferStrategyAddress;
    require getAssetsListLength() == 1;
    require getAssetToken(0) == ATokenAddress;
    require getAssetAvailableReward(ATokenAddress, 0) == rewardTokenAddress;
    require getAssetAvailableRewardsCount(ATokenAddress) == 1;

    require ghostDecimals() > 0;

    require rewardTokenAddress != transferStrategyAddress;
    require rewardTokenAddress != ATokenAddress;
    require rewardTokenAddress != currentContract;
    require ATokenAddress != currentContract;
    require ATokenAddress != transferStrategyAddress;
    require transferStrategyAddress != currentContract;
}

///////////////// Ghosts & hooks ///////////////////////

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

// Ghost copy of _assets[asset0].rewards[reward].lastUpdateTimestamp

ghost mapping (address => uint32) ghostAssetLastUpdateTimestamp {
    init_state axiom forall address reward. ghostAssetLastUpdateTimestamp[reward] == 0;
}

hook Sstore _assets[KEY address asset].rewards[KEY address reward].lastUpdateTimestamp uint32 lastUpdateTimestamp STORAGE {
    ghostAssetLastUpdateTimestamp[reward] = lastUpdateTimestamp;
}

hook Sload uint32 lastUpdateTimestamp _assets[KEY address asset].rewards[KEY address reward].lastUpdateTimestamp STORAGE {
    require ghostAssetLastUpdateTimestamp[reward] == lastUpdateTimestamp;
}

///////////////// Invariants ///////////////////////

// [participants 43] Reward token which is added to the list should be enabled
invariant rewardsInListShouldBeEnabled() forall address reward . ghostRewardsList[reward] == ghostIsRewardEnabled[reward]
    filtered { f -> !HARNESS_FUNCTIONS(f) }

///////////////// Properties ///////////////////////

// [participants 16] initializer() security modifier, second call of initialize() should revert
rule initializeCalledOnlyOnce(env e1, env e2, address addr) {

    initialize@withrevert(e1, addr);
    bool firstCallReverted = lastReverted;

    initialize@withrevert(e2, addr);
    bool secondCallReverted = lastReverted;

    assert !firstCallReverted => secondCallReverted;
}

// [participants 17] initialize() - first call should not revert
rule initializeFirstCallShouldNotRevert(env e, address addr) {

    setup(e);

    initialize@withrevert(e, addr);

    assert !lastReverted;
}

// [participants 18-25] getters integrity
rule gettersIntegrity(address asset, address reward, address user) {
    assert getClaimer(user) == ghostAuthorizedClaimers[user]; // bug18
    assert getRevisionHarness() == require_uint256(1); // bug19
    assert getRewardOracle(reward) == ghostRewardOracle[reward]; // bug20
    assert getTransferStrategy(reward) == ghostTransferStrategy[reward]; // bug21
    assert getDistributionEnd(asset, reward) == require_uint256(getAssetRewardDistributionEnd(asset, reward)); //bug22
    assert getUserAssetIndex(user, asset, reward) == getAssetRewardUserIndex(user, asset, reward); //bug23
    assert getAssetDecimals(asset) == ghostAssetsDecimals[asset]; //bug24
    assert getEmissionManager() == getEmissionManagerHarness(); //bug25
} 

// [participants 26-37] getters should not revert 
rule gettersShouldNotRevert(env e, method f, address asset, address reward, address user) 
    filtered { f -> GETTERS_NEVER_REVERTED(f) } {

    setup(e);

    require asset == ATokenAddress;
    require reward == rewardTokenAddress;

    if(f.selector == sig:getClaimer(address).selector) {
        getClaimer@withrevert(user); // bug26
    } else if(f.selector == sig:getRevisionHarness().selector) {
        getRevisionHarness@withrevert(); // bug27
    } else if(f.selector == sig:getRewardOracle(address).selector) {
        getRewardOracle@withrevert(reward); // bug28
    } else if(f.selector == sig:getTransferStrategy(address).selector) {
        getTransferStrategy@withrevert(reward); // bug29
    } else if(f.selector == sig:getRewardsData(address, address).selector) {
        getRewardsData@withrevert(asset, reward); // bug30
    } else if(f.selector == sig:getDistributionEnd(address, address).selector) {
        getDistributionEnd@withrevert(asset, reward); // bug31
    } else if(f.selector == sig:getRewardsByAsset(address).selector) {
        getRewardsByAsset@withrevert(asset); // bug32
    } else if(f.selector == sig:getRewardsList().selector) {
        getRewardsList@withrevert(); // bug33
    } else if(f.selector == sig:getUserAssetIndex(address, address, address).selector) {
        getUserAssetIndex@withrevert(user, asset, reward); // bug34
    } else if(f.selector == sig:getUserAccruedRewards(address, address).selector) {
        getUserAccruedRewards@withrevert(user, reward); // bug35
    } else if(f.selector == sig:getAssetDecimals(address).selector) {
        getAssetDecimals@withrevert(asset); // bug36
    } else if(f.selector == sig:getEmissionManager().selector) {
        getEmissionManager@withrevert(); // bug37
    }

    assert !lastReverted;
}

// [participants 9, 38-50, 128-136] configureAssets() integrity
rule configureAssetsIntegrity(
    env e, 
    uint88 emissionPerSecond, 
    uint32 distributionEnd,
    address asset,
    address reward,
    address transferStrategy,
    address rewardOracle
    ) {

    require e.msg.sender == getEmissionManager();
    require asset == ATokenAddress;
    require reward == rewardTokenAddress;

    // Asset token will be added when zero decimals
    bool zeroDecimals = getAssetDecimals(asset) == 0;
    require ghostDecimals() == getAssetDecimals(asset);

    // Reward token will be added when was not enabled
    bool rewardEnabled;
    require rewardEnabled == isRewardEnabled(reward);
    bool rewardInList;
    require rewardInList == isRewardInList(reward);

    // add reward address to asset available rewards when zero timestamp
    bool zeroTimeStamp = getAssetRewardLastUpdateTimestamp(asset, reward) == 0;

    // revert when length reach uin256 limit 
    require getAssetsListLength() < 1000;
    require getRewardsListLength() < 1000;

    uint256 oldIndex;
    uint256 newIndex;
    oldIndex, newIndex = getAssetIndexHarness(e, asset, reward);

    uint128 availableRewardsCountBefore = getAssetAvailableRewardsCount(asset);

    configureAssetsHarness(
        e, 
        emissionPerSecond, 
        distributionEnd,
        asset,
        reward,
        transferStrategy,
        rewardOracle
    );

    uint128 availableRewardsCountAfter = getAssetAvailableRewardsCount(asset);
    uint256 currentIndex = getAssetRewardIndex(asset, reward);

    assert require_uint256(emissionPerSecond) == getAssetRewardEmissionPerSecond(asset, reward); // bug45
    assert require_uint256(distributionEnd) == getAssetRewardDistributionEnd(asset, reward); // bug46
    assert zeroDecimals => isAssetInList(asset); // bug39, bug40, bug41
    assert !rewardEnabled => isRewardEnabled(reward) && isRewardInList(reward); // bug42, bug43, bug44
    assert rewardEnabled => isRewardEnabled(reward) && rewardInList == isRewardInList(reward); // bug50
    assert transferStrategy == getTransferStrategy(reward); // bug9
    assert rewardOracle == getRewardOracle(reward); // bug38
    assert zeroTimeStamp => availableRewardsCountAfter == require_uint128(availableRewardsCountBefore + require_uint128(1)); // bug47
    assert zeroTimeStamp => getAssetAvailableReward(asset, availableRewardsCountBefore) == reward; // bug48
    assert !zeroTimeStamp => availableRewardsCountAfter == availableRewardsCountBefore; // bug49

    // set in _updateRewardData()
    assert require_uint32(getAssetRewardLastUpdateTimestamp(asset, reward)) == require_uint32(e.block.timestamp); // bug128
    assert oldIndex == newIndex => currentIndex == oldIndex; // bug128-136
    assert oldIndex != newIndex => currentIndex == newIndex;
}

// [participants 8, 51-55] onlyEmissionManager() security modifier
rule onlyEmissionManagerIntegrity(method f, env e, calldataarg args) 
    filtered { f -> ONLY_EMISSION_MANAGER_FUNCTIONS(f) } {

    f@withrevert(e, args);

    assert !lastReverted => e.msg.sender == getEmissionManager();
}

// [7, 56] onlyAuthorizedClaimers() security modifier
rule onlyAuthorizedClaimersIntegrity(method f, env e, address[] assets, uint256 amount, address user, address to, address reward) 
    filtered { f -> ONLY_AUTHORIZED_CLAIMERS_FUNCTIONS(f) } {
    
    if(f.selector == sig:claimRewardsOnBehalf(address[], uint256, address, address, address).selector) {
        claimRewardsOnBehalf@withrevert(e, assets, amount, user, to, reward);
    } else if(f.selector == sig:claimAllRewardsOnBehalf(address[], address, address).selector) {
        claimAllRewardsOnBehalf@withrevert(e, assets, user, to);
    }
    
    assert !lastReverted => e.msg.sender == getClaimer(user);
}

// [participants 12-13, 52, 57] setTransferStrategy() integrity 
rule setTransferStrategyIntegrity(env e, address reward, address transferStrategy) {
    
    setup(e);

    setTransferStrategy@withrevert(e, reward, transferStrategy);
    bool reverted = lastReverted;

    assert e.msg.sender != getEmissionManager() => reverted; // bug52
    assert transferStrategy == 0 => reverted; // bug13
    assert isContractHarness(transferStrategy) == false => reverted; // bug12
    assert e.msg.sender == getEmissionManager() && transferStrategy != 0 && isContractHarness(transferStrategy) => !reverted; // RewardsController_107/bug101
    assert !reverted => getTransferStrategy(reward) == transferStrategy; // bug57
}

// [participants 8, 10, 11] setRewardOracle() integrity, never reverted with EmissionManager
rule setRewardOracleIntegrity(env e, address reward, address rewardOracle) {
    
    setup(e);

    setRewardOracle@withrevert(e, reward, rewardOracle);
    bool reverted = lastReverted;

    assert e.msg.sender != getEmissionManager() => reverted; // bug8
    assert ghostLatestAnswer() <= 0 => reverted; // bug10
    assert e.msg.sender == getEmissionManager() && ghostLatestAnswer() > 0 => !reverted; // RewardsController_107/bug105
    assert !reverted => rewardOracle == getRewardOracle(reward); // bug11
}

// [participants 14, 58, 166] _isContract() integrity, never reverted
rule isContractIntegrity(address contractAddress) {

    require ghostExtcodesize == 0;

    bool result = isContractHarness@withrevert(contractAddress);

    // Never reverted
    assert !lastReverted; // bug58

    // `ghostExtcodesize` is set in EXTCODESIZE hook
    assert ghostExtcodesize > 0 ? result == true : result == false; // bug14, bug166
}

// [participants 59-60] handleAction() integrity
rule handleActionIntegrity(env e, address user, uint256 userBalance, uint256 totalSupply) {

    require e.msg.sender == ATokenAddress;

    storage initial = lastStorage;

    updateDataHarness(e, ATokenAddress, user, userBalance, totalSupply) at initial;
    storage afterUpdateData = lastStorage;

    handleAction(e, user, totalSupply, userBalance) at initial;
    storage afterHandleAction = lastStorage;

    // Storage should be the same
    assert afterUpdateData[currentContract] == afterHandleAction[currentContract];
}

// [participants 2] claimRewards() to zero address is not allowed 
rule claimRewardsZeroAddressCheck(env e, address[] assets, uint256 amount, address to, address reward) {

    setup(e);

    claimRewards(e, assets, amount, to, reward);

    assert to != 0; // bug2
}

// [participants 61-63, 95] claimRewards() integrity
rule claimRewardsIntegrity(env e, address[] assets, uint256 amount, address user, address to, address reward) {

    setup(e);

    require assets.length == 1;
    require assets[0] == ATokenAddress;
    require user == e.msg.sender;
    setupUser(e, to);
    require reward == rewardTokenAddress;

    storage initial = lastStorage;

    uint256 claimed1 = claimRewardsHarness(e, assets, amount, e.msg.sender, user, to, reward) at initial;
    uint256 toBalance1 = rewardTokenAddress.balanceOf(e, to);
    storage storage1 = lastStorage;

    uint256 claimed2 = claimRewards(e, assets, amount, to, reward) at initial;
    uint256 toBalance2 = rewardTokenAddress.balanceOf(e, to);
    storage storage2 = lastStorage;

    assert amount == 0 => claimed2 == 0;
    assert storage1[currentContract] == storage2[currentContract]; // bug61
    assert toBalance1 == toBalance2; // bug62
    assert claimed1 == claimed2; // bug63
}

// [participants 4, 64] claimRewardsOnBehalf() from or to zero address is not allowed
rule claimRewardsOnBehalfZeroAddressCheck(env e, address[] assets, uint256 amount, address user, address to, address reward) {

    setup(e);

    // Checked in integrityOnlyAuthorizedClaimers()
    require e.msg.sender == getClaimer(user);

    claimRewardsOnBehalf(e, assets, amount, user, to, reward);

    assert user != 0 && to != 0; // bug4, bug64
}

// [participants 65-68] claimRewardsOnBehalf() integrity
rule claimRewardsOnBehalfIntegrity(env e, address[] assets, uint256 amount, address user, address to, address reward) {

    setup(e);

    // Checked in integrityOnlyAuthorizedClaimers()
    require e.msg.sender == getClaimer(user);

    require assets.length == 1;
    require assets[0] == ATokenAddress;
    setupUser(e, user);
    setupUser(e, to);
    require reward == rewardTokenAddress;

    storage initial = lastStorage;

    uint256 claimed1 = claimRewardsHarness(e, assets, amount, e.msg.sender, user, to, reward) at initial;
    uint256 toBalance1 = rewardTokenAddress.balanceOf(e, to);
    storage storage1 = lastStorage;

    uint256 claimed2 = claimRewardsOnBehalf(e, assets, amount, user, to, reward) at initial;
    uint256 toBalance2 = rewardTokenAddress.balanceOf(e, to);
    storage storage2 = lastStorage;

    assert storage1[currentContract] == storage2[currentContract];
    assert toBalance1 == toBalance2;
    assert claimed1 == claimed2;
}

// [participants 69-72] claimRewardsToSelf() integrity
rule claimRewardsToSelfIntegrity(env e, address[] assets, uint256 amount, address user, address to, address reward) {

    setup(e);

    require assets.length == 1;
    require assets[0] == ATokenAddress;
    require reward == rewardTokenAddress;
    require user == e.msg.sender;
    require to == e.msg.sender;

    storage initial = lastStorage;

    uint256 claimed1 = claimRewardsHarness(e, assets, amount, e.msg.sender, user, to, reward) at initial;
    uint256 toBalance1 = rewardTokenAddress.balanceOf(e, to);
    storage storage1 = lastStorage;

    uint256 claimed2 = claimRewardsToSelf(e, assets, amount, reward) at initial;
    uint256 toBalance2 = rewardTokenAddress.balanceOf(e, to);
    storage storage2 = lastStorage;

    assert storage1[currentContract] == storage2[currentContract];
    assert toBalance1 == toBalance2;
    assert claimed1 == claimed2;
}

// [participants 5] claimAllRewards() to zero address should revert
rule claimAllRewardsZeroAddressCheck(env e, address[] assets, address to) {

    setup(e);

    claimAllRewards(e, assets, to);

    assert to != 0; // bug5
}

// [participants 73-75] claimAllRewards() integrity
rule claimAllRewardsIntegrity(env e, address[] assets, address user, address to) {

    setup(e);

    require assets.length == 1;
    require assets[0] == ATokenAddress;
    require user == e.msg.sender;

    storage initial = lastStorage;

    claimAllRewardsHarness(e, assets, e.msg.sender, user, to) at initial;
    storage storage1 = lastStorage;

    claimAllRewards(e, assets, to) at initial;
    storage storage2 = lastStorage;

    assert storage1[currentContract] == storage2[currentContract];
    assert storage1[rewardTokenAddress] == storage2[rewardTokenAddress];
}

// [participants 6, 76] claimAllRewardsOnBehalf() from or to zero address should revert
rule claimAllRewardsOnBehalfZeroAddressCheck(env e, address[] assets, address user, address to) {

    setup(e);

    // Checked in integrityOnlyAuthorizedClaimers()
    require e.msg.sender == getClaimer(user);

    claimAllRewardsOnBehalf(e, assets, user, to);

    assert user != 0 && to != 0; // bug6, bug76
}

// [participants 77-79] claimAllRewardsOnBehalf() integrity
rule claimAllRewardsOnBehalfIntegrity(env e, address[] assets, address user, address to) {

    setup(e);

    // Checked in integrityOnlyAuthorizedClaimers()
    require e.msg.sender == getClaimer(user);

    require assets.length == 1;
    require assets[0] == ATokenAddress;

    storage initial = lastStorage;

    claimAllRewardsHarness(e, assets, e.msg.sender, user, to) at initial;
    storage storage1 = lastStorage;

    claimAllRewardsOnBehalf(e, assets, user, to) at initial;
    storage storage2 = lastStorage;

    assert storage1[currentContract] == storage2[currentContract];
    assert storage1[rewardTokenAddress] == storage2[rewardTokenAddress];
}

// [participants 80-81] claimAllRewardsToSelf() integrity
rule claimAllRewardsToSelfIntegrity(env e, address[] assets, address user, address to) {

    setup(e);

    require assets.length == 1;
    require assets[0] == ATokenAddress;
    require user == e.msg.sender;
    require to == e.msg.sender;

    storage initial = lastStorage;

    claimAllRewardsHarness(e, assets, e.msg.sender, user, to) at initial;
    storage storage1 = lastStorage;

    claimAllRewardsToSelf(e, assets) at initial;
    storage storage2 = lastStorage;

    assert storage1[currentContract] == storage2[currentContract];
    assert storage1[rewardTokenAddress] == storage2[rewardTokenAddress];
}

// [participants 1, 85] Possibility of update reward index when executing claim rewards
rule claimRewardsPossibleUpdateRewardIndex(method f, env e, address[] assets, address to, address reward) 
    filtered { f -> CLAIM_REWARDS(f) || CLAIM_ALL_REWARDS(f) } {

    setup(e);
    setupUser(e, to);

    require assets.length == 1;
    require assets[0] == ATokenAddress;
    require reward == rewardTokenAddress;

    // Precondition assumptions in _getAssetIndex()
    require getAssetRewardEmissionPerSecond(assets[0], reward) != 0;
    require getAssetRewardLastUpdateTimestamp(assets[0], reward) != e.block.timestamp;
    require getAssetRewardLastUpdateTimestamp(assets[0], reward) 
        < require_uint256(getAssetRewardDistributionEnd(assets[0], reward));

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

// [participants 86-94] Claim rewards will process token transfer when accrued available
rule claimRewardsTransferFunds(method f, env e, address user, address[] assets, uint256 amount, address to, address reward) 
    filtered { f -> CLAIM_REWARDS(f) || CLAIM_ALL_REWARDS(f) } {

    setup(e);
    setupUser(e, to);

    require user == e.msg.sender;
    require user != to;
    require assets.length == 1;
    require assets[0] == ATokenAddress;
    require reward == rewardTokenAddress;

    // Will update accrued
    updateDataMultipleHarness(e, assets, user);

    uint256 accruedBefore = getAssetRewardUserAccrued(e.msg.sender, ATokenAddress, rewardTokenAddress);
    uint256 rewardsBefore = rewardTokenAddress.balanceOf(e, to);

    if(CLAIM_REWARDS(f)) {
        claimRewards(e, assets, amount, to, reward);
    } else if (CLAIM_ALL_REWARDS(f)) {
        require accruedBefore == amount;
        claimAllRewards(e, assets, to);
    }

    uint256 accruedAfter = getAssetRewardUserAccrued(e.msg.sender, ATokenAddress, rewardTokenAddress);
    uint256 rewardsAfter = rewardTokenAddress.balanceOf(e, to);

    // Transfer all rewards
    assert accruedBefore <= amount =>
        accruedBefore == require_uint256(rewardsAfter - rewardsBefore) 
        && accruedAfter == 0;

    // Some rewards left
    assert accruedBefore > amount => 
        amount == require_uint256(rewardsAfter - rewardsBefore) 
        && accruedAfter == require_uint256(accruedBefore - amount);
}

// [participants 102] Claim zero rewards will return zero
rule claimRewardsZeroAmountReturnZero(env e, address[] assets, uint256 amount, address to, address reward) {

    setup(e);

    require assets.length == 1;
    require assets[0] == ATokenAddress;
    require amount == 0;

    storage before = lastStorage;
    uint256 claimed = claimRewards(e, assets, amount, to, reward);
    storage after = lastStorage;

    assert claimed == 0 && before[currentContract] == after[currentContract];
}

// [RewardsController_107 54] _claimRewards() integrity
rule claimRewardsInternalIntegrity(env e, address[] assets, uint256 amount, address claimer, address user, address to, address reward) {
    
    setup(e);
    setupUser(e, user);

    require assets.length == 1;
    require assets[0] == ATokenAddress;
    require reward == rewardTokenAddress;

    updateDataMultipleHarness(e, assets, user);

    uint256 accruedBefore = getAssetRewardUserAccrued(user, assets[0], reward);
    require accruedBefore != 0;
    require amount != accruedBefore;

    uint256 totalRewards = claimRewardsHarness@withrevert(e, assets, amount, claimer, user, to, reward);
    bool reverted = lastReverted;

    uint256 accrued0After = getAssetRewardUserAccrued(user, assets[0], reward);

    // _claimRewards() return 0 when zero amount set
    assert amount == 0 => !reverted && totalRewards == 0;

    // totalRewards and accrued check
    assert !reverted && amount != 0 && accruedBefore <= amount 
        => totalRewards == accruedBefore && accrued0After == 0;

    uint256 difference = accruedBefore > amount ? require_uint256(accruedBefore - amount) : 0;
    assert !reverted && amount != 0 && accruedBefore > amount 
        => totalRewards == require_uint256(accruedBefore - difference) && accrued0After == difference;
}

// [RewardsController_107 47] _claimRewards() integrity
rule claimRewardsInternalAmountGTAccruedPossibleClaimed(env e, address[] assets, uint256 amount, address claimer, address user, address to, address reward) {
    
    setup(e);
    setupUser(e, user);

    require assets.length == 1;
    require assets[0] == ATokenAddress;
    require reward == rewardTokenAddress;
    require amount != 0;

    updateDataMultipleHarness(e, assets, user);

    uint256 accruedBefore = getAssetRewardUserAccrued(user, assets[0], reward);
    require accruedBefore != 0;
    require accruedBefore < amount;

    uint256 totalRewards = claimRewardsHarness@withrevert(e, assets, amount, claimer, user, to, reward);
    bool reverted = lastReverted;

    uint256 accrued0After = getAssetRewardUserAccrued(user, assets[0], reward);

    satisfy(!reverted && accrued0After == 0 && totalRewards == accruedBefore);
}

// [RewardsController_107 72] _claimAllRewards() integrity
rule claimAllRewardsInternalIntegrity(env e, address[] assets, address claimer, address user, address to) {

    assert true;
}

// [participants 97-101, RewardsController_107 92-93] _transferRewards() integrity
rule transferRewardsIntegrity(env e, address to, address reward, uint256 amount) {

    setup(e);

    require to != transferStrategyAddress;
    require reward == rewardTokenAddress;

    // No way go inside a _transferRewards() with zero amount 
    require amount != 0;

    uint256 balanceToBefore = rewardTokenAddress.balanceOf(e, to);
    uint256 balanceStrategyBefore = rewardTokenAddress.balanceOf(e, transferStrategyAddress);

    transferRewardsHarness@withrevert(e, to, reward, amount);
    bool reverted = lastReverted;

    uint256 balanceToAfter = rewardTokenAddress.balanceOf(e, to);
    uint256 balanceStrategyAfter = rewardTokenAddress.balanceOf(e, transferStrategyAddress);

    bool enoughToTransfer = balanceStrategyBefore >= amount;
    bool couldReceive = require_uint256(MAX_UINT256() - balanceToBefore) >= amount;
    bool zeroReceiver = to == 0;
    bool shouldRevert = !enoughToTransfer || !couldReceive || zeroReceiver;

    // Not enough tokens to send or receiver balance is to large
    assert shouldRevert == reverted;

    // Sender balance
    assert !reverted => require_uint256(balanceStrategyBefore - balanceStrategyAfter) == amount;

    // Recipient balance
    assert !reverted => require_uint256(balanceToAfter - balanceToBefore) == amount;
}

// [participants 3] Claim rewards should return amount of accrued rewards
rule claimAllRewardsReturnClaimedAmounts(env e, address[] assets, address user, address to) {

    setup(e);
    setupUser(e, to);

    require assets.length == 1;
    require assets[0] == ATokenAddress;
    require user == e.msg.sender;

    updateDataMultipleHarness(e, assets, user);

    uint256 rewards = getUserAccruedRewards(user, rewardTokenAddress);

    address[] rewardsList;
    uint256[] claimedAmounts;
    rewardsList, claimedAmounts = claimAllRewards(e, assets, to);

    assert claimedAmounts[0] == rewards; // bug3
}

// [participants 15] setClaimer() integrity, never reverted with EmissionManager
rule setClaimerIntegrity(env e, address user, address caller) {

    setup(e);

    require e.msg.sender == getEmissionManager();

    setClaimer@withrevert(e, user, caller);

    assert !lastReverted;
    assert getClaimer(user) == caller; // bug15
}

// [participants 83-84] _getUserAssetBalances() integrity
rule getUserAssetBalancesIntegrity(env e, address[] assets, address user) {

    setup(e);
    setupUser(e, user);

    require assets.length == 1;
    require assets[0] == ATokenAddress;
    
    address asset;
    uint256 userBalance1;
    uint256 totalSupply1;
    asset, userBalance1, totalSupply1 = getUserAssetBalanceHarness(e, assets, user);

    uint256 userBalance2;
    uint256 totalSupply2;
    userBalance2, totalSupply2 = ATokenAddress.getScaledUserBalanceAndSupply(e, user);

    assert assets[0] == asset; // bug83
    assert userBalance1 == userBalance1;
    assert totalSupply1 == totalSupply2;
}

// [participants 103-106] getRewardsData() integrity
rule getRewardsDataIntegrity(env e, address asset, address reward) {

    setup(e);

    require asset == ATokenAddress;
    require reward == rewardTokenAddress;

    uint256 index;
    uint256 emissionPerSecond;
    uint256 lastUpdateTimestamp;
    uint256 distributionEnd;
    index, emissionPerSecond, lastUpdateTimestamp, distributionEnd = getRewardsData(asset, reward);

    assert getAssetRewardIndex(asset, reward) == index;
    assert getAssetRewardEmissionPerSecond(asset, reward) == emissionPerSecond;
    assert getAssetRewardLastUpdateTimestamp(asset, reward) == lastUpdateTimestamp;
    assert getAssetRewardDistributionEnd(asset, reward) == distributionEnd;
}

// [participants 107-109] getAssetIndex() integrity
rule getAssetIndexIntegrity(env e, address asset, address reward) {
    
    setup(e);
    
    require asset == ATokenAddress;
    require reward == rewardTokenAddress;

    storage initial = lastStorage;

    uint256 oldIndex1;
    uint256 newIndex1;
    oldIndex1, newIndex1 = getAssetIndexHarness(e, asset, reward) at initial;

    uint256 oldIndex2;
    uint256 newIndex2;
    oldIndex2, newIndex2 = getAssetIndex(e, asset, reward) at initial;

    assert oldIndex1 == oldIndex2;
    assert newIndex1 == newIndex2;
}

// [participants 119-122] _getAssetIndex() return old index for invalid params
rule getAssetIndexInternalReturnSameIndex(env e, address asset, address reward) {
    
    require asset == ATokenAddress;

    uint8 decimals = getAssetDecimals(asset);
    require decimals > 0 && decimals < 77;

    uint256 index = getAssetRewardIndex(asset, reward); 
    uint256 totalSupply = ATokenAddress.scaledTotalSupply(e);
    uint256 emissionPerSecond = getAssetRewardEmissionPerSecond(asset, reward);
    uint256 lastUpdateTimestamp = getAssetRewardLastUpdateTimestamp(asset, reward);
    uint256 distributionEnd = getAssetRewardDistributionEnd(asset, reward);

    // TODO: as invariant
    require e.block.timestamp >= lastUpdateTimestamp;

    uint256 indexOld;
    uint256 indexNew;
    indexOld, indexNew = getAssetIndexHarness@withrevert(e, asset, reward);
    
    // return (indexOld, indexOld)
    assert !GET_ASSET_INDEX_VALID_PARAMS(e, index, totalSupply, emissionPerSecond, lastUpdateTimestamp, distributionEnd)
        => !lastReverted && indexOld == indexNew;
}

// [participants 123-127] _getAssetIndex() integrity
rule getAssetIndexInternalIntegrity(env e, address asset, address reward) {
    
    require asset == ATokenAddress;

    uint8 decimals = getAssetDecimals(asset);
    require decimals > 0 && decimals < 77;

    uint256 index = getAssetRewardIndex(asset, reward); 
    uint256 totalSupply = ATokenAddress.scaledTotalSupply(e);
    uint256 emissionPerSecond = getAssetRewardEmissionPerSecond(asset, reward);
    uint256 lastUpdateTimestamp = getAssetRewardLastUpdateTimestamp(asset, reward);
    uint256 distributionEnd = getAssetRewardDistributionEnd(asset, reward);

    // TODO: as invariant
    require e.block.timestamp >= lastUpdateTimestamp;

    uint256 indexOld;
    uint256 indexNew;
    indexOld, indexNew = getAssetIndexHarness@withrevert(e, asset, reward);
    bool reverted = lastReverted;
    
    assert !reverted => indexOld == index; // bug123

    // return (indexOld, indexNew)
    assert GET_ASSET_INDEX_VALID_PARAMS(e, index, totalSupply, emissionPerSecond, lastUpdateTimestamp, distributionEnd)
        => indexNew == require_uint256(indexOld + require_uint256((require_uint256(emissionPerSecond * require_uint256((e.block.timestamp > distributionEnd ? distributionEnd : e.block.timestamp) - lastUpdateTimestamp) * require_uint256(10 ^ decimals))) / totalSupply)); // bug124-127
}

// [participants 82] getRewardsList() integrity
rule getRewardsListIntegrity(env e, uint256 i) {
    
    setup(e);

    address[] rewardsList = getRewardsList(); 
    assert ghostRewardsList[rewardsList[0]]; // bug82
}

// [participants 110] getRewardsByAsset() integrity
rule getRewardsByAssetIntegrity(env e, address asset) {

    setup(e);

    require asset == ATokenAddress;

    address reward = getAssetAvailableReward(asset, 0);

    address[] rewards = getRewardsByAsset(asset);

    assert reward == rewards[0];
}

// [participants 111] getUserAccruedRewards() integrity
rule getUserAccruedRewardsIntegrity(env e, address user, address asset, address reward) {
    
    setup(e);

    require asset == ATokenAddress;

    uint256 totalAccrued = getUserAccruedRewards(user, reward);
    uint256 accrued = getAssetRewardUserAccrued(user, asset, reward);

    assert totalAccrued == accrued;
}

// [participants 112] setDistributionEnd() integrity
rule setDistributionEndIntegrity(env e, address asset, address reward, address user, uint32 newDistributionEnd) {

    setDistributionEnd(e, asset, reward, newDistributionEnd);

    assert require_uint256(newDistributionEnd) == getAssetRewardDistributionEnd(asset, reward);   
} 

// [participants 113-115] getUserRewards() integrity`
rule getUserRewardsIntegrity(env e, address[] assets, address user, address reward) {

    setup(e);
    setupUser(e, user);

    require assets.length == 1;
    require assets[0] == ATokenAddress;
    require reward == rewardTokenAddress;

    uint256 rewards1 = getUserRewards(e, assets, user, reward);

    uint256 rewards2 = getUserRewardsHarness(e, assets, user, reward);

    assert rewards1 == rewards2;
}

// [participants 186-190] getAllUserRewards() integrity
rule getAllUserRewardsIntegrity(env e, address[] assets, address user) {

    setup(e);
    setupUser(e, user);

    require assets.length == 1;
    require assets[0] == ATokenAddress;

    address[] rewardsList; 
    uint256[] unclaimedAmounts;
    rewardsList, unclaimedAmounts = getAllUserRewards(e, assets, user);

    // One asset, one reward
    assert rewardsList.length == 1;
    assert rewardsList[0] == rewardTokenAddress;
    assert unclaimedAmounts[0] == getUserRewards(e, assets, user, rewardTokenAddress);
}

// [participants 116-118] _updateDataMultiple() integrity
rule updateDataMultipleIntegrity(env e, address[] assets, address user) {

    setup(e);

    require assets.length == 1;
    require assets[0] == ATokenAddress;

    address asset; 
    uint256 userBalance; 
    uint256 totalSupply;
    asset, userBalance, totalSupply = getUserAssetBalanceHarness(e, assets, user);

    storage initial = lastStorage;

    updateDataMultipleHarness(e, assets, user) at initial;
    storage storage1 = lastStorage;

    updateDataHarness(e, assets[0], user, userBalance, totalSupply) at initial;
    storage storage2 = lastStorage;

    // _updateDataMultiple() storage changes for `ATokenAddress` asset should be equal to _updateData(`ATokenAddress`)
    assert storage1[currentContract] == storage2[currentContract];
}

// [participants 137] setEmissionPerSecond() input arrays have equal length
rule setEmissionPerSecondArraysEqLength(env e, address asset, address[] rewards, uint88[] newEmissionsPerSecond) {

    setupEssential(e);

    setEmissionPerSecond@withrevert(e, asset, rewards, newEmissionsPerSecond);

    assert rewards.length != newEmissionsPerSecond.length => lastReverted; // bug137
}

// [participants 138-143, RewardsDistributor_181 39] setEmissionPerSecond() integrity
rule setEmissionPerSecondIntegrity(env e, address asset, address[] rewards, uint88[] newEmissionsPerSecond) {

    setup(e);

    require asset == ATokenAddress;
    require rewards.length == 1;
    require rewards[0] == rewardTokenAddress;
    // Length check in setEmissionPerSecondArraysEqLength() rule 
    require newEmissionsPerSecond.length == rewards.length;
    require require_uint256(newEmissionsPerSecond[0]) <= MAX_UINT88();

    uint8 decimals = getAssetDecimals(asset);
    bool zeroDecimals = decimals == 0;
    bool zeroLastUpdateTimestamp = getAssetRewardLastUpdateTimestamp(asset, rewardTokenAddress) == 0;

    uint256 oldIndex;
    uint256 newIndex;
    oldIndex, newIndex = getAssetIndexHarness(e, asset, rewardTokenAddress);

    setEmissionPerSecond@withrevert(e, asset, rewards, newEmissionsPerSecond);
    bool reverted = lastReverted;

    uint256 currentIndex = getAssetRewardIndex(asset, rewardTokenAddress);

    // When reverted
    assert zeroDecimals => reverted; // bug138
    assert zeroLastUpdateTimestamp => reverted; // bug139
    // TODO: another strange revert
    /*assert reverted => 
        zeroDecimals 
        || zeroLastUpdateTimestamp
        || e.msg.sender != getEmissionManager()
        || !VALID_DECIMALS(decimals); // RewardsDistributor_181/bug39 */

    assert !reverted => getAssetRewardEmissionPerSecond(asset, rewardTokenAddress) == require_uint256(newEmissionsPerSecond[0]); // bug140

    // set in _updateRewardData(), bugs141-143
    assert !reverted => require_uint32(getAssetRewardLastUpdateTimestamp(asset, rewardTokenAddress)) == require_uint32(e.block.timestamp); 
    assert !reverted && oldIndex == newIndex => currentIndex == oldIndex; 
    assert !reverted && oldIndex != newIndex => currentIndex == newIndex;

    // onlyEmissionManager() modifier
    assert !reverted => e.msg.sender == getEmissionManager();
}

// [participants 144-153] _updateRewardData() integrity
rule updateRewardDataIntegrity(env e, address asset, address reward, uint256 totalSupply, uint256 assetUnit) {

    setup(e);

    require asset == ATokenAddress;
    require reward == rewardTokenAddress;
    require totalSupply == ATokenAddress.scaledTotalSupply(e);
    uint8 decimals = getAssetDecimals(ATokenAddress);
    require assetUnit == require_uint256(10 ^ decimals);

    uint256 oldIndex;
    uint256 newIndex;
    oldIndex, newIndex = getAssetIndexHarness(e, asset, reward);

    bool result;
    uint256 resultIndex;
    resultIndex, result = updateRewardDataHarness@withrevert(e, asset, reward, totalSupply, assetUnit);
    bool reverted = lastReverted;

    uint256 currentIndex = getAssetRewardIndex(asset, reward);

    assert !reverted => require_uint32(getAssetRewardLastUpdateTimestamp(asset, reward)) == require_uint32(e.block.timestamp); 
    assert !reverted && oldIndex == newIndex => currentIndex == oldIndex; 
    assert !reverted && oldIndex != newIndex => currentIndex == newIndex;
    assert !reverted => result == (oldIndex != newIndex);

    assert newIndex > MAX_UINT104() => reverted;
}

// [participants 154-164] _updateUserData() integrity
rule updateUserDataIntegrity(env e, address asset, address reward, address user, uint256 userBalance, uint256 newAssetIndex, uint256 assetUnit) {

    setup(e);
    setupUser(e, user);

    require asset == ATokenAddress;
    require reward == rewardTokenAddress;
    require userBalance == ATokenAddress.scaledBalanceOf(e, user);
    require newAssetIndex < MAX_UINT104();

    setupTokenDecimals(asset); 
    uint256 decimals = getAssetDecimals(asset);
    require assetUnit == require_uint256(10 ^ decimals);

    uint256 index = getAssetRewardUserIndex(user, asset, reward);
    require index <= newAssetIndex;

    uint256 accruedBefore = getAssetRewardUserAccrued(user, asset, reward);
    uint256 rewardsAccruedExpected = getRewardsHarness(userBalance, newAssetIndex, index, assetUnit);

    uint256 rewardsAccrued;
    bool dataUpdated;
    rewardsAccrued, dataUpdated = updateUserDataHarness(e, asset, reward, user, userBalance, newAssetIndex, assetUnit);
    // TODO: should not revert

    uint256 accruedAfter = getAssetRewardUserAccrued(user, asset, reward);

    assert dataUpdated == (index != newAssetIndex);
    assert dataUpdated => require_uint104(getAssetRewardUserIndex(user, asset, reward)) == require_uint104(newAssetIndex);
    assert dataUpdated => rewardsAccrued == rewardsAccruedExpected;

    // `accrued` should be updated
    assert dataUpdated && userBalance != 0 => accruedAfter == require_uint256(require_uint128(accruedBefore) + require_uint256(rewardsAccrued));

    // `index` wasn't changed
    assert !dataUpdated => getAssetRewardUserIndex(user, asset, reward) == index;

    // `accrued` wasn't changed
    assert !dataUpdated || userBalance == 0 => accruedAfter == accruedBefore && rewardsAccrued == 0;
}

// [participants 179-183] _updateData() integrity
rule updateDataIntegrity(env e, address asset, address user, uint256 userBalance, uint256 totalSupply) {

    setup(e);
    setupUser(e, user);
    require asset == ATokenAddress;

    // Assume token has normal decimals
    setupTokenDecimals(asset);
    uint256 decimals = getAssetDecimals(asset);
    uint256 assetUnit;
    require assetUnit == require_uint256(10 ^ decimals);

    storage initial = lastStorage;

    updateDataHarness(e, asset, user, userBalance, totalSupply) at initial;
    storage storage1 = lastStorage;

    // _updateData(): _updateRewardData() and _updateUserData()
    bool result;
    uint256 resultIndex;
    resultIndex, result = updateRewardDataHarness(e, asset, rewardTokenAddress, totalSupply, assetUnit) at initial;
    updateUserDataHarness(e, asset, rewardTokenAddress, user, userBalance, resultIndex, assetUnit);
    storage storage2 = lastStorage;

    assert storage1[currentContract] == storage2[currentContract];
}

// [participants 184] _updateData() satisfy that _updateRewardData() called
rule updateDataCouldUpdateRewardData(env e, address asset, address reward, address user, uint256 userBalance, uint256 totalSupply) {

    setup(e);
    setupUser(e, user);
    require asset == ATokenAddress;
    require reward == rewardTokenAddress;
    require userBalance == ATokenAddress.scaledBalanceOf(e, user);
    require totalSupply == ATokenAddress.scaledTotalSupply(e);

    require getAssetRewardLastUpdateTimestamp(asset, reward) != e.block.timestamp;

    updateDataHarness(e, asset, user, userBalance, totalSupply);

    // _updateRewardData() could set timestamp as a block.timestamp
    satisfy(require_uint32(getAssetRewardLastUpdateTimestamp(asset, reward)) == require_uint32(e.block.timestamp));
}

// [participants 185] _updateData() satisfy that _updateUserData() called
rule updateDataCouldUpdateUserData(env e, address asset, address reward, address user, uint256 userBalance, uint256 totalSupply) {

    setup(e);

    uint256 initialAccrued = getAssetRewardUserAccrued(user, asset, reward);

    updateDataHarness(e, asset, user, userBalance, totalSupply);

    // _updateUserData() could increase initial accrued
    satisfy(getAssetRewardUserAccrued(user, asset, reward) > initialAccrued);
}

// [RewardsDistributor_181 123] _updateData() return when numAvailableRewards == 0
rule updateDataZeroNumAvailableRewards(env e, address asset, address user, uint256 userBalance, uint256 totalSupply) {

    setupEssential(e);

    setupTokenDecimals(asset);
    require getAssetAvailableRewardsCount(asset) == 0;

    updateDataHarness@withrevert(e, asset, user, userBalance, totalSupply);

    // Return in the function beginning
    assert !lastReverted;
}

// [participants 167-169] _getRewards() integrity
rule getRewardsIntegrity(uint256 userBalance, uint256 reserveIndex, uint256 userIndex, uint256 assetUnit) {

    // Division by zero
    require assetUnit != 0;

    // TODO: as invariant
    // Underflow/overflow
    require reserveIndex >= userIndex;
    require require_uint256(userBalance * (reserveIndex - userIndex)) < MAX_UINT256();

    uint256 rewards = getRewardsHarness@withrevert(userBalance, reserveIndex, userIndex, assetUnit);

    assert !lastReverted && rewards == require_uint256((userBalance * (reserveIndex - userIndex)) / assetUnit);
}

// [participants 170-174] _getPendingRewards() integrity
rule getPendingRewardsIntegrity(env e, address user, address reward, address asset, uint256 userBalance, uint256 totalSupply) {

    setup(e);
    setupUser(e, user);
    setupTokenDecimals(asset);

    require reward == rewardTokenAddress;
    require asset == ATokenAddress;
    require totalSupply == ATokenAddress.scaledTotalSupply(e);

    uint256 oldIndex;
    uint256 nextIndex;
    oldIndex, nextIndex = getAssetIndex(e, asset, reward);
    uint256 userIndex = getAssetRewardUserIndex(user, asset, reward);
    uint8 decimals = getAssetDecimals(asset);
    uint256 assetUnit = require_uint256(10 ^ decimals);
    uint256 expectedRewards = getRewardsHarness(userBalance, nextIndex, userIndex, assetUnit);

    uint256 rewards = getPendingRewardsHarness@withrevert(e, user, reward, asset, userBalance, totalSupply);

    assert !lastReverted => expectedRewards == rewards;
}

// [participants 175-178, RewardsDistributor_181 133] _getUserReward() integrity
rule getUserRewardIntegrity(env e, address[] assets, address user, address reward) {

    setup(e);
    setupUser(e, user);

    require assets.length == 1;
    require assets[0] == ATokenAddress;
    setupTokenDecimals(assets[0]);
    require reward == rewardTokenAddress;

    uint256 userBalance;
    uint256 totalSupply;
    userBalance, totalSupply = ATokenAddress.getScaledUserBalanceAndSupply(e, user);
    uint256 accruedRewards = getAssetRewardUserAccrued(user, assets[0], reward);
    uint256 pendingRewards = userBalance != 0 ? getPendingRewardsHarness(e, user, reward, assets[0], userBalance, totalSupply) : 0;

    uint256 rewards = getUserRewards(e, assets, user, reward);

    assert userBalance == 0 ? rewards == accruedRewards : rewards == require_uint256(accruedRewards + pendingRewards);
}