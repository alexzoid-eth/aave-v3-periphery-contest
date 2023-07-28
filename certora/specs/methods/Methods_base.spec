import "./ERC20_methods.spec";

using DummyERC20_AToken as ATokenAddress;
using DummyERC20_rewardToken as rewardTokenAddress;
using TransferStrategyHarness as transferStrategyAddress;

/////////////////// Methods ////////////////////////

methods {
    // RewardsControllerHarness envfree
    function getAssetRewardIndex(address, address) external returns (uint256) envfree;
    function getAssetRewardEmissionPerSecond(address, address) external returns (uint88) envfree;
    function getAssetRewardLastUpdateTimestamp(address, address) external returns (uint256) envfree;
    function getAssetRewardDistributionEnd(address, address) external returns (uint32) envfree;
    function getRewardToken(uint256) external returns (address) envfree;
    function getRewardsListLength() external returns (uint256) envfree;
    function isRewardInList(address) external returns (bool) envfree;
    function getAssetToken(uint256) external returns (address) envfree;
    function getAssetsListLength() external returns (uint256) envfree;
    function isAssetInList(address) external returns (bool) envfree;
    function isRewardEnabled(address) external returns (bool) envfree;
    function getAssetAvailableReward(address, uint128) external returns (address) envfree;
    function getAssetAvailableRewardsCount(address) external returns (uint128) envfree;
    function isContract(address) external returns (bool) envfree;
    function getRevisionHarness() external returns (uint256) envfree;
    function initialize(address) external envfree;

    // RewardsControllerHarness
    function updateDataMultiple(address) external;
    function configureAssetsHarness(uint88, uint32, address, address, address, address) external;

    // RewardsController envfree
    function getRewardOracle(address) external returns (address) envfree;
    function getTransferStrategy(address) external returns (address) envfree;
    function getUserAssetIndex(address, address, address) external returns (uint256) envfree;
    function getClaimer(address) external returns (address) envfree;
    function setClaimer(address, address) external envfree;

    // RewardsController
    function setRewardOracle(address, address) external;
    function setTransferStrategy(address, address) external;

    // RewardsDistributor envfree
    function getAssetDecimals(address) external returns (uint8) envfree;
    function getEmissionManager() external returns (address) envfree;
    function getRewardsData(address, address) external returns (uint256, uint256, uint256, uint256) envfree;
    function getUserAccruedRewards(address, address ) external returns (uint256) envfree; 

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