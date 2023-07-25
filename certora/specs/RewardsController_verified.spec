import "methods/Methods_base.spec";

///////////////// Properties ///////////////////////

// Property: only an authorized user or the user itself can cause a reduction in accrued rewards for this user
rule onlyAuthorizeCanDecrease(method f) filtered { f -> !f.isView } {

    address user; address reward;
    uint256 before = getUserAccruedRewards(user, reward);

    env e;
    calldataarg args;
    f(e,args);

    uint256 after = getUserAccruedRewards(user, reward);

    assert after < before => (getClaimer(user) == e.msg.sender || user == e.msg.sender);
}