import "methods/Methods_base.spec";

///////////////// Definitions ///////////////////////

definition CLAIM_REWARDS_FUNCTIONS(method f) returns bool = 
    f.selector == sig:claimRewards(address[], uint256, address, address).selector
    || f.selector == sig:claimRewardsOnBehalf(address[], uint256, address, address, address).selector
    || f.selector == sig:claimRewardsToSelf(address[], uint256, address).selector
    || f.selector == sig:claimAllRewards(address[], address).selector
    || f.selector == sig:claimAllRewardsOnBehalf(address[], address, address).selector;

definition HANDLE_FUNCTION(method f) returns bool = 
    f.selector == sig:handleAction(address, uint256, uint256).selector;

///////////////// Functions ///////////////////////

// A cvl function for precondition assumptions 
function setup(env e) {
    require e.msg.sender != 0;
    require e.block.timestamp != 0;
}

// Ghost copy of RewardsController._authorizedClaimers[]

ghost mapping(address => address) ghostAuthorizedClaimers {
    init_state axiom forall address x. ghostAuthorizedClaimers[x] == 0;
}

hook Sstore _authorizedClaimers[KEY address user] address claimer STORAGE {
    ghostAuthorizedClaimers[user] = claimer;
}

hook Sload address claimer _authorizedClaimers[KEY address user] STORAGE {
    require ghostAuthorizedClaimers[user] == claimer;
}

// Ghost copy of RewardsController._transferStrategy[]

ghost mapping(address => address) ghostTransferStrategy {
    init_state axiom forall address x. ghostTransferStrategy[x] == 0;
}

hook Sstore _transferStrategy[KEY address reward] address strategy STORAGE {
    ghostAuthorizedClaimers[reward] = strategy;
}

hook Sload address reward _transferStrategy[KEY address strategy] STORAGE {
    require ghostAuthorizedClaimers[reward] == strategy;
}

// Ghost copy of RewardsController._rewardOracle[]

ghost mapping(address => address) ghostRewardOracle {
    init_state axiom forall address x. ghostRewardOracle[x] == 0;
}

hook Sstore _rewardOracle[KEY address reward] address oracle STORAGE {
    ghostAuthorizedClaimers[reward] = oracle;
}

hook Sload address reward _rewardOracle[KEY address oracle] STORAGE {
    require ghostAuthorizedClaimers[reward] == oracle;
}

///////////////// Properties ///////////////////////

// [bug1] Possibility of update user asset data
rule possibleToUserDataUpdate(env e, method f, calldataarg args1, calldataarg args2) 
    filtered { f -> CLAIM_REWARDS_FUNCTIONS(f) || HANDLE_FUNCTION(f) } {
    
    setup(e);

    uint256 indexBefore = getUserAssetIndex(args1);

    f(e, args2);

    uint256 indexAfter = getUserAssetIndex(args1);

    satisfy(indexBefore != indexAfter);
}

// [bug2] Claiming rewards to zero address should revert
rule claimRewardsToZeroAddress(env e, address[] assets, uint256 amount, address to, address reward) {

    setup(e);

    claimRewards@withrevert(e, assets, amount, to, reward);

    assert to == 0 => lastReverted;
}

// [bug3] TODO

// [bug4] Claiming rewards on behalf from or to zero address should revert
rule claimRewardsOnBehalfFromOrToZeroAddress(env e, address[] assets, uint256 amount, address user, address to, address reward) {

    setup(e);

    claimRewardsOnBehalf@withrevert(e, assets, amount, user, to, reward);

    assert user == 0 || to == 0 => lastReverted;
}