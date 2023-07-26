import "methods/Methods_base.spec";

///////////////// Properties ///////////////////////

// [certora/bug1.patch] 
// TODO

// [certora/bug2.patch] Claiming rewards to zero address should revert
rule claimRewardsToZeroAddress(env e, address[] assets, uint256 amount, address to, address reward) {

    require e.msg.sender != 0;

    claimRewards@withrevert(e, assets, amount, to, reward);

    assert to == 0 => lastReverted;
}

// [participants/bug4.patch] Claiming rewards on behalf from or to zero address should revert
rule claimRewardsOnBehalfFromToZeroAddress(env e, address[] assets, uint256 amount, address user, address to, address reward) {

    require e.msg.sender != 0;

    claimRewardsOnBehalf@withrevert(e, assets, amount, user, to, reward);

    assert user == 0 || to == 0 => lastReverted;
}