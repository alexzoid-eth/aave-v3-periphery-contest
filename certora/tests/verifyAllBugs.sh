# verifyRewardsController_multiAsset_verified.conf
for f in certora/tests/$1/bug*.patch
do
    wildcard=${f##"certora/tests/$1"/bug}
    wildcard=${wildcard%.patch}
    certora/tests/verifyBug.sh $1 $wildcard
done

# verifyRewardsController_multiAsset_verified.conf
for f in certora/tests/$1/bug*_multiAsset.patch
do
    wildcard=${f##"certora/tests/$1"/bug}
    wildcard=${wildcard%_multiAsset.patch}
    certora/tests/verifyBug_multiAsset.sh $1 $wildcard
done