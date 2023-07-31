# Prove all bugs
for f in certora/tests/$1/bug*.patch
do
    wildcard=${f##"certora/tests/$1"/bug}
    wildcard=${wildcard%.patch}
    certora/tests/verifyBug.sh $1 $wildcard
done