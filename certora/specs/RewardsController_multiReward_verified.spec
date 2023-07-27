import "methods/Methods_base.spec";

using DummyERC20_rewardToken as _DummyERC20_rewardToken;
using DummyERC20_rewardTokenB as _DummyERC20_rewardTokenB;
using TransferStrategyMultiRewardHarnessWithLinks as _TransferStrategyMultiRewardHarnessWithLinks;
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

// CVL functions for precondition assumptions 

function setupUser(env e, address user) {
    require user != 0;
    require user != currentContract;
    require user != _DummyERC20_AToken;
    require user != _DummyERC20_rewardToken;
    require user != _TransferStrategyMultiRewardHarnessWithLinks;

    require _DummyERC20_AToken.scaledBalanceOf(e, user) <= _DummyERC20_AToken.scaledTotalSupply(e);
}

function setup(env e) {

    setupUser(e, e.msg.sender);

    require e.block.timestamp != 0;
    require getRewardsListLength() == 2;
    require getRewardToken(0) == _DummyERC20_rewardToken;
    require getRewardToken(1) == _DummyERC20_rewardTokenB;
    require getTransferStrategy(_DummyERC20_rewardToken) == _TransferStrategyMultiRewardHarnessWithLinks;
    require getTransferStrategy(_DummyERC20_rewardTokenB) == _TransferStrategyMultiRewardHarnessWithLinks;
    require getAssetsListLength() == 1;
    require getAssetToken(0) == _DummyERC20_AToken;
    require getAssetAvailableReward(_DummyERC20_AToken, 0) == _DummyERC20_rewardToken;
    require getAssetAvailableReward(_DummyERC20_AToken, 1) == _DummyERC20_rewardTokenB;
    require getAssetAvailableRewardsCount(_DummyERC20_AToken) == 2;
    
    require getAssetDecimals(_DummyERC20_AToken) > 0;
    require getAssetDecimals(_DummyERC20_AToken) < 77;
    require _DummyERC20_AToken.scaledTotalSupply(e) >= require_uint256(1000 * 10 ^ getAssetDecimals(_DummyERC20_AToken));

    require _DummyERC20_rewardToken != _TransferStrategyMultiRewardHarnessWithLinks;
    require _DummyERC20_rewardToken != _DummyERC20_AToken;
    require _DummyERC20_rewardToken != currentContract;
    require _DummyERC20_AToken != currentContract;
    require _DummyERC20_AToken != _TransferStrategyMultiRewardHarnessWithLinks;
    require _TransferStrategyMultiRewardHarnessWithLinks != currentContract;

    require _DummyERC20_rewardTokenB != _DummyERC20_rewardToken;
    require _DummyERC20_rewardTokenB != _DummyERC20_AToken;
    require _DummyERC20_rewardTokenB != _DummyERC20_AToken;
    require _DummyERC20_rewardTokenB != currentContract;
    require _DummyERC20_rewardTokenB != _TransferStrategyMultiRewardHarnessWithLinks;
}
