import "methods/Methods_base.spec";

///////////////// Ghosts & hooks ///////////////////////

// Ghost for `_.latestAnswer()` summarize
ghost ghostLatestAnswer() returns int256;

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
    require assets[0] == ATokenAddress;
    require user == e.msg.sender;

    updateDataMultiple(e, assets, user);

    uint256 rewards = getUserAccruedRewards(user, rewardTokenAddress);

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
rule integrityOnlyEmissionManager(method f, env e, calldataarg args) 
    filtered { f -> ONLY_EMISSION_MANAGER_FUNCTIONS(f) } {

    setup(e);

    f(e, args);

    assert e.msg.sender == getEmissionManager();
}

// [bug9] configureAssets() integrity
rule integrityConfigureAssets(
    env e, 
    uint88 emissionPerSecond, 
    uint256 totalSupply,
    uint32 distributionEnd,
    address asset,
    address reward,
    address transferStrategy,
    address rewardOracle
    ) {

    require e.msg.sender == getEmissionManager();

    // `asset` and `reward` are not in the list, will be added after _configureAssets() call
    require getAssetDecimals(asset) == 0;
    require getAssetsListLength() == 0 || getAssetsListLength() < 1000;
    require isRewardEnabled(reward) == false;
    require getRewardsListLength() == 0 || getRewardsListLength() < 1000;

    configureAssetsHarness(
        e, 
        emissionPerSecond, 
        distributionEnd,
        asset,
        reward,
        transferStrategy,
        rewardOracle
    );

    assert emissionPerSecond == getAssetRewardEmissionPerSecond(asset, reward);
    assert distributionEnd == getAssetRewardDistributionEnd(asset, reward);
    assert isAssetInList(asset);
    assert isRewardInList(reward);
    assert transferStrategy == getTransferStrategy(reward);
    assert rewardOracle == getRewardOracle(reward);
}

// [bug10] setRewardOracle() integrity of latestAnswer()
rule integritySetRewardOracleLatestAnswer(env e, address reward, address rewardOracle) {
 
    require e.msg.sender == getEmissionManager();

    require ghostLatestAnswer() < 1;

    setRewardOracle@withrevert(e, reward, rewardOracle);

    assert lastReverted;
}

// [bug11] setRewardOracle() integrity
rule integritySetRewardOracle(env e, address reward, address rewardOracle) {
 
    require e.msg.sender == getEmissionManager();

    setRewardOracle(e, reward, rewardOracle);

    assert rewardOracle == getRewardOracle(reward);
}

// [bug12] setTransferStrategy() integrity of isContract()
rule integritySetTransferStrategyIsContract(env e, address reward, address transferStrategy) {
    
    require e.msg.sender == getEmissionManager();
    require transferStrategy != 0;

    require isContract(transferStrategy) == false;

    setTransferStrategy@withrevert(e, reward, transferStrategy);

    assert lastReverted;
}

// [bug13] setTransferStrategy() integrity
rule integritySetTransferStrategy(env e, address reward, address transferStrategy) {
    
    require e.msg.sender == getEmissionManager();
    require isContract(transferStrategy) == true;

    setTransferStrategy(e, reward, transferStrategy);

    assert transferStrategy != 0;
    assert getTransferStrategy(reward) == transferStrategy;
}