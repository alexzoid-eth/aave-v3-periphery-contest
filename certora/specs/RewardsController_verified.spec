import "methods/ERC20_methods.spec";

using DummyERC20_AToken as ATokenAddress;
using DummyERC20_rewardToken as rewardTokenAddress;
using TransferStrategyHarness as transferStrategyAddress;

/////////////////// Methods ////////////////////////

methods {
    // RewardsControllerHarness envfree
    function getAssetRewardIndex(address, address) external returns (uint256) envfree;
    function getAssetRewardEmissionPerSecond(address, address) external returns (uint256) envfree;
    function getAssetRewardLastUpdateTimestamp(address, address) external returns (uint256) envfree;
    function getAssetRewardDistributionEnd(address, address) external returns (uint256) envfree;
    function getAssetRewardUserIndex(address, address, address) external returns (uint256) envfree;
    function getAssetRewardUserAccrued(address, address, address) external returns (uint256) envfree;
    function getRewardToken(uint256) external returns (address) envfree;
    function getRewardsListLength() external returns (uint256) envfree;
    function fillMapFromRewardsList(address[]) external envfree;
    function _rewardsMap(uint256) external returns (address) envfree;
    function isRewardInList(address) external returns (bool) envfree;
    function getAssetToken(uint256) external returns (address) envfree;
    function getAssetsListLength() external returns (uint256) envfree;
    function isAssetInList(address) external returns (bool) envfree;
    function isRewardEnabled(address) external returns (bool) envfree;
    function getAssetAvailableReward(address, uint128) external returns (address) envfree;
    function getAssetAvailableRewardsCount(address) external returns (uint128) envfree;
    function isContract(address) external returns (bool) envfree;
    function getRevisionHarness() external returns (uint256) envfree;
    function getEmissionManagerHarness() external returns (address) envfree;

    // RewardsControllerHarness
    function updateDataMultiple(address) external;
    function updateRewardData(address, address, uint256, uint256) external;
    function configureAssetsHarness(uint88, uint32, address, address, address, address) external;

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

    // AToken    
    function _.scaledBalanceOf(address) external => DISPATCHER(true);
    function _.getScaledUserBalanceAndSupply(address) external => DISPATCHER(true);
    function _.scaledTotalSupply() external => DISPATCHER(true);
    function _.handleAction(address, uint256, uint256) external => DISPATCHER(true);

    // TransferStrategyBase
    function _.performTransfer(address, address, uint256) external => DISPATCHER(true);

    // Oracle 
    function _.latestAnswer() external => ghostLatestAnswer() expect int256 ALL;
}

///////////////// DEFINITIONS //////////////////////

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

function setup(env e) {

    setupUser(e, e.msg.sender);

    require e.msg.value == 0;
    require e.block.timestamp != 0;
    require getRewardsListLength() == 1;
    require getRewardToken(0) == rewardTokenAddress;
    require getTransferStrategy(rewardTokenAddress) == transferStrategyAddress;
    require getAssetsListLength() == 1;
    require getAssetToken(0) == ATokenAddress;
    require getAssetAvailableReward(ATokenAddress, 0) == rewardTokenAddress;
    require getAssetAvailableRewardsCount(ATokenAddress) == 1;
    
    require getAssetDecimals(ATokenAddress) > 0;
    require getAssetDecimals(ATokenAddress) < 77;
    require ATokenAddress.scaledTotalSupply(e) 
        >= require_uint256(1000 * 10 ^ getAssetDecimals(ATokenAddress));

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

ghost mapping(uint256 => address) ghostRewardsList {
    init_state axiom forall uint256 x. ghostRewardsList[x] == 0;
}

hook Sstore _rewardsList[INDEX uint256 i] address reward STORAGE {
    ghostRewardsList[i] = reward;
}

hook Sload address reward _rewardsList[INDEX uint256 i] STORAGE {
    require ghostRewardsList[i] == reward;
}

// Ghost copy of _rewardsMap[]

ghost mapping(uint256 => address) ghostRewardsMap {
    init_state axiom forall uint256 x. ghostRewardsMap[x] == 0;
}

hook Sstore _rewardsMap[KEY uint256 i] address reward STORAGE {
    ghostRewardsMap[i] = reward;
}

hook Sload address reward _rewardsMap[KEY uint256 i] STORAGE {
    require ghostRewardsMap[i] == reward;
}

// Ghost copy of _assetsList[]

ghost mapping(uint256 => address) ghostAssetsList {
    init_state axiom forall uint256 x. ghostAssetsList[x] == 0;
}

hook Sstore _assetsList[INDEX uint256 i] address asset STORAGE {
    ghostAssetsList[i] = asset;
}

hook Sload address asset _assetsList[INDEX uint256 i] STORAGE {
    require ghostAssetsList[i] == asset;
}

// Ghost copy of _assets[].availableRewardsCount

ghost mapping (address => uint128) ghostAssetsAvailableRewardsCount {
    init_state axiom forall address asset. ghostAssetsAvailableRewardsCount[asset] == 0;
}

hook Sstore _assets[KEY address asset].availableRewardsCount uint128 count STORAGE {
    ghostAssetsAvailableRewardsCount[asset] = count;
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

///////////////// Properties ///////////////////////

// [bug 16] initializer() security modifier, second call of initialize() should revert
rule initializeCalledOnce(env e1, env e2, address addr) {

    initialize@withrevert(e1, addr);
    bool firstCallReverted = lastReverted;

    initialize@withrevert(e2, addr);
    bool secondCallReverted = lastReverted;

    assert !firstCallReverted => secondCallReverted;
}

// [bug 17] initialize() - first call should not revert
rule initializeFirstCallShouldNotRevert(env e, address addr) {

    setup(e);

    initialize@withrevert(e, addr);

    assert !lastReverted;
}

// [bugs 18-25] getters integrity
rule integrityGetters(address asset, address reward, address user) {
    assert getClaimer(user) == ghostAuthorizedClaimers[user]; // bug18
    assert getRevisionHarness() == require_uint256(1); // bug19
    assert getRewardOracle(reward) == ghostRewardOracle[reward]; // bug20
    assert getTransferStrategy(reward) == ghostTransferStrategy[reward]; // bug21
    assert getDistributionEnd(asset, reward) == require_uint256(getAssetRewardDistributionEnd(asset, reward)); //bug22
    assert getUserAssetIndex(user, asset, reward) == getAssetRewardUserIndex(user, asset, reward); //bug23
    assert getAssetDecimals(asset) == ghostAssetsDecimals[asset]; //bug24
    assert getEmissionManager() == getEmissionManagerHarness(); //bug25
} 

// [bugs 26-37] getters should not revert 
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

// [bugs 9, 38-50] configureAssets() integrity
rule integrityConfigureAssets(
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

    // ATokenAddress will be added when zero decimals
    bool zeroDecimals = getAssetDecimals(asset) == 0;

    // rewardTokenAddress will be added when was not enabled
    bool rewardEnabled;
    require rewardEnabled == isRewardEnabled(reward);
    bool rewardInList;
    require rewardInList == isRewardInList(reward);

    // add reward address to asset available rewards when zero timestamp
    bool zeroTimeStamp = getAssetRewardLastUpdateTimestamp(asset, reward) == 0;

    // revert when length reach uin256 limit 
    require getAssetsListLength() < 1000;
    require getRewardsListLength() < 1000;

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
}

/*
// TODO
// [bug ] configureAssets() integrity of totalSupply
rule integrityConfigureAssetsTotalSupply(
    env e, 
    uint88 emissionPerSecond, 
    uint32 distributionEnd,
    address asset,
    address reward,
    address transferStrategy,
    address rewardOracle
    ) {

    setup(e);

    require e.msg.sender == getEmissionManager();
    require asset == ATokenAddress;
    require reward == rewardTokenAddress;

    configureAssetsHarness(
        e, 
        emissionPerSecond, 
        distributionEnd,
        asset,
        reward,
        transferStrategy,
        rewardOracle
    );

    // updateRewardData() with the same params should not change contract's state
    uint256 totalSupply = ATokenAddress.scaledTotalSupply(e);
    uint8 decimals;
    require decimals == ghostAssetsDecimals[asset];
    storage storageBefore = lastStorage;
    updateRewardData(e, asset, reward, totalSupply, decimals);
    storage storageAfter = lastStorage;
    assert storageBefore == storageAfter;
}
*/

// [bugs 8, 51-55] onlyEmissionManager() security modifier
rule integrityOnlyEmissionManager(method f, env e, calldataarg args) 
    filtered { f -> ONLY_EMISSION_MANAGER_FUNCTIONS(f) } {

    f(e, args);

    assert e.msg.sender == getEmissionManager();
}

// [7, 56] onlyAuthorizedClaimers() security modifier
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

// [bugs 12-13, 52, 57] setTransferStrategy() integrity 
rule integritySetTransferStrategy(env e, address reward, address transferStrategy) {
    
    setup(e);

    // Checked in integrityOnlyEmissionManager() rule
    require e.msg.sender == getEmissionManager();

    setTransferStrategy@withrevert(e, reward, transferStrategy);

    assert transferStrategy == 0 => lastReverted; // bug13
    assert isContract(transferStrategy) == false => lastReverted; // bug12
    assert !lastReverted => getTransferStrategy(reward) == transferStrategy; // bug57
}

// [bugs 8, 10, 11] setRewardOracle() integrity, never reverted with EmissionManager
rule integritySetRewardOracle(env e, address reward, address rewardOracle) {
    
    setup(e);

    // Checked in integrityOnlyEmissionManager() rule
    require e.msg.sender == getEmissionManager();

    setRewardOracle@withrevert(e, reward, rewardOracle);

    assert ghostLatestAnswer() <= 0 => lastReverted; // bug10
    assert !lastReverted => rewardOracle == getRewardOracle(reward); // bug11
}

// [1] Possibility of update reward index when executing claim rewards
rule claimAllRewardsPossibleUpdateRewardIndex(method f, env e, address[] assets, address to, address reward) 
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

// [2] Claiming rewards to zero address should revert
rule claimRewardsToZeroAddress(env e, address[] assets, uint256 amount, address to, address reward) {

    setup(e);
    setupUser(e, to);

    claimRewards@withrevert(e, assets, amount, to, reward);

    assert to == 0 => lastReverted;
}

// TODO: long working time
// [3] Claim rewards should return amount of accrued rewards
/*
rule claimAllRewardsReturnClaimedAmounts(env e, address[] assets, address user, address to) {

    setup(e);
    setupUser(e, to);

    require assets.length == 1;
    require assets[0] == ATokenAddress;
    require user == e.msg.sender;

    updateDataMultiple(e, assets, user);

    uint256 rewards = getUserAccruedRewards(user, rewardTokenAddress);

    address[] rewardsList;
    uint256[] claimedAmounts;
    rewardsList, claimedAmounts = claimAllRewards(e, assets, to);

    assert claimedAmounts[0] == rewards;
}
*/

// [4] Claiming rewards on behalf from or to zero address should revert
rule claimRewardsOnBehalfFromOrToZeroAddress(env e, address[] assets, uint256 amount, address user, address to, address reward) {

    setup(e);
    setupUser(e, user);
    setupUser(e, to);

    claimRewardsOnBehalf@withrevert(e, assets, amount, user, to, reward);

    assert user == 0 || to == 0 => lastReverted;
}

// [5] Claiming all rewards to zero address should revert
rule claimAllRewardsToZeroAddress(env e, address[] assets, address to) {

    setup(e);
    setupUser(e, to);

    claimAllRewards@withrevert(e, assets, to);

    assert to == 0 => lastReverted;
}

// [6] Claiming all rewards on behalf from or to zero address should revert
rule claimAllRewardsOnBehalfFromOrToZeroAddress(env e, address[] assets, address user, address to) {

    setup(e);
    setupUser(e, user);

    claimAllRewardsOnBehalf@withrevert(e, assets, user, to);

    assert user == 0 || to == 0 => lastReverted;
}

// [14] _isContract() integrity, never reverted
rule integrityIsContract() {

    bool result = isContract@withrevert(currentContract);

    assert !lastReverted;
    assert result;
}

// [15] setClaimer() integrity, never reverted with EmissionManager
rule integritySetClaimer(env e, address user, address caller) {

    setup(e);

    require e.msg.sender == getEmissionManager();

    setClaimer@withrevert(e, user, caller);

    assert !lastReverted;
    assert getClaimer(user) == caller;
}

// [] getRewardsList() integrity
rule integrityGetRewardsList(env e) {

    setup(e);
    address[] rewardsList = getRewardsList(); 
    assert rewardsList[0] == ghostRewardsList[0];

    // TODO: quantifier doesn't work
    //fillMapFromRewardsList(rewardsList);
    //assert (forall uint256 i . ghostRewardsList[i] == ghostRewardsMap[i]);
}

/* TODO: violated
distributionEnd:     0xffffffff
emissionPerSecond:   0xffffffffffffffffffffff
lastUpdateTimestamp: 0xfffffffe
e.block.timestamp    0x100000000

currentTimestamp = 0xffffffff
timeDelta = 0xffffffff - 0xfffffffe = 1
firstTerm = 0xffffffffffffffffffffff * 1 * 10
totalSupply = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
*/
// [] getAssetIndex() should not revert
/*
rule getAssetIndexShouldNotRevert(env e, address asset, address reward) {

    setup(e);

    require asset == ATokenAddress;
    require reward == rewardTokenAddress;
    require e.block.timestamp >= getAssetRewardLastUpdateTimestamp(asset, reward);

    getAssetIndex@withrevert(e, asset, reward);

    assert !lastReverted;
}
*/

// [] getRewardsData() integrity
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

